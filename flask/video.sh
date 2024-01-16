#!/bin/bash
cd $HOME/babypi/flask/

if [ "$#" -eq 0 ]; then
    ./mjpeg2.py &> ./logs/ip.log
elif [ $1 = 'vflip' ]; then
    ./mjpeg2.py vflip &> ./logs/ip.log
else
echo please check valid arguments - "(vflip only)"
exit 1
fi