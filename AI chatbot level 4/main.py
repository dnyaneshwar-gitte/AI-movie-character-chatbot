from fastapi import FastAPI, Depends
from pydantic import BaseModel
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from celery import Celery
from celery.result import AsyncResult
import os
from services import get_character_response

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

class ChatRequest(BaseModel):
    character: str
    user_message: str

from celery.result import AsyncResult



@app.post("/chat", dependencies=[Depends(RateLimiter(times=5, seconds=1))])  # 5 requests/sec per user
async def chat(request: ChatRequest):
    response = await get_character_response(request.character, request.user_message)
    return {"character": request.character, "response": response}

@celery.task
def chat_background_task(character: str, user_message: str):
    response = get_character_response(character, user_message)
    return response
