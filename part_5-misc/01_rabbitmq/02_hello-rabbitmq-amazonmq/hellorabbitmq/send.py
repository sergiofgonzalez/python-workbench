"""Producer program that sends a single message to RabbitMQ queue"""

import os
import ssl

import certifi
import pika
from dotenv import load_dotenv

load_dotenv(override=True)  # take environment variables from .env.

RABBITMQ_URL: str = os.getenv(
    "RABBITMQ_URL", "amqps://user:pass@localhost:5671/vhost"
)

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations(certifi.where())

conn_parameters = pika.URLParameters(RABBITMQ_URL)
conn_parameters.ssl_options = pika.SSLOptions(context=ssl_context)

print(f"Connecting to {conn_parameters.host}")
connection = pika.BlockingConnection(conn_parameters)


channel = connection.channel()

channel.queue_declare(queue="hello")

channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
print(" [x] Sent 'Hello World!'")

connection.close()
