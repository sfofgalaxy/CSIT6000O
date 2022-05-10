import pika
import time
from minio_client import MINIO_CLIENT

MQ_KEY = 'hkust'
MQ_SECRET = 'csit6000o'
MQ_HOST = 'rabbitmq'
MQ_PORT = '5672'
QUEUE = 'markdown'
credentials = pika.PlainCredentials(MQ_KEY, MQ_SECRET)
parameters = pika.ConnectionParameters(host=MQ_HOST, port=MQ_PORT, virtual_host='/', credentials=credentials)
connection = pika.BlockingConnection(parameters = parameters)
channel = connection.channel()  
channel.queue_declare(queue=QUEUE, durable=True)

files = set()
while True:
    client = MINIO_CLIENT()
    new_files = set(client.list_files())
    s = new_files.difference(files)
    for name in s:
        channel.basic_publish(exchange='',routing_key=QUEUE,body=name) 
    files = new_files
    time.sleep(5)  # 暂停5秒

