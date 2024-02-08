#!/bin/bash

# clear the log file if it exists
FILE=sync_history.log
if test -f "$FILE"; then
  rm -f $FILE
fi

# specify file server params
IP='172.20.20.55'
PT='8080'

# inform user that server is starting
clear
echo -e "Starting to sync data from $IP:$PT ...\n"

# start a new log file
echo "============== NEW SESSION $(date) ==============" > sync_history.log

# start the sync service
python3 sync_data.py $IP $PT 
