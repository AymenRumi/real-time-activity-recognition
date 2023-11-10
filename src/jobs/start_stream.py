from src.services.stream_service import HumanActivitySensor as sensor

if __name__ == "__main__":
    sensor().start_stream()
