# Product Service GraphQL API implementation
> Step 7: Implementing field resolvers

## Description

This project takes the previous project state and implements field resolvers so that we can submit queries for types that map to other types.

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
  allProducts {
    ... on ProductInterface {
      name,
      ingredients {
        quantity,
        unit,
        ingredient {
          name
        }
      }
    }
  }
}
```

will successfully return:

```json
{
  "data": {
    "allProducts": [
      {
        "name": "Walnut Bomb",
        "ingredients": [
          {
            "quantity": 100,
            "unit": "LITERS",
            "ingredient": {
              "name": "Milk"
            }
          }
        ]
      },
      {
        "name": "Capuccino Star",
        "ingredients": [
          {
            "quantity": 75.55,
            "unit": "LITERS",
            "ingredient": {
              "name": "Milk"
            }
          }
        ]
      }
    ]
  }
}
```

This concludes all the concepts needed to finalize the implementation of the remaining queries and mutations, which you will find in 