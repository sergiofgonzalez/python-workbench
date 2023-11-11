#!/bin/bash -e

conda run -n base python -m venv .venv --upgrade-deps && \
  source .venv/bin/activate