#!/bin/bash -e

# Invoke uv to run the cookiecutter template and create a new project
VERSION=$(grep '^version = ' 999_langchain_app_cookiecutter/{{cookiecutter.project_slug}}/pyproject.toml | awk -F'"' '{print $2}')
cookiecutter 999_langchain_app_cookiecutter/cookiecutter-${VERSION}.zip