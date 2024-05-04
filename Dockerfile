FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt
COPY . /app

RUN apt-get update && \
    apt-get install -y gcc make python3-dev

RUN pip3 install TgCrypto

