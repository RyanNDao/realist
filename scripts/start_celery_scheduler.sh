#!/bin/bash

# Function to check if the process is running
check_process() {
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

BEAT_COMMAND="poetry run celery -A $UNIQUE_BEAT_IDENTIFIER --loglevel=info"
WORKER_COMMAND="poetry run celery -A $UNIQUE_WORKER_IDENTIFIER --concurrency 1 --loglevel=info"

check_process "$UNIQUE_BEAT_IDENTIFIER"
if [ $? -eq 0 ]; then
    echo "Celery Beat is already running."
else
    echo "Starting Celery Beat..."
    if [ -f ./celerybeat-schedule ]; then
      echo "Removing existing celerybeat schedule file..."
      rm ./celerybeat-schedule
    fi
    if [ -f ./celery_beat.log ]; then
      echo "Removing existing celery_beat log file..."
      rm ./celery_beat.log
    fi
    nohup $BEAT_COMMAND > celery_beat.log 2>&1 &
    echo "Celery Beat started with PID $!"
fi

check_process "$UNIQUE_WORKER_IDENTIFIER"
if [ $? -eq 0 ]; then
    echo "Celery Worker is already running."
else
    echo "Starting Celery Worker..."
    if [ -f ./celery_worker.log ]; then
      echo "Removing existing celery_worker log file..."
      rm ./celery_worker.log
    fi
    nohup $WORKER_COMMAND > celery_worker.log 2>&1 &
    echo "Celery Worker started with PID $!"
fi
