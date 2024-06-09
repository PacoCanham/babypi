#!/bin/bash
cd /home/paco/babypi/flask/

# Get the process id of app.py
pid=$(pgrep -f app.py)

# If app.py is running, kill it
if [ ! -z "$pid" ]; then
    echo "app.py is running. Process id is $pid. Stopping it now..."
    kill -9 $pid
else
    echo "app.py is not running."
fi

# Start app.py
echo "Starting app.py..."
./app.py &

echo "Done."
