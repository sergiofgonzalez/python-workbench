# 001b: Orders service (with fake in memory db)
> A basic Orders service built from an OpenAPI schema doc

## Project description

This project provides a basic implementation of a basic orders service corresponding to [Lab 1.b](../../../README.md#lab-1b-implement-orders-service-according-to-the-openapi-schema-document).

### Application specs

This service has to be built using [openapi_schema_doc.yaml](./openapi_schema_doc.yaml) as the source of information for implementation details.

Additionally, the following has been considered:

1. When listing orders, you have to return objects with the following shape:

    ```json
    {
      "orders": list_of_orders
    }
    ```

1. You should not allow additional fields in the payloads, or additional query parameters.

1. The `quantity` property is optional, with default value of 1, but if present, it cannot be null/None.

Finally, wire your manually created OpenAPI schema document to your FastAPI program and adjust it as necessary so that it matches the implementation (in terms of behavior, you can leave out the documentation pieces).

Also, at the moment you shouldn't worry about the functional status of the application (e.g., paying for a cancelled order shouldn't be allowed), or returning the orders by created timestamps for proper pagination.

#### Implementation details

The following are a few notes and decisions you should take during the implementation:

+ For the path operations that require an `order_id`, you should define it as UUID, and not as string. FastAPI will take care of transforming the strings representing uuids in your request into the corresponding UUID objects.

+ You must decide what you will be storing in the dictionary that will be used as a fake db. It can either be models or dicts. In the example, dicts were used. Therefore, you will find obj.model_dump() being used before storing in the fake db. This allows for rehidrating your different schemas using the `**dict_obj` syntax.


+ Note that functionally, the service is very weak, even in terms of its model definition. For example, in an update operation you cannot update the status of the order, only the products, quantities, and size.

+ The trick to implement "The `quantity` property is optional, with default value of 1, but if present, it cannot be null/None." is to do:

    ```python
    Annotated[int, Field(ge=1)] = 1
    ```

    That way, it won't be allowed to send null. Otherwise, if you use `Annotated[int | None, Field(ge=1)] = 1`, FastAPI will allow you to send `quantity:=null`, as in:

    ```bash
    $ http post :5050/orders/ order[0][product]="ragazzi" order[0][size]="large" order[0][quantity]:=null
    ```

+ Because the lab is about learning how to create and read OpenAPI schema docs, no test has been developed.

## Running the program

You can run the application with:

```bash
uv run fastapi dev main.py --port {port}
```

## Running your tests

You can run the tests from your IDE or from the command line using:

```bash
uv run pytest
```

## Project management

This project is managed using `uv`.

FastAPI dependency was added using:

```bash
$ uv add fastapi[standard-no-fastapi-cloud-cli]
```

as I don't intend to use FastAPI cloud at the moment.

PyYAML dependency was also added to override the OpenAPI schema doc that FastAPI generates by the one manually created:

```bash
$ uv add pyyaml
```


PyTest (+ `pytest-sugar` + `pytest-cov`) and Ruff were also added as dev dependencies:

```bash
$ uv add fastapi[standard-no-fastapi-cloud-cli] --dev
```
