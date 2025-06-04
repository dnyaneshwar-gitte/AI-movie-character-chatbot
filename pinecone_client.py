# pinecone_client.py

import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# Load local embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Pinecone config
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_REGION = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")  # fallback
INDEX_NAME = "movie-script"

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)

# Create index if not exists (dim=384 for MiniLM)
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=384,  # MiniLM outputs 384-dim vectors
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=PINECONE_REGION)
    )

# Connect to index
index = pc.Index(INDEX_NAME)

# Local embedding function
def get_embedding(text: str) -> list:
    try:
        vector = model.encode(text)
        return vector.tolist()
    except Exception as e:
        print(f"❌ Embedding error for text: '{text[:50]}' — {e}")
        return []
