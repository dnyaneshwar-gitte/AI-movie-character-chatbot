from fastapi import FastAPI
from pydantic import BaseModel
from services import get_character_response

app = FastAPI()

class ChatRequest(BaseModel):
    character: str
    user_message: str

@app.post("/chat")
def chat(request: ChatRequest):
    response = get_character_response(request.character, request.user_message)
    return {"character": request.character, "response": response}
