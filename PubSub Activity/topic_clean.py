from google.cloud import pubsub_v1

def clean_topic(project_id, subscription_name):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback(message):
        # Discard the message
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on subscription {subscription_path}...")
    try:
        streaming_pull_future.result()  # Blocks the thread indefinitely
    except KeyboardInterrupt:
        streaming_pull_future.cancel()  # Cancels the subscription upon interrupt

if __name__ == "__main__":
    project_id = "myprojectsaikrishna"
    subscription_name = "sub6"
    clean_topic(project_id, subscription_name)


