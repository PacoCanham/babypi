#!/usr/bin/python3
from flask import Flask, redirect, render_template, session, request, jsonify, Response, stream_with_context, send_from_directory
from flask_session import Session
from flask_cors import CORS, cross_origin
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from time import sleep
import time
from gettemp import gettemp
import RPi.GPIO as GPIO
import os
import json
import subprocess
import sqlite3
import re
import threading
from libcamera import controls, Transform
from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder, H264Encoder
from picamera2.outputs import FileOutput, FfmpegOutput
import io
import pigpio

LRPIN = 18
UDPIN = 13
LED_1_PIN = 35
LED_2_PIN = 37


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(LED_1_PIN, GPIO.OUT)
GPIO.setup(LED_2_PIN, GPIO.OUT)
pwm = pigpio.pi()
pwm.set_mode(UDPIN, pigpio.OUTPUT)
pwm.set_mode(LRPIN, pigpio.OUTPUT)
pwm.set_PWM_frequency(UDPIN, 50)
pwm.set_PWM_frequency(LRPIN, 50)
HLS_DIR = '/home/paco/babypi/flask/static/'

vidlog = ""
app = Flask(__name__, static_folder=HLS_DIR, static_url_path='')
cors = CORS(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = threading.Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

tuningpath = os.path.join(os.getcwd(),"tuning.json")
# tuningpath = '/home/paco/babypi/flask/tuning.json'
tuning = Picamera2.load_tuning_file(tuningpath)
picam = Picamera2(tuning=tuning)
config = picam.create_video_configuration(main={"size": (1920, 1080)}, controls={"AwbMode": controls.AwbModeEnum.Indoor, "NoiseReductionMode" : controls.draft.NoiseReductionModeEnum.Off, 'FrameDurationLimits': (40000, 40000)})
picam.configure(config)
encoder = MJPEGEncoder()
# videostream = io.BytesIO()
output = StreamingOutput()
picam.start_encoder(encoder, FileOutput(output))
# picam.start_recording(MJPEGEncoder(), FileOutput(output))
picam.start()


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def apology(reason):
    return {'error':reason}

def generateVideo():
    while True:
        with output.condition:
            output.condition.wait()
            frame = output.frame
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video.mjpg')
@login_required        
def video_feed():
    return Response(stream_with_context(generateVideo()), mimetype='multipart/x-mixed-replace; boundary=frame')
        

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/updates")
@login_required
def updates():
    ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    viewers = 0
    iplist = set()
    with open ("./logs/ip.log", "r") as file:
        for line in file:
            if "GET" in line:
                ipadd = ip_pattern.search(line)
                if ipadd:
                    ipadd = ipadd.group()
                    if ipadd not in iplist: 
                        iplist.add(ipadd)
            elif "Errno" in line:
                ipadd = ip_pattern.search(line)
                if ipadd:
                    ipadd = ipadd.group()
                    if ipadd in iplist:
                        iplist.remove(ipadd)
    viewers = len(iplist)
    temp = gettemp()
    return jsonify({'viewers' : viewers, "temp":temp})

@app.route("/data")
@login_required
def data():
    (UDValue, LRValue, flipped, led) = loadconfig()
    return f"App Loaded<hr>LRPIN : {LRPIN}<br>UDPIN : {UDPIN}<br>UDValue : {UDValue}<br>LRValue : {LRValue}<br>Flipped : {flipped}<hr>"

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/up")
@login_required
def up():
    (UDValue, LRValue, flipped, led) = loadconfig()
    if (flipped):
        if UDValue < 2500 :
            UDValue += 50
    else:
        if UDValue > 500 :
            UDValue -= 50
    pwm.set_servo_pulsewidth(UDPIN, UDValue) 
    saveconfig(UDValue, LRValue, flipped, led)
    return ('', 204)

@app.route("/down")
@login_required
def down():
    (UDValue, LRValue, flipped, led) = loadconfig()
    if (flipped):
        if UDValue > 500 :
            UDValue -= 50
    else:
        if UDValue < 2500 :
            UDValue += 50
    pwm.set_servo_pulsewidth(UDPIN, UDValue) 
    saveconfig(UDValue, LRValue, flipped, led)
    return ('', 204)

@app.route("/right")
@login_required
def right():
    (UDValue, LRValue, flipped, led) = loadconfig()
    if (flipped):
        if LRValue < 2500 :
            LRValue += 50
    else:
        if LRValue > 500 :
            LRValue -= 50
    pwm.set_servo_pulsewidth(LRPIN, LRValue) 
    saveconfig(UDValue, LRValue, flipped, led)
    return ('', 204)

@app.route("/left")
@login_required
def left():
    (UDValue, LRValue, flipped, led) = loadconfig()
    if (flipped):
        if LRValue > 500 :
            LRValue -= 50
    else:
        if LRValue < 2500 :
            LRValue += 50
    pwm.set_servo_pulsewidth(LRPIN, LRValue) 
    saveconfig(UDValue, LRValue, flipped, led)
    return ('', 204)

@app.route("/flip")
@login_required
def flip():
    global config
    (UDValue, LRValue, flipped, led) = loadconfig()
    picam.stop()
    if not flipped:
        flipped = True
    else:
        flipped = False
    config["transform"] = Transform(vflip=flipped)
    picam.configure(config)
    picam.start()
    saveconfig(UDValue, LRValue, flipped, led)
    return ('', 204)

@app.route("/led_on_off")
@login_required
def led_on_off():
    (UDValue, LRValue, flipped, led) = loadconfig()
    led = not led
    GPIO.output(LED_1_PIN, led)  
    GPIO.output(LED_2_PIN, led)
    saveconfig(UDValue, LRValue, flipped, led)
    return ('', 204)

def loadconfig():
    try:
        with open ("config.json", "r") as config:
            values = json.load(config)
            UDValue = values["UDValue"]
            LRValue = values["LRValue"]
            flipped = values["flipped"]
            led = values["led"]
            return (UDValue, LRValue, flipped, led)
    except OSError as e:
        saveconfig(7.5,7.5,False,False)
        loadconfig()

def saveconfig(UDValue, LRValue, flipped, led):
    with open ("config.json", "w") as config:
        data = {"UDValue" : UDValue,"LRValue" : LRValue,"flipped" : bool(flipped),"led":bool(led)}
        json.dump(data, config)

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        conn = sqlite3.connect("babycam.db")
        cur = conn.cursor()
        data = request.json
        username = data.get("username").lower()
        password = data.get("password")
        if not username:
            return apology("must provide username")
        elif not password:
            return apology("must provide password")
        cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = cur.fetchall()
        if len(rows) != 1 or not check_password_hash(rows[0][2], password):
            return apology("invalid username and/or password")
        session["user_id"] = rows[0][0]
        session["username"] = rows[0][1]
        user_id = session["user_id"]
        conn.close()
        return {'url':'/'}
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if request.method == "POST":
        conn = sqlite3.connect("babycam.db")
        cur = conn.cursor()
        data = request.json
        username = data.get("username").lower()
        password = data.get("password")
        confirmation = data.get("confirmation")
        passwordhash = generate_password_hash(password)
        cur.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        usernamecheck = cur.fetchone()
        if password != confirmation:
            return apology("Passwords do not match")
        if usernamecheck:
            return apology("Username Taken")
        elif not password:
            return apology("Please enter a password")
        elif not username:
            return apology("Please enter a username")
        else:
            cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, passwordhash,))
