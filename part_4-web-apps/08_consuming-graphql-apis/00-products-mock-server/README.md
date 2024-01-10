# SDL specs for the Products service

## Running the mock server using Docker

At the time of writing, npm install freezes, so you cannot use `npm install`. Luckily, GraphQL-Faker supports starting up the server with Docker.

In order to use it, you need to do:

```bash
docker run -p 9002:9002 -v ${PWD}:/workdir apisguru/graphql-faker ./schema.graphql
```