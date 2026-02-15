# Coockiecutter
> creating projects from project templates

## Installation

You can install Cookiecutter as a tool managed by `uv`. That makes it available for all your needs as long as you rely on `uv` for project management.

```bash
# install cookiecutter as a uv tool
$ uv tool install cookiecutter

# upgrade cookiecutter (if it was already available)
$ uv tool upgrade cookiecutter

# list available tools controlled by uv
$ uv tool list
cookiecutter v2.6.0
- cookiecutter
httpie v3.2.4
- http
- httpie
- https
ruff v0.15.0
- ruff
```

## Getting to know Cookiecutter by creating a project

Cookiecutter is a tool for creating projects. You can get familiar with it by creating a project from an available template:

```bash
$ uv run cookiecutter \
  https://github.com/audreyfeldroy/cookiecutter-pypackage.git
```

Immediately after, Cookiecutter will start asking you a series of questions that are required to generate the project:

```
$ uv run cookiecutter \
  https://github.com/audreyfeldroy/cookiecutter-pypackage.git
  [1/9] full_name (Audrey M. Roy Greenfeld): Jason Isaacs
  [2/9] email (audreyfeldroy@example.com): jason.isaacs@example.com
  [3/9] github_username (audreyfeldroy): jsonisaacs
  [4/9] pypi_package_name (python-boilerplate):
  [5/9] project_name (Python Boilerplate):
  [6/9] project_slug (python_boilerplate):
  [7/9] project_short_description (Python Boilerplate contains all the boilerplate you need
to create a Python package.): My first project created with Cookiecutter
  [8/9] pypi_username (jsonisaacs):
  [9/9] first_version (0.1.0):
Your Python package project has been created successfully!
```

Right after that, you'll see a project generated in your current directory:

```
$ tree python-boilerplate/
python-boilerplate/
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── HISTORY.md
├── LICENSE
├── MANIFEST.in
├── README.md
├── docs
│   ├── index.md
│   ├── installation.md
│   └── usage.md
├── justfile
├── pyproject.toml
├── src
│   └── python_boilerplate
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── python_boilerplate.py
│       └── utils.py
└── tests
    ├── __init__.py
    └── test_python_boilerplate.py
```

Files will not be only be created, also adjusted with the values provided above. For example, in your [`pyproject.toml`](01_using_cookiecutter/python-boilerplate/pyproject.toml) your name and project named will have been adjusted.

After running the `cookiecutter` command, the corresponding GitHub project mentioned will be downloaded into `~/.cookiecutters`. You will find a directory for each of the templates you've used.

To understand how the different files were generated, you just need to take a look at the downloaded package (or you can browse it in GitHub).

That project will have the following structure:

```
$ tree cookiecutter-pypackage/
cookiecutter-pypackage/
├── AGENTS.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
├── cookiecutter.json
├── docs
│   ├── console_script_setup.md
│   ├── index.md
│   ├── prompts.md
│   ├── pypi_release_checklist.md
│   ├── troubleshooting.md
│   └── tutorial.md
├── hooks
│   ├── post_gen_project.py
│   └── pre_gen_project.py
├── justfile
├── pyproject.toml
├── run.py
├── src
│   └── cookiecutter_pypackage
│       ├── __init__.py
│       └── cli.py
├── tests
│   └── test_bake_project.py
├── uv.lock
└── {{cookiecutter.pypi_package_name}}
    ├── CODE_OF_CONDUCT.md
    ├── CONTRIBUTING.md
    ├── HISTORY.md
    ├── LICENSE
    ├── MANIFEST.in
    ├── README.md
    ├── docs
    │   ├── index.md
    │   ├── installation.md
    │   └── usage.md
    ├── justfile
    ├── pyproject.toml
    ├── src
    │   └── {{cookiecutter.project_slug}}
    │       ├── __init__.py
    │       ├── __main__.py
    │       ├── cli.py
    │       ├── utils.py
    │       └── {{cookiecutter.project_slug}}.py
    └── tests
        ├── __init__.py
        └── test_{{cookiecutter.project_slug}}.py
```

