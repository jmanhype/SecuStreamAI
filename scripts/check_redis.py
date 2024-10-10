import redis
import json

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Get all keys
keys = r.keys('event:*')

print(f"Total events stored: {len(keys)}")

# Print details of the first 5 events
for key in keys[:5]:
    value = r.get(key)
    event_data = json.loads(value)
    print(f"\nKey: {key.decode('utf-8')}")
    print(f"Value: {json.dumps(event_data, indent=2)}")