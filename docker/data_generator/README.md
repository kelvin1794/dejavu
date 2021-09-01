# Docker Image for `data_generator`

This image is build upon [`python:3.7-slim-buster`](https://github.com/docker-library/python/blob/b59ce53e3213c9717177fe9a4f25f3e3ffeba56e/3.7/buster/slim/Dockerfile). It includes 2 custom files:

- [`transaction_generator.py`](./transaction_generator.py) that generates dummy transactions data and streams to the Kafka container
- [`wait_for_kafka.sh`](./wait_for_kafka.sh) which is a workaround to wait for the Kafka container to get ready before streaming

## Usage

- To build the image, run `./build.sh`
- To push the image, run `./push.sh`. Currently it's pushing to my Docker Hub, but feel free to change the tag.
