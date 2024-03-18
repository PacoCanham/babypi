#!/usr/bin/python3
import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

encoder = H264Encoder(10000000)

output = FfmpegOutput('-movflags frag_keyframe+empty_moov -f mp4 -', audio=True)
print(output.stdout)

picam2.start_recording(encoder, output)
# time.sleep(10)
while True:
    print(output.stdout)
# picam2.stop_recording()