#!/usr/bin/env sh

source venv/bin/activate && python3 manage.py db upgrade && python3 apply_seeds.py
