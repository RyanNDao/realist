#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 number_of_workers"
  exit 1
fi

number_of_workers=$1

if pgrep -f "src.backend.server.flask_index:app" > /dev/null; then
    echo "Gunicorn server is already running."
    exit 1
fi

if [ -f ./gunicorn.log ]; then
  echo "Removing existing log file..."
  rm ./gunicorn.log
fi

echo "Starting Gunicorn server with $number_of_workers workers..."
poetry run gunicorn -w $number_of_workers "src.backend.server.flask_index:app" --bind 0.0.0.0:8000 --log-file ./gunicorn.log 2>&1 | tee -a ./gunicorn.log &

echo "Gunicorn server started with $number_of_workers workers. Logs are being written to ./gunicorn.log"
