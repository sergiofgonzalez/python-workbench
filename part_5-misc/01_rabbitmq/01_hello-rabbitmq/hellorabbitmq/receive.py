"""Consumer program that outputs messages from a RabbitMQ queue"""

import os
import sys

import pika
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD),
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue="hello")

    def callback(
        ch, method, properties, body
    ):  # pylint: disable=W0613:unused-argument
        print(f" [x] Received {body}")

    channel.basic_consume(
        queue="hello", on_message_callback=callback, auto_ack=True
    )

    print("Waiting for messages. Press CTRL+C to exit")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
