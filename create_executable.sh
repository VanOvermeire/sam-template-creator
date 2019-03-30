#!/usr/bin/env bash

pyinstaller --onefile template_creator.py
rm template_creator.spec
rm -rf build
