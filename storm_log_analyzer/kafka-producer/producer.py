from kafka import SimpleProducer, KafkaClient
import json

# To send messages synchronously
kafka = KafkaClient('localhost:9092')
producer = SimpleProducer(kafka)

# Note that the application is responsible for encoding messages to type bytes
while True:
    producer.send_messages(b'teste', b'mensagem dividida')

