# Builder pattern: Implementing a URL object builder

Use the **builder** patterns to create URL objects.

The goal is to implement a URL class that can hold all the components of a standard URL, validate them, and format them back into a string.

The elements the URL must feature are:
+ protocol: as in http / https / ftp / ...
+ username
+ password
+ hostname
+ port
+ pathname
+ search
+ hash

The class should check that all the elements have the expected type and format, and expose a __str__() method that provides the correct string representation of the URL.

Then you should implement a builder object for that class, so that the consumer code has an easier job building the instance.

## Running the project

To create the virtual environment without running the project:

```bash
uv venv
```

To run the project run:

```bash
uv run main.py
```