import json

import numpy as np
from pyflink.common import Configuration
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.datastream.connectors import FlinkKafkaConsumer

from src.config import FlinkSettings, KafkaSettings


class FlinkJob:
    def __init__(self):

        self.env = None

        self.__set_stream_env()

        self.kafka_settings = KafkaSettings()
        self.flink_settings = FlinkSettings()

        self.conf = {
            "bootstrap.servers": self.kafka_settings.KAFKA_BOOTSTRAP_SERVER,
            "client.id": self.kafka_settings.KAFKA_CLIENT_ID,
        }

    @staticmethod
    def to_numpy_array(data_points):
        return np.array(data_points)

    @staticmethod
    def window_function(window, values):

        data_points = [json.loads(value) for value in values]
        return FlinkJob.to_numpy_array(data_points)

    def __set_stream_env(self) -> None:
        config = Configuration()
        config.set_string("jobmanager.rpc.address", "jobmanager")
        config.set_string("jobmanager.rpc.port", self.flink_settings.FLINK_SERVER)
        self.env = StreamExecutionEnvironment.get_execution_environment(config)

        self.env.set_stream_time_characteristic(TimeCharacteristic.ProcessingTime)

    def start_job(self):
        kafka_source = FlinkKafkaConsumer(
            topics=self.kafka_settings.KAFKA_CLIENT_ID,
            deserialization_schema=SimpleStringSchema(),
            properties=self.conf,
        )

        data_stream = self.env.add_source(kafka_source)

        # TODO: Process stream data, feed into ML model

        self.env.execute("Flink Kafka Streaming Job")
