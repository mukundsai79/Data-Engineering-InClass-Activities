import urllib.request
import json
from google.cloud import pubsub_v1
import concurrent.futures
import threading

# GCP Configuration
project_id = 'myprojectsaikrishna'
topic_id = 'archivetest'

# Publisher client
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(project_id, topic_id)

# Global counters with threading lock
total_messages_sent = 0
total_messages_published = 0
counter_lock = threading.Lock()

vehicle_ids = [
    3029, 3235, 4027, 3608, 3059, 3213, 3507, 2902, 3721, 3024,
    3555, 3702, 3146, 2904, 3018, 3704, 3542, 2935, 3244, 3234,
    4205, 4526, 3119, 4520, 2928, 3019, 3650, 3538, 3505, 3558,
    3411, 3115, 3638, 4502, 3546, 3021, 3258, 3169, 3046, 3254,
    3419, 4011, 2924, 3030, 3408, 3201, 4211, 3719, 3756, 3267,
    3266, 4505, 3557, 3525, 3017, 4210, 3325, 3054, 3728, 3802,
    3005, 3035, 3937, 3420, 3530, 4007, 3630, 3705, 3622, 3631,
    3503, 3212, 3724, 4070, 3910, 3964, 3012, 3634, 3605, 4236,
    4518, 3559, 4237, 3710, 3237, 3906, 3644, 3805, 3513, 4048,
    4207, 3627, 3524, 3727, 3733, 3518, 3045, 3023, 3904, 3734
]

def publish_callback(future, vehicle_id):
    """Handles the result of the asynchronous publish call."""
    global total_messages_published
    try:
        future.result()
        with counter_lock:
            total_messages_published += 1
    except Exception as e:
        print(f"Failed to publish message for vehicle ID {vehicle_id}: {e}")

def fetch_and_publish_data(vehicle_id):
    """Fetch JSON data for a vehicle and publish each record to GCP Pub/Sub."""
    global total_messages_sent
    url = f"https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id={vehicle_id}"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            print(f"Starting processing for vehicle ID {vehicle_id}")
            for record in data:
                message = json.dumps(record).encode('utf-8')
                future = publisher.publish(topic_path, message)
                future.add_done_callback(lambda f: publish_callback(f, vehicle_id))
                with counter_lock:
                    total_messages_sent += 1
            print(f"Finished processing vehicle ID {vehicle_id}")
    except urllib.error.URLError as e:
        print(f"Failed to fetch data for vehicle ID {vehicle_id}: {e}")

def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch_and_publish_data, vehicle_id) for vehicle_id in vehicle_ids]
        concurrent.futures.wait(futures)
    
    print(f"Total messages sent: {total_messages_sent}")
    print(f"Total messages published: {total_messages_published}")

if __name__ == "__main__":
    main()
