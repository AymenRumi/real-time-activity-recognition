from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    KAFKA_BOOTSTRAP_SERVER: str
    KAFKA_CLIENT_ID: str
    KAFKA_DATA_SOURCE: str


class FlinkSettings(BaseSettings):
    FLINK_SERVER: str


# class MLFlowSettings(BaseSettings):
#     server: str = Field(None, env="MLFLOW_SERVER")
