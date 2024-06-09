import numpy as np
from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

# Initialize Picamera2
picam2 = Picamera2()

# Configure the video settings for main and lores streams
video_config = picam2.create_video_configuration(main={"size": (1920, 1080), "format": "RGB888"},
                                                 lores={"size": (640, 480), "format": "YUV420"})
picam2.configure(video_config)

# Start the camera
picam2.start()

# Set the resolution for lores stream
w, h = 640, 480
prev_frame = None
motion_detected = False

while True:
    # Capture the lores buffer
    lores_frame = picam2.capture_buffer("lores")
    lores_frame = lores_frame[:w * h].reshape(h, w)

    # If it's the first frame, initialize it
    if prev_frame is None:
        prev_frame = lores_frame
        continue

    # Calculate the absolute difference between current and previous frame
    frame_diff = np.abs(lores_frame.astype(float) - prev_frame.astype(float))
    mean_diff = np.mean(frame_diff)

    # Define a threshold for what counts as motion
    if mean_diff > 15:  # You can adjust this threshold
        if not motion_detected:
            print("Motion Detected")
            motion_detected = True
    else:
        motion_detected = False

    # Update the previous frame
    prev_frame = lores_frame
