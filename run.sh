#!/usr/bin/bash
cd ~/babypi/
cd babypi/src/
./mjpeg2.py &
cd ../../flask/
./app.py &
cd ../babypi
npm run dev -- --host --port 5174 &
