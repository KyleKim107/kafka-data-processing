
from confluent_kafka import Consumer, KafkaError

# Define the Kafka consumer configuration
conf = {
    'bootstrap.servers': '172.31.6.238:9092',  # Replace with your Kafka bootstrap servers
    'group.id': 'apartinfo',           # Replace with your consumer group ID
    'auto.offset.reset': 'earliest',                # Set to 'earliest' to read from the beginning of the topic
}


# Create the Kafka consumer
consumer = Consumer(conf)

# Subscribe to the Kafka topic
topic = 'apartinfo'  # Replace with the Kafka topic you want to consume
consumer.subscribe([topic])

# Poll for messages
try:
    while True:
        msg = consumer.poll(1.0)  # Poll for messages, with a timeout of 1 second

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                print(f"Reached end of partition for {msg.topic()} [{msg.partition()}]")
            else:
                print(f"Error: {msg.error()}")
        else:
            # Process the received message
            print(f"Received message: {msg.value().decode('utf-8')}\n")

except KeyboardInterrupt:
    pass
finally:
    # Close down consumer to commit final offsets.
    consumer.close()
