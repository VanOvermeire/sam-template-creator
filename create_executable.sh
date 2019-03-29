#!/usr/bin/env bash

pyinstaller --onefile template_creator.py
mv dist/template_creator ./template_creator
rm template_creator.spec
rm -rf dist
rm -rf build
