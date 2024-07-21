#!/bin/bash

# This script starts the scheduler for celery. If a process is already running, it will not start another process

check_process() {
  pgrep -f "$1" > /dev/null 2>&1
  return $?
}

BEAT_COMMAND="celery -A src.backend.server.configurations.celery_conf beat"
WORKER_COMMAND="celery -A src.backend.server.configurations.celery_conf worker"

check_process "$BEAT_COMMAND"
if [ $? -eq 0 ]; then
    echo "Celery Beat is already running."
else
    nohup $BEAT_COMMAND --loglevel=info > celery_beat.log 2>&1 &
    BEAT_PID=$!
    echo "Celery Beat started with PID $BEAT_PID"
fi

check_process "$WORKER_COMMAND"
if [ $? -eq 0 ]; then
    echo "Celery Worker is already running."
else
    nohup $WORKER_COMMAND --loglevel=info > celery_worker.log 2>&1 &
    WORKER_PID=$!
    echo "Celery Worker started with PID $WORKER_PID"
fi