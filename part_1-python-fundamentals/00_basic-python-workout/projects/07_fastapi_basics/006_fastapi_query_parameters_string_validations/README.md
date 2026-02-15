# 006: String validations on query parameters
> Illustrates how to apply string validations to query parameters

## Project description

This project illustrates how to do string validations on query parameters. Similar capabilities are available for other types (e.g., numeric) and other concepts (path parameters, headers, request bodies, cookies, ...).

### Using `Annotated` and `Query`

The necessary additional information required to configured a query parameter with additional validations is done through the standard `Annotated` concept from `typing` and FastAPI's `Query` class.

Define a coroutine for the path operation `GET /items/` which includes an optional query parameter `q` whose length cannot exceded 50 chars.

In the implementation, return the following JSON:

```json
{"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
```

including a `q` field if it was sent in the response.

What is the error you get if you send a `q` string longer than 50 chars?

SOLUTION: you get an HTTP 422 response code telling you that the query parameter should have at most have 50 chars.

### Additional string validations

Create a `/v2/items/` path operation that allows for a query parameter `q` that:
+ has a minimum length of 3
+ has a maximum length of 50
+ must comply with the regular expression `^\d+$` (only numerical digits allowed)

In the implementation, return the following JSON:

```json
{"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
```

including a `q` field if it was sent in the response.

What is the error you get if you send a `q` string that breaks any of the validations? What is the error you get if you break 2 or more validation rules?

SOLUTION: you get a 422 error. If you break multiple rules, only one is returned.

### Default values

Create a `/v3/items/` path operation that allows for a query parameter `q` that:
+ has a minimum length of 3
+ must comply with the regular expression `^\d+$` (only numerical digits allowed)
+ has the default value "012345"

In the implementation, return the following JSON:

```json
{"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
```

including a `q` field if it was sent in the response.

Check that if you don't supply q in the request, `q` features the default value.

### Required query parameter

Create a `/v4/items/` path operation that allows for a query parameter `q` that:
+ has a minimum length of 3
+ the query parameter is required, and it can't be None.

In the implementation, return the following JSON:

```json
{"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
```

including a `q` field if it was sent in the response.

Check that if you don't supply q in the request, `q` features the default value.

### Query parameter of type list (multiple values)

Create a `/v5/items/` path operation that allows for a query parameter `q` that is of type `list[str]`.

In the implementation, return the following JSON:

```json
{"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
```

including a `q` field if it was sent in the response.

Confirm that you can provide q value as a list (by providing the `q` query parameter multiple times). What happens if you don't provide a default value for the query parameter in the path operation?

Then, create a `/v6/items/` path operation that allows for a query parameter `q` that is of type `list[str]` that has a default value other than `None` and a `/v7/items/` that has a default value of `None`.

In the implementation, return the following JSON:

```json
{"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
```

including a `q` field if it was sent in the response.

Confirm that `q` receives the default value, and that when that value is not `None` there are no problems when invoking the path operation multiple times.

SOLUTION:

```bash
$ http get localhost:5000/v5/items/ q==1 q==2 q==3
```

I confirmed that there are no problems when assigning a value other than `None`.

### Declaring additional metadata

Create a `/v7/items/` path operation that allows for a query parameter `q` that:
+ has a min_length = 3
+ has a max_length = 10
+ features a title "Query string"
+ features a description "Query string for the items to search in the db"

In the implementation, return the following JSON:

```json
{"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
```

including a `q` field if it was sent in the response.

Confirm that the information is available in the `/docs` endpoint.


### Alias parameters

Alias parameters are useful when the query parameter do not follow Python naming rules.

Create a `/v8/items/` path operation that allows for a query parameter `item-query` and create an alias for it so that it is mapped to `q`.:
+ has a min_length = 3
+ has a max_length = 10

In the implementation, return the following JSON:

```json
{"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
```

including a `q` field if it was sent in the response.

Confirm that the information is available in the `/docs` endpoint.

### Deprecating parameters

Create a `/v9/items/` path operation that allows for a query parameter `q` that is flagged as deprecated.

In the implementation, return the following JSON:

```json
{"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
```

including a `q` field if it was sent in the response.

Confirm that the information is available in the `/docs` endpoint.

### Excluding parameters from the OpenAPI schema

Create a `/v10/items/` path operation that allows for a query parameter `hidden_query` that is hidden from the OpenAPI schema.

In the implementation, if `hidden_query` is used, update the response to include `{"hidden_query": hidden_query}`. Otherwise, return `{"hidden_query": "Not found"}`.

Confirm that the query parameter is not is available in the `/docs` endpoint.

### Custom Validation with `AfterValidator`.

Create a `/v11/items/` that implements a custom validation that ensures that the item's keys begin with either "isbn-" or "imdb-".

For doing so, declare the global variable:

```python
data = {
    "isbn-9781529046137": "The Hitchhiker's Guide to the Galaxy",
    "imdb-tt0371724": "The Hitchhiker's Guide to the Galaxy",
    "isbn-9781439512982": "Isaac Asimov: The Complete Stories, Vol. 2",
}
```

Then define a simple function `check_valid_id` that receives a string (the item's key) and either:
+ raises a `ValueError` if the key doesn't start with "isbn-" or "imdb-".
+ return the `id` if the validation checks out.

Then, in the path operation declare a query parameter configured with `AfterValidator` (note that there's no need to use `Query`). In the implementation, if the validation passes, you should return the id from the data dictionary, or return a random data item if that id is not found.

Create a `/v12/items/` which uses both `AfterValidator` and `Query` to confirm those can be used for different purposes.

### Optional parameter accepting `None`

Create a `/v12/items/` path operation that allows for a query parameter `q` that is required but accepts `None`.

In the implementation, return the following JSON:

```json
{"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
```

including a `q` field if it was sent in the response.

SOLUTION:

You can use the following HTTPie command:

```bash
$ http get localhost:5000/v12/items/ q== --verbose
```

That sends an empty `q` which gets mapped to `None`. If you don't send the `q` you'll get a 422.


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
