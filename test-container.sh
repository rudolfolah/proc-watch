#!/bin/bash

echo "Building Docker image..."
docker build -t proc-watch .

echo "Running container..."
docker run -d --name proc-watch-test proc-watch

echo "Waiting for container to start..."
sleep 10

echo "Checking container status..."
docker ps -f name=proc-watch-test

echo "Checking health status..."
docker inspect --format='{{.State.Health.Status}}' proc-watch-test

echo "Checking metrics file..."
docker exec proc-watch-test ls -la /app/metrics/

echo "Viewing metrics content..."
docker exec proc-watch-test cat /app/metrics/proc_watch.prom

echo "Checking container logs..."
docker logs proc-watch-test --tail 10

echo "Cleaning up..."
docker stop proc-watch-test
docker rm proc-watch-test