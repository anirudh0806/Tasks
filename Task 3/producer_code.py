import time
import json
import random
from datetime import datetime
from data_generator import generate_message
from kafka import KafkaProducer
import redis

def serializer(message):
    """
    Serializing a message as JSON.

    """
    return json.dumps(message).encode('utf-8')

def main():
    """
    Kafka Producer that is used to generate and send messages to a Kafka topic.
    """
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],
        value_serializer=serializer
    )

    count = 0
    # Running the loop till 10 messages are produced
    while count < 10:
        dummy_message = generate_message()
        count += 1

        print(f'Producing message @ {datetime.now()} with Message = {str(dummy_message)}')
        producer.send('messages', dummy_message)

        # Ensuring gap between message production
        time_to_sleep = random.randint(1, 11)
        time.sleep(time_to_sleep)

if __name__ == '__main__':
    main()
