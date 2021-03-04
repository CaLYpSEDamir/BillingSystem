from kafka.admin import KafkaAdminClient


CLIENT_ID = 'payment'
KAFKA_INSTANCE = "localhost:9092"

admin_client = KafkaAdminClient(
        bootstrap_servers=KAFKA_INSTANCE,
        client_id=CLIENT_ID,
    )


def delete(topics):
    admin_client.delete_topics(topics)


topics = admin_client.list_topics()
print(topics)

delete(['addition'])

print(admin_client.describe_topics(['addition']))
