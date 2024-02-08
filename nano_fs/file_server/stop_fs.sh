#!/bin/bash

# gracefully terminate the server
pkill -15 -f "python3 -u -m http.server 8080"
pkillexitstatus=$?

# ensure that the process was successfully killed
if [ $pkillexitstatus -eq 0 ]; then
  echo "Server successfully stopped."
else
  echo "[WARNING] No running webserver matched stop critera"
fi

# terminate data acquisition script
pkill -15 -f "python3 generate_data.py"
pkillexitstatus=$?

# ensure that the process was successfully killed
if [ $pkillexitstatus -eq 0 ]; then
  echo "Data aquisition service successfully stopped."
else
  echo "[WARNING] No running service matched stop criteria"
fi
 