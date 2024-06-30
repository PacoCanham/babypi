#!../../.babycamvenv/bin/python3
from flask import Flask, redirect, render_template, session, request, jsonify, Response, stream_with_context, send_from_directory
from flask_session import Session
from flask_cors import CORS, cross_origin
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from time import sleep, time
from modules.classes import *
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
import io
import pigpio
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
settings = {'camera' : 
{'UDValue':1750, 'LRValue':1750, 'flipped':False, 'led':False, 
'volume': 20, 'trackname':'30-Stream-60min.mp3', 'playstate':False}, 
'notifications':{'video':{'Vee': {
        'movThres': 60,
        'movNumLow': 3,
        'movNumHigh': 30,
        'notificationDelay': 600,
        'enabled' : True
    },
    'Paco': {
        'movThres': 250,
        'movNumLow': 3,
        'movNumHigh': 30,
        'notificationDelay': 600,
        'enabled' : True

    }}, 'audio':{
        'Vee': {
        'delayLow': 600,
        'delayHigh': 1800,
        'volumeLow': 100,
        'volumeHigh': 1000,
        'sampleLength': 3,
        'enabled' : True

    },
    'Paco': {
        'delayLow': 600,
        'delayHigh': 1800,
        'volumeLow': 100,
        'volumeHigh': 1000,
        'sampleLength': 3,
        'enabled' : True
    }
    }}}

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

import modules.notification_settings

# settings["notifications"] = {"move_threshold":60, "detection_threshold":1000, "movement_count_low" : 4, "movement_count_high":30,"delaytime_low":600,"delaytime_high":600}

def detect_movement():
    movement_count = 0
    lastNotification = 0
    while True:
        try:
            for curUser in ["paco", "vee"]:
                if settingssettings["notifications"]['video'][curUser.capitalize()]["enabled"] == True:
                    image1 = output.return_array()
                    sleep(0.25)
                    image2 = output.return_array()
                    # Convert the images to grayscale
                    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
                    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)

                    # Compute the absolute difference between the two images
                    diff = cv2.absdiff(gray1, gray2)

                    # Apply a binary threshold to the difference (you can adjust the threshold value as needed)
                    _, thresholded_diff = cv2.threshold(diff, settingssettings["notifications"]['video'][curUser.capitalize()]["move_threshold"], 255, cv2.THRESH_BINARY)

                    # Count the number of white pixels in the thresholded image
                    white_pixels = np.sum(thresholded_diff == 255)

                    if white_pixels > settingssettings["notifications"]['video'][curUser.capitalize()]["detection_threshold"] :
                        movement_count += 1
                        print(f"Motion Detected {movement_count} times")
                        if movement_count == settingssettings["notifications"]['video'][curUser.capitalize()]["movement_count_low"] :
                            if time() - lastNotification >= settingssettings["notifications"]['video'][curUser.capitalize()]["delaytime_low"]:  # 600 seconds = 10 minutes
                                priority = '3'
                                title = "Movement Detected"
                                tags = "warning"
                                lastP3notification = time()  # Update the timestamp
                                requests.put(f"https://192.168.4.182:8181/babycam{curUser.capitalize()}",
                                data=output.return_bytes().getvalue(),
                                headers={ "Filename": "Blanca",
                                "Title" : title,
                                "Tags" : tags,
                                "Priority" : priority
                                })
                        elif movement_count == settingssettings["notifications"]['video'][curUser.capitalize()]["movement_count_high"] :
                            if time() - lastNotification >= settingssettings["notifications"]['video'][curUser.capitalize()]["delaytime_high"]:  # 600 seconds = 10 minutes
                                priority = '4'
                                title = f'Continuous Movement (Over {settings["notifications"]["video"][session["username"].capitalize()]["movement_count_high"]} Seconds!)'
                                tags = "bangbang"
                                requests.put(f"https://192.168.4.182:8181/babycam{curUser.capitalize()}",
                                data=output.return_bytes().getvalue(),
                                headers={ "Filename": "Blanca",
                                "Title" : title,
                                "Tags" : tags,
                                "Priority" : priority
                                })
                    else:
                        movement_count = 0
                else:
                    loadconfig()
                    sleep(5)
                sleep(0.5)
        except Exception as e:
            print("Waiting for first frame")
            print(e)
            sleep(5)

mov = threading.Thread(target=detect_movement)
mov.start()


@app.route("/toggleNotifications")
@login_required
def toggleNotifications():
    settings['notifications']['video'][session['username'].capitalize()]['enabled'] = not settings['notifications']['video'][session['username'].capitalize()]['enabled']  
    settings['notifications']['audio'][session['username'].capitalize()]['enabled'] = not settings['notifications']['audio'][session['username'].capitalize()]['enabled']  
    saveconfig()
    return "ok", 200
    
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


@app.route("/updates")
@login_required
def updates():
    user_check()
    temp = gettemp()
    return jsonify({'viewers' : active_users, "temp":temp})


