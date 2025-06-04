# main.py
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from services import get_character_response
from data_loader import scrape_all_dialogues
from rate_limiter import enforce_rate_limit, is_rate_limited
import asyncio

app = FastAPI()

class ChatRequest(BaseModel):
    character: str
    user_message: str

class ScriptRequest(BaseModel):
    url: str

@app.post("/chat")
def chat(request: Request, body: ChatRequest):
    enforce_rate_limit(request)
    response = get_character_response(body.character, body.user_message)
    return {"character": body.character, "response": response}

@app.post("/scrape")
async def scrape_script(request: Request, data: ScriptRequest):
    enforce_rate_limit(request)
    try:
        result = await scrape_all_dialogues(data.url)
        return result
    except Exception as e:
        print(f"❌ Exception during scraping: {e}")
        return {"success": False, "message": f"Exception occurred: {str(e)}"}
    
@app.websocket("/ws/chat")
async def websocket_chat_endpoint(websocket: WebSocket):
    await websocket.accept()  # Accept the WebSocket connection

    client_ip = websocket.client.host  # Get client's IP for rate limiting

    try:
        while True:
            data = await websocket.receive_json()  # Receive JSON data from client
            character = data.get("character")
            user_message = data.get("user_message")

            # Basic validation
            if not character or not user_message:
                await websocket.send_json({"error": "Missing 'character' or 'user_message'"})
                continue

            # Rate limiting check
            if is_rate_limited(client_ip):
                await websocket.send_json({"error": "⚠️ Too many messages. Please slow down."})
                continue

            # Generate response using your service function
            response = get_character_response(character, user_message)

            # Send response back to client
            await websocket.send_json({
                "character": character,
                "response": response
            })

    except WebSocketDisconnect:
        print(f"Client disconnected: {client_ip}")
