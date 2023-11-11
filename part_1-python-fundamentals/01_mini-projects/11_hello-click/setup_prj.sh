#!/bin/bash -e

if [ $# -ne 2 ]; then
  echo "Wrong number of arguments"
  echo "Usage: $0 [prj_name] [module_name]"
  exit 1
fi

mkdir -p $1
cd $1 && conda run -n base python -m venv .venv --upgrade-deps && echo "# $1: $2" >> README.md && touch $2.py && cd ..
