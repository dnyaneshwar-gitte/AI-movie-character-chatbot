from fastapi import FastAPI
from pydantic import BaseModel
from services import get_character_response

# Initialize FastAPI app
app = FastAPI()

class ChatRequest(BaseModel):
    character: str
    user_message: str

@app.post("/chat")
def chat(request: ChatRequest):
    """Handles chat requests by first checking the database for a response and falling back to AI if needed."""
    response = get_character_response(request.character, request.user_message)
    return {"character": request.character, "response": response}
