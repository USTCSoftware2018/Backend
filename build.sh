#!/usr/bin/env bash
IMAGE_NAME=biohub_api
docker rmi $IMAGE_NAME
docker build -t $IMAGE_NAME . --no-cache