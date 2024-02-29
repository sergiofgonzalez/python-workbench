# FastAPI in depth: Authentication and Authorization

In this chapter we will deal with:
+ Authentication &mdash; who are you?
+ Authorization &mdash; What do you want?

We will see different techniques that we can use to place the authentication and authorization code.

| NOTE: |
| :---- |
| Additional information on this area can be found in https://fastapi.tiangolo.com/tutorial/security/. |


## Authentication Methods

+ Username and password &mdash; using classic HTTP Basic Authentication and Digest Authentication.

+ API key &mdash; using an opaque long string with an accompanying secret.

+ OAuth2 &mdash; a set of standards for authentication and authorization.

+ Json Web Tokens (JWT) &mdash; an encoding format containing cryptographically signed user information.

## Global Authentication: Shared Secret

The simplest authentication method is to pass a secret that's normally known only by the web server. If it matches, authentication succeeds and you're in.

Obviously, this method is not safe if your API is exposed to the public using HTTP instead of HTTPS, or if your client is a frontend that is open.

The following snippet illustrates how you can add a Basic Auth layer to a FastAPI web app. In the example, an endpoint `GET /who` is defined to return the credentials sent by the user, as an illustration of how you can access the credentials in the request.

It also illustrates how you can leverage the dependency to customize the behavior.

```python
from datetime import datetime
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

basic = HTTPBasic()


@app.get("/who")
def get_user_credentials(creds: HTTPBasicCredentials = Depends(basic)):
    return {"username": creds.username, "password": creds.password}


@app.get("/health-check", dependencies=[Depends(basic)])
def health_check():
    return {"now": datetime.utcnow(), "status": "OK"}


@app.get("/")
def top_public():
    return {"endpoints": ["/", "/who", "/health-check"]}
```

+ `GET /` &mdash; public endpoint with no authentication required.
+ `GET /health-check` &mdash; protected endpoint which doesn't use the authentication details: it just requires authentication information to be present in the request.
+ `GET /who` &mdash; protected endpoint that uses the authentication information present in the request.

The previous example can be enhanced to make the basic auth information present in the request match some secret information only known to the server.

```python
secret_user: str = "bill.harford"
secret_pass: str = "fidelio"


@app.get("/who")
def get_user_credentials(creds: HTTPBasicCredentials = Depends(basic)) -> dict:
    if creds.username == secret_user and creds.password == secret_pass:
        return {"username": creds.username, "password": creds.password}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrent user or password",
    )
```

## Simple Individual Authentication

The previous approach lay out the basis for the identification of individual users.

To authenticate real individual users you'll need to:

+ Pass the user credentials in the `Authorization` HTTP header. When using the basic authorization scheme, it will look like `Authorization: Basic user:pass`, with the `user:pass` section encoded in Base64.

+ Use HTTPS instead of HTTP to prevent MITM attacks.

+ Store the credentials in a database table containing the usernames and the hashed password (never the plain-text password!). The password should be hashed to a different string in a way that the result is not *de-hashable*.

+ When receiving a request with authentication information, hash the password and compare it with the information of the database table. If it matches, pass the matching user object up the stack. If it doesn't, return `None` or raise an exception.

+ In the service layer, do all the required per-user metrics/logging/telemetry.

+ In the web layer, send the authenticated user information to any functions that require it.

## OAuth2

OAuth 2.0, which stands for "Open Authorization", is a standard designed to allow a website or application to access resources hosted by other web apps on behalf of a user.

OAuth offers various flows for different circumstances.

This works as follows:

+ An endpoint `POST /user/token` is defined with the following signature:

        ```python
        ...
        oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")

        def unauthenticated():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrent username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        @router.post("/token")
        async def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
        ```

        This endpoint accepts a form with the fields `username` and `password`. Upon receiving this information, the application must check that the user is defined and whether the password that has been sent (after being hashed), matches the hash stored in the database. If that is the case, an access token (JWT) will be generated, otherwise a 401 status code is returned.

+ If an endpoint has the dependency `oauth2_dep`, it requires an access token to proceed to the endpoint implementation.

## OpenID Connect (OIDC) Authentication

OpenID Connect (OIDC) is an authentication mechanism built on top of OAuth2. When you connect to an external OIDC-enabled identity provider you'll typically get back an OAuth2 access token and an ID token identifying the user.

There's a great discussion on FastAPI website (https://github.com/tiangolo/fastapi/discussions/7888). There are also specific packages that help with that type of authentication such as [fastapi-third-party-auth](https://fastapi-third-party-auth.readthedocs.io/en/latest/).

## Authorization

Authentication handles the *who* (identity) and authorization is in charge the *what* (permissions).

If the endpoints are open (as has been the case until now), you don't need to think about authorization. With authentication in place, you need to start thinking *who* can do *what*.

You can start simple and tag each user with a boolean flag that identifies the user as an admin and enable admin users with full CRUD capabilities, and regular users with simple R permissions.

As you evolve your application, you can make your permissions more fine-grained.

## Middleware

Because FastAPI is built atop Starlette, and Starlette supports middleware, you can use middleware in FastAPI too.

The middleware will typically:
+ Intercept the request
+ Do something with the request
+ Pass the request to a path function
+ Intercept the response returned by the path function
+ Do something with the response
+ Return the response to the caller

So, in concept, it is very similar to a Python decorator, in the sense that it wraps some existing logic with additional functionality that can be executed before and after that existing logic.

In FastAPI, you could either use middleware or dependency injection via `Depends()`. Middleware is typically more appropriate for global behavior (like CORS), but it lacks proper integration with FastAPI in terms of types, automatic documentation, OpenAPI integration, etc.

The recommended way to support CORS in your FastAPI application is with the `CORSMiddleware` (see https://fastapi.tiangolo.com/tutorial/cors/).

## CORS

CORS is a security mechanism that must be implemented in web servers that let the browser know what clients the backend trusts.

When using CORS you configure the following:
+ Trusted Origins
+ Allowed HTTP methods
+ Allowed HTTP headers
+ CORS cache timeout

For example, following code enables CORS for the domain `ui.cryptids.com` and `http://localhost:8080`:

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ui.cryptids.com", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
```

That will allow those origins, and not other, to interact with our backend APIs.

