#!/bin/bash
ffmpeg -f alsa -i plughw:1,0 -ac 1 -b:a 256k -c:a aac -strict experimental -f hls -hls_time 1 -hls_list_size 5 -hls_flags delete_segments /home/paco/babypi/flask/static/stream.m3u8 &
