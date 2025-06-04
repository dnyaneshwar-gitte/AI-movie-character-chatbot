# redis_cache.py
import redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")       # e.g., "my-redis.website.com"
REDIS_PORT = int(os.getenv("REDIS_PORT", 11078))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

# Create Redis client
cache = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True  # so we get strings not bytes
)
