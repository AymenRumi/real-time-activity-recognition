from src.services.flink_service import FlinkJob

if __name__ == "__main__":

    flink_job = FlinkJob()
    flink_job.start_job()
