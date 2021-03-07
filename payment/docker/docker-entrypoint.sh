#!/bin/sh

set -e

echo Command is: "$@"

# waiting for kafka
echo 'Start sleeping'
sleep 10
echo 'End sleeping'

if [ "$1" = 'start_server' ]; then
  exec uvicorn app.main:app --host 0.0.0.0

elif [ "$1" = 'start_consumer' ]; then
  python app/broker/consumer.py

fi
