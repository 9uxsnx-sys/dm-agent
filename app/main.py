from fastapi import FastAPI
from app.router import router
from db import Base, engine
from app.prompt_manager import prompt_manager
from app.webhook_security import webhook_security
from app.db_cache import db_cache
from app.task_queue import task_queue
from app.monitoring import router as monitoring_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await prompt_manager.initialize()
    await webhook_security.initialize()
    await db_cache.initialize()
    await task_queue.initialize()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await task_queue.stop()

app = FastAPI(
    title="AI Sales Agent",
    version="2.0.0",
    lifespan=lifespan
)

app.include_router(router)
app.include_router(monitoring_router)

@app.get("/")
async def root():
    return {"message": "AI Sales Agent", "version": "2.0.0"}
