import re
import time
import requests
import json
import random
import time
import subprocess
import os

# Replace with your New Relic Insights Insert API key
INSIGHTS_INSERT_API_KEY = "Enter your new relic api key"

INSIGHTS_INSERT_URL = 'https://insights-collector.eu01.nr-data.net/v1/accounts/3954612/events'

def send_custom_metric_to_new_relic(metric_name,ip_address,num_connections,timestamp=None):
    event = {
        "eventType": "CustomMetric",
        "timestamp": timestamp or int(time.time() * 1000),  # Convert to milliseconds
        "metricName": metric_name,
        "ipAddress": ip_address,
        "numConnections": num_connections
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


bash_command = "/bin/bash /home/sidd/newrelic-custom/netstat.sh"

os.system(bash_command + " > /home/sidd/newrelic-custom/data")
file=open('/home/sidd/newrelic-custom/data')
netstat_data = file.read()
list = []
for line in netstat_data.split('\n'):
    if any(char.isalpha() for char in line.strip()):
        pass
    else:    
        list.append(line.strip())

for net_data in list:
     number,ip = extract_number_from_line(net_data)
     if number == None and ip == None :
            pass
     else:
        print('number :',number ,'ip :',ip)
        send_custom_metric_to_new_relic('netstat_data',ip,number)



   

      

   

    




