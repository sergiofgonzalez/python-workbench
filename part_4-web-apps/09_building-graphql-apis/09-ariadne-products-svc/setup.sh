#!/bin/bash -e

conda run -n web python -m venv .venv --upgrade-deps
source .venv/bin/activate
python -m pip install -r requirements.txt