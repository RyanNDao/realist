#!/bin/bash

pkill -SIGTERM -f 'celery -A src.backend.server.configurations.celery_conf beat'
pkill -SIGTERM -f 'celery -A src.backend.server.configurations.celery_conf worker'

echo "Waiting for Celery processes to terminate gracefully..."
sleep 30

pkill -9 -f 'celery -A src.backend.server.configurations.celery_conf beat'
pkill -9 -f 'celery -A src.backend.server.configurations.celery_conf worker'

echo "Celery processes stopped"
