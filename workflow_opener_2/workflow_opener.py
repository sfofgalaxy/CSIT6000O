#!/usr/bin/env python
import json

import pika
import requests

# RabbitMQ configuration
MQ_KEY = "hkust"
MQ_SECRET = "csit6000o"
MQ_HOST = "rabbitmq"
MQ_PORT = 5672
QUEUE = "markdown"
EXCHANGE = "amq.direct"
ROUTING_KEY = "markdown"
# OpenFaaS configuration
OF_HOST = "faas"
OF_PORT = "60000"
URL = "http://{}:{}/".format(OF_HOST, OF_PORT)


def callback(c_channel, method_frame, header_frame, body):
    body = str(body, "utf-8")
    data = json.loads(body)["Key"].replace("markdown/", "")
    c_channel.basic_ack(delivery_tag=method_frame.delivery_tag)
    payload = {"url": "{}".format(data)}

    requests.post(URL + "conversion", data=payload)
    requests.post(URL + "sentiment", data=payload)


# # Step #1: Connect to RabbitMQ using the default parameters
credentials = pika.PlainCredentials(MQ_KEY, MQ_SECRET)
parameters = pika.ConnectionParameters(
    host=MQ_HOST, port=MQ_PORT, virtual_host="/", credentials=credentials
)
connection = pika.BlockingConnection(parameters=parameters)
channel = connection.channel()

result = channel.queue_declare(queue=QUEUE, durable=True)
channel.exchange_declare(exchange=EXCHANGE, durable=True, exchange_type="direct")
channel.queue_bind(
    exchange=EXCHANGE, queue=result.method.queue, routing_key=ROUTING_KEY
)
channel.basic_consume(QUEUE, callback)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
