import aio_pika
import asyncio
import json
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
import aiohttp
import time


class RabbitMQWorker:
    def __init__(self, rabbitmq_url: str, telegram_token: str, chat_id: str):
        self.rabbitmq_url = rabbitmq_url
        self.telegram_token = telegram_token
        self.chat_id = chat_id 
        self.bot = Bot(token=telegram_token)
        self.dp = Dispatcher() 
        self.dp["bot"] = self.bot
        self.connection = None
        self.channel = None

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(self.rabbitmq_url)
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

    async def listen_to_queue(self, queue_name: str) -> None:
        queue = await self.channel.declare_queue(queue_name, durable=True)
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    user_data = json.loads(message.body)
                    await self.send_welcome_message(user_data["username"])

    async def send_welcome_message(self, username: str) -> None:
        welcome_message = f"Привет, {username}!"
        await self.bot.send_message(self.chat_id, welcome_message)

    async def close(self) -> None:
        if self.channel:
            await self.channel.close()
        if self.connection:
            await self.connection.close()

    async def start(self) -> None:

        await self.connect()
        try:
            await self.listen_to_queue("user_registered")
        except asyncio.CancelledError:
            print("Worker stopped")
        finally:
            await self.close()


if __name__ == "__main__":
    print("Hello!")
    RABBITMQ_URL = "amqp://guest:guest@rabbitmq:5672/"
    TELEGRAM_TOKEN = os.getenv("TGBOT_TOKEN", None)
    CHAT_ID = os.getenv("CHAT_ID", None)
    print("Hello!")
    time.sleep(15)
    
    worker = RabbitMQWorker(RABBITMQ_URL, TELEGRAM_TOKEN, CHAT_ID)

    asyncio.run(worker.start())