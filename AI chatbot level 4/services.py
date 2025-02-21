import redis.asyncio as redis
from dotenv import load_dotenv
from vector_db import search_similar
import os
import groq

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
REDIS_URL = os.getenv("REDIS_URL")

# Initialize Redis & Groq Client
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)
groq_client = groq.Groq(api_key=GROQ_API_KEY)

async def get_character_response(character: str, user_message: str):
    cache_key = f"{character}:{user_message}"
    
    cached_response = await redis_client.get(cache_key)
    if cached_response:
        return cached_response  # Return cached response if available

    retrieved_dialogue = await search_similar(user_message)
    
    if retrieved_dialogue:
        await redis_client.setex(cache_key, 3600, retrieved_dialogue)  # Cache for 1 hour
        return retrieved_dialogue

    # Generate response using Groq API if no match in database
    response = groq_client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": f"You are {character}. Respond in character."},
            {"role": "user", "content": user_message}
        ]
    ).choices[0].message.content

    await redis_client.setex(cache_key, 3600, response)  # Cache response for faster future retrieval
    return response
