#!../../.babycamvenv/bin/python3
from flask import Flask, redirect, render_template, session, request, jsonify, Response, stream_with_context, send_from_directory
from flask_session import Session
from flask_cors import CORS, cross_origin
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from time import sleep, time
import pyaudio

from datetime import datetime,timedelta
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
#from audiotest import process_audio_from_ffmpeg
import io
import pigpio
import vlc
from PIL import Image
import requests
import cv2
import numpy as np

LRPIN = 18
UDPIN = 13
LED_1_PIN = 35
LED_2_PIN = 37

active_users = 0
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

app = Flask(__name__, static_folder=HLS_DIR, static_url_path='')
cors = CORS(app)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

user_activity_log = {}

class CustomAudioPlayer:
    def __init__(self):
        self.instance = vlc.Instance('--input-repeat=-1')
        self.player = self.instance.media_player_new()
        self.playing = False
        self.current_track = None

    def play(self, track):
        if not self.playing:
            self.playing = True
            self.current_track = self.instance.media_new(track)
            self.player.set_media(self.current_track)
            self.player.play()

    def pause(self):
        if self.playing:
            self.playing = False
            self.player.pause()

    def resume(self):
        if not self.playing and self.current_track:
            self.playing = True
            self.player.play()

    def stop(self):
        if self.playing:
            self.playing = False
            self.player.stop()

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = threading.Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

    def save(self, filename):
        if self.frame is not None:
            image = Image.open(io.BytesIO(self.frame))
            image.save(filename)
        else:
            print("No frame available")

    def return_bytes(self):
        if self.frame is not None:
            return io.BytesIO(self.frame)
        else:
            print("No frame available")
            return None

    def return_array(self):
        if self.frame is not None:
            image = Image.open(io.BytesIO(self.frame))
            return np.array(image)
        else:
            print("No frame available")
            return None

tuningpath = os.path.join(os.getcwd(),"tuning.json")
#tuningpath = '/home/paco/babypi/flask/tuning.json'
tuning = Picamera2.load_tuning_file(tuningpath)
picam = Picamera2(tuning=tuning)
config = picam.create_video_configuration(main={"size": (1920, 1080)}, lores={"size":(320,240)}, controls={"AwbMode": controls.AwbModeEnum.Indoor, "NoiseReductionMode" : controls.draft.NoiseReductionModeEnum.Off, 'FrameDurationLimits': (40000, 40000)})
picam.configure(config)
encoder = MJPEGEncoder()
# videostream = io.BytesIO()
output = StreamingOutput()
picam.start_encoder(encoder, FileOutput(output))
picam.start_recording(MJPEGEncoder(), FileOutput(output))
#picam.start()
noise_player = CustomAudioPlayer()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# @app.route("/movement")
def movement():
    movement_count = 0
    lastP3notification = 0
    continuous_movement = False
    while True:
        try:
            image1 = output.return_array()
            sleep(0.1)
            image2 = output.return_array()
            # Convert the images to grayscale
            gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

            # Compute the absolute difference between the two images
            diff = cv2.absdiff(gray1, gray2)

            # Apply a binary threshold to the difference (you can adjust the threshold value as needed)
            _, thresholded_diff = cv2.threshold(diff, 60, 255, cv2.THRESH_BINARY)

            # Count the number of white pixels in the thresholded image
            white_pixels = np.sum(thresholded_diff == 255)

            if white_pixels > 1000 :
                movement_count += 1
                print(f"Motion Detected {movement_count} times")
                if movement_count > 4 :
                    if not continuous_movement :
                        if time() - lastP3notification >= 600:  # 600 seconds = 10 minutes
                            priority = '3'
                            title = "Movement Detected"
                            tags = "warning"
                            lastP3notification = time()  # Update the timestamp
                            requests.put("https://192.168.4.182:8181/babycam",
                            data=output.return_bytes().getvalue(),
                            headers={ "Filename": "Blanca",
                            "Title" : title,
                            "Tags" : tags,
                            "Priority" : priority
                            })
                    continuous_movement = True
                    print("Waiting 30s to check for movement")
                    sleep(30)
                    image1_after_sleep = output.return_array()
                    sleep(0.1)
                    image2_after_sleep = output.return_array()
                    gray1_after_sleep = cv2.cvtColor(image1_after_sleep, cv2.COLOR_BGR2GRAY)
                    gray2_after_sleep = cv2.cvtColor(image2_after_sleep, cv2.COLOR_BGR2GRAY)

                    diff_after_sleep = cv2.absdiff(gray2_after_sleep, gray1_after_sleep)
                    _, thresholded_diff_after_sleep = cv2.threshold(diff_after_sleep, 60, 255, cv2.THRESH_BINARY)
                    white_pixels_after_sleep = np.sum(thresholded_diff_after_sleep == 255)
                    if white_pixels_after_sleep > 1000:
                        priority = '4'
                        title = "Continuous Movement (Over 30 Seconds!)"
                        tags = "bangbang"
                        requests.put("https://192.168.4.182:8181/babycam",
                        data=output.return_bytes().getvalue(),
                        headers={ "Filename": "Blanca",
                        "Title" : title,
                        "Tags" : tags,
                        "Priority" : priority
                        })
                    else:
                        continuous_movement = False
                        movement_count = 0
            else:
                continuous_movement = False
                movement_count = 0
            sleep(1)
        except Exception as e:
            print(e)
            print("Waiting for first frame")
            sleep(5)

