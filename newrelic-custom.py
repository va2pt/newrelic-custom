import time
import requests
import json
import random
import time
import sys
from curl import get_metric

# Replace with your New Relic Insights Insert API key
INSIGHTS_INSERT_API_KEY = "c9e1b2c28fb2917569084e208844c856FFFFNRAL"
# Replace with your New Relic account ID
NEW_RELIC_ACCOUNT_ID = "3894757"

INSIGHTS_INSERT_URL = f"https://insights-collector.newrelic.com/v1/accounts/{NEW_RELIC_ACCOUNT_ID}/events"

def send_custom_metric_to_new_relic(metric_name, value, timestamp=None):
    event = {
        "eventType": "Mongo_status",
        "timestamp": timestamp or int(time.time() * 1000),  # Convert to milliseconds
        "metricName": metric_name,
        "metricValue": value
    }

    headers = {
        "X-Insert-Key": INSIGHTS_INSERT_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(INSIGHTS_INSERT_URL, headers=headers, data=json.dumps(event))
        response.raise_for_status()
        print(f"Custom metric sent: {metric_name}={value}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending custom metric: {e}")

# Example usage:
# Replace 'YOUR_METRIC_NAME' and 'YOUR_METRIC_VALUE' with your desired metric name and value


## loop python to test data is going to newrelic or not
# for x in range(1, 10000):
#     send_custom_metric_to_new_relic("VA2PT/MySQL", random.randrange(10, 99))
#     time.sleep(1)
# Linux command to run in the background
command = "netstat -tulpn | awk '{print $4}' | xargs curl -s | grep -i 'MongoDB' | wc -l" 
value = get_metric(command)
send_custom_metric_to_new_relic('va2pt/mongo_status',value)