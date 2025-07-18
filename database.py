from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from bson import ObjectId
from pinecone_client import index, get_embedding
import certifi
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "movie_chatbot"

async_client = AsyncIOMotorClient(MONGO_URI, tlsCAFile=certifi.where())
async_db = async_client[DB_NAME]

sync_client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
sync_db = sync_client[DB_NAME]
dialogues_collection = sync_db["dialogues"]
profiles_collection = sync_db["character_profiles"]

def get_async_db():
    return async_db

def get_personality(character: str):
    result = profiles_collection.find_one({"character": character.lower()})
    return result["personality"] if result else None

def insert_personality(character: str, personality: str):
    profiles_collection.insert_one({
        "character": character.lower(),
        "personality": personality
    })

def insert_dialogue(character: str, dialogue: str, skip_pinecone=False):
    exists = dialogues_collection.find_one({
        "character": character.lower(),
        "dialogue": dialogue
    })
    if exists:
        return None  # Avoid duplicates

    result = dialogues_collection.insert_one({
        "character": character.lower(),
        "dialogue": dialogue
    })

    inserted_id = str(result.inserted_id)
    print(f"✅ Inserted: {character} - {dialogue[:50]}...")

    if skip_pinecone:
        return {"_id": inserted_id, "character": character.lower(), "dialogue": dialogue}

    try:
        vector = get_embedding(dialogue)
        metadata = {
            "character": character.lower(),
            "dialogue": dialogue
        }
        index.upsert([(inserted_id, vector, metadata)])
    except Exception as e:
        print(f"❌ Pinecone upsert failed: {e}")

    return None

def query_pinecone(character: str, user_message: str, top_k=3):
    query_vector = get_embedding(user_message)
    query_filter = {"character": character.lower()}

    try:
        result = index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True,
            filter=query_filter
        )

        if result and result.matches:
            return [match.metadata.get("dialogue", "") for match in result.matches if match.metadata.get("dialogue")]
    except Exception as e:
        print(f"❌ Pinecone query failed: {e}")

    return []

def get_dialogue(character: str, user_message: str):
    character = character.strip().lower()
    user_message = user_message.strip()

    print(f"🔍 Looking for dialogue from character like '{character}', message: {user_message}")

    result = dialogues_collection.find_one({
        "character": character,
        "dialogue": user_message
    })
    if result:
        return result["dialogue"]

    result = dialogues_collection.find_one({
        "character": {"$regex": f"^{character}$", "$options": "i"},
        "dialogue": user_message
    })
    if result:
        return result["dialogue"]

    result = dialogues_collection.find_one({
        "character": {"$regex": character, "$options": "i"},
        "dialogue": {"$regex": user_message, "$options": "i"}
    })
    if result:
        return result["dialogue"]

    print("⚠️ No match found.")
    return None
