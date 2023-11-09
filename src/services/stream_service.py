import json

import pandas as pd
from confluent_kafka import Producer

from src.config import KafkaSettings
from src.utils import logger


class HumanActivitySensor:
    def __init__(self):

        self.data_source = None
        self.kafka_producer = None

        self.settings = KafkaSettings()

        self.__connect_to_source()
        self.__connect_to_kafka()

    def __connect_to_source(self):
        self.data_source = pd.read_csv(self.settings.KAFKA_DATA_SOURCE).drop(
            columns=["rn"]
        )

    def __connect_to_kafka(self) -> None:

        conf = {
            "bootstrap.servers": self.settings.KAFKA_BOOTSTRAP_SERVER,
            "client.id": self.settings.KAFKA_CLIENT_ID,
        }

        self.kafka_producer = Producer(conf)

    def __push_sensor_data(self, data: bytes) -> None:
        self.kafka_producer.produce(
            self.settings.KAFKA_CLIENT_ID, value=data, callback=self.__delivery_report
        )
        self.kafka_producer.poll(0)

    def __delivery_report(self, err, msg):
        if err is not None:
            logger.warning(f"Message delivery failed: {err}")
        else:
            logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def start_stream(self):

        i = 0
        rows = len(self.data_source)
        while True:
            self.__push_sensor_data(
                json.dumps(self.data_source.iloc[i % rows].to_dict()).encode("utf-8")
            )
            self.kafka_producer.flush()
            i += 1
