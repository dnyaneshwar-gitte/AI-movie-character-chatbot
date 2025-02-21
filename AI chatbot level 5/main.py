from fastapi import FastAPI, Depends
from pydantic import BaseModel
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from celery import Celery
from services import get_character_response
from database import save_chat_history, get_chat_history
import os

# Initialize FastAPI
app = FastAPI()

# Load environment variables
REDIS_URL = os.getenv("REDIS_URL")
BROKER_URL = os.getenv("CELERY_BROKER_URL")

# Redis Connection for Rate Limiting
redis_client = None

@app.on_event("startup")
async def startup():
    global redis_client
    redis_client = await redis.Redis.from_url(REDIS_URL, decode_responses=True)
    await FastAPILimiter.init(redis_client)

# Celery Setup
celery = Celery(__name__, broker=BROKER_URL)

# Request Models
class ChatRequest(BaseModel):
    user_id: str
    character: str
    user_message: str

# Chat Endpoint with Rate Limiting
@app.post("/chat", dependencies=[Depends(RateLimiter(times=5, seconds=1))])  # 5 requests per second
async def chat(request: ChatRequest):
    response = await get_character_response(request.character, request.user_message)
    
    # Save chat history to the database
    save_chat_history(request.user_id, request.character, request.user_message, response)
    
    return {"character": request.character, "response": response}

# Background Task for Asynchronous Processing
@celery.task
def chat_background_task(character: str, user_message: str):
    return get_character_response(character, user_message)
