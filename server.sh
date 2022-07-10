#!/usr/bin/sh
gunicorn -w 4 -b :8080 'app:app'
