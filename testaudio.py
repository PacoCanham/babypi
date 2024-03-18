from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput, FfmpegOutput
import time
import subprocess
import threading


general_options = ['-loglevel', 'warning', '-y', '-fflags', 'nobuffer', '-flags', 'low_delay', '-strict', 'experimental']
# extras = ['-use_wallclock_as_timestamps', '1']
audio_input = ['-f', 'pulse', '-sample_rate', '48000', '-thread_queue_size', '1024', '-i', 'default']
audio_codec = ['-b:a', '128000', '-c:a', 'libvorbis']
output_options = ['-f', 'webm', 'pipe:1']  # Output to stdout in WebM format
video_input = ['-use_wallclock_as_timestamps', '1',
            '-thread_queue_size', '64', '-input_format', 'h264',  # necessary to prevent warnings
            '-i', '/dev/video0', '-f', 'v4l2']
video_codec = ['-c:v', 'copy']

command = ['ffmpeg'] + general_options + video_input + video_codec + audio_input + audio_codec + output_options

# Start the ffmpeg process without stdin
process = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=0)

# while True:
    # print(process.stdout.read(1024))