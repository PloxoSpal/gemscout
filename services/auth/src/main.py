from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from src.utils.redis_manager import redis_manager
from src.brokers.publisher import rabbitmq_manager
from src.api.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    await rabbitmq_manager.connect()
    yield
    await redis_manager.disconnect()
    await rabbitmq_manager.disconnect()

app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)

if __name__ == '__main__':
    uvicorn.run('src.main:app', host="0.0.0.0", port=8002, reload=True)