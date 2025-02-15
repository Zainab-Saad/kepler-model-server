#!/bin/bash

num_clients=5

# change the node_type if testing for different node type in specpower data
node_type=86

# run the docker container for specpower db
CONTAINER_NAME="kepler_spec_power_db"

if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
    echo "The container '$CONTAINER_NAME' is already running."
else
    if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
        echo "Starting existing container '$CONTAINER_NAME'..."
        docker start $CONTAINER_NAME
    else
        echo "Running a new container..."
        docker run -d --name $CONTAINER_NAME -p 8080:80 quay.io/sustainability/kepler_spec_power_db:v0.7
    fi
fi

# run the FL clients simulation
for client_num in $(seq 1 $num_clients); do
    echo "Starting training for client no. ${client_num}"
    # Run the Python script in the background
    python3 ../clients/specpower_trainer_client_machine.py --pipeline_name "cl${client_num}" --client "${client_num}" --node_type "${node_type}" --num_clients "${num_clients}" &
    sleep 2
done

wait
echo "FL simuation done."
