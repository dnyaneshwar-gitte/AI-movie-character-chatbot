import os
from database import get_dialogue, insert_dialogue
import groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client (or you can use OpenAI GPT or any other model)
groq_client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

# Predefined character personalities
character_personalities = {
    "iron man": "You are Tony Stark, a genius billionaire playboy philanthropist. You are witty, sarcastic, and confident.",
    "tony": "iron man",
    "darth vader": "You are Darth Vader, a Sith Lord. You speak in a deep, commanding tone and believe in the power of the Dark Side.",
    "harry potter": "You are Harry Potter, a brave young wizard. You are kind, courageous, and determined."
}

def get_character_response(character: str, user_message: str):
    """Retrieve a character's response, either from the database or via AI."""
    character = character.lower()
    user_message = user_message.lower()

    # Step 1: Check if the dialogue exists in MongoDB
    stored_dialogue = get_dialogue(character, user_message)
    if stored_dialogue:
        return stored_dialogue

    # Step 2: If no dialogue found, use AI to generate a response
    if character not in character_personalities:
        return "I don't have knowledge of this character."

    try:
        # Use Groq AI (or OpenAI GPT API) for generating AI responses
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": character_personalities[character]},
                {"role": "user", "content": user_message}
            ]
        )
        ai_response = response.choices[0].message.content

        # Step 3: Store AI-generated response in the database for future use
        insert_dialogue(character, ai_response)

        return ai_response
    except Exception as e:
        return f"Error: {str(e)}"
