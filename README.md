# Task 1: Python Calculator
## Installing Docker on Windows

This guide will help you install Docker on your Windows machine.

### Prerequisites

Before you begin, make sure your system meets the following requirements:

- Windows 10 Pro, Enterprise, or Education edition.
- Virtualization must be enabled in BIOS/UEFI settings.
- At least 4GB of RAM.

### Installation Steps

1. Download Docker Desktop for Windows from the official website: [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop).

2. Run the installer and follow the on-screen instructions.

3. During installation, you may be prompted to enable Hyper-V and Windows Subsystem for Linux (WSL). Allow these features if prompted.

4. Once the installation is complete, launch Docker Desktop.

5. Docker should now be up and running on your Windows machine.

6. Open a command prompt or PowerShell and verify Docker is installed by running:

     ```bash
     docker --version
     ```
## Build the Docker Image

Build the Docker image using the provided Dockerfile:
        
```bash
docker build -t calculator .
```

## Run the Docker Container

Run the Docker container, providing any two integers as command line numeric arguments:

```bash
docker run calculator 10 20
```

## View the Results

The script will calculate and display the following results:
- The sum of the two numbers.
- The difference between the two numbers.
- The product of the two numbers.
- The result of dividing the first number by the second number.

#### Find the image on Docker Hub: [Docker Image on Docker Hub](https://hub.docker.com/r/anirudh0806docker/calculator-first-task)

---






# Task 2:  Kafka Server, Redis Server


### Prerequisites

Before you begin, ensure you have the following prerequisites installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose: [Install Docker Compose](https://docs.docker.com/compose/install/)



### Installing Kafka on Docker using Docker Compose
Kafka will be run on Docker using Docker Compose. Kafka will be running in a Docker container alongside ZooKeeper for managing Kafka's data.


1. Find `docker-compose.yml` file in the sub-folder named ‘kafka-installation’ in the ‘Task 2’ folder. 

2. Save the `docker-compose.yml` file in your project directory.

3. Open a terminal or command prompt and navigate to the directory where your `docker-compose.yml` file is located.

4. Run the following command to start the Kafka and ZooKeeper containers:

    ```bash
    docker-compose -f docker-compose.yml up -d
    ```

5. To verify that the containers are running, you can run the following command:

    ```bash
    docker ps
    ```


### Installing Redis on Docker using Docker Compose
1. Find `redis-docker-compose.yml` file in the sub-folder named ‘redis-installation’ in the ‘Task-2’ folder.
2. Save the `redis-docker-compose.yml` file in your project directory.

3. Open a terminal or command prompt and navigate to the directory where your `redis-docker-compose.yml` file is located.

4. Run the following command to start the Redis and Redis Insight containers:

    ```bash
    docker-compose -f redis-docker-compose.yml up -d
    ```
5. To verify that the containers are running, you can run the following command:

    ```bash
    docker ps
    ```
6. Configure Redis at http://localhost:8001 in your device using Redis Insight.

### Using Kafka and Redis

Both Redis and Kafka are now up and running in Docker.

##### Running and Configuration of Kafka server and Redis:
- Start the Kafka server by typing this in the Kafka terminal

    ```bash
    docker exec -it kafka /bin/sh
    ```
- Redis CLI can also be used [Optional]
    ```bash
    docker exec -it redis redis-cli
    ```
    Configure redis on http://localhost:8001
### Execution



###### Create a Kafka Topic
1.	In the Kafka terminal, navigate to Kafka's bin directory:
    ```bash
    cd /opt/kafka_2.13-2.8.1/bin 
    ```
2.	Create a Kafka topic (e.g., 'secondtask'):
    ```bash
    bin/kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic secondtask 
    ```
3.	To list all topics, run:
    ```bash
    kafka-topics.sh --list --zookeeper zookeeper:2181 
    ```
##### Kafka Consumer
###### Consume Messages from the Topic
4.	Open another terminal or split the terminal to visit the same directory. Consume messages from the 'secondtask' topic using the Kafka console consumer:
    ```bash
    kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic secondtask --from-beginning 
    ```
##### Kafka Producer    
###### Produce a Message to the Topic
5.	Produce a message to the topic 'secondtask' using the Kafka console producer:
    ```bash
    kafka-console-producer.sh --broker-list kafka:9092 --topic secondtask 
    ```
    Type your message in JSON format and press Enter. For example:
    ```bash
    {"num":1, "user_name":"Ram", "message":"Success"}
    ```
    The messages produced by the Kafka producer would be visible in the consumer terminal.



##### Sending Messages to Redis
6.	Run the Python script task2_code.py in a parallel terminal to receive data from the Kafka producer and send messages to Redis:
    ```bash
    python task2_code.py
    ```
---

# Task 3: Kafka Server, Redis Server, Producer, and Consumer

## Prerequisites

Before you begin, ensure you have the following prerequisites installed on your system:

- [Apache Kafka](https://kafka.apache.org/) installed and running.
- Python (greater than v3.0) installed.

### Kafka Setup

1. Start your Kafka server (if not already running) and ZooKeeper. You can refer to the previous task for installation and setup instructions.

2. Create a Kafka topic named 'messages' using the following command:

   ```bash
   kafka-topics.sh --create --zookeeper zookeeper:2181 --replication-factor 1 --partitions 1 --topic messages
   ```
## Running the Kafka Consumer

1. Open another terminal or command prompt.
2. Navigate to the directory containing the Python Kafka consumer code.
3. Run the Kafka consumer code by executing the following command:

   ```bash
   python consumer_code.py
   ```
## Running the Kafka Producer

1. Open a terminal or command prompt.
2. Navigate to the directory containing the Python Kafka producer code.
3. Run the Kafka producer code by executing the following command:

   ```bash
   python producer_code.py
   ```
    The interaction between the producer and consumer, with messages being produced and consumed can be observed.

---

# Task 4: Message Processing in Kafka

This is a Python code that processes image URLs from a Kafka topic, downloads the images, resizes them, and stores the result in a Redis database. It is designed to work with the Kafka topic named 'secondtask'.

## Prerequisites

Before running the script, ensure the installation and functioning of the following components:
1.  Python 3
2. `requests` library for making HTTP requests.
3. `shutil` library for file operations.
4. `kafka-python` library for Kafka integration.
5. `PIL` (Pillow) library for image processing.
6.  Redis server and Kafka server are running.

    You can install the required Python libraries using pip:

    ```bash
    pip install requests kafka-python Pillow redis
    ```

## Execution

1. Start a Kafka producer to send messages with image URLs and output size information to the 'secondtask' Kafka topic.
2. Run the script using Python:

    ```bash
    python code.py
    ```

3. The script will consume messages from the 'secondtask' Kafka topic, download the images, resize them according to the specified dimensions, and store the results in Redis with keys like 'image0', 'image1', and so on.

## Configuration

- You can adjust the Kafka server settings by modifying the `bootstrap_servers` parameter in the script.
- Ensure that the Redis server is running and accessible at `localhost:6379`.


   




