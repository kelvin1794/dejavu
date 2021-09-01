#! /bin/bash
# Push docker image to Docker Hub

set -xue
cd $(dirname $0)

TAG=${1-$(cat ../VERSION)}
IMAGE=dejareve:${TAG}

docker tag \
    $IMAGE \
    knguyen1794/$IMAGE

docker push knguyen1794/$IMAGE
