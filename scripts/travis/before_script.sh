#!/usr/bin/env bash
set -ev
if [ "$SNIPSKIT_REQUIREMENTS" == "all" ]
then
  export PYTEST_ADDOPTS="--cov src --cov-report xml"
  curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
  chmod +x ./cc-test-reporter
  ./cc-test-reporter before-build
fi
