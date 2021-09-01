#! /bin/bash
# Build docker image and tag with the preset version

set -xue
cd $(dirname $0)

docker build -t data_generator .
