from pydantic import BaseSettings


class DBSettings(BaseSettings):
    """Database settings."""
    postgres_host: str = 'postgres'
    postgres_port: int = 5432
    postgres_db: str
    postgres_user: str
    postgres_password: str
    pool_min_size: int = 5
    pool_max_size: int = 10


class BrokerSettings(BaseSettings):
    """Message broker settings."""
    broker_host: str = 'kafka'
    broker_port: int = 9092
    topic_partition_count: int = 1
    topic_name: str
    client_id: str
    consumer_group_id: str


db_config = DBSettings()
broker_config = BrokerSettings()
