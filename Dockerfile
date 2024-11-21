FROM python:3.11.9-slim-bookworm as base
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN mkdir /points_collection

WORKDIR /points_collection

FROM base as runtime-image

COPY requirements.txt  /points_collection/
RUN apt-get update && apt-get -y upgrade \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && playwright install --with-deps chromium \
    && apt-get clean 

COPY . /points_collection
