from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "movie_chatbot"

# Connect to MongoDB
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())  
db = client[DB_NAME]
dialogues_collection = db["dialogues"]

def insert_dialogue(character: str, dialogue: str):
    """Insert a new character dialogue into MongoDB."""
    dialogues_collection.insert_one({"character": character.lower(), "dialogue": dialogue})
    print(f"✅ Inserted into MongoDB: {character} - {dialogue[:50]}...")  # Debugging

def get_dialogue(character: str, user_message: str):
    """Search for a dialogue in MongoDB using flexible matching."""
    print(f"🔍 Searching for dialogues of '{character}' matching: {user_message}")  # Debugging

    # First, try an exact match
    result = dialogues_collection.find_one({"character": character.lower(), "dialogue": user_message})
    if result:
        return result["dialogue"]

    # If not found, try a flexible regex search for partial matching
    query = {"character": character.lower(), "dialogue": {"$regex": user_message, "$options": "i"}}
    result = dialogues_collection.find_one(query)
    if result:
        return result["dialogue"]

    print(f"⚠️ No exact or partial match found in database for '{character}'.")
    return None
