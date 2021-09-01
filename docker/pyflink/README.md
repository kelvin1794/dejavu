# Docker Image for PyFlink

This image is created from OpenJDK 8 with Flink and PyFlink installed on top of it.

- [OpenJDK](https://hub.docker.com/_/openjdk)
- [Flink](https://flink.apache.org/)
- [PyFlink](https://ci.apache.org/projects/flink/flink-docs-master/docs/dev/python/overview/)

In general, it start with the base of OpenJDK and install Flink and PyFlink and some other utilities such as `gosu` to step down from `root`.

- To build the image, run `./build.sh`
- To push the image, run `./push.sh`. Currently it's pushing to my Docker Hub, but feel free to change the tag.
