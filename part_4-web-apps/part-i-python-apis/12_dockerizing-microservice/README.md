# Dockerizing microservice APIs

+ How to dockerize an application
+ How to use Docker Compose to run an application
+ Publishing a Docker image to AWS ECR

## Intro

In this chapter, we will see how to Dockerize a Python application. We will focus on dockerizing (i.e., making an application run as a Docker container) the Orders service.

## Dockerizing the Orders Service

In our first take, we take a simplistic approach that pretty much resembles how we run the application in our local environment:

```dockerfile
FROM python:3.10-slim

LABEL maintainer="sergio.f.gonzalez@gmail.com"
ENV REFRESHED_AT "2024-01-29 09:23:14.443427"

# Use SQLite as the default DB engine
ENV DB_URL=sqlite:///orders.db

RUN mkdir -p /orders_svc/orders

WORKDIR /orders_svc

COPY pyproject.toml poetry.lock /orders_svc/

# Create virtual environment within the project
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN pip install -U poetry && poetry install --no-root --no-directory --without dev


COPY orders/orders_service /orders_svc/orders/orders_service
COPY orders/repository /orders_svc/orders/repository
COPY orders/web /orders_svc/orders/web
COPY oas.yaml /orders_svc/oas.yaml
COPY public_key /orders_svc/public_key

EXPOSE 8080

CMD ["poetry", "run", "uvicorn", "orders.web.app:app", "--host", "0.0.0.0", "--port", "8080"]
```

The only relevant details of this first version are:

+ We use `python:3.10-slim` as the base image
+ We define the default value for `DB_URL` and configure it to point to a local file named `orders.db` (as we do when running without a container).
+ We create a directory `orders_svc/` within the container to host our application artifacts.
+ We copy the `pyproject.toml` and the corresponding lockfile, install poetry and install without the dev dependencies. Note that we instruct poetry to install the virtual environment within the project.
+ We copy the corresponding relevant sources to `orders_svc/`
+ We define 8080 as the default port for the web app
+ We run the application with `poetry run`

## Improving the container image with multi-stage builds

The previous image can be made more flexible and at the same time improve its size by using build arguments and multi-stage builds.

By adding build args, you can use the same Dockerfile template for different microservices (no matter the name):

```dockerfile
# Global build args
ARG APP_BASE_PATH=/home/pyuser/app
ARG APP_PACKAGE_NAME=web_svc

# Stage 1: Install dependencies
FROM python:3.10-slim as builder

ARG APP_BASE_PATH

WORKDIR $APP_BASE_PATH

COPY pyproject.toml poetry.lock ./

# Create virtual environment within the project
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN pip install -U poetry
RUN poetry install --no-root --no-directory --without dev

# Stage 2: Prepare runtime
FROM python:3.10-slim as runtime

ARG APP_BASE_PATH
ARG APP_PACKAGE_NAME


WORKDIR $APP_BASE_PATH

COPY orders/ ./$APP_PACKAGE_NAME
COPY oas.yaml ./
COPY public_key ./

COPY --from=builder $APP_BASE_PATH/.venv/ ./.venv

ENV PATH=$APP_BASE_PATH/.venv/bin:$PATH
ENV DB_URL=sqlite:///orders.db

EXPOSE 8080

ENV PY_APP_PACK_NAME=$APP_PACKAGE_NAME

CMD exec uvicorn ${PY_APP_PACK_NAME}.web.app:app --host 0.0.0.0 --port 8080
```

The relevant parts are:

a couple of build arguments are defined:
  + `APP_BASE_PATH` &mdash; path to where the application will be installed in the container's file system. The default value is set to `/home/pyuser/app`.
  + `APP_PACKAGE_NAME` &mdash; the name of the app package (i.e., `orders` for this microservice). The default value is set to `web_svc`.

In the first stage of the build, we just install Poetry and the dev dependencies.

In the second stage, we prepare the runtime by copying only the virtual environment and the sources needed.

Because we want to make the `Dockerfile` generic, we want to use a variable in the command. This requires a special approach. First of all, build arguments cannot be used in `CMD` (`CMD` is a runtime thing, while build arg applies only to build time). This can be worked around using environment variables.

The default way of encoding a command is through a JSON array as in:

```dockerfile
CMD ["command", "param1", "param2"]
```

However, when doing so, you cannot use environment variables.

You can use instead something like:

```dockerfile
CMD "command $var param2"
```

but this results in the command being passed to the shell, so the process will show:

```bash
/bin/sh -c uvicorn orders.web.app:app --host 0.0.0.0 --port 8080
```

