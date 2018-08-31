#!/usr/bin/env bash
NAME=biohub_api
MIGRATE_NAME=biohub_api_migrate
IMAGE_NAME=biohub_api
APP_DIR=$(cd `dirname $0`; pwd)/biohub

# migrate
docker stop ${MIGRATE_NAME} && docker rm ${MIGRATE_NAME}
docker run -d \
  -e MODULE=${NAME} \
  -v ${APP_DIR}:/code \
  --name ${MIGRATE_NAME} \
  ${IMAGE_NAME} \
  python3 manage.py migrate

# api server
docker stop ${NAME} && docker rm ${NAME}
docker run -d \
  -p 8000:8000 \
  -e MODULE=${NAME} \
  -v ${APP_DIR}:/code \
  --name ${NAME} \
  ${IMAGE_NAME}