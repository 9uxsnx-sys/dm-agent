"""
Database caching utilities.
"""
import json
from typing import Optional, Any
from functools import wraps
from app.config import REDIS_URL

class DatabaseCache:
    def __init__(self):
        self.redis = None
        self.default_ttl = 300
    
    async def initialize(self):
        try:
            from app.config import settings
            if settings.USE_MOCK_REDIS:
                from app.mock_redis import MockRedis
                self.redis = await MockRedis.from_url(REDIS_URL, decode_responses=True)
            else:
                self.redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
        except Exception as e:
            print(f"[DatabaseCache] Redis unavailable: {e}")
    
    async def get(self, prefix: str, identifier: str) -> Optional[Any]:
        if not self.redis:
            return None
        key = f"db_cache:{prefix}:{identifier}"
        cached = await self.redis.get(key)
        return json.loads(cached) if cached else None
    
    async def set(self, prefix: str, identifier: str, value: Any, ttl: int = None):
        if not self.redis:
            return
        key = f"db_cache:{prefix}:{identifier}"
        await self.redis.setex(key, ttl or self.default_ttl, json.dumps(value))

db_cache = DatabaseCache()

def cached_query(prefix: str, ttl: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            identifier = str(args[0]) if args else "default"
            cached = await db_cache.get(prefix, identifier)
            if cached is not None:
                return cached
            result = await func(*args, **kwargs)
            if result is not None:
                await db_cache.set(prefix, identifier, result, ttl)
            return result
        return wrapper
    return decorator
