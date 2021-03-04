#!/bin/sh

set -e

echo Command is: "$@"

if [ "$1" = 'start_server' ]; then
  echo 'Starting server 0.0.0.0:8000'
fi
