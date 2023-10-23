#!/bin/bash

# clear the log file
rm server.log

# get current ip address
ip=$(hostname -I | cut -d " " -f1)

# inform user that server is starting
echo "Starting HTTP server at $ip on port 8080 ..."

# start a new log file
echo "============== NEW SESSION $(date) ==============" > server.log

# start the HTTP server using python
python3 -m http.server 8080 >> server.log 2>&1

# inform user that server is stopping
echo -e "\nServer closed."

