import torch
from confluent_kafka import Consumer, KafkaError

from src.config import KafkaSettings
from src.mlflow.model import ConvNN
from src.services.ml_service import logit_to_activity
from src.services.sensor_service import decode_sensor_data, read_buffer
from src.utils.logging import logger

WINDOW_SIZE = 7


class RealTimeRecognition:
    def __init__(self):

        self.kafka_consumer = None
        self.settings = KafkaSettings()

        self.model = self.load_model_from_registry()

        self.__connect_to_kafka()

    def __connect_to_kafka(self) -> None:

        conf = {
            "bootstrap.servers": self.settings.KAFKA_BOOTSTRAP_SERVER,
            "group.id": "mygroup",  # Consumer group ID
            "auto.offset.reset": "latest",  # Start from the latest
            "enable.auto.commit": True,
        }
        self.kafka_consumer = Consumer(conf)
        self.kafka_consumer.subscribe([self.settings.KAFKA_CLIENT_ID])

    def __tensor(self, buffer):
        return buffer.unsqueeze(0).unsqueeze(0).float()

    def load_model_from_registry(self):

        logger.info("Initializing Model:")
        model = ConvNN()

        model.load_state_dict(torch.load("checkpoint.pth")["model_state_dict"])
        logger.info(model)
        model.eval()

        return model

    def predict_activity(self, buffer):
        with torch.no_grad():
            return logit_to_activity(self.model(self.__tensor(buffer)))

    def read_sensor_stream(self):
        # Initialize an empty list as the buffer

        if not self.model:
            raise Exception("No Model")
        buffer = []

        try:
            while True:
                sensor_data = self.kafka_consumer.poll(1.0)  # Poll for messages

                if sensor_data is None:
                    continue
                if sensor_data.error():
                    if sensor_data.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(sensor_data.error())
                        break

                data = decode_sensor_data(sensor_data.value())

                buffer.append(data)

                if len(buffer) > WINDOW_SIZE:
                    buffer.pop(0)

                # print(read_buffer(buffer))

                if len(buffer) == WINDOW_SIZE:
                    logger.task((self.predict_activity(read_buffer(buffer))))

        except KeyboardInterrupt:
            pass
        finally:
            # Close down consumer to commit final offsets.
            self.kafka_consumer.close()
