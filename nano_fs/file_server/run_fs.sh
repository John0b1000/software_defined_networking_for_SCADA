#!/bin/bash

# inform the user that data aquisition is beginning
echo "Beginning data aquisition service ..."

# start the data aquisition script
python3 generate_data.py &

# clear the log file if it exists
FILE=server.log
if test -f "$FILE"; then
  rm -f $FILE
fi

# get current ip address
ip=$(hostname -I | cut -d " " -f1)

# inform user that server is starting
echo "Starting HTTP server at $ip on port 8080 ..."

# start a new log file
echo "============== NEW SESSION $(date) ==============" > server.log

# start the HTTP server using python
python3 -u -m http.server 8080 >> server.log 2>&1 &

# call the observe script
. observe.sh
