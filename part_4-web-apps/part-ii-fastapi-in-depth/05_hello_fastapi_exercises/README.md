# A few simple FastAPI exercises

This chapter lists a few simple examples to cement basic FastAPI capabilities seen in the previous chapters.

## Exercise

Create a web app that exposes an endpoint `GET /health-check` that returns a JSON object:

```json
{
  "utc_timestamp": <current-timestamp-in-utc>,
  "status": "OK"
}
```

## Exercise

Create a web app that exposes an endpoint `GET /hi/<who>` and returns a JSON string "Hello? <who>?"

## Exercise

Repeat the previous exercise, but this time the endpoint is `GET /hi` and the name is provided as a query parameter named `who`. That is, the request `GET /hi/who=jason` should return a JSON object "Hello? jason?"

## Exercise

Repeat the previous exercise, but this time the name is provided in the body of the request. That is, the following JSON object:

```json
{
  "who": "name"
}
```

Is it possible to use a `GET` request?

## Exercise

Repeat the previous exercise, but this time the name is provided in an HTTP header named `who`.

## Exercise

Create a web app with a public and protected endpoint:

+ `GET /public/hi` &mdash; will return a hardcoded "Hello, world!"
+ `GET /protected/hi` &mdash; will return a hardcoded string only when there's present a header `Authorization` with the contents `Bearer ` followed by a string. When not present it should return a 401 Unauthorized.

## Exercise

Create a simple task management web app that lets you create, and get all the tasks which are defined as:

+ title &mdash; string, required
+ description &mdash; string, optional
+ urgency &mdash; integer

When created, a task is given an ID, which is never returned to the user.
