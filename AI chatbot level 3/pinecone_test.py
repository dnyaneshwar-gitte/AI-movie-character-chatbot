import os
from pinecone import Pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get Pinecone API Key from .env
PINECONE_API_KEY = os.getenv("VECTOR_DB_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("Pinecone API Key is missing. Check your .env file.")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# List existing indexes
try:
    indexes = pc.list_indexes().names()  # Get index names
    print("✅ Pinecone is working! Available indexes:", indexes)
except Exception as e:
    print("❌ Error connecting to Pinecone:", e)
