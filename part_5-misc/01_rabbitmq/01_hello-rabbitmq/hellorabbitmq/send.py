"""Producer program that sends a single message to RabbitMQ queue"""

import os

import pika
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD),
    )
)

channel = connection.channel()

channel.queue_declare(queue="hello")

channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
print(" [x] Sent 'Hello World!'")

connection.close()
