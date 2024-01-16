# Product Service GraphQL API implementation
> Step 4: Adding pagination

## Description

This project takes the previous project state and implements pagination.

The GraphQL schema is defined in [`web/schema.graphql.py`](./web/schema.py), and the entry point is the [`server.py`](server.py).


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

The following queries can be executed:

```graphql
{
  products(input: {resultsPerPage: 1, page: 1, available: null}) {
    ... on ProductInterface {
      name
    }
  }
}
```

which will return:

```json
{
  "data": {
    "products": [
      {
        "name": "Walnut Bomb"
      }
    ]
  }
}
```

And
```graphql
{
  products(input: {resultsPerPage: 1, page: 2, available: null}) {
    ... on ProductInterface {
      name
    }
  }
}
```

which will return:

```json
{
  "data": {
    "products": [
      {
        "name": "Capuccino Star"
      }
    ]
  }
}
```