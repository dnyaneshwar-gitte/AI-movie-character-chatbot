import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import redis.asyncio as redis

# Load Environment Variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
REDIS_URL = os.getenv("REDIS_URL")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

if PINECONE_INDEX not in [idx["name"] for idx in pc.list_indexes()]:
    raise ValueError(f"Pinecone index '{PINECONE_INDEX}' does not exist.")

index = pc.Index(PINECONE_INDEX)
model = SentenceTransformer("all-MiniLM-L6-v2")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

async def search_similar(query):
    query_vector = model.encode(query).tolist()
    results = index.query(vector=query_vector, top_k=5, include_metadata=True)

    if results and "matches" in results and results["matches"]:
        return results["matches"][0].get("metadata", {}).get("dialogue", "")

    return None
