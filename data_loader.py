# data_loader.py
from motor.motor_asyncio import AsyncIOMotorClient
from pinecone_client import get_embedding, index
from bs4 import BeautifulSoup
from database import get_async_db
import httpx
import asyncio
import re

def is_character_line(line):
    if not line.isupper():
        return False
    if line.endswith(":") or re.match(r'^(INT\.|EXT\.)', line):
        return False
    if re.search(r'\b(FADE IN|FADE OUT|CUT TO)\b', line):
        return False
    if len(line.split()) > 4:
        return False
    return True


async def scrape_all_dialogues(url, batch_size=100):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    if response.status_code != 200:
        return {"success": False, "message": "Failed to fetch the script"}

    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find("pre") or soup.find("td", class_="scrtext")
    if not script:
        return {"success": False, "message": "Script not found in HTML"}

    lines = script.get_text().split("\n")
    current_character = None
    dialogue_buffer = []
    extracted_dialogues = []

    for line in lines:
        line = line.strip()
        if is_character_line(line):
            if current_character and dialogue_buffer:
                dialogue = " ".join(dialogue_buffer).strip()
                extracted_dialogues.append((current_character.lower(), dialogue))
                dialogue_buffer.clear()
            current_character = line
        elif current_character:
            if line == "":
                if dialogue_buffer:
                    dialogue = " ".join(dialogue_buffer).strip()
                    extracted_dialogues.append((current_character.lower(), dialogue))
                    dialogue_buffer.clear()
                current_character = None
            else:
                dialogue_buffer.append(line)

    if current_character and dialogue_buffer:
        dialogue = " ".join(dialogue_buffer).strip()
        extracted_dialogues.append((current_character.lower(), dialogue))

    db = get_async_db()
    collection = db["dialogues"]

    # Check for duplicates
    existing_set = set()
    for i in range(0, len(extracted_dialogues), 1000):
        batch = extracted_dialogues[i:i+1000]
        query = {"$or": [{"character": c, "dialogue": d} for c, d in batch]}
        cursor = collection.find(query, {"character": 1, "dialogue": 1})
        async for doc in cursor:
            existing_set.add((doc["character"], doc["dialogue"]))

    duplicate_count = sum(1 for c, d in extracted_dialogues if (c, d) in existing_set)
    if duplicate_count >= 20:
        return {"success": True, "message": "✅ Extraction skipped: Data already present with 20+ duplicates."}

    new_dialogues = [(c, d) for c, d in extracted_dialogues if (c, d) not in existing_set]

    if not new_dialogues:
        return {"success": True, "message": "No new dialogues to insert."}

    bulk_docs = [{"character": c, "dialogue": d} for c, d in new_dialogues]
    result = await collection.insert_many(bulk_docs)
    inserted_ids = result.inserted_ids

    # Pinecone batch
    pinecone_batch = []

    for idx, (c, d) in enumerate(new_dialogues):
        vector = get_embedding(d)
        if vector:
            pinecone_batch.append((str(inserted_ids[idx]), vector, {"character": c, "dialogue": d}))
        if len(pinecone_batch) >= batch_size:
            try:
                index.upsert(pinecone_batch)
                print(f"🚀 Batched {len(pinecone_batch)} vectors to Pinecone")
            except Exception as e:
                print(f"❌ Pinecone batch upsert failed: {e}")
            pinecone_batch.clear()

    if pinecone_batch:
        try:
            index.upsert(pinecone_batch)
            print(f"🚀 Final Pinecone batch with {len(pinecone_batch)} vectors")
        except Exception as e:
            print(f"❌ Final Pinecone batch upsert failed: {e}")

    return {"success": True, "message": f"✅ Extracted and stored {len(new_dialogues)} dialogues."}
