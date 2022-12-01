FROM ubuntu:18.04
COPY . /app
WORKDIR /app

RUN apt-get update
RUN apt-get install -y apt-transport-https gpg gpg-agent curl ca-certificates librdkafka-dev libssl-dev
RUN apt-get install -qy build-essential wget gettext-base python3.8 python3.8-dev python3.8-venv python3-distutils

# Add Datadog repository and signing keys
ENV DATADOG_APT_KEYRING="/usr/share/keyrings/datadog-archive-keyring.gpg"
ENV DATADOG_APT_KEYS_URL="https://keys.datadoghq.com"
RUN sh -c "echo 'deb [signed-by=${DATADOG_APT_KEYRING}] https://apt.datadoghq.com/ stable 7' > /etc/apt/sources.list.d/datadog.list"
RUN touch ${DATADOG_APT_KEYRING}

RUN curl -o /tmp/DATADOG_APT_KEY_CURRENT.public "${DATADOG_APT_KEYS_URL}/DATADOG_APT_KEY_CURRENT.public" && gpg --ignore-time-conflict --no-default-keyring --keyring ${DATADOG_APT_KEYRING} --import /tmp/DATADOG_APT_KEY_CURRENT.public
RUN curl -o /tmp/DATADOG_APT_KEY_F14F620E.public "${DATADOG_APT_KEYS_URL}/DATADOG_APT_KEY_F14F620E.public" && gpg --ignore-time-conflict --no-default-keyring --keyring ${DATADOG_APT_KEYRING} --import /tmp/DATADOG_APT_KEY_F14F620E.public
RUN curl -o /tmp/DATADOG_APT_KEY_382E94DE.public "${DATADOG_APT_KEYS_URL}/DATADOG_APT_KEY_382E94DE.public" && gpg --ignore-time-conflict --no-default-keyring --keyring ${DATADOG_APT_KEYRING} --import /tmp/DATADOG_APT_KEY_382E94DE.public

# Install the Datadog agent
RUN apt-get update && apt-get -y --force-yes install --reinstall datadog-agent

# python dependencies
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3.8 get-pip.py
RUN pip install -r requirements.txt

# Copy entrypoint
COPY heroku/heroku-entrypoint.sh ./

# Expose DogStatsD and trace-agent ports
EXPOSE 8125/udp 8126/tcp
ENV DD_APM_ENABLED=true
# Copy your Datadog configuration
COPY heroku/datadog-config/ /etc/datadog-agent/

CMD ["/entrypoint.sh"]

CMD ["bash", "heroku-entrypoint.sh"]