#            session["user_id"] = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username").lower(),)).fetchall()[0][0]
#            user_id = session["user_id"]
            conn.commit()
            conn.close()
            return jsonify({'url' : '/login'})
    else:
        return render_template("register.html")

@login_required
@app.route("/getOnce")
def getOnce():
    username = session["username"]
    # threading.Thread(target=start_ffmpeg).start()
    (UDValue, LRValue, flipped, led) = loadconfig()
    return jsonify({"username" : username.capitalize(), "led":led})

@app.route("/logout")
def logout():
	session.clear()
	return jsonify({"url":"/login"})


# picam2 = Picamera2()
# video_config = picam2.create_video_configuration()
# picam2.configure(video_config)

# encoder = H264Encoder(10000000)

# output = FfmpegOutput('-ac 1 -f webm pipe:1',audio_codec="libopus",audio_bitrate='96k', audio_device='plughw:2,0', audio=True)
# #movflags frag_keyframe+empty_moov 
# # print(output.stdout)

# picam2.start_recording(encoder, output)
# @app.route("/test.webm")
# def testmp4():
#     def generatemp4():
#         # time.sleep(10)
#         while True:
#             yield(output.stdout)
#     return Response(stream_with_context(generatemp4()), mimetype='video/webm')




playing = False
# @app.route('/audio/old')
# @login_required
# def stream_audio():
#     audio_output = StreamingOutput()
#     def generate():
#         # global playing
#         # if not playing:
#         # Define the command to process the audio with low latency options
#             #general_options = ['-loglevel', 'warning', '-y', '-fflags', 'nobuffer', '-flags', 'low_delay', '-strict', 'experimental']
#             # extras = ['-use_wallclock_as_timestamps', '1']
#             #audio_input = ['-f', 'pulse', '-sample_rate', '44100', '-thread_queue_size', '1024', '-i', 'default']
#             #audio_codec = ['-b:a', '128000', '-c:a', 'libvorbis']
#             #output_options = ['-f', 'webm', 'pipe:1']  # Output to stdout in WebM format
#             # video_input = ['-use_wallclock_as_timestamps', '1',
#             #            '-thread_queue_size', '64',  # necessary to prevent warnings
#             #            '-i', '/dev/video0']
#             # video_codec = ['-c:v', 'copy']

