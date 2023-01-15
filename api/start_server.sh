#!/usr/bin/env sh

source venv/bin/activate && python3 manage.py db upgrade && gunicorn --worker-class eventlet wsgi:app --timeout 0 --workers=1
