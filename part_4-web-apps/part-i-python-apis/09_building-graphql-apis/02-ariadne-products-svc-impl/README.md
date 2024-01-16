# Product Service GraphQL API implementation
> Step 1: entry-point implementation and simple resolver

## Description

This project takes the previous project state and implements the entry point for the GraphQL server based on the Ariadne framework that implements the Products service API.

The GraphQL schema is defined in [`web/schema.graphql.py`](./web/schema.py), and the entry point is the [`server.py`](server.py).

It also implements a simple resolver for `allIngredients()` query.


### Setting up shop

The project uses venv for virtual environment management and pip for dependency management.

As a result, you just need to:

```bash
$ conda run -n web python -m venv .venv --upgrade-deps
$ source .venv/bin/activate
$ pip install -r requirements.txt
```


To run the project, type:

```bash
$ uvicorn server:server --port 8080 --reload
```

The GraphQL endpoint can be tested from the GraphiQL UI provided by Ariadne in `http://localhost:8080/`, or using curl:

```bash
$ curl --verbose 'http://localhost:8080/' \
  -H 'content-type: application/json'   \
  --data-raw '{"query":"{allIngredients{name}}"}' \
  --compressed | jq
```


The following queries are supported:
```graphql
{
  allIngredients {
    name
  }
}
```

and a more complex one:

```graphql
{
  allIngredients {
    id,
    name,
		products {
      ... on ProductInterface {
        name
      }
    },
    description
  }
}
```

which will return:

```json
{
  "data": {
    "allIngredients": [
      {
        "id": "17fc61c1-7517-4ac9-8c30-d7c7e4c90944",
        "name": "Milk",
        "products": [],
        "description": null
      }
    ]
  }
}
```

Note that `products` return an empty list, because to return products we need a more complicated resolver.