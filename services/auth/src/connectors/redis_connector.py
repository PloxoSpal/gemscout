import redis.asyncio as redis

from src.config import settings

class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client: redis.Redis | None = None

    async def connect(self):
        self.client = redis.Redis(host=self.host, port=self.port)

    async def disconnect(self):
        if self.client:
            await self.client.close()

    async def set_code(self, key: str, value: int, expire: int = 120):
        await self.client.setex(key, expire, value)

    async def get_code(self, key: str):
        value = await self.client.get(key)
        return value.decode() if value else None

    async def delete_code(self, key: str):
        await self.client.delete(key)

    async def code_exists(self, key: str):
        return await self.client.exists(key) == 1

redis_manager = RedisManager(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)

