SHELL:= /bin/bash
PROJECT:= dejareve
BASE_DIR=$(shell pwd)
VERSION=`cat VERSION`

target:
	$(info ${HELP_MESSAGE})
	@exit 0

all: destroy install test

destroy:  # => Delete current & latest build
	$(info[*] Who needs all that anyway? Destroying...)
	deactivate || true
	find . -type d -name '*pycache*' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm --force {} \;
	rm -rf .venv

install:
	$(info[+] Installing dependencies...")
	python -m venv .venv
	.venv/bin/pip install -U -r docker/requirements.txt
	wget https://archive.apache.org/dist/flink/flink-${VERSION}/python/apache-flink-libraries-${VERSION}.tar.gz -P /tmp
	.venv/bin/pip install /tmp/apache-flink-libraries-${VERSION}.tar.gz
	rm /tmp/apache-flink-libraries-${VERSION}.tar.gz
	wget https://archive.apache.org/dist/flink/flink-${VERSION}/python/apache-flink-${VERSION}.tar.gz -P /tmp
	.venv/bin/pip install /tmp/apache-flink-${VERSION}.tar.gz
	rm /tmp/apache-flink-${VERSION}.tar.gz

test:
	$(info[+] Executing tests...")
	source .venv/bin/activate
	PYTHONPATH=${PYTHONPATH}:${BASE_DIR}/app:${BASE_DIR}/tests python -m unittest discover -v -s tests

define HELP_MESSAGE
Usage:
	...::: Installs all required packages :::...
	$ make install

	...::: Destroys up the environment - Deletes Virtualenv and data :::...
	$ make destroy

	...::: Execute project tests :::...
	$ make test
endef
