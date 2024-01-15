#!/usr/bin/python3

import io
import time
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

class StreamingOutput(io.BufferedIOBase):
    def __init__(self, filename):
        self.file = open(filename, "wb")
        self.frame = None

    def write(self, buf):
        self.file.write(b"--FRAME\r\n")
        self.file.write(b"Content-Type: image/jpeg\r\n")
        self.file.write(b"Content-Length: %d\r\n\r\n" % len(buf))
        self.file.write(buf)
        self.file.write(b"\r\n")
        self.frame = buf

picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (640, 480)}))
output = StreamingOutput("stream.mjpg")
picam2.start_recording(JpegEncoder(), FileOutput(output))

try:
    while True:
        time.sleep(1)
finally:
    picam2.stop_recording()
    output.file.close()

