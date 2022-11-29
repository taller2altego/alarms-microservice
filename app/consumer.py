#!/usr/bin/env python
import os
import sys
import json
import statsd
from confluent_kafka import Consumer, KafkaException, KafkaError

if __name__ == '__main__':
    print('Start metrics microservice')
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
    stat = statsd.StatsClient('localhost', 8125)

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
                    stat.incr(res['metricName'])
                    print('logged metric')
                except Exception:
                    print('failed processing metric')

    except KeyboardInterrupt:
        sys.stderr.write('%% Aborted by user\n')
    except Exception as err:
        print(err)

    c.close()
