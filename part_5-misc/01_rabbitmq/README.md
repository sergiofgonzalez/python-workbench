# RabbitMQ concepts and projects



## Intro

RabbitMQ is a message broker: it accepts and forwards messages.

RabbitMQ, and messaging systems in general, uses some specific jargon:

+ **Producing** &mdash; sending a message. A program that sends messages is a producer and is denoted as:

    ![Producer](pics/producer.png)

+ **Queue** &mdash; a queue is the place where messages are stored. It's essentially a large message buffer.

    Many *producers* can send messages that go to one queue, and many *consumers* can try to receive data from one queue.

    ![Queue](pics/queue.png)


+ **Consuming** &mdash; receiving a message. A consumer is a program that mostly waits to receive messages.

    ![Consumer](pics/consumer.png)


In a messaging system, *producer*, *consumer*, and *broker* do not have to reside on the same host. Also, an application can be both a *producer* and *consumer* too.

## Hello RabbitMQ with `pika`

In this section we write two small programs:
+ a producer (sender) that sends a single message.
+ a consumer (receiver) that receives messages and prints them out.

The overall design look like the following:

![Hello world RabbitMQ](pics/hello-world-rabbitmq.png)

RabbitMQ speaks multiple protocols. This tutorial uses AMQP-0-9-1, which is an open, general-purpose protocol for messaging. The `pika` client can be used to interact with RabbitMQ.

### Producer

The producer code looks like the following:

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="hello")

channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")
print(" [x] Sent 'Hello World!'")

connection.close()
```

The first thing is to establish the connection to the RabbitMQ server, which we do using `pika.BlockingConnection()` function followed by the `connection.channel()` call. In the example, we're establishing the connection to `localhost`.

If you need to include credentials you can use:

```bash
connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost",
        credentials=pika.PlainCredentials(
            {user}, {password}
        ),
    )
)
```

Before sending the message, we need to make sure the recipient queue exists. Otherwise, RabbitMQ will simply ignore the message. We do so using `queue_declare`. This function will cre

In RabbitMQ, messages are not sent directly to the queue &mdash; it always needs to go through an exchange. For our simple scenario, we can use the default exchange identified by the empty string. The `routing_key` identifies the queue in which the message should go. The `body` identifies the message payload.

Finally, we call `connection.close()` to make sure network buffers are flushed and our message delivered to RabbitMQ.


## Receiving

The `receive.py` program will receive messages from the queue and print them on the screen.

The following snippet illustrates how to do that:

```python
"""Consumer program that outputs messages from a RabbitMQ queue"""

import sys

import pika


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="localhost",
            credentials=pika.PlainCredentials(
                "{user}", "{password}"
            ),
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue="hello")

    def callback(ch, method, properties, body):
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
```

Because the program is a bit more complicated, it's been structured on a dedicated `main()` function. Because the program will run until the user decides to stop it, we include a `KeyboardInterrupt` exception block to trap when the user types CTRL+C:

```python
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        sys.exit(0)
```

In the `main()` function, we begin by establishing the connection and getting the channel.

Then we use again:

```python
channel.queue_declare(queue="hello")
```

This is a good practice because we don't know if the queue is already there or not. If it has already been created, invoking `queue_declare()` will have no effect, otherwise, it will create the queue so that the consumer logic can work.

Receiving messages from the queue requires that you subscribe a callback function to a queue. Whenever you receive a message this callback function will be executed.

In our simple example, the callback implementation will simply print the message contents:

```python
def callback(ch, method, properties, body):
    print(f" [x] Received {body}")
```

Immediately after, you instruct RabbitMQ to invoke that callback when messages pop up in the `"hello"` queue:

```python
channel.basic_consume(
    queue="hello", on_message_callback=callback, auto_ack=True
)
```

| NOTE: |
| :---- |
| The `auto_ack` will remove the mesage from the queue automatically as soon as the callback is invoked. This is the appropriate thing to do in this simple example, but in more complicated cases you will want to handle the acknowledgement in your code.<br>When doing so you can force the message to reappear in the queue if there's a problem managing the message. |


Finally, we enter a never-ending loop that waits for messages on the given queue and invoke callbacks when a message pops up.

```python
channel.start_consuming()
```

## Using rabbitmqctl

When using the docker container, you can do:

```bash
$ docker exec rabbitmq rabbitmqctl list_queues
Timeout: 60.0 seconds ...
Listing queues for vhost / ...
name    messages
hello   1
```