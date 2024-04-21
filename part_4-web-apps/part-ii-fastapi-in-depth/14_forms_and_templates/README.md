# Forms and Templates

## Intro

This chapter illustrates how to deal with HTML forms and templates in FastAPI applications.

## Handling form data

The `Form` object can be used to handle form data in your FastAPI projects:

```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.get("/who")
def greet(name: str = Form()):
    return f"Hello, {name} on GET!"

@app.post("/who")
def greet2(name: str = Form()):
    return f"Hello, {name} on POST!"
```

## Templates

You can use Jinja2 templating engine in FastAPI to return HTML from your FastAPI Python applications.

```python
...
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.include_router(explorer.router)
app.include_router(creature.router)
app.include_router(user.router)

BASE_DIR = Path(__file__).resolve().parent

template_obj = Jinja2Templates(directory=BASE_DIR / "template")
```

The template syntax is pretty similar to the one you'll find in other templating engines:

```html
<body>
  <table class="table">
    <thead>
      <tr>
        <th colspan="5">Creatures</th>
      </tr>
      <tr>
        <th scope="col">Name</th>
        <th scope="col">Description</th>
        <th scope="col">Country</th>
        <th scope="col">Area</th>
        <th scope="col">AKA</th>
      </tr>
    </thead>
    <tbody>
      {% for creature in creatures: %}
      <tr>
        <th scope="row">{{ creature.name }}</td>
        <td>{{ creature.description }}</td>
        <td>{{ creature.country }}</td>
        <td>{{ creature.area }}</td>
        <td>{{ creature.aka }}</td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
```

Then, in your path function you just need provide the values you're passing the template:

```python
@app.get("/")
def home(request: Request):
    explorers = explorer.get_all()
    return template_obj.TemplateResponse(
        "list.html",
        {
            "request": request,
            "explorers": explorers,
            "creatures": creature.get_all(),
        },
    )
```
