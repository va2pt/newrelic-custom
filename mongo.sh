#!/bin/bash
# MongoDB connection details
MONGO_HOST="your_mongo_host"
MONGO_PORT="your_mongo_port"
MONGO_USERNAME="your_mongo_username"
MONGO_PASSWORD="your_mongo_password"
AUTH_DB="your_mongo_authentication_database"
# Create the MongoDB connection string
CONNECTION_STRING="mongodb://${MONGO_USERNAME}:${MONGO_PASSWORD}@${MONGO_HOST}:${MONGO_PORT}/${AUTH_DB}"
# Function to execute the MongoDB command
execute_mongo_command() {
    local mongo_command="$1"
    # Run the MongoDB shell command and pass the connection string
    mongo "${CONNECTION_STRING}" --eval "${mongo_command}"
}
# Run the show dbs command
execute_mongo_command "show dbs"