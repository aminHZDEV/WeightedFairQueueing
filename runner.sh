#!/bin/bash

# Start destination first
python3 destination/destination.py &

# Give the destination some time to start up (adjust the sleep duration as needed)
sleep 3

# Start the router
python3 router/router.py &

# Give the router some time to start up
sleep 2

# Start the client
python3 client/client.py