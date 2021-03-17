#! /usr/bin/env bash

gunicorn --config conf/gunicorn.conf.py "$FLASK_APP"
