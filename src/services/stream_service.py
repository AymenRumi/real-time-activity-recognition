import pandas as pd
from confluent_kafka import Producer

from src.config import KafkaSettings


class HumanActivitySensor:
    def __init__(self):

        self.data_connection = None
        self.kafka_producer = None

    def __connect_to_source(self):
        self.data_connection = pd.read_df("../data/human_activity.csv")

    def __connect_to_kafka(self):
        settings = KafkaSettings()

        conf = {
            "bootstrap.servers": settings.bootstrap_servers,
            "client.id": settings.client_id,
        }
        self.kafka_producer = Producer(conf)

    def start_sensor_stream(self):

        """
        while:
            push_to_topic



        """
