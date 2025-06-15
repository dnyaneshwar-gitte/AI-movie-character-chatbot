# redis_cache.py
import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")      
REDIS_PORT = int(os.getenv("REDIS_PORT", 11078))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

cache = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True  
)
