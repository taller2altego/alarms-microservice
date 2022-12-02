#!/usr/bin/env python
import os
import sys
import json
import requests
from confluent_kafka import Consumer, KafkaException, KafkaError
from datadog import initialize, statsd

if __name__ == '__main__':
    print('Start metrics microservice')
    r = requests.get('https://altego-fiuber-apigateway.herokuapp.com/')

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gettingstarted.settings")
    topics = ['oqgbz3ul-metrics', 'oqgbz3ul-default']

    conf = {
        'bootstrap.servers': 'dory-01.srvs.cloudkafka.com:9094,dory-02.srvs.cloudkafka.com:9094,dory-03.srvs.cloudkafka.com:9094',
        'group.id': 'cloudkarafka-example',
        'session.timeout.ms': 6000,
        'default.topic.config': {'auto.offset.reset': 'smallest'},
        'security.protocol': 'SASL_SSL',
	    'sasl.mechanisms': 'SCRAM-SHA-256',
        'sasl.username': 'oqgbz3ul',
        'sasl.password': 'iaF7T41JyBkHHiR-Y4pMp9s9u_bhCbvb'
    }

    c = Consumer(**conf)
    c.subscribe(topics)

    options = {
        'statsd_host':'127.0.0.1',
        'statsd_port':8125
    }
    initialize(**options)

    try:
        while True:
            msg = c.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' % (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                try:
                    res = json.loads(msg.value().decode())
                    metricName = res['metricName']
                    print(metricName)
                    
                    statsd.increment(metricName)
                    print('logged metric')
                except Exception:
                    print('failed processing metric')

    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')
    except Exception as err:
        print(err)

    c.close()
