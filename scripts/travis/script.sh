#!/usr/bin/env bash
set -ev
if [ "$SNIPSKIT_REQUIREMENTS" == "all" ]
then
    pytest --verbose --cov src --cov-report xml
    scripts/check_examples.sh
    scripts/generate_docs.sh
    scripts/build_package.sh
else
    # Don't test coverage when we only test a part of the modules.
    pytest --verbose
fi
