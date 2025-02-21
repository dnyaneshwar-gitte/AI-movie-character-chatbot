from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi

# Load environment variables
load_dotenv()

# Load MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "movie_chatbot"

# Connect to MongoDB
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[DB_NAME]
dialogues_collection = db["dialogues"]

# Define character aliases
character_aliases = {
    "tony": "iron man",  # Alias for Tony Stark
    "cap": "captain america",  # Alias for Captain America
    "vader": "darth vader",  # Alias for Darth Vader
    # Add other aliases here
}

# Function to insert dialogue
def insert_dialogue(character: str, dialogue: str):
    # Normalize character name to full form
    character = character_aliases.get(character.lower(), character.lower())
    dialogues_collection.insert_one({
        "character": character.lower(),
        "dialogue": dialogue
    })
    print(f"✅ Inserted into MongoDB: {character} - {dialogue[:50]}...")

# Function to get dialogue by character and user message
def get_dialogue(character: str, user_message: str):
    # Normalize character name to full form
    character = character_aliases.get(character.lower(), character.lower())
    dialogue = dialogues_collection.find_one({
        "character": character.lower(),
        "dialogue": user_message.lower()
    })
    return dialogue["dialogue"] if dialogue else None
