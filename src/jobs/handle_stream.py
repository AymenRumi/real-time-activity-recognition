from src.services.recognition_service import RealTimeRecognition as activity_recognition

if __name__ == "__main__":
    activity_recognition().read_sensor_stream()
