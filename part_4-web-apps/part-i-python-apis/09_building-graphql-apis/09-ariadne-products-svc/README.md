# Product Service GraphQL API implementation
> Step 8: Final version of the Products Service implementation

## Description

This project takes the previous project state and implements the remaining queries and mutations so that you end up with a full implementation of the schema.

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

Note that the idea of the project is to have a project illustrating all the concepts of GraphQL in Ariadne framework. There might be specific implementation details that could be improved in the resolvers, such as reusing suppliers when you add new ingredients, etc.

### Queries

The following queries can be tested in the running project:

```graphql
{
  allIngredients {
    name,
    description,
    lastUpdated,
    supplier {
      id,
      name,
      address,
      contactNumber
    },
    products {
      ... on ProductInterface {
        id,
        name
      }
    }
  }
}
```

will successfully return:

```json
{
  "data": {
    "allIngredients": [
      {
        "name": "Milk",
        "description": null,
        "lastUpdated": "2024-01-10T15:38:43.411326",
        "supplier": {
          "id": "b8db009c-09a2-4830-ba29-297cd729f4cf",
          "name": "Milk Supplier",
          "address": "55 Milky way Avenue",
          "contactNumber": "(123)456-7890"
        },
        "products": [
          {
            "id": "910095bf-980b-455e-8d47-48394b6deba0",
            "name": "Walnut Bomb"
          },
          {
            "id": "c8d5c681-6c44-4c9e-bf94-5a238ec93e37",
            "name": "Capuccino Star"
          }
        ]
      }
    ]
  }
}
```

The query:

```graphql
{
  allProducts {
    ... on ProductInterface {
      id,
      name,
      price,
      size,
      ingredients {
        ingredient {
          id,
          name,
          lastUpdated,
          supplier {
            id,
            name,
            address
            contactNumber
          }
        },
        quantity,
        unit
      }
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
        "id": "910095bf-980b-455e-8d47-48394b6deba0",
        "name": "Walnut Bomb",
        "price": 37,
        "size": null,
        "ingredients": [
          {
            "ingredient": {
              "id": "cb0db1b5-e03d-45b5-961c-bfd5a4c7629d",
              "name": "Milk",
              "lastUpdated": "2024-01-10T15:39:10.221226",
              "supplier": {
                "id": "b8db009c-09a2-4830-ba29-297cd729f4cf",
                "name": "Milk Supplier",
                "address": "55 Milky way Avenue",
                "contactNumber": "(123)456-7890"
              }
            },
            "quantity": 100,
            "unit": "LITERS"
          }
        ]
      },
      {
        "id": "c8d5c681-6c44-4c9e-bf94-5a238ec93e37",
        "name": "Capuccino Star",
        "price": 12.5,
        "size": "SMALL",
        "ingredients": [
          {
            "ingredient": {
              "id": "cb0db1b5-e03d-45b5-961c-bfd5a4c7629d",
              "name": "Milk",
              "lastUpdated": "2024-01-10T15:39:10.221226",
              "supplier": {
                "id": "b8db009c-09a2-4830-ba29-297cd729f4cf",
                "name": "Milk Supplier",
                "address": "55 Milky way Avenue",
                "contactNumber": "(123)456-7890"
              }
            },
            "quantity": 75.55,
            "unit": "LITERS"
          }
        ]
      }
    ]
  }
}
```

The query:

```graphql
{
  products(input: {sortBy: price, available: null, sort: ASCENDING}) {
    ... on ProductInterface {
      id
      name
      price
      available
    }
  }
}
```

will return:

```json
{
  "data": {
    "products": [
      {
        "id": "c8d5c681-6c44-4c9e-bf94-5a238ec93e37",
        "name": "Capuccino Star",
        "price": 12.5,
        "available": true
      },
      {
        "id": "910095bf-980b-455e-8d47-48394b6deba0",
        "name": "Walnut Bomb",
        "price": 37,
        "available": false
      }
    ]
  }
}
```

The query:

```graphql
{
  product(id: "c8d5c681-6c44-4c9e-bf94-5a238ec93e37") {
    ... on ProductInterface {
      id
      name
      price
      size
      available
      lastUpdated
      ingredients {
        ingredient {
          id
          name
          lastUpdated
          supplier {
            id
            name
            address
            contactNumber
            email
          }
          stock {
            quantity
            unit
          }
        }
        quantity
        unit
      }
    }
    ... on Beverage {
      hasCreamOnTopOption
      hasServeOnIceOption
    }
		... on Cake {
      hasNutsToppingOption
      hasFilling
    }
  }
}
```

will return:

```json
{
  "data": {
    "product": {
      "id": "c8d5c681-6c44-4c9e-bf94-5a238ec93e37",
      "name": "Capuccino Star",
      "price": 12.5,
      "size": "SMALL",
      "available": true,
      "lastUpdated": "2024-01-10T15:39:10.221230",
      "ingredients": [
        {
          "ingredient": {
            "id": "cb0db1b5-e03d-45b5-961c-bfd5a4c7629d",
            "name": "Milk",
            "lastUpdated": "2024-01-10T15:39:10.221226",
            "supplier": {
              "id": "b8db009c-09a2-4830-ba29-297cd729f4cf",
              "name": "Milk Supplier",
              "address": "55 Milky way Avenue",
              "contactNumber": "(123)456-7890",
              "email": "milk@milksupplier.com"
            },
            "stock": {
              "quantity": 100,
              "unit": "LITERS"
            }
          },
          "quantity": 75.55,
          "unit": "LITERS"
        }
      ],
      "hasCreamOnTopOption": true,
      "hasServeOnIceOption": true
    }
  }
}
```

