from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Pinecone
PINECONE_API_KEY = os.getenv("VECTOR_DB_API_KEY")
pinecone = Pinecone(api_key=PINECONE_API_KEY)
index_name = "aichatbot"  # Change this to your Pinecone index name
index = pinecone.Index(index_name)

# Load SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embedding(text):
    """Generate an embedding vector for a given text."""
    return model.encode(text).tolist()

def search_similar(query):
    """Find the most similar dialogue from the index."""
    query_vector = generate_embedding(query)
    
    # Perform a similarity search in Pinecone
    results = index.query(vector=query_vector, top_k=1, include_metadata=True)
    
    if results["matches"]:
        return results["matches"][0].get("metadata", {}).get("dialogue", "")  # ✅ Return actual dialogue text
    return None

