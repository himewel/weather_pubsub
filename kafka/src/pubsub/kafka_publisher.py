import json
import logging
import os
import time
from datetime import datetime

from kafka import KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError, TopicAlreadyExistsError


class KafkaPublisher:
    def __init__(self, bootstrap_server=None, topic_name=None):
        env_server = os.getenv("BOOTSTRAP_SERVER")
        env_topic = os.getenv("TOPIC_NAME")

        self.bootstrap_server = bootstrap_server or env_server
        self.topic_name = topic_name or env_topic

    def create_topic(self):
        logging.info(f"Creating new kafka topic {self.topic_name}")
        client = KafkaAdminClient(bootstrap_servers=self.bootstrap_server)
        topic = NewTopic(
            name=self.topic_name,
            num_partitions=1,
            replication_factor=1,
        )

        try:
            client.create_topics(new_topics=[topic])
            logging.info("Kafka topic created")
        except TopicAlreadyExistsError:
            logging.info("Kafka topic already exists")

    def publish(self, data_list):
        logging.info("Creating kafka producer")
        producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_server,
            value_serializer=lambda m: json.dumps(m).encode('ascii'),
        )

        index = 0
        while index < len(data_list) and data_list:
            logging.info("Sending new message")
            data = data_list[index]
            response = producer.send(topic=self.topic_name, value=data)

            try:
                record_metadata = response.get(timeout=10)
                timestamp = datetime.fromtimestamp(record_metadata.timestamp / 1000)
                logging.info(f"Timestamp: {timestamp}")
                logging.info(f"Offset: {record_metadata.offset}")

                index += 1
            except KafkaError as e:
                logging.exception(e)

            logging.info("Waiting a few seconds to a new try...")
            time.sleep(30)
