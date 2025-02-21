from vector_db import search_similar
import groq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
groq_client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

# Mapping character aliases to full names
character_aliases = {
    "tony": "iron man",
    "steve": "captain america",
    "darth": "darth vader",
    # Add more aliases if needed
}

# Character personalities
character_personalities = {
    "iron man": "You are Tony Stark, a brilliant engineer and billionaire who is also a member of the Avengers.",
    "captain america": "You are Steve Rogers, also known as Captain America, a super-soldier and a key figure in the Avengers.",
    "darth vader": "You are Darth Vader, the Sith Lord formerly known as Anakin Skywalker, a key figure in the Star Wars universe.",
    # Add more personalities as needed
}

def get_character_response(character: str, user_message: str):
    # Normalize character name to full form using the alias dictionary
    normalized_character = character_aliases.get(character.lower(), character.lower())
    
    # Retrieve the most relevant dialogue from Pinecone
    retrieved_dialogue = search_similar(user_message)
    context = retrieved_dialogue if retrieved_dialogue else ""
    
    # If the character is not recognized in the personality dictionary
    if normalized_character not in character_personalities:
        return "I don't know this character."
    
    # Generate a response using the Groq API with the retrieved context
    response = groq_client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {"role": "system", "content": character_personalities[normalized_character]},
        {"role": "user", "content": f"Context: {context}\nUser: {user_message}"}
    ]
)

    
    return response.choices[0].message.content
