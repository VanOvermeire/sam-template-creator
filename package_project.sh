#!/usr/bin/env bash
set -e

# for tests, expects a virtualenv called testenv

if [[ $# -lt 1 ]]; then
    echo "usage package_project.sh [test|prod]"
    exit 1
fi

env=$1

python3 -m pip install --user --upgrade setuptools wheel
python3 setup.py sdist bdist_wheel

if [[ ${env} == "test" ]]; then
    python3 -m twine upload -u VanOvermeire --repository-url https://test.pypi.org/legacy/ dist/*
    echo "Now install (preferably in a virtualenv) with:"
    echo "python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps sam-template-creator --upgrade"
elif [[ ${env} == "prod" ]]; then
    twine upload -u VanOvermeire dist/*
    echo "Now install with:"
    echo "pip install sam-template-creator"
else
    echo "Invalid argument ${env}"
    exit 1
fi

rm -rf build
rm -rf dist
