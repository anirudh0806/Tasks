import requests
import shutil
from kafka import KafkaConsumer
import json
import redis
from PIL import Image

# Image processing class
class ImageProcessing:
    def download_image(self, url, file_name):
        # Download the image from a URL and save it as a file
        res = requests.get(url, stream=True)
        if res.status_code == 200:
            with open(file_name, 'wb') as f:
                shutil.copyfileobj(res.raw, f)
            print('Image successfully downloaded:', file_name)
        else:
            print('Image Couldn\'t be retrieved')

    def resize_image(self, file_name, dimension):
        # Resize the image to the specified dimensions
        image = Image.open(file_name)
        print(f"Original size: {image.size}")
        width, height = map(int, dimension.split("x"))
        sunset_resized = image.resize((width, height))
        sunset_resized.save(file_name)
        print(f"New size: {dimension}")

# Database handling class
class DBHandling:
    def update_json_message(self, message, new_file_loc):
        # Update a JSON message with the path to the resized image
        content = message[6]
        content["output_image_path"] = new_file_loc
        return json.dumps(content)

    def store_in_redis(self, counter, key_val, json_data):
        # Store JSON data in Redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.set(key_val, json_data)

# Adapter class for processing Kafka messages containing image information
class KafkaImageAdapter:
    def __init__(self):
        self.image_processing = ImageProcessing()
        self.db_handling = DBHandling()

    def process_kafka_message(self, message, counter):
        # Extract relevant information from the message
        url = message[6]["image_url"]
        file_name = "newfile.jpg"
        dimension = message[6]["output_size"]
        new_file_loc = "test\newfile-resized.jpeg"

        # Download the image
        self.image_processing.download_image(url, file_name)

        # Resize the image
        self.image_processing.resize_image(file_name, dimension)

        # Update the JSON message and store in Redis
        json_data = self.db_handling.update_json_message(message, new_file_loc)
        key_val = "image" + str(counter)
        self.db_handling.store_in_redis(counter, key_val, json_data)

        return new_file_loc

# Main function
def main():
    # Creates a KafkaConsumer for the 'secondtask' topic
    consumer = KafkaConsumer('secondtask', bootstrap_servers=['localhost:9092'],
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    counter = 0

    kafka_image_adapter = KafkaImageAdapter()

    for message in consumer:
        # Process Kafka message containing image information
        kafka_image_adapter.process_kafka_message(message, counter)
        counter += 1

if __name__ == "__main__":
    main()
