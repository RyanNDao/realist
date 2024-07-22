#!/bin/bash

# Function to check if the process is running
check_process() {
  # This checks for the presence of a celery command related to the specific configuration file
  echo "Checking for process: $1"
  pcount=$(pgrep -f "$1" | grep -v grep | wc -l)
  echo "Process count: $pcount"
  if [ $pcount -gt 0 ]; then
    return 0
  else
    return 1
  fi
}

UNIQUE_BEAT_IDENTIFIER="src.backend.server.configurations.celery_conf beat"
UNIQUE_WORKER_IDENTIFIER="src.backend.server.configurations.celery_conf worker"

BEAT_COMMAND="poetry run celery -A $UNIQUE_BEAT_IDENTIFIER"
WORKER_COMMAND="poetry run celery -A $UNIQUE_WORKER_IDENTIFIER"

check_process "$UNIQUE_BEAT_IDENTIFIER"
if [ $? -eq 0 ]; then
    echo "Celery Beat is already running."
else
    echo "Starting Celery Beat..."
    nohup $BEAT_COMMAND --loglevel=info > celery_beat.log 2>&1 &
    echo "Celery Beat started with PID $!"
fi

check_process "$UNIQUE_WORKER_IDENTIFIER"
if [ $? -eq 0 ]; then
    echo "Celery Worker is already running."
else
    echo "Starting Celery Worker..."
    nohup $WORKER_COMMAND --loglevel=info > celery_worker.log 2>&1 &
    echo "Celery Worker started with PID $!"
fi
