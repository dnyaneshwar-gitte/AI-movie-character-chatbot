import requests
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from vector_db import store_embedding
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Pinecone and SentenceTransformer
PINECONE_API_KEY = os.getenv("VECTOR_DB_API_KEY")
index_name = "aichatbot"  # Pinecone index name
model = SentenceTransformer("all-MiniLM-L6-v2")

def scrape_movie_script(url, character):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Failed to fetch page: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find("pre") or soup.find("td", class_="scrtext")
    if not script:
        print("❌ No script found!")
        return

    character_lower = character.lower()
    lines = script.get_text().split("\n")
    
    for i, line in enumerate(lines):
        if line.strip().lower() == character_lower and i + 1 < len(lines):
            # Capture 3-5 lines after the character's name
            dialogue = " ".join(lines[i+1:i+5]).strip()  
            
            if dialogue:
                dialogue_id = f"{character_lower}_{i}"
                store_embedding(dialogue, dialogue_id)
