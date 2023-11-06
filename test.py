from src.services.stream_service import HumanActivitySensor

if __name__ == "__main__":

    sensor = HumanActivitySensor()

    sensor.start_stream()
