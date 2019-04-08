#!/bin/sh
bashate scripts/*.sh scripts/travis/*.sh && shellcheck scripts/*.sh scripts/travis/*.sh