mov = threading.Thread(target=movement)
mov.start()

@app.route("/hourly")
@login_required
def hourly():
    requests.put("https://192.168.4.182:8181/babycam",
    data=output.return_bytes().getvalue(),
    headers={ "Filename": "Blanca",
    "Title" : "Photo of Blanca"
    # "Icon": "https://pacocanham.ddns.net:18244/file/7aSMfeESZbmy.jpg"
     })
    # with open('output.jpg', 'wb') as f:
        # f.write(test.getvalue())
    return "Notification Sent", 200


@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.before_request
def update_user_count():
    if "user_id" in session:
        if active_users == 0:
            picam.start()

        user_id = session["user_id"]
        user_activity_log[user_id] = datetime.now()
        user_check()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

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

def apology(reason):
    return {'error':reason}

def user_check():
    global active_users
    timeout = timedelta(minutes=1)
    active_users = sum(1 for timestamp in user_activity_log.values() if timestamp > datetime.now() - timeout)
#     if active_users == 0 :
#         picam.stop()
#         stop_ffmpeg()

# def run_user_check():
#     while True:
#         user_check()
#         time.sleep(45)

#threading.Thread(target=process_audio_from_ffmpeg).start()

@app.route("/updates")
@login_required
def updates():
    user_check()
    temp = gettemp()
    return jsonify({'viewers' : active_users, "temp":temp})

@app.route("/up")
@login_required
def up():
    (UDValue, LRValue, flipped, led, volume, trackname, playstate) = loadconfig()
    if (flipped):
        if UDValue < 2500 :
            UDValue += 50
    else:
        if UDValue > 500 :
            UDValue -= 50
    pwm.set_servo_pulsewidth(UDPIN, UDValue) 
    saveconfig(UDValue, LRValue, flipped, led, volume, trackname, playstate)
    return ('', 204)

@app.route("/down")
@login_required
def down():
    (UDValue, LRValue, flipped, led, volume, trackname, playstate) = loadconfig()
    if (flipped):
        if UDValue > 500 :
            UDValue -= 50
    else:
        if UDValue < 2500 :
            UDValue += 50
    pwm.set_servo_pulsewidth(UDPIN, UDValue) 
    saveconfig(UDValue, LRValue, flipped, led, volume, trackname, playstate)
    return ('', 204)

@app.route("/right")
@login_required
def right():
    (UDValue, LRValue, flipped, led, volume, trackname, playstate) = loadconfig()
    if (flipped):
        if LRValue < 2500 :
            LRValue += 50
    else:
        if LRValue > 500 :
            LRValue -= 50
    pwm.set_servo_pulsewidth(LRPIN, LRValue) 
    saveconfig(UDValue, LRValue, flipped, led, volume, trackname, playstate)
    return ('', 204)

@app.route("/left")
@login_required
def left():
    (UDValue, LRValue, flipped, led, volume, trackname, playstate) = loadconfig()
    if (flipped):
        if LRValue > 500 :
            LRValue -= 50
    else:
        if LRValue < 2500 :
            LRValue += 50
    pwm.set_servo_pulsewidth(LRPIN, LRValue) 
    saveconfig(UDValue, LRValue, flipped, led, volume, trackname, playstate)
    return ('', 204)

@app.route("/flip")
@login_required
def flip():
    global config
    (UDValue, LRValue, flipped, led, volume, trackname, playstate) = loadconfig()
    picam.stop()
    if not flipped:
        flipped = True
    else:
        flipped = False
    config["transform"] = Transform(vflip=flipped)
    picam.configure(config)
    picam.start()
    saveconfig(UDValue, LRValue, flipped, led, volume, trackname, playstate)
    return ('', 204)

