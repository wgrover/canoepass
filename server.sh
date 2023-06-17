#!/usr/bin/env sh
gunicorn -w 4 -b :8000 'app:app'
