from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "movie_chatbot"

client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
db = client[DB_NAME]
dialogues_collection = db["dialogues"]

def insert_dialogue(character: str, dialogue: str):
    dialogues_collection.insert_one({"character": character.lower(), "dialogue": dialogue})

def get_dialogue(character: str, user_message: str):
    return dialogues_collection.find_one({"character": character.lower(), "dialogue": user_message.lower()})
