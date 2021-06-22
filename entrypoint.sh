#! /usr/bin/env bash

gunicorn --config conf/gunicorn.conf.py "$GUNICORN_APP"
