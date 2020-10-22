ARG BUILD_FROM=homeassistant/amd64-base-python:3.9-alpine3.12
FROM $BUILD_FROM

ENV LANG C.UTF-8

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN apk add --no-cache --virtual .build-deps build-base libffi-dev openssl-dev && \
    python -m pip install poetry>=1.1.0 && \
    poetry config virtualenvs.in-project true && \
    poetry install --no-dev -v && \
    apk del .build-deps

COPY start.sh /app/start.sh
ENTRYPOINT ["/app/start.sh"]

LABEL io.hass.version="VERSION" io.hass.type="addon" io.hass.arch="armhf|aarch64|i386|amd64"
