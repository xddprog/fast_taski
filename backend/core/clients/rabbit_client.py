import asyncio
import json
from random import choice
import time
from typing import Any
import aio_pika
from aio_pika.abc import AbstractQueue
from fastapi import HTTPException
import orjson
from backend.infrastructure.config.broker_configs import RABBIT_CONFIG


class RabbitClient:
    def __init__(self):
        self.connection: aio_pika.Connection = None
        self.channel: aio_pika.Channel = None
        self._initialized = False

    async def declare_queue(self, queue_name: str) -> AbstractQueue:
        if not self._initialized:
            await self.init_connection()
        return await self.channel.declare_queue(queue_name, durable=True)

    async def declare_delayed_queue(
        self, 
        queue_name: str, 
        dead_letter_exchange: str, 
        dead_letter_routing_key: str
    ) -> AbstractQueue:
        if not self._initialized:
            await self.init_connection()
        dlx = await self.channel.declare_exchange(dead_letter_exchange, durable=True)
        queue = await self.channel.declare_queue(queue_name, durable=True, arguments={
            "x-dead-letter-exchange": dead_letter_exchange,
            "x-dead-letter-routing-key": dead_letter_routing_key
        })
        dlx = await self.channel.get_exchange(dlx.name)
        tasks_queue = await self.channel.get_queue("tasks_queue")
        await tasks_queue.bind(dlx, routing_key=dead_letter_routing_key)
        return queue

    async def send_message(self, queue_name: str, message: dict):
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=orjson.dumps(message), expiration=5), 
            routing_key=queue_name,
        )

    async def send_delayed_message(self, queue_name: str, message: dict, delay: int):
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=orjson.dumps(message), expiration=delay),
            routing_key=queue_name
        )

    async def get_queue(self, queue_name: str):
        return await self.channel.get_queue(queue_name)

    async def init_connection(self):
        self.connection = await aio_pika.connect_robust(
            host=RABBIT_CONFIG.RABBIT_HOST,
            port=RABBIT_CONFIG.RABBIT_PORT,
            login=RABBIT_CONFIG.RABBIT_USER,
            password=RABBIT_CONFIG.RABBIT_PASS,
        )
        self.channel = await self.connection.channel()
        return self

    async def delete_queue(self, queue_name: str):
        await self.channel.queue_delete(queue_name)

    async def close(self):
        if self.connection:
            await self.connection.close()
        if self.channel:
            await self.channel.close()
