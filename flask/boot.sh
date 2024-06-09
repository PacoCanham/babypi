#!/bin/bash

# Define the directory path
dir_path="/home/paco/babypi/flask/"

# Change to the defined directory
cd $dir_path

# Check if the directory change was successful
if [ $? -eq 0 ]; then
    echo "Directory change successful."
else
    echo "Failed to change directory. Please check the directory path."
    exit 1
fi

# Start the pigpio daemon
sudo pigpiod
echo "Started pigpiod with PID $!"

# Run the scripts
./ffmpeg_hls.sh &
echo "Started ffmpeg_hls.sh with PID $!"

./thermal_pull_up_boot.py &
echo "Started thermal_pull_up_boot.py with PID $thermal_pid"

./audiotest &
echo "Started AudioTest with PID $audiotest"

./app.py &
echo "Started app.py with PID $!"

echo "ffmpeg_hls.sh, app.py and pigpiod are running in the background."
