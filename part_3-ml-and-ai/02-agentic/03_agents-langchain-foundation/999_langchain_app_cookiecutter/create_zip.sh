#!/bin/bash -e

# Create a zip file of the cookiecutter template directory
SOURCE_DIR=$(basename $PWD)
VERSION=$(grep '^version = ' {{cookiecutter.project_slug}}/pyproject.toml | awk -F'"' '{print $2}')
ZIP=cookiecutter-${VERSION}.zip

pushd .. && \
  zip -r $ZIP $SOURCE_DIR --exclude $SOURCE_DIR/$ZIP \
  --exclude $SOURCE_DIR/create_zip.sh \
  --exclude $SOURCE_DIR/CHANGELOG.md \
  --quiet && \
  mv $ZIP $SOURCE_DIR/$ZIP && \
  popd && \
  echo "Cookiecutter full path: $PWD/$ZIP"
