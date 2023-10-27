#!/bin/bash

# gracefully terminate the sync service
pkill -15 -f "python3 sync_data.py"
pkillexitstatus=$?

# ensure that the process was successfully killed
if [ $pkillexitstatus -eq 0 ]; then
  echo "Service successfully stopped."
else
  echo "[WARNING] No running service matched stop criteria"
fi
