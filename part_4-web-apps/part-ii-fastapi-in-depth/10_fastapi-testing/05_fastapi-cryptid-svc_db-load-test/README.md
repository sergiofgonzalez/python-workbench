# Cryptid service using FastAPI framework
> Adding database load tests with Faker

This project illustrates how to build a web application that implements the management of *cryptids* (imaginary creatures) and the explorers who seek them.

This version includes an example of how to measure db performance using Faker to generate data.

## Setting up shop

The project uses Poetry. To set things up type:

```bash
poetry install
```

## Running the application

To run the application in development mode type:

```bash
poetry run python cryptid/main.py
```

This will start the server in port 8080 with reloading enabled.

You can also run the application with `uvicorn`:

```bash
poetry run uvicorn cryptid.main:app \
  --port 8080 \
  --reload
```

| NOTE: |
| :---- |
| The code of the data layer does not include `connection.commit()`. As a result, the database file is never updated, which helps with the testing.<br>If you want to persist the changes so that they survive server restarts you simply need to commit the changes after every operation that *changes* the database. |

## Testing the application

This application features a full set of unit and end-to-end tests, so that you can run them using PyTest or vscode.

| NOTE: |
| :---- |
| For some reason, you cannot run in parallel the full and unit tests, but they work well if you submit them separately. |


You can also run the (basic set of) schemathesis tests doing:

```bash
$ schemathesis run http://localhost:8080/openapi.json --experimental=openapi-3.1
```

### Unit tests

The application include a full set of unit tests for the data, service, and web layer using PyTest framework.

Note that the data layer is tested using an in-memory approach, and the service and web layer are wired with a fake layer so that no db is used.

### Manual Integration tests with HTTPie

#### OAuth2 integration

The interesting part of the project is the OAuth2 integration for the authentication and authorization of a couple of endpoints.

Essentially, a `POST /user/token` endpoint is defined, which accepts a form with the fields `username` and `password`. Upon receiving this information, the application will check that the user is defined in the database and then check whether the password that has been sent (after being hashed), matches the hash stored in the database. If that is the case, an access token (JWT) will be generated, otherwise a 401 status code is returned.

Additionally, a `GET /user/token` endpoint is defined with the dependency `oauth2_dep`, which makes it require an access token to proceed to the endpoint implementation.


In order to test the flow with HTTPie and Python REPL you can do:

Simulate a login form sending username/password to the web server with a user that has not been previously defined.

```bash
http --form POST localhost:8080/user/token username='jason.isaacs' password='secret'
```

Then, you can insert a new user to test the happy authentication flow:

First you need to generate the hash for a user's password:

```python
>>> from cryptid.service import user as service
>>> service.get_hash("fidelio")
'$2b$12$nK9IAYkv120UeKGQ.SWmOO8Ex6II/OtQprsy/evyRyv/shs8IjONa'
```

Then you can call the endpoint that creates a new user, which should return a 201:

```bash
$ http POST localhost:8080/user name='jason.isaacs' password_hash='$2b$12$nK9IAYkv120UeKGQ.SWmOO8Ex6II/OtQprsy/evyRyv/shs8IjONa'
```

Finally, you can call the POST /user/token this time knowing that the user has been previously defined, and therefore, the authentication should succeed.

```bash
http --form POST localhost:8080/user/token username='jason.isaacs' password='fidelio'
```

It should return something along the lines:

```json
{
    "access_token": "eyJ..._U",
    "token_type": "bearer"
}
```

The payload of the token after decoding it should look like:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}.{
  "sub": "jason.isaacs",
  "exp": 1709047297
}.[Signature]
```


With the access token in your possession, you can now call a protected endpoint:

```bash
$ http localhost:8080/user/token "Authorization: Bearer ey..._U"
HTTP/1.1 200 OK
content-length: 145
content-type: application/json
date: Tue, 27 Feb 2024 15:01:13 GMT
server: uvicorn

