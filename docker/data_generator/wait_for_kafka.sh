#!/bin/sh

set -e
  
until python /usr/src/app/transaction_generator.py ; do
  >&2 echo "Kafka is not yet available - sleeping..."
  sleep 3
done
  
>&2 echo "Kafka is up! - starting generator..."
exec "$@"

