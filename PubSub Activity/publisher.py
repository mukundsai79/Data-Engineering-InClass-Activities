import json
import requests
from google.cloud import pubsub_v1


project_id = 'myprojectsaikrishna'
topic_id = 'topic3'

# Publisher client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# List of vehicle IDs
vehicle_ids = [3029, 3235]

def fetch_data(vehicle_id):
    """Fetch JSON data for a vehicle."""
    url = f"https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id={vehicle_id}"
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to fetch data for vehicle ID {vehicle_id}: {e}")
        return None

def save_to_file(data, filename='bcsample.json'):
    """Save data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

def publish_to_pubsub(message, project_id, topic_id):
    """Publish message to Pub/Sub."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    future = publisher.publish(topic_path, message.encode('utf-8'))
    print(f"Published message. ID: {future.result()}")

def main():
    all_data = []

    # Fetch data for each vehicle
    for vehicle_id in vehicle_ids:
        data = fetch_data(vehicle_id)
        if data:
            all_data.extend(data)

    # Save all data to a new file
    save_to_file(all_data)