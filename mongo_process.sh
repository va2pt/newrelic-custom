#!/bin/bash

# Run lsof to get a list of processes and ports
lsof_output=$(sudo lsof -i -n -P)

# Parse lsof output to extract IP addresses and port numbers
ip_port_list=$(echo "$lsof_output" | awk '/LISTEN/ { print $9 }')

# Loop through each IP address and port and make a curl request
for ip_port in $ip_port_list; do
    ip=$(echo "$ip_port" | cut -d':' -f1)
    port=$(echo "$ip_port" | cut -d':' -f2)
    echo "Making a request to $ip:$port"
    curl "http://$ip:$port"
    echo
done

# Count MongoDB processes
mongo_process_count=$(echo "$lsof_output" | grep -w "mongod" | wc -l)
echo "Number of MongoDB processes: $mongo_process_count"