For example, `{{cookiecutter.project_slug}}` is a directory that will contain the source files.

If you have a look at `pyproject.toml` within that directory you will see:

```toml
$ cat cookiecutter-pypackage/\{\{cookiecutter.pypi_package_name\}\}/pyproject.toml
[project]
name = "{{cookiecutter.pypi_package_name}}"
version = "{{ cookiecutter.first_version }}"
description = "{{ cookiecutter.project_short_description | replace('\\', '\\\\') | replace('\"', '\\\"') }}"
readme = "README.md"
authors = [
  {name = "{{ cookiecutter.full_name | replace('\\', '\\\\') | replace('\"', '\\\"') }}", email = "{{cookiecutter.email}}"}
]
maintainers = [
  {name = "{{ cookiecutter.full_name | replace('\\', '\\\\') | replace('\"', '\\\"') }}", email = "{{cookiecutter.email}}"}
]
...
```

All those variables are pulled from the `cookiecutter.json` file:

```json
$ cat cookiecutter-pypackage/cookiecutter.json
{
  "full_name": "Audrey M. Roy Greenfeld",
  "email": "audreyfeldroy@example.com",
  "github_username": "audreyfeldroy",
  "pypi_package_name": "python-boilerplate",
  "project_name": "Python Boilerplate",
  "project_slug": "{{ cookiecutter.pypi_package_name.replace('-', '_') }}",
  "project_short_description": "Python Boilerplate contains all the boilerplate you need to create a Python package.",
  "pypi_username": "{{ cookiecutter.github_username }}",
  "first_version": "0.1.0",
  "__gh_slug": "{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}"
}
```

## Create a Cookiecutter from scratch

1. Start by creating a directory for your cookiecutter and cd into it:

```bash
$ mkdir cookiecutter-website-simple

$ cd cookiecutter-website-simple/
```

1. Create a `cookiecutter.json`:

    The file `cookiecutter.json` contains fields referenced in the template.

    For each field, you can define a default value, and user will be prompted during cookiecutter execution.

    The only mandatory field is `project_slug` which should comply with PEP8 naming conventions:

    ```json
    {
      "project_name": "Cookiecutter Website Simple",
      "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '_') }}",
      "author": "anonymous"
    }
    ```

1. Create `index.html`:

    Inside of `{{cookiecutter.project_slug}}/` directory, create an `index.html` file:

    ```hmtl
    <!doctype html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>{{ cookiecutter.project_name }}</title>
        </head>

        <body>
            <h1>{{ cookiecutter.project_name }}</h1>
            <p>by {{ cookiecutter.author }}</p>
        </body>
    </html>
    ```

1. Pack the template into ZIP:

    There are many ways to run Cookiecutter templates, one of them being zipping the cookiecutter and then run it for testing.

    The following command will generate a `cookiecutter.zip` file and echo the full path to the file:

    | NOTE: |
    | :---- |
    | Remember, you should be within the cookiecutter-website-simple/ directory when running the script below. |

    ```bash
    $ (SOURCE_DIR=$(basename $PWD) ZIP=cookiecutter.zip && \
      pushd .. && \
      zip -r $ZIP $SOURCE_DIR --exclude $SOURCE_DIR/$ZIP --quiet && \
      mv $ZIP $SOURCE_DIR/$ZIP && \
      popd &&
      echo "Cookiecutter full path: $PWD/$ZIP")
    ```

    After executing the script you should have a `cookiecutter.zip` file created within the cookiecutter-website-simple/ directory.

1. Run cookiecutter:

In whatever work directory you're interested in creating an instantiation of the cookiecutter template run the following:

    ```bash
    $ uv run cookiecutter <path-to-cookiecutter-zip>
    ```

In your example, it'll be:

```bash
$ uv run cookiecutter \
  ../02_cookiecutter_from_scratch/cookiecutter-website-simple/cookiecutter.zip
  [1/3] project_name (Cookiecutter Website Simple): Test Web
  [2/3] project_slug (test_web):
  [3/3] author (anonymous): Jason Isaacs
```