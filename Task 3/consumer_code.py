import json 
from kafka import KafkaConsumer
import redis


if __name__ == '__main__':
   
    """
    Kafka Consumer that reads messages, stores them in Redis, and retrieves them.
    """
    # Kafka Consumer
    consumer = KafkaConsumer(
        'messages',
        bootstrap_servers='localhost:9092',
        
    )
    
    k = 0

    for message in consumer:
        key_val = 'message' + str(k)
        k += 1
        
        
        # Parse and print the JSON message
        parsed_message = json.loads(message.value)
        print(parsed_message)
        
        # Connect to the Redis server
        r = redis.Redis(host='localhost', port=6379, db=0)
        
        # Store the message in Redis
        r.set(key_val, message.value)
        
        # Retrieve and print the message from Redis
        stored_message = r.get(key_val)
        print(stored_message)