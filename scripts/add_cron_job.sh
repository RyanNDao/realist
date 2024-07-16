#!/bin/bash

# Script to add a cron job automatically 
# Note: the validation for this is a little buggy so running this multiple times may create duplicate cron jobs. only run this ONCE

# Define the cron job command
CRON_JOB="0 0 * * * /trigger_trulia_scrape_runs.sh"

# Check if the cron job already exists
crontab -l | grep -q "$CRON_JOB"

# Add the cron job if it doesn't exist
if [ $? -eq 1 ]
then
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "Cron job added: $CRON_JOB"
else
    echo "Cron job already exists"
fi
