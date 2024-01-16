# Product Service GraphQL API implementation
> Step 2: implementation of complex resolvers

## Description

This project takes the previous project state and implements a more complex resolver that includes a type resolver.

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

The following query will work:

```graphql
allProducts {
  ... on ProductInterface {
    name
  }
}
```

which will return:

```json
{
  "data": {
    "allProducts": [
      {
        "name": "Walnut Bomb"
      },
      {
        "name": "Capuccino Star"
      }
    ]
  }
}
```