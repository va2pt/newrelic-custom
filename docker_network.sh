#!/bin/bash

NETWORK_NAME="bridge"

# Get a list of all container IDs in the specified network
container_ids=$(docker network inspect --format='{{range $id, $c := .Containers}}{{$id}} {{end}}' "$NETWORK_NAME")

# Loop through each container ID and curl a generic URL
for container_id in $container_ids; do
    # Get the container's IP address
    container_ip=$(docker inspect --format '{{ .NetworkSettings.Networks.'$NETWORK_NAME'.IPAddress }}' $container_id)

    # Define the port
    port=27017  # Change to the appropriate port

    # Try to curl a generic URL in the current container and capture the output
    curl_result=$(docker exec $container_id curl -s "http://$container_ip:$port" 2>/dev/null)

    # Print the container ID and curl result
    echo "Container $container_id:"
    echo "$curl_result"
    echo
done
