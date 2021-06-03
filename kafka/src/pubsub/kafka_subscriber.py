import json
import logging
import os
from datetime import datetime

from kafka import KafkaConsumer


class KafkaSubscriber:
    def __init__(self, bootstrap_server=None, topic_name=None):
        env_server = os.getenv("BOOTSTRAP_SERVER")
        env_topic = os.getenv("TOPIC_NAME")

        self.bootstrap_server = bootstrap_server or env_server
        self.topic_name = topic_name or env_topic

    def subscribe(self):
        logging.info("Creating kafka consumer")
        consumer = KafkaConsumer(
            bootstrap_servers=self.bootstrap_server,
            value_deserializer=lambda m: json.loads(m.decode('ascii')),
        )
        consumer.subscribe(topics=[self.topic_name])

        for message in consumer:
            logging.info(f"New message received from {self.topic_name}")
            logging.info(f"Timestamp: {datetime.fromtimestamp(message.timestamp/1000)}")
            logging.info(f"Offset: {message.offset}")
            logging.info(f"Value: {message.value}")
