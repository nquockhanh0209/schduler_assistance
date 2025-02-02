# syntax=docker/dockerfile:1.3
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive \
    USER=root

ENV TZ=Asia/Ho_Chi_Minh

RUN apt-get update
RUN apt-get install -y python3-dev \
                        git \
                        python-dev \
                        python3 \
                        python3-pip \
                        python3.8-dev \
                        cmake \
                        g++ \
                        build-essential

COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

COPY . /app
WORKDIR /app
