#!/bin/bash

NETWORK_NAME="bridge"
total_count=0

# Get a list of all container IDs in the specified network
container_ids=$(docker network inspect --format='{{range $id, $c := .Containers}}{{$id}} {{end}}' "$NETWORK_NAME")

# Loop through each container ID and curl a generic URL
for container_id in $container_ids; do
    # Get the container's IP address
    container_ip=$(docker inspect --format '{{ .NetworkSettings.Networks.'$NETWORK_NAME'.IPAddress }}' $container_id)

    # Define the port
    port=27017  # Change to the appropriate port

    # Try to curl a generic URL in the current container and capture the output
    curl_result=$(docker exec $container_id curl -s "http://$container_ip:$port" 2>/dev/null || true)

    # Check if the curl_result indicates MongoDB over HTTP
    if echo "$curl_result" | grep -q "MongoDB over HTTP"; then
        total_count=$((total_count + 1))
    fi
done

# Print the total count
echo "Total count of MongoDB over HTTP requests from Docker containers: $total_count"

# Run lsof to get a list of processes and ports
netstat_output=$(sudo netstat -putan | grep LISTEN)

# Count MongoDB processes on the host
mongo_process_count=$(echo "$netstat_output" | grep -w "mongod" | wc -l)
echo "Number of MongoDB processes on the host: $mongo_process_count"
