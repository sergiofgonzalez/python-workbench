# 001: Hello, FalkorDB
> Illustrates the basics of FalkorDB

## Project description

This lab illustrates the basics of FalkorDB
+ Running Docker to spin up a FalkorDB server
+ Getting a connection
+ Creating a graph
+ Running a few simple queries


## Running the program

First of all, you need to spin up a Docker container to run the FalkorDB server:

```bash
docker run \
  -p 6379:6379 -p 3000:3000 \
  -it \
  --rm \
  -v ./data:/var/lib/falkordb/data falkordb/falkordb
```



If you tan to create the container with an empty databas


You can run the application with:

```bash
uv run main.py
```

## Project management

This project is managed using `uv`.

FalkorDB dependency was added using:

```bash
$ uv add FalkorDB
```

The only other dependencies for development are ruff and ty:

```bash
$ uv add ruff ty --dev
```
