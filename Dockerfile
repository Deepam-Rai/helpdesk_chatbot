FROM python:3.8-slim AS base

RUN apt-get update \
    && apt-get --assume-yes --no-install-recommends install \
        build-essential \
        curl \
        git \
        jp \
        libgomp1 \
        vim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install requests
RUN pip install rasa==3.4.0
RUN pip install websocket-client==1.6.1
RUN pip install websockets==10.0
RUN pip install rasa[spacy]
RUN python -m spacy download en_core_web_md
RUN pip install prettytable
# COPY . /app/
# COPY ./actions /app/actions
