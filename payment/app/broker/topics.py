from typing import List

from kafka.admin import KafkaAdminClient, NewTopic

CLIENT_ID = 'payment'
KAFKA_INSTANCE = "kafka:9092"
# KAFKA_INSTANCE = "localhost:9092"

# fixme needs settings

admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_INSTANCE,
        client_id=CLIENT_ID,
    )


def get_topic_name():
    """Get topic name from settings."""
    topic_name = 'addition'
    return topic_name


def create_topic():
    """Creating topic in broker."""

    print('Starting creating topic')
    topic_name = get_topic_name()
    exist_topics = admin_client.list_topics()

    if topic_name not in exist_topics:
        topic = NewTopic(
                name=topic_name,
                num_partitions=2,
                replication_factor=1,
            )
        admin_client.create_topics(
            new_topics=[topic],
            timeout_ms=3000,
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
    print('', admin_client.describe_topics(topics))


# if __name__ == '__main__':
#     pass
#     delete([get_topic_name()])
#     describe_topics([get_topic_name()])
