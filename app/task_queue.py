"""
Background task queue.
"""
import asyncio
from app.config import REDIS_URL

class BackgroundTaskQueue:
    def __init__(self):
        self.redis = None
        self.running = False
    
    async def initialize(self):
        if self.redis is None:
            from app.config import settings
            if settings.USE_MOCK_REDIS:
                from app.mock_redis import MockRedis
                self.redis = await MockRedis.from_url(REDIS_URL, decode_responses=True)
            else:
                import aioredis
                self.redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
        self.running = True
    
    async def stop(self):
        self.running = False

task_queue = BackgroundTaskQueue()
