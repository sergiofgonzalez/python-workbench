# 031: Hello, A basic OAuth2 Password Bearer exam
> A basic OAuth2 Password Bearer example

## Project description

`OAuth2PasswordBearer` is a FastAPI class that lets you configure the OAuth2 password flow in your application.

### Introducing OAuth2PasswordBearer dependency

Start by creating a path operation for `GET /items/`. In the path operation implementation, include a dependency with an instance `OAuth2PasswordBearer`.

Visit /docs to see how the SwaggerUI displays your authenticated endpoint.

Note that you won't be able to authenticate to the endpoint from neither SwaggerUI nor HTTPie.

## Running the program

You can run the application with:

```bash
uv run fastapi dev main.py --port {port}
```

## Project management

This project is managed using `uv`.

FastAPI dependency was added using:

```bash
$ uv add fastapi[standard-no-fastapi-cloud-cli]
```

as I don't intend to use FastAPI cloud at the moment.

The only other dependency was ruff:

```bash
$ uv add ruff --dev
```
