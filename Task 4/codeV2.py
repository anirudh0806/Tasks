import requests
import shutil
from kafka import KafkaConsumer
import json
import redis
from PIL import Image

def process_image_message(message, counter):
    """
    Processes a Kafka message containing image information, downloads the image,
    resizes it, and stores it in Redis.

    """

    # Extract relevant information from the message
    url = message[6]["image_url"]
    file_name = "newfile.jpg"
    dimension = message[6]["output_size"]
    new_file_loc = "test\newfile-resized.jpeg"

    res = requests.get(url, stream=True)

    # Download the image
    if res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image successfully downloaded:', file_name)
    else:
        print('Image Couldn\'t be retrieved')
        return None

    
    # Open and resize the image
    image = Image.open('newfile.jpg')
    print(f"Original size: {image.size}")
    width, height = map(int, dimension.split("x"))
    sunset_resized = image.resize((width, height))
    sunset_resized.save(new_file_loc)
    print(f"New size: {dimension}")

    # Updating the JSON message to be stored in RedisDB
    content = message[6]
    z = content
    y = {"output_image_path": new_file_loc}
    z.update(y)
    print(json.dumps(z))

    r = redis.Redis(host='localhost', port=6379, db=0)
    key_val = "image" + str(counter)
    counter += 1

    r.set(key_val, json.dumps(z))

    return new_file_loc

def main():
    # Creates a KafkaConsumer for the 'secondtask' topic
    consumer = KafkaConsumer('secondtask', bootstrap_servers=['localhost:9092'],
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    counter = 0

    for message in consumer:
        process_image_message(message, counter)
        counter += 1

if __name__ == "__main__":
    main()
