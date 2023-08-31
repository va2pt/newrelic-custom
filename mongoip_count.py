import time
import requests
import json
import random
import time
import sys
import subprocess

def run_bash_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return "Error occurred:" +{result.stderr.strip()}
    except Exception as e:
        return "Error occurred:" +{str(e)}
    

# Replace with your New Relic Insights Insert API key
INSIGHTS_INSERT_API_KEY = "c9e1b2c28fb2917569084e208844c856FFFFNRAL"
# Replace with your New Relic account ID
NEW_RELIC_ACCOUNT_ID = "3894757"

INSIGHTS_INSERT_URL = f"https://insights-collector.newrelic.com/v1/accounts/{NEW_RELIC_ACCOUNT_ID}/events"

def send_custom_metric_to_new_relic(metric_name,ip_address ,value, timestamp=None):
    event = {
        "eventType": "Mongo_status",
        "timestamp": timestamp or int(time.time() * 1000),  # Convert to milliseconds
        "metricName": metric_name,
        "metric_ip": ip_address ,
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


def separate_ip_and_count(input_string):
    parts = input_string.split(':')
    if len(parts) == 2:
        ip_address = parts[0].strip()
        count = int(parts[1].strip())
        return ip_address, count
    else:
        raise ValueError("Invalid input format. Expected 'IP : Count'.")
    
bash_command = "ENTER YOUR BASH COMMAND HERE "
mongo_data = run_bash_command(bash_command)    

input_string = str (mongo_data)
ip_address, count = separate_ip_and_count(input_string)
send_custom_metric_to_new_relic('VA2PT/Mongo_ip_count',ip_address ,count)

