#!/usr/bin/env bash

cd ../..
echo "Creating command line version of project"
pyinstaller --onefile command_line.py

echo "Moving command line to test dir and removing other files"
mv dist/command_line tests/it-test
rm command_line.spec
rm -rf build
rm -rf dist

cd -
