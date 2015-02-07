#!/usr/bin/env bash

function python_files() {
    find . -type f -name '*.py' -print0
}

python_files \
| xargs -0 pep8

python_files \
| xargs -0 pylint --rcfile pylintrc