@app.route("/led_on_off")
@login_required
def led_on_off():
    (UDValue, LRValue, flipped, led, volume, trackname, playstate) = loadconfig()
    led = not led
    GPIO.output(LED_1_PIN, led)  
    GPIO.output(LED_2_PIN, led)
    saveconfig(UDValue, LRValue, flipped, led, volume, trackname, playstate)
    return ('', 204)

def loadconfig():
    try:
        with open ("config.json", "r") as config:
            values = json.load(config)
            UDValue = values["UDValue"]
            LRValue = values["LRValue"]
            flipped = values["flipped"]
            led = values["led"]
            volume = values["volume"]
            trackname = values["trackname"]
            playstate = values["playstate"]
            return (UDValue, LRValue, flipped, led, volume, trackname, playstate)
    except OSError as e:
        saveconfig(7.5,7.5,False,False,20,"30-Stream-60min.mp3",False)
        loadconfig()

def saveconfig(UDValue, LRValue, flipped, led, volume, trackname, playstate):
    with open ("config.json", "w") as config:
        data = {"UDValue" : UDValue,"LRValue" : LRValue,"flipped" : bool(flipped),"led":bool(led),"volume":int(volume),"trackname":trackname,"playstate":playstate}
        json.dump(data, config)

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
    (UDValue, LRValue, flipped, led, volume, trackname, playstate) = loadconfig()
    return jsonify({"username" : username.capitalize(), "led":led, "volume":volume, "playstate":playstate,})

@app.route("/logout")
def logout():
    session.clear()
    return jsonify({'url' : '/login'})

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

@app.route('/audio')
def serve_hls():
    return send_from_directory(app.static_folder, 'stream.m3u8')

@app.route('/restart_cam')
@login_required
def restart_cam():
    picam.stop()
    sleep(0.5)
    # picam.start_encoder(encoder, FileOutput(output))
    # sleep(0.5)
    picam.start()
    return jsonify(message="Camera Restarted")


noiselist = []
for filename in os.listdir(f'{HLS_DIR}/noise/'):
    if os.path.isfile(f'{HLS_DIR}/noise/{filename}'):
        noiselist.append(filename)

noise_started = False
noise_paused = False

@login_required
@app.route('/noiselist')
def get_noiselist():
    (UDValue, LRValue, flipped, led, volume, trackname, playstate) = loadconfig()
    return jsonify({'noiselist':noiselist, "playstate":playstate, "trackname":trackname, "volume":volume})

@login_required
@app.route('/change_noise/<noisename>')
def change_noise(noisename):
    (UDValue, LRValue, flipped, led, volume, trackname, playstate) = loadconfig()
    if noisename in noiselist:
        trackname = noisename
        print(f"track changed to {trackname}")
    else :
        print(f"track change failed {trackname}")
    if playstate:
        noise_player.stop()
        noise_player.play(f'{HLS_DIR}/noise/{trackname}')
        print(f"continuing to play {HLS_DIR}/noise/{trackname}")
        playstate = True
    saveconfig(UDValue, LRValue, flipped, led, volume, trackname, playstate)
    return "ok"

@login_required
@app.route('/noise')
def nosie():
    (UDValue, LRValue, flipped, led, volume, trackname, playstate) = loadconfig()
    global noise_started
    global noise_paused
    if noise_started == False:
        setVolume(volume)
        noise_player.play(f'{HLS_DIR}/noise/{trackname}')
        noise_started = True
        playstate = True
    elif noise_started and not noise_paused:
        noise_player.pause()
        noise_started = True
        noise_paused = True
        playstate = False
    elif noise_started and noise_paused:
        noise_player.resume()
        noise_started = True
        noise_paused = False
        playstate = True
    saveconfig(UDValue, LRValue, flipped, led, volume, trackname, playstate)
    return "ok"

@login_required
@app.route('/setVolume/<newVolume>')
def setVolume(newVolume):
    (UDValue, LRValue, flipped, led, volume, trackname, playstate) = loadconfig()
    volume = newVolume
    command = ["amixer", "-M", "set", "PCM", f"{volume}%"]
    subprocess.run(command, shell=False)
    saveconfig(UDValue, LRValue, flipped, led, volume, trackname, playstate)
    return f"volume now : {volume}", 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
    #  ssl_context=('pacocanham.ddns.net.crt', 'pacocanham.ddns.net.key'))
 #ssl_context=('cert.pem', 'key.pem'))
    # ssl_context='adhoc'

