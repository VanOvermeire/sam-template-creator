#!/usr/bin/env bash

rm dist/template_creator
pyinstaller --onefile template_creator.py
rm template_creator.spec
rm -rf build
