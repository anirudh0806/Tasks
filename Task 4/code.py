import requests  # request image from web
import shutil  # save image locally
from kafka import KafkaConsumer
import json
import redis
from PIL import Image

# Create a KafkaConsumer for the 'secondtask' topic
consumer = KafkaConsumer('secondtask', bootstrap_servers=['localhost:9092'],
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))
k=0
for message in consumer:
    # Extract relevant information from the message
    url = message[6]["image_url"]
    file_name = "newfile.jpg"
    dimension = message[6]["output_size"]
    width, height = map(int, dimension.split("x"))

    # Download the image
    res = requests.get(url, stream=True)
    if res.status_code == 200:
        with open(file_name, 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image successfully Downloaded:', file_name)
    else:
        print('Image Couldn\'t be retrieved')

    # Open and resize the image
    image = Image.open('newfile.jpg')
    print(f"Original size: {image.size}")
    sunset_resized = image.resize((width, height))
    sunset_resized.save('newfile-resized.jpeg')
    print(f"New size: {dimension}")

    # Updating the JSON message to be stored in RedisDB
    content=message[6]
    new_file_loc="test\newfile-resized.jpeg"
    z=content
    y={"output_image_path":new_file_loc}
    z.update(y)
    print(json.dumps(z))

    # Connects to the Redis server
    r = redis.Redis(host='localhost', port=6379, db=0)
    key_val="image"+str(k)
    k+=1

    # Stores the specific field from the message in Redis with the key such as 'image0','image1' and so on
    r.set(key_val, json.dumps(z))
    


