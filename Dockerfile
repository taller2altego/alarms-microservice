FROM ubuntu:18.04
COPY . /app
WORKDIR /app
RUN apt-get update && apt-get install -y apt-transport-https
RUN apt-get install -qy build-essential wget gettext-base
RUN apt-get install -qy python3.8 python3.8-dev python3.8-venv python3-distutils
RUN apt-get install libssl-dev
RUN yes | apt-get librdkafka-dev
RUN pip install -r requirements.txt
RUN python3.8 consumer.py