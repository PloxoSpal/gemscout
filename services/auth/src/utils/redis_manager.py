import redis.asyncio as redis

from src.config import settings

class RedisManager:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client: redis.Redis | None = None

    async def connect(self):
        self.client = redis.Redis(host=self.host, port=self.port, decode_responses=True)

    async def disconnect(self):
        if self.client:
            await self.client.aclose()

    async def set_code(self, phone: str, value: str, ttl: int = 120):
        await self.client.setex(f'sms:{phone}', ttl, value)

    async def get_code(self, phone: str):
        return await self.client.get(f'sms:{phone}')

    async def delete_code(self, phone: str):
        await self.client.delete(f'sms:{phone}')

    async def try_lock_throttle(self, phone: str,  ttl: int = 120):
        result = await self.client.set(
            f"sms_throttle:{phone}",
            "1",
            ex=ttl,
            nx=True
        )
        return result is not None

    async def incr_attempts(self, phone: str, ttl=600):
        key = f"verify_attempts:{phone}"
        attempts = await self.client.incr(key)
        if attempts == 1:
            await self.client.expire(key, ttl)
        return attempts

    async def reset_attempts(self, phone: str):
        await self.client.delete(f"verify_attempts:{phone}")

    async def blacklist_token(self, jti, ttl: int):
        await self.client.setex(f"blacklist_token:{jti}", ttl, "1")

    async def is_blacklisted(self, jti: str):
        return await self.client.get(f"blacklist_token:{jti}") is not None

redis_manager = RedisManager(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)

