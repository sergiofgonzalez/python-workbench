# Introduction to LangChain

## Setting up shop

This Jupyter notebook uses Poetry for dependency management.

To create the `pyproject.toml` I typed:

```bash
poetry init --name 01_langchain_intro \
  --description "description here"
  --author "Sergio F. Gonzalez <sergio.f.gonzalez@gmail.com>" \
  --python "^3.10"
```
Then I added the `package-mode = false` because the project is not supposed to be installed as a package, but only used to track the dependencies.