@app.route("/move/<direction>")
@login_required
def move(direction):
    match (direction):
        case ("up"):
                if (settings["camera"]["flipped"]):
                    if settings["camera"]["UDValue"] < 2500 :
                        settings["camera"]["UDValue"] += 50
                else:
                    if settings["camera"]["UDValue"] > 500 :
                        settings["camera"]["UDValue"] -= 50
        case ("down"):
                if settings["camera"]["flipped"]:
                    if settings["camera"]["UDValue"] > 500 :
                        settings["camera"]["UDValue"] -= 50
                else:
                    if settings["camera"]["UDValue"] < 2500 :
                        settings["camera"]["UDValue"] += 50
        case ("right"):
                if settings["camera"]["flipped"]:
                    if settings["camera"]["LRValue"] < 2500 :
                        settings["camera"]["LRValue"] += 50
                else:
                    if settings["camera"]["LRValue"] > 500 :
                        settings["camera"]["LRValue"] -= 50
        case ("left"):
                if settings["camera"]["flipped"]:
                    if settings["camera"]["LRValue"] > 500 :
                        settings["camera"]["LRValue"] -= 50
                else:
                    if settings["camera"]["LRValue"] < 2500 :
                        settings["camera"]["LRValue"] += 50
    pwm.set_servo_pulsewidth(UDPIN, settings["camera"]["UDValue"]) 
    pwm.set_servo_pulsewidth(LRPIN, settings["camera"]["LRValue"]) 
    saveconfig()
    return ('', 204)


@app.route("/flip")
@login_required
def flip():
    global config
    picam.stop()
    if not settings["camera"]["flipped"]:
        settings["camera"]["flipped"] = True
    else:
        settings["camera"]["flipped"] = False
    config["transform"] = Transform(vflip=flipped)
    picam.configure(config)
    picam.start()
    saveconfig()
    return ('', 204)

@app.route("/led_on_off")
@login_required
def led_on_off():
    led = not settings["camera"]["led"]
    settings["camera"]["led"] = led
    GPIO.output(LED_1_PIN, led)  
    GPIO.output(LED_2_PIN, led)
    saveconfig()
    return ('', 204)

@app.route("/getNotificationSettings")
@login_required
def get_notifications_settings():
    return jsonify(settings["notifications"]['video'][session['username'].capitalize()])

def loadconfig():
    try:
        with open ("config.json", "r") as config:
            settings = json.load(config)
    except OSError as e:
        saveconfig()
        loadconfig()

def saveconfig():
    with open ("config.json", "w") as config:
        json.dump(settings, config)

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
            conn.commit()
            conn.close()
            return jsonify({'url' : '/login'})
    else:
        return render_template("register.html")

@login_required
@app.route("/getOnce")
def getOnce():
    username = session["username"]
    return jsonify({"username" : username.capitalize(), "led":settings["camera"]["led"], "volume":settings["camera"]["volume"], "playstate":settings["camera"]["playstate"]})

@app.route("/logout")
def logout():
    session.clear()
    return render_template("login.html")

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
    return jsonify({'noiselist':noiselist, "playstate":settings["camera"]["playstate"], "trackname":settings["camera"]["trackname"], "volume":settings["camera"]["volume"]})

@login_required
@app.route('/change_noise/<noisename>')
def change_noise(noisename):
    if noisename in noiselist:
        settings["camera"]["trackname"] = noisename
        print(f'track changed to {settings["camera"]["trackname"]}')
    else :
        print(f'track change failed {settings["camera"]["trackname"]}')
    if playstate:
        noise_player.stop()
        noise_player.play(f'{HLS_DIR}/noise/{settings["camera"]["trackname"]}')
        print(f'continuing to play {HLS_DIR}/noise/{settings["camera"]["trackname"]}')
        playstate = True
    saveconfig()
    return "ok"

@login_required
@app.route('/noise')
def nosie():
    global noise_started
    global noise_paused
    if noise_started == False:
        setVolume(volume)
        noise_player.play(f'{HLS_DIR}/noise/{settings["camera"]["trackname"]}')
        noise_started = True
        settings["camera"]["playstate"] = True
    elif noise_started and not noise_paused:
        noise_player.pause()
        noise_started = True
        noise_paused = True
        settings["camera"]["playstate"] = False
    elif noise_started and noise_paused:
        noise_player.resume()
        noise_started = True
        noise_paused = False
        settings["camera"]["playstate"] = True
    saveconfig()
    return "ok"

@login_required
@app.route('/setVolume/<newVolume>')
def setVolume(newVolume):
    settings["camera"]["volume"] = newVolume
    command = ["amixer", "-M", "set", "PCM", f"{newVolume}%"]
    subprocess.run(command, shell=False)
    saveconfig()
    return f"volume now : {newVolume}", 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=443, debug=False, threaded=True,ssl_context=('pacocanham.ddns.net.crt', 'pacocanham.ddns.net.key'))
