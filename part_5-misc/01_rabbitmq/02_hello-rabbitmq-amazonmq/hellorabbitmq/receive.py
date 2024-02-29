"""Consumer program that outputs messages from a RabbitMQ queue"""

import os
import ssl
import sys
from datetime import datetime

import certifi
import pika
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "")

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.load_verify_locations(certifi.where())


def main():
    conn_parameters = pika.URLParameters(RABBITMQ_URL)
    conn_parameters.ssl_options = pika.SSLOptions(context=ssl_context)
    connection = pika.BlockingConnection(conn_parameters)
    channel = connection.channel()
    channel.queue_declare(queue="hello")

    def callback(
        ch, method, properties, body
    ):  # pylint: disable=W0613:unused-argument
        print(f" [x] Received {body!r} at {datetime.utcnow()}")

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
