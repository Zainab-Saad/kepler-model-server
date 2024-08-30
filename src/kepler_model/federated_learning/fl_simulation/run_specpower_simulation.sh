#!/bin/bash

num_clients=3

# change the node_type if testing for different node type in specpower data
node_type=86

for client_num in $(seq 1 $num_clients); do
    echo "Starting training for client no. ${client_num}"
    # Run the Python script in the background
    python3 ../clients/specpower_trainer_client_machine.py --pipeline_name "cl${client_num}" --client "${client_num}" --node_type "${node_type}" &
    # Optional: Add a small delay to prevent resource contention
    sleep 2
done

# Wait for all background processes to complete
wait
echo "FL simuation done."
