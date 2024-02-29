# Hello, RabbitMQ
> the simplest pub/sub example in RabbitMQ

## Running RabbitMQ using Docker

```bash
docker run -d --hostname my-rabbitmq --name rabbitmq \
-p 8080:15672 \
-p 5672:5672 \
-e RABBITMQ_DEFAULT_USER={rabbitmq_user} \
-e RABBITMQ_DEFAULT_PASS={rabbitmq_password} \
rabbitmq:3-management
```

You can access the console in http://localhost:8080, you can connect to the server using the port 5672.

You can also run `rabbitmqctl` commands using Docker:

```bash
$ docker exec rabbitmq rabbitmqctl list_queues
Timeout: 60.0 seconds ...
Listing queues for vhost / ...
name    messages
hello   1
```

## Running the application

The application consists of a *producer* (`send.py`) that writes messages to a `"hello"` queue, and a *consumer* (`receive.py`) that run continuously waiting for messages on that queue and prints them.

The project uses `poetry`, therefore, you'll first need to do:

```bash
poetry install
```


For the application configuration, the project uses [python-dotenv](https://github.com/theskumar/python-dotenv).

The following snippet lists the contents of the `.env` file, whose values can also be overridden with environment variables:

```bash
# RabbitMQ config parameters
RABBITMQ_HOST="localhost"
RABBITMQ_USER="..."
RABBITMQ_PASSWORD="..."
```

With the packages installed you can run:

```bash
# The consumer runs until you press CTRL+C
poetry run python hellorabbitmq/receive.py
```

And in another terminal, you can run the producer:

```bash
# The consumer runs until you press CTRL+C
poetry run python hellorabbitmq/send.py
```
