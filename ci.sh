#!/bin/sh

echo "===> Creating virtual environment: .venv"
virtualenv .venv || exit 1

echo && echo && echo "===> Installing dependancies"
.venv/bin/pip install -r requirements.txt || exit 1

echo && echo && echo "===> Running test suite"
.venv/bin/python manage.py test || exit 1
