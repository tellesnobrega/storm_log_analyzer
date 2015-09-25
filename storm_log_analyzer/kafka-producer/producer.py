from kafka import SimpleProducer, KafkaClient
import json

# To send messages synchronously
kafka = KafkaClient('localhost:9092')
producer = SimpleProducer(kafka)

# Note that the application is responsible for encoding messages to type bytes
with open('../../sahara-all-small.log', 'r') as f:
    for line in f:
        producer.send_messages(b'logs', b'%s' % line)

