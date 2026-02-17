import json
from app.config import REDIS_URL

redis = None

async def get_redis():
    global redis
    if redis is None:
        from app.config import settings
        if settings.USE_MOCK_REDIS:
            from app.mock_redis import MockRedis
            redis = await MockRedis.from_url(REDIS_URL, decode_responses=True)
        else:
            redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
    return redis

async def get_session(user_id: str):
    r = await get_redis()
    data = await r.get(f"session:{user_id}")
    return json.loads(data) if data else None

async def set_session(user_id: str, data: dict):
    r = await get_redis()
    await r.setex(f"session:{user_id}", 3600, json.dumps(data))

async def clear_session(user_id: str):
    r = await get_redis()
    await r.delete(f"session:{user_id}")
