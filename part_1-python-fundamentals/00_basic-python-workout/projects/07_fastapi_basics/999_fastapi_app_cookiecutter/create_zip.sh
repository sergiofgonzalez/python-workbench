#!/bin/bash -e

# Create a zip file of the cookiecutter template directory
SOURCE_DIR=$(basename $PWD) ZIP=cookiecutter.zip && \
  pushd .. && \
  zip -r $ZIP $SOURCE_DIR --exclude $SOURCE_DIR/$ZIP --exclude $SOURCE_DIR/create_zip.sh --quiet && \
  mv $ZIP $SOURCE_DIR/$ZIP && \
  popd &&
  echo "Cookiecutter full path: $PWD/$ZIP"
