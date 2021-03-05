from kafka.admin import KafkaAdminClient, NewTopic

CLIENT_ID = 'payment'
KAFKA_INSTANCE = "localhost:9092"
ADD_TOPIC = 'addition'
ADD_TOPIC_PARTITIONS = 2


def create_topics():
    """"""
    admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_INSTANCE,
        client_id=CLIENT_ID,
    )

    to_create_topics = []
    exist_topics = admin_client.list_topics()

    if ADD_TOPIC not in exist_topics:
        to_create_topics.append(
            NewTopic(
                name=ADD_TOPIC,
                num_partitions=ADD_TOPIC_PARTITIONS,
                replication_factor=1,
            )
        )
    else:
        print('Addition topic exists')

    admin_client.create_topics(
        new_topics=to_create_topics,
        validate_only=False,
    )
