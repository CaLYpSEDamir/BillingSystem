from typing import List

from kafka.admin import KafkaAdminClient, NewTopic

from app.settings import broker_config

admin_client = KafkaAdminClient(
    bootstrap_servers=f'{broker_config.broker_host}:{broker_config.broker_port}',
    client_id=broker_config.client_id,
)


def create_topic():
    """Creating topic in broker."""
    print(f'Starting creating topic {broker_config.topic_name}')

    topic_name = broker_config.topic_name
    exist_topics = admin_client.list_topics()

    if topic_name not in exist_topics:
        topic = NewTopic(
            name=topic_name,
            num_partitions=broker_config.topic_partition_count,
            replication_factor=1,
        )
        admin_client.create_topics(
            new_topics=[topic],
            validate_only=False,
        )
        print(f'Topic `{topic_name}` was created')
    else:
        print(f'Topic `{topic_name}` already exists.')


def delete(topics: List[str]):
    """Delete topic."""
    admin_client.delete_topics(topics)


def describe_topics(topics: List[str]):
    """Get topics descriptions."""
    print('All topics:', admin_client.list_topics())
    print(admin_client.describe_topics(topics))
