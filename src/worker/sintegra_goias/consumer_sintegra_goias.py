import aio_pika
import asyncio
import json
import logging
from config.rabbit_config import rabbit
from controllers.sintegra_goias_controller import SintegraGoiasController

class RabbitMQConsumer:
    def __init__(self):
        self.queue_name = "CRAWLER_CNPJ_SINTEGRA_GOIAS"
        self.connection = None
        self.channel = None
        self.controller = SintegraGoiasController()

    async def connect(self) -> None:
        self.connection = await aio_pika.connect_robust(
            f"amqp://{rabbit['User']}:{rabbit['Pass']}@{rabbit['Ip']}:{rabbit['Port']}/"
        )
        self.channel = await self.connection.channel()
        await self.channel.set_qos(prefetch_count=1)

    async def process_message(self, message) -> None:
        async with message.process():
            try:
                msg = json.loads(message.body)
                self.controller.scraping(msg)
            except Exception as e:
                logging.error("Error processing message: %s", e)

    async def consume(self) -> None:
        queue = await self.channel.declare_queue(self.queue_name, durable=True)
        async for message in queue:
            await self.process_message(message)

    async def run(self) -> None:
        await self.connect()
        await self.consume()

if __name__ == "__main__":
    consumer = RabbitMQConsumer()
    asyncio.run(consumer.run())