#             #command = ['ffmpeg'] + general_options + audio_input + audio_codec + output_options
#         command = ['ffmpeg', '-f', 'alsa', '-i', 'plughw:2,0', '-ac',
#             '1', '-c:a', 'libopus', '-b:a', '32k', '-f', 'webm', '-content_type', "'audio/webm'", 'pipe:1']

#             # Start the ffmpeg process without stdin
#         process = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=0)  # Set buffer size to 0 for reduced latency
#             # playing = True
            
#         # Read the output from ffmpeg's stdout and yield as stream
#         while True:
#             audio_output.write(process.stdout.read(1024))  # Read in smaller chunks for reduced latency
#             # if not output:
#             #     break
#             yield audio_output.frame

        # Wait for the process to finish
        # process.wait()

        # Check if the process was successful

    # return Response(stream_with_context(generate()), mimetype='audio/webm')


@app.route('/audio')
def serve_hls():
    global playing
    if playing == False:
        # command = ['ffmpeg', '-f', 'alsa','-i', 'plughw:2,0', '-ac', '1', '-c:a',
        # 'aac', '-b:a', '32K', '-f', 'hls', '-hls_time', '1', '-hls_list_size', '3', '-tune', 'zerolatency', '-hls_flags', 'delete_segments', './static/stream.m3u8']
        # audioprocess = subprocess.Popen(command, bufsize=0)  # Set buffer size to 0 for reduced latency
        command = [
    'ffmpeg', '-f', 'alsa', '-i', 'plughw:2,0',
    '-ac', '1', '-c:a', 'aac', '-b:a', '32K',
    '-f', 'hls', '-hls_time', '0.5', '-hls_list_size', '10',
    '-hls_flags', 'delete_segments', '-tune', 'zerolatency', './static/stream.m3u8'
        ]
        audioprocess = subprocess.Popen(command, bufsize=0)


        playing = True
    return send_from_directory(app.static_folder, 'stream.m3u8')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True, ssl_context=('cert.pem', 'key.pem'))
 #ssl_context=('cert.pem', 'key.pem'))
    # ssl_context='adhoc'

