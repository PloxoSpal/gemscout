from typing import Annotated
from fastapi import Depends
from src.utils.redis_manager import redis_manager, RedisManager

def get_redis() -> RedisManager:
    return redis_manager

RedisDep = Annotated[RedisManager, Depends(get_redis)]