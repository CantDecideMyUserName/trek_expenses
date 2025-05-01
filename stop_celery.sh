#!/bin/bash
# Script to stop Celery worker and beat processes

echo "Stopping Celery worker and beat..."
pkill -f 'celery worker'
pkill -f 'celery beat'
echo "Celery processes stopped."