This might have unintended consequences when trapping signals. In order to solve it, you need to use:

```dockerfile
CMD exec uvicorn ${PY_APP_PACK_NAME}.web.app:app --host 0.0.0.0 --port 8080
```

When using `exec` you end up running the app directly, and not passed through the shell:

```dockerfile
/home/pyuser/app/.venv/bin/python /home/pyuser/app/.venv/bin/uvicorn orders.web.app:app
```

| NOTE: |
| :---- |
| If you find that `ps` is not available in your Docker image you can install it using `apt update && apt install procps`. |

## Securing the container with a non-root user

In the final installment of our container, we introduce a few changes leading to a container that is not running as user named `monty` instead of root.

```dockerfile
# Global build args
ARG APP_BASE_PATH=/home/monty/app

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Stage 1: Install dependencies on a virtual env managed by Poetry
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FROM python:3.10-slim as builder

# Reference global build arg so that it can be used in this stage
ARG APP_BASE_PATH

# Set working directory for subsequent COPY and RUN operations
WORKDIR $APP_BASE_PATH

# Copy pyproject.toml and lockfile to the app's base directory
COPY pyproject.toml poetry.lock ./

# Install Poetry in a separate virtual environment (as recommended)
ENV POETRY_HOME=/opt/poetry
RUN python -m venv ${POETRY_HOME}
RUN ${POETRY_HOME}/bin/pip install poetry

# Install project's runtime dependencies in app's base directory
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
RUN ${POETRY_HOME}/bin/poetry install --no-root --no-directory --without dev

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Stage 2: Prepare runtime
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FROM python:3.10-slim as runtime

# Reference global build arg so that it can be used in this stage
ARG APP_BASE_PATH

# Define app's package name as a build-arg
ARG APP_PACKAGE_NAME=web_svc

# Create user `monty` and switch to it
ARG GID=1000
ARG UID=1000
RUN groupadd -g "${GID}" monty
RUN useradd --create-home --no-log-init -u "${UID}" -g "${GID}" monty
USER monty

# Set working directory for COPY and CMD operations
WORKDIR $APP_BASE_PATH

# Copy application resources to the corresponding directories
COPY --chown=monty:monty orders/ ./$APP_PACKAGE_NAME
COPY --chown=monty:monty oas.yaml ./
COPY --chown=monty:monty public_key ./

# Copy the virtualenv from previous stage
COPY --chown=monty:monty --from=builder $APP_BASE_PATH/.venv/ ./.venv

# Make virtual env binaries available in the $PATH
ENV PATH=$APP_BASE_PATH/.venv/bin:$PATH

# Set the default DB_URL to point to a file `orders.db` in the current dir
ENV DB_URL=sqlite:///orders.db

# Inform Docker that the container will listen in 8080 at runtime
EXPOSE 8080

# Map a build arg into an env var so that CMD is configurable and start server
ENV PY_APP_PACK_NAME=$APP_PACKAGE_NAME
CMD exec uvicorn ${PY_APP_PACK_NAME}.web.app:app --host 0.0.0.0 --port 8080
```

The first stage contains only minor changes to align poetry recommendations. Note that in this first stage, we use the root user for the installation and configuration as that simplifies things with pip and poetry. We also install poetry in its own virtualenv, so that it doesn't get mixed with the rest of the dependencies in the container or the project.

In the second stage is where we introduced the non-root user `monty`. As the Python user does not come with a non-root user, we define it, and assign to it the ID=100 and GID=1000, as some documentation suggests that not doing so can lead to problems in the management of volumes.

Immediately after having created the user we switch to it, making the rest of operations under that user permissions, which limits the surface attack of the container (e.g., that user cannot run `apt install`).

Then we copy only the relevant artifacts from the `builder` stage with the approrpiate permissions, and make the virtual environment that we've copied available in the PATH for the user.

Finally, we execute `uvicorn` to start the server.

## Running containers with Docker Compose

Now that we have a solid approach for running the FastAPI microservice running in a Docker container we can try and switch the database to PostgreSQL.

A common strategy to connect our web server and the Database server is using Docker compose, which allows you to run multiple containers within a shared network so that they can talk to each other.

To install/update Docker Compose you just need to type:

```bash
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

Then you can confirm the successful installation/upgrade:

```bash
$ docker compose version
Docker Compose version v2.24.5
```

Next you can proceed to write your Docker Compose file within the root directory of your application in a file named `docker-compose.yaml`. This file declares all the resources needed to run your application:

```yaml
version: "3.9"