{
    "token": "eyey..._U"
}
```

#### CRUD layer

The CRUD layer for creatures, explorers, and users can be tested using HTTPie as illustrated below.

#### Explorer

Sample HTTPie commands:

```bash
# Create explorer
$ http localhost:8080/explorer/ name="Beau Buffette" country="US" description="Manually created explorer"
```

```bash
# Replace entry (PUT)
$ http PUT localhost:8080/explorer/"Beau Buffette" name="Jason Isaacs" country="UK" description="Hello to Jason!"
```

```bash
# Partially modify entry (PATCH)
$ http patch localhost:8080/explorer/"Beau Buffette" name="Jason Isaacs"
```

```bash
# Delete entry
$ http delete http://localhost:8080/explorer/"Beau Buffette"
```


- [X] Get all explorers using `GET /explorer/` should return an empty array.

- [X] Get all explorers using `GET /explorer` should now work (with the two decorators).

- [X] Explorer creation with mispelled property (e.g., `contry` should fail with 422).

- [X] Explorer creation with correct attributes should work and return the created record (201 should be returned).

    ```bash
    $ http localhost:8080/explorer/ name="Beau Buffette" country="US" description="Manually created explorer"
    HTTP/1.1 200 OK
    content-length: 81
    content-type: application/json
    date: Mon, 12 Feb 2024 14:53:53 GMT
    server: uvicorn

    {
        "country": "US",
        "description": "Manually created explorer",
        "name": "Beau Buffette"
    }

    ```

- [X] Now get all explorers should return the recently created record.

- [X] Get one should also work `GET /explorer/"Beau Buffette"`

- [X] Try to define the same record twice should fail with 422.

    The server logs show: `ERROR:    cryptid.data.explorer : IntegrityError: cannot create explorer Beau Buffette: UNIQUE constraint failed: explorer.name`

- [X] Try to get a non-existent record should fail with 404

- [X] Replace the description of an explorer (using PUT)

- [X] Replace the name of an explorer with a new name (using PUT)

- [X] Replace the name of an explorer with one that already exists should fail with 422. (PUT)

- [X] Replace the name of an non-existent explorer should fail with 404 (PUT)

- [X] Replace the country of an explorer using PATCH

        ```bash
        $ http patch localhost:8080/explorer/"Beau Buffette" country="ES
        ```
- [X] Replace the country of non-existent explorer should fail with 404 (PATCH)

- [X] Replace the name of an explorer with one that already exists should fail with 422 (PATCH)

- [X] Replace the name of an explorer should work OK (PATCH)

- [X] Delete one that doesn't exist

- [X] Delete one that exists

#### Creature

Sample HTTPie commands:

```bash
# Create explorer
$ http localhost:8080/creature/ name="yeti" country="CN" area="Himalayas" description="Snowperson" aka="The Abominable Snowman"
```

```bash
# Replace entry (PUT)
$ http put localhost:8080/creature/yeti name="Sasquatch" country="CN" area="Himalayas" description="Snowperson" aka="yeti"
```

```bash
# Partially modify entry (PATCH)
$ http patch localhost:8080/creature/Yeti aka="Sasquatch"
```

```bash
# Delete entry
$ http delete localhost:8080/creature/Yeti
```


- [X] Get all creatures using `GET /creature/` should return an empty array.

- [X] Get all creatures using `GET /creature` should now work (with the two decorators).

- [X] Creature creation with mispelled property (e.g., `contry` should fail with 422).

- [X] Creture creation with correct attributes should work and return the created record (201 should be returned).

- [X] Now get all explorers should return the recently created record.

- [X] Get one should also work `GET /creaure/"yeti"`

- [X] Try to define the same record twice should fail with 422.

    The server logs show: `ERROR:    cryptid.data.creature : IntegrityError: cannot create creature yeti: UNIQUE constraint failed: creature.name`

- [X] Try to get a non-existent record should fail with 404

- [X] Replace the description of an creature (using PUT)

- [X] Replace the name of an creature with a new name (using PUT)

- [X] Replace the name of an creature with one that already exists should fail with 422. (PUT)

- [X] Replace the name of an non-existent creature should fail with 404 (PUT)

- [X] Replace the country of a creature using PATCH

- [X] Replace the country of non-existent creature should fail with 404 (PATCH)

- [X] Replace the name of an explorer with one that already exists should fail with 422 (PATCH)

- [X] Replace the name of an explorer should work OK (PATCH)

- [X] Delete one that doesn't exist

- [X] Delete one that exists