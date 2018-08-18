#!/usr/bin/env bash
IMAGE_NAME=ustc_igem_api
docker rmi $IMAGE_NAME
docker build -t $IMAGE_NAME . --no-cache