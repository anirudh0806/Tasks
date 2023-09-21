from kafka import KafkaConsumer
import json
import redis

# Create a KafkaConsumer for the 'secondtask' topic
consumer = KafkaConsumer('secondtask', bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))

# Print a message to indicate that the consumer is ready
print('Consumer is ready')

k = 0

for message in consumer:
    """
    Consume messages from the 'secondtask' Kafka topic,
    extract a specific field, and store it in Redis.

    :param message: The Kafka message.
    """
    key_val = 'val' + str(k)
    k = k + 1

    # Prints the entire message
    print("Consumer records:\n")
    print(message)

    # Prints a specific field from the message (adjust index as needed). 6th index contains the message.
    print(message[6])

    # Connects to the Redis server
    r = redis.Redis(host='localhost', port=6379, db=0)

    # Stores the specific field from the message in Redis with the key such as 'val0','val1' and so on
    r.set(key_val, json.dumps(message[6]))
