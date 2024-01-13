#!/usr/bin/bash
cd ~/babypi/
cd babypi/
npm run dev -- --host --port 5174 &
cd ../flask
./app.py
