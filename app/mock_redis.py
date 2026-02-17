from typing import Optional, Any
import json
import asyncio

class MockRedis:
    def __init__(self):
        self.data = {}

    async def get(self, key: str) -> Optional[str]:
        return self.data.get(key)

    async def set(self, key: str, value: str) -> None:
        self.data[key] = value

    async def setex(self, key: str, time: int, value: str) -> None:
        self.data[key] = value
        # In a real mock, we might handle expiration, but for simple local dev/testing
        # without long-running processes, ignoring TTL or implementing a simple cleanup might suffice.
        # For now, we'll just store it.

    async def delete(self, key: str) -> None:
        if key in self.data:
            del self.data[key]

    async def close(self) -> None:
        pass
    
    @classmethod
    async def from_url(cls, url: str, decode_responses: bool = False):
        return cls()