because it is a Beverage, and the same query for the id `910095bf-980b-455e-8d47-48394b6deba0` will return:

```json
{
  "data": {
    "product": {
      "id": "910095bf-980b-455e-8d47-48394b6deba0",
      "name": "Walnut Bomb",
      "price": 37,
      "size": null,
      "available": false,
      "lastUpdated": "2024-01-10T16:06:42.070074",
      "ingredients": [
        {
          "ingredient": {
            "id": "cb0db1b5-e03d-45b5-961c-bfd5a4c7629d",
            "name": "Milk",
            "lastUpdated": "2024-01-10T16:06:42.070071",
            "supplier": {
              "id": "b8db009c-09a2-4830-ba29-297cd729f4cf",
              "name": "Milk Supplier",
              "address": "55 Milky way Avenue",
              "contactNumber": "(123)456-7890",
              "email": "milk@milksupplier.com"
            },
            "stock": {
              "quantity": 100,
              "unit": "LITERS"
            }
          },
          "quantity": 100,
          "unit": "LITERS"
        }
      ],
      "hasNutsToppingOption": true,
      "hasFilling": false
    }
  }
}
```

The query:

```graphql
{
  ingredient(id: "cb0db1b5-e03d-45b5-961c-bfd5a4c7629d") {
    id
    name
    lastUpdated
    stock {
      quantity
      unit
    }
    products {
      ... on ProductInterface {
        id
        name
        price
        size
      }
    }
  }
}
```

will return:

```json
{
  "data": {
    "ingredient": {
      "id": "cb0db1b5-e03d-45b5-961c-bfd5a4c7629d",
      "name": "Milk",
      "lastUpdated": "2024-01-10T16:13:27.744597",
      "stock": {
        "quantity": 100,
        "unit": "LITERS"
      },
      "products": [
        {
          "id": "910095bf-980b-455e-8d47-48394b6deba0",
          "name": "Walnut Bomb",
          "price": 37,
          "size": null
        },
        {
          "id": "c8d5c681-6c44-4c9e-bf94-5a238ec93e37",
          "name": "Capuccino Star",
          "price": 12.5,
          "size": "SMALL"
        }
      ]
    }
  }
}
```

### Mutations

The following mutation adds a new supplier

```graphql
mutation {
  addSupplier(name: "Chocotainment", input: {address: "Wonka way", contactNumber: "(123)-987-6543", email: "choco@late.com"}) {
    id
    name
    address
    contactNumber
    email
  }
}
```

which will return

```json
{
  "data": {
    "addSupplier": {
      "id": "fc15d9df-d0de-4885-ad6f-25cbea5504b1",
      "name": "Chocotainment",
      "address": "Wonka way",
      "contactNumber": "(123)-987-6543",
      "email": "choco@late.com"
    }
  }
}
```

```graphql
mutation {
  addIngredient(name: "Chocolate", input: { description: "85% pure chocolate", supplier: {address: "Wonka Way", contactNumber: "(123)-987-6543",  email: "choco@late.com"}, stock: { quantity: 10, unit: KILOGRAMS} }) {
    id
    name
  }
}
```

will return:

```json
{
  "data": {
    "addIngredient": {
      "id": "61beaaef-c1af-4e80-a9a7-5352ebbe1e56",
      "name": "Chocolate"
    }
  }
}
```

The query:

```graphql
mutation {
  updateProduct(id: "910095bf-980b-455e-8d47-48394b6deba0", input: {price: 99.99, ingredients: { ingredient: "cb0db1b5-e03d-45b5-961c-bfd5a4c7629d", quantity: 55.12, unit: KILOGRAMS }}) {
    ... on ProductInterface {
      name
      price
    }
  }
}
```

returns:

```json
{
  "data": {
    "updateProduct": {
      "name": "Walnut Bomb",
      "price": 99.99
    }
  }
}
```

The query:

```graphql
mutation {
  deleteProduct(id: "910095bf-980b-455e-8d47-48394b6deba0")
}
```

returns:

```json
{
  "data": {
    "deleteProduct": true
  }
}
```

and if you run the same query again, you get:

```graphql
{
  "data": null,
  "errors": [
    {
      "message": "Cannot delete Product with ID 910095bf-980b-455e-8d47-48394b6deba0: not found",
      "locations": [
        {
          "line": 2,
          "column": 3
        }
      ],
      "path": [
        "deleteProduct"
      ],
      "extensions": {
        "exception": {
          "stacktrace": [
            "Traceback (most recent call last):",
            "  File \"/home/ubuntu/Development/git-repos/side_projects/python-workbench/part_4-web-apps/09_building-graphql-apis/09-ariadne-products-svc/.venv/lib/python3.10/site-packages/graphql/execution/execute.py\", line 521, in execute_field",
            "    result = resolve_fn(source, info, **args)",
            "  File \"/home/ubuntu/Development/git-repos/side_projects/python-workbench/part_4-web-apps/09_building-graphql-apis/09-ariadne-products-svc/web/mutations.py\", line 74, in resolve_delete_product",
            "    raise ItemNotFoundError(f\"Cannot delete Product with ID {id}: not found\")",
            "exceptions.ItemNotFoundError: Cannot delete Product with ID 910095bf-980b-455e-8d47-48394b6deba0: not found"
          ],
          "context": {
            "id": "'910095bf-980...-48394b6deba0'",
            "_": "(None, GraphQLResolv...7fbbbc2723b0>))",
            "index": "0",
            "product": "{'available': True, 'hasCreamOnTopOption': True, 'hasServeOnIceOption': True, 'id': 'c8d5c681-6c4...-5a238ec93e37', ...}"
          }
        }
      }
    }
  ]
}
```

