#!/usr/bin/env bash

SCRIPT=$1
BROKER_HOST=$2
BROKER_PORT=$3

echo "Waiting kafka broker to launch on $BROKER_HOST:$BROKER_PORT..."
while ! nc -z $BROKER_HOST $BROKER_PORT; do
    sleep 1
done

python3 $SCRIPT
