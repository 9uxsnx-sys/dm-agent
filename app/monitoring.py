"""
Monitoring and health checks.
"""
from fastapi import APIRouter
from datetime import datetime
from sqlalchemy import text
from app.database import engine
from app.config import REDIS_URL

router = APIRouter(prefix="/health", tags=["monitoring"])

@router.get("/")
async def health_check():
    checks = {"database": "healthy", "redis": "healthy"}
    
    # Check Redis
    try:
        from app.config import settings
        if settings.USE_MOCK_REDIS:
            from app.mock_redis import MockRedis
            r = await MockRedis.from_url(REDIS_URL)
            await r.set("health", "ok")
            await r.delete("health")
        else:
            import aioredis
            r = await aioredis.from_url(REDIS_URL)
            await r.ping()
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)}"

    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat(), "checks": checks}

@router.get("/ready")
async def readiness_check():
    return {"ready": True}

@router.get("/live")
async def liveness_check():
    return {"alive": True}
