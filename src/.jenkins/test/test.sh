#!/usr/bin/env bash

set -u # crash on missing env
set -e # stop on any error

echo "Waiting for db"
source .jenkins/docker-wait.sh
source .jenkins/docker-migrate.sh

# echo "Running style checks"
# flake8 --config=./flake.cfg ./ds_demo

echo "Running unit tests"
python ./manage.py test
