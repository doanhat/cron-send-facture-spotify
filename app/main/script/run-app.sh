#!/bin/bash
# shellcheck disable=SC2164
cd /usr/src
# shellcheck disable=SC2155
export PYTHONPATH=$PYTHONPATH:$(pwd)
export PORT="8080"
. venv/bin/activate && cd app/main/ && gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
exit