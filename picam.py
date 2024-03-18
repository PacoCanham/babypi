import time
import io
# import picamera2
from libcamera import controls, Transform
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import ffmpegOutput
import threading
from flask import Flask, redirect, render_template, session, request, jsonify, Response, stream_with_context

app = Flask(__name__)


class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = threading.Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

b = io.BytesIO()
# picam = Picamera2()
tuningpath = '/home/paco/babypi/flask/tuning.json'
tuning = Picamera2.load_tuning_file(tuningpath)
picam = Picamera2(tuning=tuning)
# config = picam.create_video_configuration(main={"size": (1920, 1080)})
# picam.configure(config)
config = picam.create_video_configuration(main={"size": (1920, 1080)}, controls={"AwbMode": controls.AwbModeEnum.Indoor, "NoiseReductionMode" : controls.draft.NoiseReductionModeEnum.Off, 'FrameDurationLimits': (40000, 40000)})
# picam.configure(config)


encoder = MJPEGEncoder()
stream = StreamingOutput()
output = FfmpegOutput("")

picam.start_and_record_video(encoder=encoder, output=output, config=config, audio=True, duration=0)

@app.route('/audio.mp4')
def stream_audio():
    def generate():
        while True:
            yield(stream.frame)
    return Response(stream_with_context(generate()), mimetype='video/mp4')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
