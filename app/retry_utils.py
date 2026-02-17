"""
Retry utilities with exponential backoff.
"""
import functools
import asyncio
import random
from typing import Callable, Any

def async_retry(max_attempts: int = 3, initial_delay: float = 1.0, exceptions: tuple = (Exception,)):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            for attempt in range(1, max_attempts + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    await asyncio.sleep(delay * (0.5 + random.random()))
                    delay *= 2
            raise RuntimeError(f"Retry loop exited unexpectedly in {func.__name__}")
        return wrapper
    return decorator
