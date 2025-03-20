import pika
import os
import time

# Configuration variables
queue_name = os.getenv('RMQ_QUEUE_NAME', 'app1')
host = os.getenv('RMQ_HOST', "rabbitmq-0.rabbitmq-headless.rmq.svc.cluster.local")
port = int(os.getenv('RMQ_PORT', 5672))
username = os.getenv('RMQ_USERNAME', 'vegito')
password = os.getenv('RMQ_PASSWORD', 'K3da#123')
consume_speed = int(os.getenv('CONSUME_SPEED', 1))  # Default to 1 second
batch_size = 20  # Number of messages to fetch in each batch

def consume_message(queue_name, host='localhost', port=5672, username='guest', password='guest', consume_speed=1, batch_size=20):
    # Set up connection parameters
    credentials = pika.PlainCredentials(username, password)
    connection_params = pika.ConnectionParameters(host=host, port=port, credentials=credentials)
    
    # Establish a connection and open a channel
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    
    # Declare the queue
    channel.queue_declare(queue=queue_name, durable=True)

    # Set prefetch count to limit the number of messages fetched at a time
    channel.basic_qos(prefetch_count=batch_size)

    def callback(ch, method, properties, body):
        try:
            print(f" [x] Received '{body.decode()}' from queue '{queue_name}'")
            # Simulate message processing
            time.sleep(consume_speed)
            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f" [x] Acknowledged message with delivery tag {method.delivery_tag}")
        except Exception as e:
            print(f"Error processing message: {e}")
            # Optional: reject the message and requeue it if processing fails
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    # Consume messages with manual acknowledgment
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
    print(f" [*] Waiting for messages in queue '{queue_name}'. To exit press CTRL+C")
    
    try:
        # Start consuming messages
        channel.start_consuming()
    except KeyboardInterrupt:
        # Graceful shutdown
        print(' [!] Consumer interrupted, shutting down...')
        channel.stop_consuming()
    finally:
        # Close the connection properly
        connection.close()

# Start consuming messages
consume_message(queue_name, host=host, port=port, username=username, password=password, consume_speed=consume_speed, batch_size=batch_size)
