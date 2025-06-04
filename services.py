#services.py 
import os
from database import get_dialogue, insert_dialogue, get_personality, insert_personality
from database import query_pinecone
import groq
from redis_cache import cache
import hashlib
import json
from dotenv import load_dotenv

load_dotenv()

groq_client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

# You can keep some known personalities here as a fallback or override.
character_personalities = {
    "iron man": "You are Tony Stark, a genius billionaire playboy philanthropist. You are witty, sarcastic, and confident.",
    "tony": "iron man",
    "darth vader": "You are Darth Vader, a Sith Lord. You speak in a deep, commanding tone and believe in the power of the Dark Side.",
    "harry potter": "You are Harry Potter, a brave young wizard. You are kind, courageous, and determined."
}

def get_or_create_personality(character: str):
    # Check DB first
    personality = get_personality(character)
    if personality:
        return personality

    # Check hardcoded fallback
    if character in character_personalities:
        return character_personalities[character]

    # Generate personality dynamically using Groq
    try:
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes fictional characters into personality descriptions."},
                {"role": "user", "content": f"Describe the personality of the fictional character '{character}' from popular media in 2-3 sentences."}
            ]
        )
        personality_text = response.choices[0].message.content.strip()

        # Save generated personality to DB for future use
        insert_personality(character, personality_text)
        return personality_text

    except Exception as e:
        # Fallback personality if error occurs
        return "You are a fictional character."

def make_cache_key(character: str, user_message: str) -> str:
    composite = json.dumps({"character": character.lower(), "user_message": user_message.strip()}, sort_keys=True)
    return "chat:" + hashlib.md5(composite.encode()).hexdigest()

def get_character_response(character: str, user_message: str):
    character = character.lower()
    user_message = user_message.strip()

    cache_key = make_cache_key(character, user_message)
    cached_response = cache.get(cache_key)
    if cached_response:
        print(f"🧠 Cache hit for: {character} - {user_message[:30]}...")
        return cached_response

    print(f"🌀 Cache miss: generating response for {character}...")

    personality = get_or_create_personality(character)
    retrieved_dialogues = query_pinecone(character, user_message, top_k=5)

    if retrieved_dialogues:
        context_dialogues = "\n".join(f"- {d}" for d in retrieved_dialogues)
        system_prompt = f"""
        You are {character}. {personality}
        You are given some example dialogues from this character to assist in answering questions:
        {context_dialogues}
        Please generate a unique, context-aware, and relevant response to the user's question.
        Avoid repeating exact phrases from the example dialogues.
        """
        prompt_messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        try:
            response = groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=prompt_messages
            ).choices[0].message.content.strip()

            cache.setex(cache_key, 3600, response)  # Cache for 1 hour
            return response
        except Exception as e:
            print(f"❌ Groq generation error: {e}")
            return retrieved_dialogues[0]

    # Fallback if no context
    try:
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": f"You are {character}. {personality}"},
                {"role": "user", "content": user_message}
            ]
        ).choices[0].message.content.strip()

        cache.setex(cache_key, 3600, response)
        return response
    except Exception as e:
        print(f"❌ Groq generation error: {e}")
        return "I don't have a response for that right now."
    
    