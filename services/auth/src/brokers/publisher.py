import aio_pika
from aio_pika.abc import AbstractConnection, AbstractChannel

from src.config import settings

class RabbitMQManager:
    def __init__(self, url: str):
        self.url = url
        self.connection: AbstractConnection | None = None
        self.channel: AbstractChannel | None = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()

    async def disconnect(self):
        if self.connection:
            await self.connection.close()

    async def publish(self, routing_key: str, body: bytes):
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=body),
            routing_key=routing_key,
        )

rabbitmq_manager = RabbitMQManager(url=settings.RABBITMQ_URL)