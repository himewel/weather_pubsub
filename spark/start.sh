#!/usr/bin/env bash

SCRIPT=$1
BROKER_HOST=$2
BROKER_PORT=$3

echo "Waiting kafka broker to launch on $BROKER_HOST:$BROKER_PORT..."
while ! nc -z $BROKER_HOST $BROKER_PORT; do
    sleep 1
done

spark-submit \
    --class org.apache.spark.examples.SparkPi \
    --master local \
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 \
    $SCRIPT
