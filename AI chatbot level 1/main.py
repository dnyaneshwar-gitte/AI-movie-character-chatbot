from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import groq

# Load environment variables
load_dotenv()
groq_client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))  # Use Groq API Key

app = FastAPI()

class ChatRequest(BaseModel):
    character: str
    user_message: str

# Define character personalities manually
character_personalities = {
    "iron man": "You are Tony Stark, a genius billionaire playboy philanthropist. You are witty, sarcastic, and confident.",
    "darth vader": "You are Darth Vader, a Sith Lord. You speak in a deep, commanding tone and believe in the power of the Dark Side.",
    "harry potter": "You are Harry Potter, a brave young wizard. You are kind, courageous, and determined."
}

@app.post("/chat")
def chat(request: ChatRequest):
    character = request.character.lower()  # Convert input to lowercase
    user_message = request.user_message.lower()
    
    if character not in character_personalities:
        raise HTTPException(status_code=400, detail="Character not found")
    
    try:
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",  # Use Groq model instead of OpenAI
            messages=[
                {"role": "system", "content": character_personalities[character]},
                {"role": "user", "content": user_message}
            ]
        )
        return {"character": request.character, "response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
