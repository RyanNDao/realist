#!/bin/bash

script_name=$(basename "$0")  # Gets the name of the current script

# Step 1: Find all gunicorn processes and count them
gunicorn_pids=$(pgrep -af "gunicorn" | grep -v "$script_name" | wc -l)

echo "Number of gunicorn processes running: $gunicorn_pids"

# Step 2: Kill all gunicorn processes if any
if [ "$gunicorn_pids" -gt 0 ]; then
    echo "Killing all gunicorn processes..."
    pgrep -af "gunicorn" | grep -v "$script_name" | cut -d ' ' -f 1 | xargs kill

    # Wait a bit for processes to terminate
    sleep 2

    # Step 3: Verify that all gunicorn processes have been killed
    new_count=$(pgrep -af "gunicorn" | grep -v "$script_name" | wc -l)
    if [ "$new_count" -eq 0 ]; then
        echo "All gunicorn processes have been successfully terminated."
    else
        echo "Failed to kill all gunicorn processes. Remaining processes: $new_count"
    fi
else
    echo "No gunicorn processes are running."
fi
