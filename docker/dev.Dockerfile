# The base image compilation
FROM python:3.10-slim AS compile-image
RUN python -m venv /karrio/venv
RUN apt-get update -y && apt-get install -y gcc
ENV PATH="/karrio/venv/bin:$PATH"
COPY . /karrio/app/
RUN cd /karrio/app && \
    pip install -r requirements.dev.txt --upgrade && \
    pip install -r requirements.server.dev.txt


# The runtime image
FROM python:3.10-slim AS build-image

RUN apt-get update -y && apt-get install -y libpango1.0-0 libpangoft2-1.0-0 gcc ghostscript
RUN useradd -m karrio -d /karrio
USER karrio
COPY --chown=karrio:karrio --from=compile-image /karrio/ /karrio/
RUN mkdir -p /karrio/.karrio

WORKDIR /karrio/app

# Make sure we use the virtualenv:
ENV PATH="/karrio/venv/bin:$PATH"
