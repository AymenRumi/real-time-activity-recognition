from confluent_kafka import Consumer, KafkaError

from src.config import KafkaSettings
from src.services.sensor_service import decode_sensor_data, read_buffer

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
            "auto.offset.reset": "earliest",  # Start from the earliest messages
            "enable.auto.commit": True,
        }
        self.kafka_consumer = Consumer(conf)
        self.kafka_consumer.subscribe([self.settings.KAFKA_CLIENT_ID])

    def load_model_from_regsistry(self):
        pass

    def predict_activity(self):
        pass

    def read_sensor_stream(self):
        # Initialize an empty list as the buffer
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

                # Decode and load the message
                message_value = decode_sensor_data(sensor_data.value())

                # Add the message to the buffer
                buffer.append(message_value)

                # Maintain the buffer size to the last 10 messages
                if len(buffer) > WINDOW_SIZE:
                    buffer.pop(0)  # Remove the oldest message

                # Optional: Print the type of the message or other processing
                print(read_buffer(buffer).size())
                print("")

        except KeyboardInterrupt:
            pass
        finally:
            # Close down consumer to commit final offsets.
            self.kafka_consumer.close()
