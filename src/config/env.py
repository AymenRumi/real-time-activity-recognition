from pydantic import Base, Field


class KafkaSettings(Base):
    bootstrap_servers: str = Field(None, env="KAFKA_BOOTSTRAP_SERVER")
    client_id: str = Field(None, env="KAFKA_CLIENT_ID")


class FlinkSettings(Base):
    server: str = Field(None, env="FLINK_SERVER")


class MLFlowSettings(Base):
    server: str = Field(None, env="MLFLOW_SERVER")
