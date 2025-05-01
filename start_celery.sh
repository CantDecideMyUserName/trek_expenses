#!/bin/bash
# Script to start Celery worker and beat for clients app

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Navigate to the project directory (where manage.py is)
cd "$SCRIPT_DIR"

# Create logs directory if it doesn't exist
mkdir -p logs

# Start Celery worker
echo "Starting Celery worker..."
celery -A clients worker -l info --logfile=logs/celery-worker.log --detach

# Start Celery beat
echo "Starting Celery beat..."
celery -A clients beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler --logfile=logs/celery-beat.log --detach

echo "Celery worker and beat started successfully!"
echo "Check logs in the 'logs' directory for details."