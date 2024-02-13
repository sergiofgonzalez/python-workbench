# Cryptid service using FastAPI framework
> Step 3: adding basic models, fake services and wiring the web layer to the fakes

This project illustrates how to build a web application that implements the management of *cryptids* (imaginary creatures) and the explorers who seek them.

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

## Testing the application with HTTPie

You can test the `/explorer` and `/creature` endpoints with HTTPie:

```bash
$ http localhost:8080/explorer/
HTTP/1.1 200 OK
content-length: 153
content-type: application/json
date: Wed, 07 Feb 2024 11:45:44 GMT
server: uvicorn

[
    {
        "country": "FR",
        "description": "Scarce during full moons",
        "name": "Claude Hande"
    },
    {
        "country": "DE",
        "description": "Myopic machete man",
        "name": "Noah Weise"
    }
]
```

```bash
$ http localhost:8080/explorer/"Noah Weise"
HTTP/1.1 200 OK
content-length: 71
content-type: application/json
date: Wed, 07 Feb 2024 11:47:04 GMT
server: uvicorn

{
    "country": "DE",
    "description": "Myopic machete man",
    "name": "Noah Weise"
}
```

```bash
$ http localhost:8080/creature/
HTTP/1.1 200 OK
content-length: 211
content-type: application/json
date: Wed, 07 Feb 2024 11:50:33 GMT
server: uvicorn

[
    {
        "aka": "Abominable Snowman",
        "area": "Himalayas",
        "country": "CN",
        "description": "Hirsute Himalayan",
        "name": "Yeti"
    },
    {
        "aka": "Yeti's cousin Eddie",
        "area": "*",
        "country": "US",
        "description": "Sasquatch",
        "name": "Bigfoot"
    }
]
```

```bash
$ http localhost:8080/creature/Bigfoot
HTTP/1.1 200 OK
content-length: 98
content-type: application/json
date: Wed, 07 Feb 2024 11:50:49 GMT
server: uvicorn

{
    "aka": "Yeti's cousin Eddie",
    "area": "*",
    "country": "US",
    "description": "Sasquatch",
    "name": "Bigfoot"
}
```
