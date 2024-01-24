# API Authentication and Authorization

+ Using Open Authorization (OAuth2) to allow access to your APIs
+ Using OpenID connect (OIDC) to verify the identity of your API users
+ Authorization flows and suitability depending on the scenario
+ Understanding JSON Web Tokens (JWT) and using PyJWT
+ Adding authentication adn authorization middleware to your APIs

## Intro

Authentication is the process of verifying the identity of a user, while authorization is the process of determining whether a user has access to certain resources or operations.

In order to add authentication and authorization to our services, we will need to add a couple of libraries:
+ [PyJWT](https://github.com/jpadilla/pyjwt) &mdash; to work with JSON Web Tokens (JWTs).
+ [cryptography](https://github.com/pyca/cryptography/) &mdash; to verify tokens' signatures.

## Understanding authentication and authorization protocols

The two most important protocols you need to know are:
+ OpenID Connect (OIDC)
+ Open Authorization v2 (OAuth2)

### Understanding OAuth2

OAuth2 is a standard protocol for access delegation. OAuth2 allows a user to grant third-party application access to protected resources they own in another website without having to share their credentials. Typically, access is granted by issuing a token, which the third-party app uses to access the user's information.

Consider the following scenario in which Susan, both a user of Facebook and LinkedIn, wants to import her list of Facebook contacts into LinkedIn.

To allow LinkedIn to import her Facebook contacts, Susan has to grant LinkedIn access to her protected resource in Facebook.

One option would be to give LinkedIn her Facebook credentials to access her account. While technical viable, that would pose a security risk.

Instead, OAuth2 defines a protocol that allows Susan to tell Facebook that LinkedIn can access her list of contacts. Technically, Facebook will issue a temporary token that LinkedIn can use to import Susan's contacts.

The following diagram illustrates the flow by which Susan can grant a 3rd party application (LinkedIn) access to their information on another server (Facebook).

![OAuth2 flow: High-level](pics/oauth2-flow-hl.png)

OAuth2 defines various roles that are involved in this access delegation that ends up granting access to a protected resource (Susan's Facebook contacts):

+ **Resource owner** &mdash; the user who's granting access to the resource (Susan).

+ **Resource server** &mdash; the server hosting the user's protected resources (Facebook).

+ **Client** &mdash; the application or server requesting access to the user's resources (LinkedIn).

+ **Authorization server** &mdash; the server that grants the client access to the resources (Facebook).

| NOTE: |
| :---- |
| In this case, Facebook plays both the role of *resource server* and *authorization server*. While this is common, you will find cases on which the *authorization server* might be completely different from the *resource server* (e.g., using Microsoft Entra or Google authentication as the *authorization server*. |

OAuth2 offers different flows to grant authorization to a user depending on the access conditions:
+ Authorization code flow
+ PKCE flow
+ Client credentials flow
+ Refresh token flow

| NOTE: |
| :---- |
| Best practices in OAuth2 change over time as we learn more about application vulnerabilities.<br>The latest best practices can be found in ["OAuth 2.0 Security Best Current Practice"](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics-20). For example, that document describes two additional flows &mdash; resource owner password flow and implicit flow as deprecated as they expose serious vulnerabilities. |


| NOTE: |
| :---- |
| Another popular flow is the [*device authorization grant*](https://datatracker.ietf.org/doc/html/rfc8628), which allows input-constrained devices such as Smart TVs to obtain tokens. |


The latest version of OAuth is 2.1, which is described [here](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-06)

#### Authorization Code flow

In the authorization code flow, the client server exchanges a secret with the authorization server to produce a signing URL.

After the user signs in using this URL, the client obtains a one-time code it can exchange for an access token.

This flow uses a client secret, and therefore, is only appropriate for applications in which the code is not publicly exposed (i.e., it's not appropriate for single-page UIs).

> OAuth 2.1 recommends using the authorization code flow in combination with PKCE.

The following diagram illustrates the authorization code flow, in which the authorization server produces a signing URL, which they user can utilize to prove their identity and grant access to the 3rd party app:

![Authorization Code flow](pics/oauth2-authorization-code-flow.png)

#### Proof of Key for Code Exchange (PKCE) flow

The Proof of Key for Code Exchange flow (PKCE flow, pronounced "pixie") is an extension of the authorization code flow designed to protect applications whose source code is publicly exposed, such as mobile applications and SPAs.

In those applications, the client cannot use a secret key to obtain the one-time code.

In the PKCE flow, the client generates a secret called the *code verifier*, and it encodes it. The result of encoding it is called the *code challenge*. When sending an authorization request to the server, the client includes both the code verifier and the code challenge in the request.

In return, the server produces an authorization code, which the client can exchange for an access token. To get the access token, the client must send both the authorization code and the code challenge.

Thanks to the code challenge, the PKCE flow also prevents authorization code injection attacks, in which a malicious user intercepts the authorization code and uses it to get hold of an access token.

Because of this, PKCE is now also recommended for old-style UI applications that don't expose the source to the client.

#### Client Credentials flow

The client credentials flow is aimed for server-to-server communication, and as you can see it involves the exchange of a secret to obtain an access token. This flow is suitable for enabling communication between microservices over a secure network.

#### Refresh Token flow

The refresh token flow allows client to exchange a refresh token for a new access token.

For security reasons, access tokens are valid for a limited period of time. However, API clients often need to be able to communicate with the API server after an access token has expired. API clients can use the refresh flow to obtain a new token without involving the interaction of the user.

API clients typically receive both an access token and a refresh token when they successfully gain access to the API. Refresh tokens are usually valid for a limited period of time, and they're valid for a one-time use &mdash; every time you refresh your access token, you'll get a new one.


### Understanding OpenID Connect

OpenID Connect (OIDC) is an open standard for identity verification that's built on top of OAuth.

OIDC allows users to authenticate to a website by using a 3rd party identity provider &mdash; that's what you do when you use your Google account to sign into other websites.

In those cases, Google is the identity provider (IdP).

OIDC is very convenient because it allows users to utilize the same identity across different websites without having to create and manage new usernames and passwords.

With OIDC, a user signs in with an OIDC server. The OIDC server issues an ID token and an access token, which the user can use to access an application.

![OIDC Sign-in flow](pics/oidc-signin-flow.png)

OIDC is typically invoked in OAuth authorization flows.

Both tokens generated by OIDC are JSON Web tokens, but they serve different purposes:
+ ID tokens identify the user, and they tipically contain information such as the user name, email, and personal details.
+ Access tokens don't typically contain claims abouth the access rights a user possess.

> You use ID tokens to verify user identity, never to determine if a user has access to an API. API access is validated with access tokens.<br>As a consequence, the audience for those tokens is different: the ID token audience is the client application making the authentication request, while the audience for the access token is the API server.

IdP's that offer OIDC integration expose a `/.well-known/openid-configuration` endpoint (note the leading '.'), which is also known as the *discovery endpoint*, which tells the API consumer how to authenticte and obtain their access tokens.

For example, the OIDC's well-known endpoint for Google IdP is https://accounts.google.com/.well-known/openid-configuration and it returns:

```bash
$ poetry run http https://accounts.google.com/.well-known/openid-configuration -v
GET /.well-known/openid-configuration HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: accounts.google.com
User-Agent: HTTPie/3.2.2



HTTP/1.1 200 OK
Accept-Ranges: bytes
Access-Control-Allow-Origin: *
Age: 1221
Alt-Svc: h3=":443"; ma=2592000,h3-29=":443"; ma=2592000
Cache-Control: public, max-age=3600
Content-Encoding: gzip
Content-Length: 464
Content-Security-Policy-Report-Only: require-trusted-types-for 'script'; report-uri https://csp.withgoogle.com/csp/federated-signon-mpm-access
Content-Type: application/json
Cross-Origin-Opener-Policy: same-origin; report-to="federated-signon-mpm-access"
Date: Tue, 23 Jan 2024 12:46:58 GMT
Expires: Tue, 23 Jan 2024 13:46:58 GMT
Last-Modified: Thu, 16 Jan 2020 21:53:16 GMT
Report-To: {"group":"federated-signon-mpm-access","max_age":2592000,"endpoints":[{"url":"https://csp.withgoogle.com/csp/report-to/federated-signon-mpm-access"}]}
Server: sffe
Vary: Accept-Encoding
X-Content-Type-Options: nosniff
X-XSS-Protection: 0

{
    "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
    "claims_supported": [
        "aud",
        "email",
        "email_verified",
        "exp",
        "family_name",
        "given_name",
        "iat",
        "iss",
        "locale",
        "name",
        "picture",
        "sub"
    ],
    "code_challenge_methods_supported": [
        "plain",
        "S256"
    ],
    "device_authorization_endpoint": "https://oauth2.googleapis.com/device/code",
    "grant_types_supported": [
        "authorization_code",
        "refresh_token",
        "urn:ietf:params:oauth:grant-type:device_code",
        "urn:ietf:params:oauth:grant-type:jwt-bearer"
    ],
    "id_token_signing_alg_values_supported": [
        "RS256"
    ],
    "issuer": "https://accounts.google.com",
    "jwks_uri": "https://www.googleapis.com/oauth2/v3/certs",
    "response_types_supported": [
        "code",
        "token",
        "id_token",
        "code token",
        "code id_token",
        "token id_token",
        "code token id_token",
        "none"
    ],
    "revocation_endpoint": "https://oauth2.googleapis.com/revoke",
    "scopes_supported": [
        "openid",
        "email",
        "profile"
    ],
    "subject_types_supported": [
        "public"
    ],
    "token_endpoint": "https://oauth2.googleapis.com/token",
    "token_endpoint_auth_methods_supported": [
        "client_secret_post",
        "client_secret_basic"
    ],
    "userinfo_endpoint": "https://openidconnect.googleapis.com/v1/userinfo"
}
```

The well-known endpoint tells us which URL we must use to obtain the authorization access token, which URL returns user information, or which URL to use to revoke an access token.

It also lists the available claims and URI for the JSON Web Keys.

| NOTE: |
| :---- |
| You will typically use a library to handle these endpoints in your behalf. |

## Working with JSON Web Tokens (JWTs)

In OAuth and OIDC, user access is verified by means of a token known as JSON Web Token or JWT.

A JWT is a token that represents a JSON document. The JSON document contains claims, such who issued the token, the audience of the token, or when the token expires.

The token is typically encoded in Base64, and signed with a private secret or a cryptographic key.

A JWT looks like the following:

```
base64url_encoded_HEADER.base64url_encoded_PAYLOAD.base64url_encoded_SIGNATURE
```

### Understanding the JWT header

JWTs contain a header that describe the type of token, as well as the algorithm and the key used to sign the token.

JWTs are commonly signed using either:
+ HS256 &mdash; uses a secret to encrypt the token. It stands for HMAC-SHA256, and it's a form of encryption that uses a key to produce a hash.

+ RS256 &mdash; uses a private/public key pair to sign the token. It stands for RSA-SHA256. It uses a private key to sign the payload, which we can verify using the public key.

Depending of the method used, you will apply the appropriate algorithm to verify the token's signature.

The header might look like the following:

```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "ZweIFRR4l1dJlVPHOoZqf"
}
```

### Understanding JWT claims

The second part of a JWT contains a set of claims in JSON format, as key-value pairs.

There are two types of claims:
+ reserved claims &mdash; the ones defined by the JWT spec.
+ custom claims &mdash; the ones we can add to the payload to enrich the token with additional information.

The JWT spec defines seven reserved claims:

| Claim | Friendly Name | Description |
| :---- | :------------ | :---------- |
| `iss` | Issuer | Identifies the issuer of the JWT. If the issuer is an identity-aaS provider, this claim identifies that service. It is typically an ID or a URL. |
| `sub` | Subject | Identifies the subject of the JWT, that is, the user sending the request to the server. It typically comes in the form of an opaque ID that doesn't disclose the user's personal details. |
| `aud` | Audience | Indicates the intended recipient of the JWT. It typically comes in the form of an ID or URL. It's crucial to check this field to validate that the token is intended for our APIs. If you are validating the request, the audience will identify your API server, and you must disregard the token if you don't recognize the value in the field. |
| `exp` | Expiration Time | A UTC timestamp indicating when the JWT expires, encoded as the number of seconds from 1970-01-01T00:00:00Z UTC ignoring leap seconds. Requests with expired tokens must be rejected. |
| `nbf` | Not Before Time | A UTC timestamp indicating the time before which the JWT must not be accepted, encoded as the number of seconds from 1970-01-01T00:00:00Z UTC ignoring leap seconds. |
| `iat` | Issued at Time | A UTC timestamp that indicates when the JWT was issued, encoded as the number of seconds from 1970-01-01T00:00:00Z UTC ignoring leap seconds. It can be used to determine the age of the JWT. |
| `jti` | JWT ID | A unique identifier for the JWT. |

While the reserved claims are not required in the JWT payload, it's recommended to include them to ensure interoperability.

A typical JWT payload will look like the following:

```json
{
  "iss": "https://auth.coffeemesh.io/",
  "sub": "ec7bbccf-ca89-4af3-82ac-b41e4831a962",
  "aud": "http://127.0.0.1:8080/orders",
  "iat": 1667155816,
  "exp": 1667238616,
  "azp": "7c2773a4-3943-4711-8997-70570d9b099c",
  "scope": "openid"
}
```

+ `iss` &mdash; the token has been generated by coffeemesh.io identity service, which can be found at https://auth.coffeemesh.io/.

+ `sub` &mdash; the user identifier who is backing the request. The receiving API can use this value in the identity service to control access to the resources owned by this user, or to get more info about the user.

+ `aud` &mdash; tells us that the token has been issued to grant access to the Orders service running in http://127.0.0.1:8080/orders. If the Orders service receive a different value here, the service should reject the request.

+ `iat` &mdash; tells us the token was issued at Sun Oct 30 19:50:16 CET 2022 (see note below).

+ `exp` &mdash; tells us the token expired at Mon Oct 31 18:50:16 CET 2022 (see note below).

+ `azp` &mdash; tells us that the token has been requested by an application with identifier `7c2773a4-3943-4711-8997-70570d9b099c`. This claim is common in tokens that have been issued as part of the OIDC protocol.

+ `scope` &mdash; the value `"openid"` tells us that the token was issued using the OIDC protocol.


| NOTE: |
| :---- |
| You can use the `date` command in Linux to get a human-readable datetime from a numeric timestamp `$ date -d @1667155816`. |

### Producing JWTs

To form a JWT, you need to encode the header, the payload, and the signature using base64url encoding.

| NOTE: |
| :---- |
| Base64url encoding is similar to Base64 but it uses non-alphanumeric characters and omits padding. |

Then, the header, payload, and signature are concatenated with periods `.` as separators. Libraries like PyJWT take care of the heavy lifting for producing a JWT.

Let's assume we want to produce a token for the following payload:

```json
{
  "iss": "https://auth.coffeemesh.io/",
  "sub": "ec7bbccf-ca89-4af3-82ac-b41e4831a962",
  "aud": "http://127.0.0.1:8080/orders",
  "iat": 1667155816,
  "exp": 1667238616,
  "azp": "7c2773a4-3943-4711-8997-70570d9b099c",
  "scope": "openid"
}
```

To produce a signed token, we just need to use the `encode()` method of PyJWT library:

```python
>>> import jwt
>>>
>>> payload = {
...   "iss": "https://auth.coffeemesh.io/",
...   "sub": "ec7bbccf-ca89-4af3-82ac-b41e4831a962",
...   "aud": "http://127.0.0.1:8080/orders",
...   "iat": 1667155816,
...   "exp": 1667238616,
...   "azp": "7c2773a4-3943-4711-8997-70570d9b099c",
...   "scope": "openid"
... }
>>> jwt.encode(payload=payload, key="secret", algorithm="HS256")
'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2F1dGguY29mZmVlbWVzaC5pby8iLCJzdWIiOiJlYzdiYmNjZi1jYTg5LTRhZjMtODJhYy1iNDFlNDgzMWE5NjIiLCJhdWQiOiJodHRwOi8vMTI3LjAuMC4xOjgwODAvb3JkZXJzIiwiaWF0IjoxNjY3MTU1ODE2LCJleHAiOjE2NjcyMzg2MTYsImF6cCI6IjdjMjc3M2E0LTM5NDMtNDcxMS04OTk3LTcwNTcwZDliMDk5YyIsInNjb3BlIjoib3BlbmlkIn0.pE4_0oZnVvb2V3dRpKSCVJ1qyzSwxQH81xAFS9uK1qI'
>>>
```

The method above uses the HS256 algorithm to sign the token with the key "secret".

We can use a similar approach to sign the token with the RS256 algorithm.

First, we need to generate a private/public key pair using OpenSSL tooling:

```bash
openssl req -x509 -nodes -newkey rsa:2048 \
  -keyout private_key.pem \
  -out public_key \
  -subj "/CN=coffeemesh"
```

The command will generate two files representing the public and private keys.

With the key in place, you can write a simple program that generates a JWT signed by the private key of the generated key pair.

```python
from datetime import datetime, timedelta
from pathlib import Path
from math import floor

import jwt
from cryptography.hazmat.primitives import serialization


def generate_rsa_signed_jwt():
    now = datetime.utcnow()
    payload = {
        "iss": "https://auth.coffeemesh.io/",
        "sub": "ec7bbccf-ca89-4af3-82ac-b41e4831a962",
        "aud": "http://127.0.0.1:8080/orders",
        "iat": floor(now.timestamp()),
        "exp": floor((now + timedelta(hours=24)).timestamp()),
        "scope": "openid",
    }
    private_key_contents = Path("private_key.pem").read_text(encoding="utf-8")
    private_key = serialization.load_pem_private_key(
        private_key_contents.encode(),
        password=None,
    )
    return jwt.encode(
        payload=payload, key=private_key, algorithm="RS256"  # type: ignore
    )
```

In the function, we create a payload with dynamic values for `iat` and `exp` using the `datetime` module. The token is set to expire in 24 hours from the time the function is invoked.

The private key is passed to `jwt.encode()` after having read the private key as a text file, and then transformed to an special cryptography type using `serialization.load_pem_private_key()`.

This will give us a token that we could inspect at https://jwt.ms to get:

```json
{
  "alg": "RS256",
  "typ": "JWT"
}.{
  "iss": "https://auth.coffeemesh.io/",
  "sub": "ec7bbccf-ca89-4af3-82ac-b41e4831a962",
  "aud": "http://127.0.0.1:8080/orders",
  "iat": 1706024003,
  "exp": 1706110403,
  "scope": "openid"
}.[Signature]
```

In order to validate the signature, you can use the `public_key` file, or use another `openssl` command to generate a more compact public key file from the certificate:

```bash
$ openssl x509 -pubkey -noout < ./03_jwt-generator/public_key > ./03_jwt-generator/public_key.key
```

Then you can visit `https://jwt.io`, where you can also validate the signature:

![Signature verified](pics/signature-verified.png)

Note that you can also inspect the components of the JWT using the `base64` Linux command:

Header:

```bash
$ echo eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9 | base64 --decode | jq
{
  "alg": "RS256",
  "typ": "JWT"
}
```

Payload:

```bash
$ echo eyJpc3MiOiJodHRwczovL2F1dGguY29mZmVlbWVzaC5pby8iLCJzdWIiOiJlYzdiYmNjZi1jYTg5LTRhZjMtODJhYy1iNDFlNDgzMWE5NjIiLCJhdWQiOiJodHRwOi8vMTI3LjAuMC4xOjgwODAvb3JkZXJzIiwiaWF0IjoxNzA2MDI0MDAzLCJleHAiOjE3MDYxMTA0MDMsInNjb3BlIjoib3BlbmlkIn0 | base64 --decode | jq
base64: invalid input
{
  "iss": "https://auth.coffeemesh.io/",
  "sub": "ec7bbccf-ca89-4af3-82ac-b41e4831a962",
  "aud": "http://127.0.0.1:8080/orders",
  "iat": 1706024003,
  "exp": 1706110403,
  "scope": "openid"
}
```

We can do the same using Python:

```python
>>> import base64
>>>
>>> base64.decodebytes("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9".encode())
b'{"alg":"RS256","typ":"JWT"}'
```

Note that you need to invoke `encode()` method on the string to transform it in a sequence of bytes that can be passed to the `decodebytes()` function.

### Validating JWTs

There are two steps to validating a JWT:
1. Validate the token signature
2. Validate that the claims are correct (e.g., token isn't expired and audience is correct).

Both steps of the validation are required, and every user request must carry a token.

The following snippet illustrates how to do the validation:

```python
from pathlib import Path

import jwt
from cryptography.x509 import load_pem_x509_certificate

public_key_cert_contents = Path("public_key").read_text()
public_key = load_pem_x509_certificate(
    public_key_cert_contents.encode("utf-8")
).public_key()

access_token = "<token-here>"  # pylint: disable=C0301:line-too-long

print(jwt.decode(
    access_token,
    key=public_key,  # type: ignore
    algorithms=["RS256"],
    audience=["http://127.0.0.1:8080/orders"],
))
```

If the process goes well (token valid), you'll get something like:

```python
{'iss': 'https://auth.coffeemesh.io/', 'sub': 'ec7bbccf-ca89-4af3-82ac-b41e4831a962', 'aud': 'http://127.0.0.1:8080/orders', 'iat': 1706024003, 'exp': 1706110403, 'scope': 'openid'}
```

Otherwise, you'll get an exception from the `jwt.exceptions` package.

## Adding authorization to the API server

In this section you'll see how to add authorization to the Orders API.

As in most of the web apps there will be some protected endpoints (i.e., will require valid access tokens) while others will be accessible to everyone.

The plan is:
+ `/docs/orders` &mdash; public
+ `/openapi/orders.json` &mdash; public (this endpoint serves our API documentation).
+ rest of the endpoints &mdash; protected

And the behavior to implement in the protected endpoints is:
> if the token is invalid or missing in the request, a 401 (Unauthorized) status code will be returned.

When implementing authorization there are two popular strategies:
+ Handle authorization validation in an API gateway &mdash; an API gateway is a network layer that sits in front of your APIs. In terms of authentication and authorization, its main role is to facilitate service discovery, authorize user access, validate access token, and enrich the request with custom headers that add information about the user. It can be used to accommodate other cross cutting concerns such as payload validation, protection against attacks, logging, etc.
+ Handle authorization within each API &mdash; authorization is performed at the service level. This is typically done when an API gateway doesn't fit in your architecture, or when your API gateway cannot handle authorization.

As in our case, we don't have an API gateway, we'll learn how to handle authorization within our service.

The best place to put our authorization check is in the *middleware* layer, as it needs to happen for all the protected endpoints, and before executing the service logic.

Most web servers have a concept of middleware (or request preprocessor) that we can use for this purpose. Middleware components are usually executed in a sequence, and our authorization check should happen early to prevent additional logic to be executed for unauthorized requests.

The following diagram illustrates this concept:

![Middleware](pics/middleware.png)

### Creating an authorization module

With the approach decided, we're ready to create a module to encapsulate your authorization related code.

The following snippet illustrates the implementation, which uses the pieces of code we used in the previous sections:

```python
from pathlib import Path

import jwt
from cryptography.x509 import load_pem_x509_certificate

public_key_text = (Path(__file__).parent / "../../../public_key").read_text()
public_key = load_pem_x509_certificate(
    public_key_text.encode("utf-8")
).public_key()


def decode_and_validate_token(access_token):
    return jwt.decode(
        access_token,
        key=public_key,  # type: ignore
        algorithms=["RS256"],
        audience=["http://localhost:8080/orders"],
    )
```

Being a part of our API layer, the contents of the snippet before can be accommodated in `orders/web/api/auth.py` file.


### Creating an authorization middleware

The following listing shows how to implement the authorization middleware. We implement it as a simple class called `AuthorizeRequestMiddleware` which inherits from Starlette's `BaseHTTPMiddleware` class. As per specs, the entry point for the middleware must be implemented in a function called `dispatch()`.

| NOTE: |
| :---- |
| Alternatively, we could have used FastAPI dependencies. |


```python
"""FastAPI app entrypoint"""
import os
from pathlib import Path

import yaml
from fastapi import FastAPI
from jwt import (
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAlgorithmError,
    InvalidAudienceError,
    InvalidKeyError,
    InvalidSignatureError,
    InvalidTokenError,
    MissingRequiredClaimError,
)
from starlette import status
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from orders.web.api.auth import decode_and_validate_token

app = FastAPI(
    debug=True, openapi_url="/openapi/orders.json", docs_url="/docs/orders"
)

app.openapi = lambda: oas_doc
oas_doc = yaml.safe_load((Path(__file__).parent / "../../oas.yaml").read_text())


class AuthorizeRequestMiddleware(BaseHTTPMiddleware):
    """Starlette middleware that performs auth check on protected endpoints"""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Check feature flag that disables auth (for testing purposes)
        if os.getenv("AUTH_ON", "False").lower() != "True".lower():
            request.state.user_id = "test"
            return await call_next(request)

        # Check if requesting public endpoint
        if request.url.path in ["/docs/orders", "/openapi/orders.json"]:
            return await call_next(request)

        # Check if OPTIONS
        if request.method == "OPTIONS":
            return await call_next(request)

        # Otherwise: process request
        bearer_token = request.headers.get("Authorization")
        if not bearer_token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Missing access token",
                    "body": "Missing access token",
                },
            )

        if not bearer_token.startswith("Bearer "):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Unexpected authorization format",
                    "body": "Unexpected authorization format",
                },
            )

        try:
            auth_token = bearer_token.split(" ")[1].strip()
            token_payload = decode_and_validate_token(auth_token)
        except (
            ExpiredSignatureError,
            ImmatureSignatureError,
            InvalidAlgorithmError,
            InvalidAudienceError,
            InvalidKeyError,
            InvalidSignatureError,
            InvalidTokenError,
            MissingRequiredClaimError,
        ) as error:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": str(error), "body": str(error)},
            )
        else:
            request.state.user_id = token_payload["sub"]
        return await call_next(request)


app.add_middleware(AuthorizeRequestMiddleware)


from orders.web.api import api
```

In the class implementation we:

1. Check the value of an environment variable called `AUTH_ON` that we set to `"False"` if nout found.

    This flag, when set to `"False"` or not set will allow us to override the authorization mechanism. When disabled, we set the user ID associated to the request to `test` to make it clear it is a test request.

    Finally, as good middleware citizens, we invoke the next middleware in the chain.

2. Check whether the request is for a public endpoint.

    If so, there's nothing to check, so we simply invoke the next middleware in the chain.

3. Check if we're dealing with an `OPTIONS` request.

    If it's an `OPTIONS` request generated by the browser to check origins, methods, and headers accepted by the API server we need to skip the authorization check as mandated by the [W3C standards for CORS request](https://www.w3.org/TR/2020/SPSD-cors-20200602/). Then, if it's a CORS request, we invoke the next middleware in the chain.

    CORS requests, also known as preflight requests, are requests sent by the web browser to understand which methods, origins, and headers are accepted by the API server. If CORS requests are not processed correctly the browser will abort communication with the API and the UI app won't work.

    Most web frameworks contain plug-ins or extensions that help us handle CORS correctly.

4. Perform the authorization check.

    If none of the scenarios above match, we proceed to do the authorization check,

    We start by checking if the `Authorization` HTTP header is present. If not, we return a 401 Unauthorized. We can even skip the processing of further middlewares, as there's no point in doing so if request is not going to proceed.

    If the `Authorization` header is present, we check that we're getting the expected format `"Bearer {access-token}`. If `"Bearer "` is not there, we should also break the chain and return a 401 Unauthorized.

    If the header is present and it starts with `"Bearer"`, we need to extract the token to start validating it. We can do so by splitting the header value around the space.

    Then we use PyJWT to validate the extracted token. If an exception is raised we catch it and return 401, otherwise, we set the `user_id` associated to the request to the value found in the `sub` claim of the token payload.


Note that for the middleware to work, we also need to register it using `app.add_middleware(AuthorizeRequestMiddleware)`.

With all these changes in place, you'll have your API endpoints prepared to handle authentication.

### Adding CORS middleware

Since we're going to allow interactions with a frontend application running on a browser, we also need to enable the CORS middleware.

FastAPI's CORS middleware takes care of populating our responses with the required headers to let the browser pass the requests sent by the JavaScript application running on the browser.

In Starlette's middleware, the components in the middleware chain are executed in reverse order of registration.

As a result, we should register the CORS middleware last, so that it is executed before the authorization middleware.

## Authorizing resource access

With the authentication layer in place, we can now update the code to take the user ID originating the request under consideration when an order is created, or when we return a list of orders.

### Updating the database to link users and orders

Before doing the application changes done, we need to update the database schema and data so that the `orders` table include a `user_id`.

As we don't have any production data in place, we can opt for removing all the existing data in our `orders.db` file.

| NOTE: |
| :---- |
| In a real scenario, we'd need to plan for a migration exercise so that existing data is not lost. In any case, the technique described below can also be followed. |

We can benefit from Python's REPL, and all do the preparation in it:

```python
>>> from orders.repository.orders_repository import OrdersRepository
>>> from orders.repository.unit_of_work import UnitOfWork
>>> with UnitOfWork() as unit_of_work:
...     orders_repository = OrdersRepository(unit_of_work.session)
...     orders = orders_repository.list()
...     for order in orders: order.delete(order.id)
...     unit_of_work.commit()
```




### Updating the OrdersModel

The best way to consider the user in our application is to simply add a `user_id` field in our `OrderModel`, which will end up being reflected as an additional column on the `order` table:

Finally, we add the `user_id` field to our `OrderModel` so that it ends up in our database.

```python
...
class OrderModel(Base):
    __tablename__ = "order"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False)  # Added field
    items = relationship("OrderItemModel", backref="order")
    status = Column(String, nullable=False, default="created")
    created = Column(DateTime, default=datetime.utcnow())
    schedule_id = Column(String)
    delivery_id = Column(String)

    def dict(self):
...
```

Now we need to use Alembic to managa our migrations. This tool will check the differences between the `OrderModel` and the `order` table definition and perform the necessary updates.

As SQLite has limited support for `ALTER` statements, we will need to enable batch support so that we can run batch operations.

First of all, in the `migrations/env.py` file we will need to update the following block to include the `render_as_batch`:

```python
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,   # Added to support batch operations
        )
```

Now we can generate the Alembic migration and update the database:

```bash
poetry run alembic revision --autogenerate -m "Add user ID to order table"
```

And if everything goes well, we can update the database:

```bash
poetry run alembic upgrade heads
```

### Updating the endpoints

Let's focus on how to update the `POST /orders` endpoint to capture the user ID when placing the order.

We start on the API layer, where we update the *path function* that is activated when a `POST /orders` is received.

```python
@app.post(
    "/orders",
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
)
def create_order(request: Request, payload: CreateOrderSchema):
    with UnitOfWork() as unit_of_work:
        repo = OrdersRepository(unit_of_work.session)
        orders_service = OrdersService(repo)
        order = payload.model_dump()["order"]
        for item in order:
            item["size"] = item["size"].value
        order = orders_service.place_order(order, request.state.user_id)
        unit_of_work.commit()
        response_payload = order.dict()
    return response_payload
```

We update the signature of the function to receive the `Request` object, which FastAPI will populate for us. Then, we modify how we invoke the `place_order()` method on the `OrdersService` to supply the `user_id` that comes in the request.

We modify the `OrdersService` to receive the `user_id`, which we pass to the data access layer:

```python
class OrdersService:
...

    def place_order(self, items, user_id):
        return self.orders_repository.add(items, user_id)
```

We do the same for the `OrderRepository.add()` method:

```python
class OrdersRepository:
...

    def add(self, items, user_id):
        record = OrderModel(
            items=[OrderItemModel(**item) for item in items], user_id=user_id
        )
        self.session.add(record)
        return Order(**record.dict(), order_=record)
```

Now we can modify the `GET /orders` endpoint so that a user will only get to see a list of their own orders when they call the endpoint.

In the corresponding path function, we make sure to pass the `user_id` as a filter to the `OrdersService.list_orders()` method.

```python
@app.get("/orders", response_model=GetOrdersSchema)
def get_orders(
    request: Request,
    cancelled: Optional[bool] = None,
    limit: Optional[int] = None,
):
    with UnitOfWork() as unit_of_work:
        repo = OrdersRepository(unit_of_work.session)
        orders_service = OrdersService(repo)
        results = orders_service.list_orders(
            cancelled=cancelled, limit=limit, user_id=request.state.user_id
        )
    return {"orders": [result.dict() for result in results]}
```

In turn, the service will automatically pass the filter to the repository (no changes needed on the `OrdersService.listOrders()`).

The repository's `list()` method does not need to be modified either because it was already considering a flexible list of filter when doing `query.filter_by(**filters).limit(limit).all()`.

We should do something similar to the `GET /orders/{order_id}`. In order to apply the same flexible solution we implemented for the `OrdersService.list()` and `OrdersRepository.list()` we can include an additional variadic keyword argument named `**filters` so that we can accommodate more requirements of this type in the future (e.g., `tenant_id`).

```python
class OrdersService:
...

    def get_order(self, order_id, **filters):
        order = self.orders_repository.get(order_id, **filters)
        if order is not None:
            return order
        else:
            raise OrderNotFoundError(f"Order with id {order_id} not found")
```


```python
class OrdersRepository:
...
    def _get(self, id_, **filters):
        return (
            self.session.query(OrderModel)
            .filter(OrderModel.id == str(id_))
            .filter_by(**filters)
            .first()
        )

    def get(self, id_, **filters):
        order = self._get(id_, filters)
        if order is not None:
            return Order(**order.dict())
```

