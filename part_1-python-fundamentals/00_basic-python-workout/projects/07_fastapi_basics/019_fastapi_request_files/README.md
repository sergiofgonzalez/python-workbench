# 019: Hello, FastAPI request files
> Illustrates the basics of FastAPI request files

## Project description

You can define files to be uploaded by the client using `File()` and `UploadFile`(`UploadFile` being the most appropriate in most cases).

### Using `File()` and `UploadedFile`

Create a couple of path operations:
+ `POST /files/`: accepts a `file` declared as a bytes object that is identified as a `File()`. In the path operation return the size of the bytes by calculating the size of the corresponding bytes object.

+ `POST /uploadfile/`: accepts a file of type `UploadFile` and returns its name and content type.

SOLUTION:

This can be tested with:

```bash
# send `./main.py` to file argument in the path operation
$ http --form POST :5000/files/ file@./main.py

# send `./main.py` to ffile argument in the path operation
$ http --form POST :5000/uploadfile/ file@./main.py
```

### Declaring optional files and upload files

Create a couple of path operations:
+ `POST /v2/files/`: accepts a `file` declared as a bytes object that is identified as a `File()`. In the path operation return the size of the bytes by calculating the size of the corresponding bytes object.

+ `POST /v2/uploadfile/`: accepts a file of type `UploadFile` and returns its name and content type.

Both files should be optional, and the path operations should return a message stating "No file was sent" in case the file was not available in the request.

### Adding metadata to files and upload files

Create a couple of path operations:
+ `POST /v3/files/`: accepts a `file` declared as a bytes object that is identified as a `File()`. In the path operation return the size of the bytes by calculating the size of the corresponding bytes object.

+ `POST /v3/uploadfile/`: accepts a file of type `UploadFile` and returns its name and content type.

Both files should be required and they should feature their corresponding description metadata.

### Multiple file uploads

Create a program with three path operations:

+ `POST /v4/files/`: accepts multiple `file` declared as a bytes object that is identified as a `File()`. In the path operation return the size of all the files received in the request.

+ `POST /v4/uploadfiles/`: accepts a list of files of type `UploadFile` and returns their name and content type.

+ `GET /`: return an HTML with the following content:

    ```html
    <body>
      <form action="/files/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
      </form>
      <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
        <input name="files" type="file" multiple>
        <input type="submit">
      </form>
    </body>
    ```

### Multiple file uploads with description

Repeat [Multiple file uploads](#multiple-file-uploads) adding the corresponding description for the files.

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
