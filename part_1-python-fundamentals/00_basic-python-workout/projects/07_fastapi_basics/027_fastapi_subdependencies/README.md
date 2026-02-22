# 027: Hello, FastAPI sub-dependencies
> Illustrates the basics of FastAPI subdependencies

## Project description

FastAPI allows you to have dependencies, which in turn have dependencies.

### Application with subdependencies

Create a FastAPI app that defines a dependency `query_extractor()` that returns the query parameter named `q` it receives.

Then, declare another dependency `query_or_cookie_extractor()` which receives an optional query parameter `q` and a cookie named `last_query`. In the implementation, this dependency should return `q` if given, or the contents of the `last_query` cookie otherwise.

Then, define a path operation for `GET /items/` which declares a dependency with `query_or_cookie` extractor and returns the result of invoking `query_or_cookie` extractor.

Create a simple httpie flow to test the functionality.

SOLUTION:

You can use this flow to test this:

```bash
# Send a query, it should return the value of the query
$ http get :5000/items/ q=="query_1"

# In the second request, we set the value of the cookie but also send the query
$ http get :5000/items/ q=="query_2" Cookie:last_query="query_1"

# In the third request, we update the value of the cookie, but don't send the query
$ http get :5000/items/ Cookie:last_query="query_2"
```



### Disabling caching for sub-dependencies

FastAPI by default caches the invocation of sub-dependencies, so that they're only called once, and the result of calling them is reused by default whenever that dependency is found again for the same request.

That default can be disabled using `use_cache=False` within your `Depends()`.

Create a program that illustrates both the default and non-default behavior by creating a sub-dependency that returns a random number each time it is called. Confirm that when the default behavior is given, the value is always the same, while when using `use_cache=False` is (in general) different.

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
