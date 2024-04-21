# FastAPI: Production grade Orders Service
> Applying a few best practices on the web layer

## Description

In this version I just make sure that recommended FastAPI best practices are applied to the project's source code.


Note that:
+ We prefer using response_model because each layer handles their own representation of data. For a small project this might be a bit of an overkill, but will work well in large projects as there's no dependency between layers. Also, the mapping and validation are handled very seamlessly by FastAPI, and you can bank on the service objects to filter out what you don't need.

+ Exceptions are raised from the business layer. I think it'll be better to raise them from the data layer. Otherwise, when you find an Integrity error you will be forcing the service layer to deal with those lower level errors. Instead, you could just raise a DuplicateError from the data layer and let the service layer bubble it up.

+ The service layer defines the `Order` and `OrderItem` objects. These are returned by the data layer, so there's a bit of coupling. We could say the that the repository layer handles the data access using their own internal SQLAlchemy models and is also responsible for mapping those to domain objects.

        There are some things that could be used: Define a `model` folder so that the domain objects do not belong to the service layer, and define them as Pydantic models instead of regular Python classes.

        None of these things seems a good idea, because by defining them as classes we can provide them with complex behavior (e.g., `order.cancel()` handles cancelling the order on a separate microservice), and because they have such behaviors that are invoked from the service layer, it seems a good idea to keep them there.


- [X] Check the empty path: get /orders and get /orders work

- [x] Correct error messages for 404.

## Setting up shop

The project uses Poetry. To start the server do:

```bash
$ poetry install

# In case db is empty (otherwise ignore)
$ DB_URL="sqlite:///orders.db" alembic upgrade heads

# Run the web server (dev mode)
DB_URL="sqlite:///orders.db" python orders/main.py

# Run the web server (through uvicorn)
$ DB_URL="sqlite:///orders.db" poetry run uvicorn orders.main:app --port 8080 --reload
```

## Testing the application

At this stage there is no unit, integration or end-to-end tests, but you can test the application with HTTPie or your browser using Swagger.

### Shakedown using HTTPie

```bash
$ http localhost:8080/orders order[0][product]=capuccino order[0][size]=small order[0][quantity]:=1 -v
```

```bash
$ http localhost:8080/orders
```

```bash
# Replace existing record
$ http PUT localhost:8080/orders/6173b4bf-6448-428d-8cca-8ce8ebcf3d9b order[0][product]="cortadito" order[0][size]=medium order[0][quantity]:=3
```


```bash
# Delete existing record
$ http DELETE localhost:8080/orders/2b9d5007-075c-4a3f-9df6-a2b8020ac4b7
```