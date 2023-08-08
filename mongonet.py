import re
import time
import requests
import json
import random
import time
import subprocess
import os

# Replace with your New Relic Insights Insert API key
INSIGHTS_INSERT_API_KEY = "c9e1b2c28fb2917569084e208844c856FFFFNRAL"

INSIGHTS_INSERT_URL = 'https://insights-collector.newrelic.com/v1/accounts/3894757/events'

def send_custom_metric_to_new_relic(metric_name,value,timestamp=None):
    event = {
        "eventType": "CustomMetric",
        "timestamp": timestamp or int(time.time() * 1000),  # Convert to milliseconds
        "metricName": metric_name,
        "conn_count": value
    }

    headers = {
        "X-Insert-Key": INSIGHTS_INSERT_API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(INSIGHTS_INSERT_URL, headers=headers, data=json.dumps(event))
        response.raise_for_status()
        
    except requests.exceptions.RequestException as e:
        print(e)

def extract_number_from_line(line):
    pattern = r'^\s*(\d+)\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*$'
    matches = re.match(pattern, line)
    if matches:
        number = int(matches.group(1))
        ip = matches.group(2)
        return number , ip
    return None, None

def find_first_digits(input_string):
    digits_pattern = r'\d+'
    match = re.search(digits_pattern,input_string)
    if match:
        return match.group()
    else:
        return None

def ip_and_connection(string):
    pattern = r"(\d)\s+tcp\s+\d+\s+\d+\s+([\d.])"
    matches = re.search(pattern, string)
    if matches:
        connection = int(matches.group(1))
        ip_address =matches.group(2)
    else:
        print("None")
    return ip_address,connection     

bash_command = "/bin/bash /root/netstat.sh"

os.system(bash_command + " > /opt/newrelic-custom/data")
file=open('/opt/newrelic-custom/data')
netstat_data = file.read()
list = []
for line in netstat_data.split('\n'):
        list.append(line.strip())

for net_data in list:

    #ip , connections = ip_and_connection(net_data)
     print(netstat_data)
     send_custom_metric_to_new_relic('netstat_data', net_data)
