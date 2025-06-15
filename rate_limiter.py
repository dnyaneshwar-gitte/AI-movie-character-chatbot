# rate_limiter.py
import time
from redis_cache import cache
from fastapi import Request, HTTPException

RATE_LIMIT = 100  
WINDOW_SIZE = 1 

def get_user_ip(request: Request) -> str:
    return request.client.host  

def is_rate_limited(user_ip: str) -> bool:
    key = f"rate:{user_ip}"
    current_count = cache.get(key)

    if current_count is None:
        
        cache.setex(key, WINDOW_SIZE, 1)
        return False
    elif int(current_count) < RATE_LIMIT:
    
        cache.incr(key)
        return False
    else:
        return True

def enforce_rate_limit(request: Request):
    user_ip = get_user_ip(request)
    if is_rate_limited(user_ip):
        raise HTTPException(
            status_code=429,
            detail="⚠️ Too many requests. Please slow down."
        )
