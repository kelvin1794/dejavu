#! /bin/bash
# Build docker image and tag with the preset version

set -xue
cd $(dirname $0)

VERSION=${1-$(cat ../VERSION)}
docker build --build-arg FLINK_VERSION=${VERSION} -t dejareve .
