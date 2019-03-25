#!/bin/sh
if [ "$SNIPSKIT_REQUIREMENTS" == "all" ]
then
  pytest --verbose
  scripts/check_examples.sh
  scripts/generate_docs.sh
  scripts/build_package.sh
fi
