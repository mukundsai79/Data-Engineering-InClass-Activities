from google.cloud import pubsub_v1
import json
import os


project_id = 'myprojectsaikrishna'
subscription_id = 'sub6'  

# Subscriber client
subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

file_path = 'pubsub_records.json'

def callback(message):
    print(f"Received message: {message.data}")
    try:
        data = json.loads(message.data.decode('utf-8'))
        
        with open(file_path, 'a') as file:
            file.write(json.dumps(data) + '\n')

        message.ack()
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    if not os.path.exists(file_path):
        with open(file_path, 'w'):
            pass

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}...")

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

if __name__ == "__main__":
    main()
