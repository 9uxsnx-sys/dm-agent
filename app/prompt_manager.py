"""
Prompt Manager - Caches prompts in memory and Redis to avoid file I/O.
"""
import os
import asyncio
from typing import Dict, Optional
from app.config import REDIS_URL

class PromptManager:
    def __init__(self):
        self._memory_cache: Dict[str, str] = {}
        self._redis: Optional[object] = None # Changed type hint to object as it can be aioredis.Redis or MockRedis
        self._initialized = False
    
    async def initialize(self):
        if not self._initialized:
            try:
                if self._redis is None:
                    from app.config import settings
                    if settings.USE_MOCK_REDIS:
                        from app.mock_redis import MockRedis
                        self._redis = await MockRedis.from_url(REDIS_URL, decode_responses=True)
                    else:
                        import aioredis
                        self._redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
                
                await self._load_all_prompts()
                self._initialized = True
            except Exception as e:
                print(f"[PromptManager] Redis unavailable: {e}")
                await self._load_all_prompts_from_files()
                self._initialized = True
    
    async def _load_all_prompts(self):
        prompt_files = {
            "intent": "prompts/intent.txt",
            "extract": "prompts/extract.txt",
            "response": "prompts/response.txt"
        }
        for name, filepath in prompt_files.items():
            content = await self._read_file(filepath)
            if content:
                self._memory_cache[name] = content
                if self._redis:
                    await self._redis.setex(f"prompt:{name}", 3600, content)
    
    async def _read_file(self, filepath: str) -> Optional[str]:
        try:
            if not os.path.exists(filepath):
                return None
            loop = asyncio.get_event_loop()
            with open(filepath, 'r', encoding='utf-8') as f:
                return await loop.run_in_executor(None, f.read)
        except Exception as e:
            print(f"[PromptManager] Error reading {filepath}: {e}")
            return None
    
    async def get_prompt(self, name: str) -> str:
        if name in self._memory_cache:
            return self._memory_cache[name]
        if self._redis:
            cached = await self._redis.get(f"prompt:{name}")
            if cached:
                self._memory_cache[name] = cached
                return cached
        return self._get_default_prompt(name)
    
    def _get_default_prompt(self, name: str) -> str:
        defaults = {
            "intent": "Categorize into: NEW_ORDER, CHECK_ORDER, COMPLAINT, OTHER",
            "extract": "Extract product, quantity, customer_type. Return JSON.",
            "response": "Draft a polite, professional response. Keep it short."
        }
        return defaults.get(name, "You are a helpful assistant.")

prompt_manager = PromptManager()

async def get_prompt(name: str) -> str:
    if not prompt_manager._initialized:
        await prompt_manager.initialize()
    return await prompt_manager.get_prompt(name)
