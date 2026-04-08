from confluent_kafka import Producer
from abc import ABC, abstractmethod


class ProducerABC(ABC): 
    @abstractmethod
    def send(self, key, value):
        pass

class KafkaProducer(ProducerABC):
    def __init__(self, producer: Producer, topic: str):
        self.producer = producer
        self.topic = topic

    def send(self, key, value):
        self.producer.produce(topic=self.topic, key=key, value=value)
        self.producer.flush()   