#!/bin/bash

terminate_process() {
  local identifier=$1
  echo "Terminating $identifier..."
  
  pids=$(pgrep -f "$identifier" | grep -v grep)
  
  if [ -z "$pids" ]; then
    echo "No $identifier processes running."
    return
  fi

  # Send SIGTERM to allow for graceful shutdown
  echo "Sending SIGTERM to $identifier processes..."
  echo $pids | xargs kill -SIGTERM
  
  sleep 20
  
  # Double-check if any processes are still running and force kill if necessary
  if pgrep -f "$identifier" > /dev/null; then
    echo "Forcing shutdown of remaining $identifier processes..."
    echo $pids | xargs kill -9
  fi
  
  echo "$identifier processes terminated."
}

UNIQUE_BEAT_IDENTIFIER="src.backend.server.configurations.celery_conf beat"
UNIQUE_WORKER_IDENTIFIER="src.backend.server.configurations.celery_conf worker"

terminate_process "$UNIQUE_BEAT_IDENTIFIER"
terminate_process "$UNIQUE_WORKER_IDENTIFIER"

if [ -f ./celerybeat-schedule ]; then
  echo "Removing celerybeat schedule file..."
  rm ./celerybeat-schedule
fi
