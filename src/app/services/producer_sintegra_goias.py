import aio_pika
import json
import logging

from config.rabbit_config import rabbit

class RabbitMQProducer:   
    def __init__(self):
        self.connection = None
        self.channel = None

    async def connect(self) -> None:        
        self.connection = await aio_pika.connect_robust(
            f"amqp://{rabbit['User']}:{rabbit['Pass']}@{rabbit['Ip']}:{rabbit['Port']}/"
        )
        self.channel = await self.connection.channel()

    async def send_message(self, queue_name: str, message: dict) -> None:
        
        if not self.channel:
            await self.connect()

        message_body = json.dumps(message)       
        queue = await self.channel.declare_queue(queue_name, durable=True)

        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message_body.encode()),
            routing_key=queue.name,
        )
        logging.info(f"Message sent to queue {queue_name}: {message_body}")

    async def close(self) -> None:   
        if self.connection:
            await self.connection.close()


