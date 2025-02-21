from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi
from datetime import datetime

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "movie_chatbot"

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[DB_NAME]
dialogues_collection = db["dialogues"]
chat_history_collection = db["chat_history"]

def insert_dialogue(character: str, dialogue: str):
    dialogues_collection.insert_one({"character": character.lower(), "dialogue": dialogue})

def get_dialogue(character: str, user_message: str):
    return dialogues_collection.find_one({"character": character.lower(), "dialogue": user_message.lower()})

def save_chat_history(user_id: str, character: str, user_message: str, bot_response: str):
    chat_history_collection.insert_one({
        "user_id": user_id,
        "character": character,
        "user_message": user_message,
        "bot_response": bot_response,
        "timestamp": datetime.utcnow()
    })

def get_chat_history(user_id: str, limit: int = 50):
    return list(chat_history_collection.find({"user_id": user_id}).sort("timestamp", -1).limit(limit))
