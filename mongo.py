import re
import time
import requests
import json
import random
import time
import sys
import subprocess

# Replace with your New Relic Insights Insert API key
INSIGHTS_INSERT_API_KEY = "c9e1b2c28fb2917569084e208844c856FFFFNRAL"
# Replace with your New Relic account ID
NEW_RELIC_ACCOUNT_ID = "3894757"

INSIGHTS_INSERT_URL = f"https://insights-collector.newrelic.com/v1/accounts/{NEW_RELIC_ACCOUNT_ID}/events"

def send_custom_metric_to_new_relic(metric_name, value, timestamp=None):
    event = {
        "eventType": "CustomMetric",
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

# send_custom_metric_to_new_relic(sys.argv[1], sys.argv[2])
# python script_name metric_name value
## Eample code - python send_custom_metrics_to_newrelic.py VA2PT/MySQL 99

## Sample NRQL
## SELECT median(metricValue) from CustomMetric where metricName = 'VA2PT/MySQL'  TIMESERIES 1 minute

def run_bash_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error occurred: {result.stderr.strip()}"
    except Exception as e:
        return f"Error occurred: {str(e)}"

def find_ip_addresses(input_string):
    # Define a regular expression pattern for finding IP addresses
    ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'

    # Use the findall() function from the re module to find all matches in the input string
    ip_addresses = re.findall(ip_pattern, input_string)

    return ip_addresses

def find_first_digits(input_string):
    # Define a regular expression pattern to find the first occurrence of digits
    digits_pattern = r'\d+'

    # Use re.search() to find the first match in the input string
    match = re.search(digits_pattern, input_string)

    if match:
        return match.group()
    else:
        return None

#### SAMPLE MONGO OUTPUT

# mongo_data="""MongoDB shell version v4.4.23
# connecting to: mongodb://172.17.0.9:27017/admin?compressors=disabled&gssapiServiceName=mongodb
# Implicit session: session { "id" : UUID("11b5b547-d2d1-4be9-a14c-38ca4e21eb68") }
# MongoDB server version: 4.4.4
# source: 192.168.5.35:27017
# 	syncedTo: Thu Aug 03 2023 06:18:28 GMT+0000 (UTC)
# 	99 secs (0 hrs) behind the primary 
# source: 192.168.5.37:27017
# 	syncedTo: Thu Aug 03 2023 06:18:28 GMT+0000 (UTC)
# 	1 secs (0 hrs) behind the primary"""

bash_command = "bash get_mongo_rep_data.sh"
mongo_data = run_bash_command(bash_command)

mongo_servers = {}
lag = ""
ip_addr = ""

for line in mongo_data.split('\n'):
    if "source:" in line:
        ip_addr = find_ip_addresses(line)[0]
    if "behind the primary" in line:
        lag = find_first_digits(line)
        mongo_servers[ip_addr] = lag

print(mongo_servers)

for key, value in mongo_servers.values():
    send_custom_metric_to_new_relic("VA2PT/Mongo" + key, value)