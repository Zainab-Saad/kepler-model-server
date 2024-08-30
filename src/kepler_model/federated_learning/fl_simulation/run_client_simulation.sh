#!/bin/bash

# Number of clients
num_clients=3

for client_num in $(seq 1 $num_clients); do
    echo "Starting training for client no. ${client_num}"
    # Run the Python script in the background
    python3 ../clients/client.py --pipeline_name "cl${client_num}" &
    # Optional: Add a small delay to prevent resource contention
    sleep 2
done

# Wait for all background processes to complete
wait
echo "FL simuation done..."
