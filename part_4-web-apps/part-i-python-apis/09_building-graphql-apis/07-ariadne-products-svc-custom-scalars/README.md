# Product Service GraphQL API implementation
> Step 6: Implementing support for custom scalar types

## Description

This project takes the previous project state and implements all the necessary support logic (deserialization, serialization, validation) for custom scalar types.

The GraphQL schema is defined in [`web/schema.graphql.py`](./web/schema.py), and the entry point is the [`server.py`](server.py).


### Setting up shop

Execute:

```bash
source ./setup.sh
```

In the script a venv virtual environment is set up from a conda one (to accommodate a particular Python version), then activated, and finally the `requirements.txt` are installed.

As a result, the script is equivalent to:

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
  allProducts{
    ... on ProductInterface {
      name,
      lastUpdated
    }
  }
}
```

will return:

```json
{
  "data": {
    "allProducts": [
      {
        "name": "Walnut Bomb",
        "lastUpdated": "2024-01-10T11:36:08.204046"
      },
      {
        "name": "Capuccino Star",
        "lastUpdated": "2024-01-10T11:36:08.204047"
      }
    ]
  }
}
```

Similarly:

```graphql
{
  allIngredients {
    name,
    lastUpdated
  }
}
```

```json
{
  "data": {
    "allIngredients": [
      {
        "name": "Milk",
        "lastUpdated": "2024-01-10T11:36:08.204044"
      }
    ]
  }
}
```