services:
  database:
    image: postgres:14.2
    ports:
      - 5432:5432
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=postgres
    volumes:
      - database-data:/var/lib/postgresql/data

  api:
    build:
      context: .
      args:
        - APP_PACKAGE_NAME=orders
    ports:
      - 8080:8080
    depends_on:
      - database
    environment:
      - DB_URL=postgresql://postgres:postgres@database:5432/postgres

volumes:
  database-data:

```

With the file in place you can run:

```bash
# Rebuild the images if needed
docker compose up --build
```

After running that command, both the database server and API should be up. However, because we haven't run the migrations yet, the database will be completely empty:

![Empty Postgres](pics/postgres-empty.png)

Alembic is available in our local virtual env, which makes it easy to run the migration from the working directory by just pointing the `DB_URL` to our Postgres db server running in the container:

```bash
$ DB_URL=postgresql://postgres:postgres@localhost:5432/postgres poetry \
  run alembic upgrade heads
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 0e8aed7229af, Fix incorrect order_id type
```

| NOTE: |
| :---- |
| Alembic was declared as a `dev` dependency in your `pyproject.toml` and therefore, it is not available in the runtime image. |

Once the migration is successful, you can browse the tables:

![Postgres populated](pics/postgres-populated.png)

Now you can start running tests and validating it works as expected:

```bash
$ poetry run http localhost:8080/orders order[0][prod
uct]=capuccino order[0][size]=small order[0][quantity]:=1 -v
POST /orders HTTP/1.1
Accept: application/json, */*;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 69
Content-Type: application/json
Host: localhost:8080
User-Agent: HTTPie/3.2.2

{
    "order": [
        {
            "product": "capuccino",
            "quantity": 1,
            "size": "small"
        }
    ]
}


HTTP/1.1 201 Created
content-length: 165
content-type: application/json
date: Thu, 01 Feb 2024 07:17:43 GMT
server: uvicorn

{
    "created": "2024-02-01T07:13:24.098979",
    "id": "d47320ae-3c9b-4a56-91c2-7da109a7c907",
    "order": [
        {
            "product": "capuccino",
            "quantity": 1,
            "size": "small"
        }
    ],
    "status": "created"
}

```

With the application validated, you just need to run:

```bash
$ docker compose down
$ docker compose down
[+] Running 3/3
 ✔ Container 03_fastapi-orders-svc-docker-compose-api-1       Removed                                         0.7s
 ✔ Container 03_fastapi-orders-svc-docker-compose-database-1  Removed                                         0.4s
 ✔ Network 03_fastapi-orders-svc-docker-compose_default       Removed                                         0.2s
```

If you run `docker compose up` again after bringing the system down, the data from the previous execution will still be there. In this case, the volume mapping is happening outside your working directory, as you can see using the `docker inspect` command:

```bash
$ docker inspect -f "{{ .Mounts }}" 800c8fb289f8
[{volume 03_fastapi-orders-svc-docker-compose_database-data /var/lib/docker/volumes/03_fastapi-orders-svc-docker-compose_database-data/_data /var/lib/postgresql/data local z true }]

$ ls -la /var/lib/docker/volumes/03_fastapi-orders-svc-docker-compose_database-data/_data
total 136
drwx------ 19 lxd  docker  4096 Feb  1 08:21 .
drwx-----x  3 root root    4096 Feb  1 07:49 ..
-rw-------  1 lxd  docker     3 Feb  1 07:49 PG_VERSION
drwx------  5 lxd  docker  4096 Feb  1 07:49 base
drwx------  2 lxd  docker  4096 Feb  1 08:21 global
drwx------  2 lxd  docker  4096 Feb  1 07:49 pg_commit_ts
drwx------  2 lxd  docker  4096 Feb  1 07:49 pg_dynshmem
-rw-------  1 lxd  docker  4821 Feb  1 07:49 pg_hba.conf
-rw-------  1 lxd  docker  1636 Feb  1 07:49 pg_ident.conf
drwx------  4 lxd  docker  4096 Feb  1 08:26 pg_logical
drwx------  4 lxd  docker  4096 Feb  1 07:49 pg_multixact
drwx------  2 lxd  docker  4096 Feb  1 07:49 pg_notify
drwx------  2 lxd  docker  4096 Feb  1 07:49 pg_replslot
drwx------  2 lxd  docker  4096 Feb  1 07:49 pg_serial
drwx------  2 lxd  docker  4096 Feb  1 07:49 pg_snapshots
drwx------  2 lxd  docker  4096 Feb  1 08:21 pg_stat
drwx------  2 lxd  docker  4096 Feb  1 08:27 pg_stat_tmp
drwx------  2 lxd  docker  4096 Feb  1 07:49 pg_subtrans
drwx------  2 lxd  docker  4096 Feb  1 07:49 pg_tblspc
drwx------  2 lxd  docker  4096 Feb  1 07:49 pg_twophase
drwx------  3 lxd  docker  4096 Feb  1 07:49 pg_wal
drwx------  2 lxd  docker  4096 Feb  1 07:49 pg_xact
-rw-------  1 lxd  docker    88 Feb  1 07:49 postgresql.auto.conf
-rw-------  1 lxd  docker 28835 Feb  1 07:49 postgresql.conf
-rw-------  1 lxd  docker    36 Feb  1 08:21 postmaster.opts
-rw-------  1 lxd  docker    94 Feb  1 08:21 postmaster.pid
```

## Publishing Docker images to a private container registry

This section illustrates how to publish the recently created container to both AWS ECR and Azure ACR.

### Publishing to AWS Elastic Container Registry (ECR)

In ECR, you first need to create the repository. That can be done manually from the ECR section of the console:

![AWS ECR](pics/aws-ecr.png)

| NOTE: |
| :---- |
| The commands assume the acocunt id `123456789012` and an AWS profile named `awsia`. |

Alternatively, you can use the AWS CLI:

```bash
aws ecr create-repository --repository-name coffeemesh/orders_svc --profile awsia
```

Then you just need to tag the image as instructed by the AWS console documentation:

```bash
# login to ECR using docker
$ aws ecr get-login-password --region us-east-1 --profile awsia | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# tag the image (first locally)
$ docker tag sergiofgonzalez/orders_svc:0.1.0 sergiofgonzalez/orders_svc:latest

# tag the image for ECR
$ docker tag sergiofgonzalez/orders_svc:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/coffeemesh/orders_svc:latest

$ docker tag 123456789012.dkr.ecr.us-east-1.amazonaws.com/coffeemesh/orders_svc:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/coffeemesh/orders_svc:0.1.0

# Push 0.1.0 and latest to ECR
docker push \
    123456789012.dkr.ecr.us-east-1.amazonaws.com/coffeemesh/orders_svc:0.1.0
docker push \
    123456789012.dkr.ecr.us-east-1.amazonaws.com/coffeemesh/orders_svc:latest
```

Now, we can confirm that we can spin up our application using the ECR image (we don't need the local version):

```yaml
version: "3.9"

services:
  database:
    image: postgres:14.2
    ports:
      - 5432:5432
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=postgres
    volumes:
      - database-data:/var/lib/postgresql/data

  api:
    image: 123456789012.dkr.ecr.us-east-1.amazonaws.com/coffeemesh/orders_svc
    ports:
      - 8080:8080
    depends_on:
      - database
    environment:
      - DB_URL=postgresql://postgres:postgres@database:5432/postgres

volumes:
  database-data:
```

See how now the image for the `api` service references the image in ECR.

### Publishing to Azure Container Registry (ACR)

Publishing to ACR is similar. You first need to access the corresponding `Username` and `password` from the "Access keys" blade in the Azure Portal.

Then, you need to:

```bash
docker login <registry-name>.azurecr.io
Username: <Username-from-portal>
Password: <pass-from-portal>
WARNING! Your password will be stored unencrypted in /home/ubuntu/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credentials-store

Login Succeeded
```


Then you can proceed to tag the local image to be able to be able to push it to ACR:

```bash
$ docker tag sergiofgonzalez/orders:0.1.0 <registry-name>.azurecr.io/coffeemesh/orders:0.1.0

$ docker tag sergiofgonzalez/orders:0.1.0 <registry-name>.azurecr.io/coffeemesh/orders:latest

$ docker push <registry-name>.azurecr.io/coffeemesh/orders
Using default tag: latest
The push refers to repository [<registry-name>.azurecr.io/coffeemesh/orders]
bf95b2689bc8: Pushed
902f0baf670c: Pushed
6b0d9bf9e9f9: Pushed
a093acba4d8f: Pushed
5dbe8ac71761: Pushed
1ed833ad545f: Pushed
3c1abd3602db: Pushed
d3a090682432: Pushed
c6d948842d1e: Pushed
760fe20c9771: Pushed
da5d55102092: Pushed
fb1bd2fc5282: Pushed
latest: digest: sha256:f545dd299b4409ef6338bb694c648f99e1e1de691d7f29cceabe99f6839e968e size: 2830
```

Once push you can use your image locally and it will be pulled

