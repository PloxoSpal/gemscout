from typing import Annotated
from fastapi import Depends
from src.connectors.redis_connector import redis_manager, RedisManager

def get_redis() -> RedisManager:
    return redis_manager

RedisDep = Annotated[RedisManager, Depends(get_redis)]