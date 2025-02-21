from pymongo import MongoClient
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Pinecone and MongoDB
PINECONE_API_KEY = os.getenv("VECTOR_DB_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME")

pinecone = Pinecone(api_key=PINECONE_API_KEY)
model = SentenceTransformer("all-MiniLM-L6-v2")
index_name = "aichatbot"  # Change this to your Pinecone index name

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

# Initialize Pinecone index (create if it doesn't exist)
if index_name not in pinecone.list_indexes().names():
    pinecone.create_index(
        name=index_name,
        dimension=384,  # Dimensionality of "all-MiniLM-L6-v2"
        metric="cosine"
    )

# Connect to the index
index = pinecone.Index(index_name)

def generate_embedding(text):
    """Generate an embedding vector for a given text."""
    return model.encode(text).tolist()

def store_embeddings_in_pinecone():
    """Retrieve dialogues from MongoDB and store their embeddings in Pinecone."""
    dialogues = collection.find()  # Fetch all documents from MongoDB collection
    
    for dialogue in dialogues:
        dialogue_text = dialogue.get("dialogue", "")  # Adjust this if your dialogue field has a different name
        if not dialogue_text:
            continue
        
        # Generate embedding for the dialogue
        dialogue_id = str(dialogue["_id"])  # Using MongoDB's unique _id as the Pinecone ID
        embedding = generate_embedding(dialogue_text)
        
        # Store the embedding in Pinecone
        index.upsert([(dialogue_id, embedding)])
        print(f"✅ Stored embedding for dialogue: {dialogue_text[:50]}...")
        
# Call this function to migrate data from MongoDB to Pinecone
store_embeddings_in_pinecone()
