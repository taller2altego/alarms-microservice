FROM ubuntu:18.04
COPY . /app
WORKDIR /app
RUN apt-get update
RUN apt-get install -qy build-essential wget gettext-base
RUN apt-get install -qy python3.8 python3.8-dev python3.8-venv python3-distutils
RUN apt-get install libssl-dev
RUN apt-get apt-transport-https
RUN yes | apt-get librdkafka-dev
RUN pip install -r requirements.txt
RUN python3.8 consumer.py