import aio_pika
import json
from aio_pika import Message, DeliveryMode, Channel, Connection
from typing import Any

class RabbitMQProducer:
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self.connection: Connection = None
        self.channel: Channel = None

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()

    async def publish_message(self, message: Any, queue_name: str) -> None:
        if not self.connection or not self.channel:
            await self.connect()

        message_json = json.dumps(message)
        
        await self.channel.default_exchange.publish(
            Message(body=message_json.encode(), delivery_mode=DeliveryMode.PERSISTENT),
            routing_key=queue_name
        )

    async def close(self) -> None:
        if self.channel:
            await self.channel.close() 

        if self.connection:
            await self.connection.close() 