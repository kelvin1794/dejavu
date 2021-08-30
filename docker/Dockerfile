###############################################################################
# Build PyFlink image on top of OpenJDK image
# More about OpenJDK: https://hub.docker.com/_/openjdk
# More about PyFlink: https://flink.apache.org/
###############################################################################

FROM openjdk:8-jdk-slim-buster
ARG FLINK_VERSION

# Install dependencies
RUN set -ex; \
    apt-get update; \
    apt-get -y install libsnappy1v5 wget build-essential; \
    rm -rf /var/lib/apt/lists/*

# Install Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    python3.7 \
    python3-pip \
    python3.7-dev \
    python3-setuptools \
    python3-wheel && \
    # Symlink python3 and pip3 to python and pip, respectively
    ln -s /usr/bin/python3 /usr/bin/python; \
    ln -s /usr/bin/pip3 /usr/bin/pip

# Install dependencies
COPY ./requirements.txt /opt
RUN set -ex; \
    apt-get update; \
    python -m pip install --upgrade pip; \
    pip install -r /opt/requirements.txt

# Install pyflink
RUN set -ex; \
    wget https://archive.apache.org/dist/flink/flink-${FLINK_VERSION}/python/apache-flink-libraries-${FLINK_VERSION}.tar.gz -P /opt \
    # Below line is optional. It's just to surpress the verbose output of wget
    -q --show-progress --progress=bar:force:noscroll; \
    python -m pip install /opt/apache-flink-libraries-${FLINK_VERSION}.tar.gz \
    rm -f /opt/apache-flink-libraries-${FLINK_VERSION}.tar.gz

RUN set -ex; \ 
    wget https://archive.apache.org/dist/flink/flink-${FLINK_VERSION}/python/apache-flink-${FLINK_VERSION}.tar.gz -P /opt \
    # Below line is optional. It's just to surpress the verbose output of wget
    -q --show-progress --progress=bar:force:noscroll; \
    python -m pip install /opt/apache-flink-${FLINK_VERSION}.tar.gz \
    rm -f /opt/apache-flink-${FLINK_VERSION}.tar.gz

# Grab gosu for easy step-down from root
ENV GOSU_VERSION 1.11
RUN set -ex; \
    wget -nv -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$(dpkg --print-architecture)"; \
    wget -nv -O /usr/local/bin/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$(dpkg --print-architecture).asc"; \
    export GNUPGHOME="$(mktemp -d)"; \
    for server in ha.pool.sks-keyservers.net $(shuf -e \
    hkp://p80.pool.sks-keyservers.net:80 \
    keyserver.ubuntu.com \
    hkp://keyserver.ubuntu.com:80 \
    pgp.mit.edu) ; do \
    gpg --batch --keyserver "$server" --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4 && break || : ; \
    done && \
    gpg --batch --verify /usr/local/bin/gosu.asc /usr/local/bin/gosu; \
    gpgconf --kill all; \
    rm -rf "$GNUPGHOME" /usr/local/bin/gosu.asc; \
    chmod +x /usr/local/bin/gosu; \
    gosu nobody true

# Prepare environment
ENV FLINK_HOME=/opt/flink
ENV PATH=$FLINK_HOME/bin:$PATH
RUN groupadd --system --gid=1000 flink && \
    useradd --system --home-dir $FLINK_HOME --uid=1000 --gid=flink flink && \
    adduser flink sudo
WORKDIR $FLINK_HOME

# Build flink from source and put it in the current folder
RUN set -ex; \ 
    wget https://archive.apache.org/dist/flink/flink-${FLINK_VERSION}/flink-${FLINK_VERSION}-bin-scala_2.11.tgz -P /opt \
    -q --show-progress --progress=bar:force:noscroll; \
    tar -xzf /opt/flink-${FLINK_VERSION}-bin-scala_2.11.tgz -C /opt; \
    cp -a /opt/flink-${FLINK_VERSION}/. /opt/flink

# Also put Kafka, Json jars into the flink lib folder
RUN wget -P /opt/flink/lib/ -q --show-progress --progress=bar:force:noscroll \
    https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-kafka_2.11/${FLINK_VERSION}/flink-sql-connector-kafka_2.11-${FLINK_VERSION}.jar

# Configure container
COPY docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
EXPOSE 6123 8081
CMD ["help"]
