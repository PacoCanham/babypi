#!/usr/bin/python3

from flask import Flask, redirect, render_template
import RPi.GPIO as GPIO
from time import sleep
import os
import json

LRPIN = 12
UDPIN = 33

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(UDPIN, GPIO.OUT)
GPIO.setup(LRPIN, GPIO.OUT)
UD = GPIO.PWM(UDPIN, 50)
LR = GPIO.PWM(LRPIN, 50)
UD.start(0)
LR.start(0)

app = Flask(__name__)

@app.route("/")
def index():
#    (UDValue,LRValue,flipped) = loadconfig()
#    return f"App Loaded<hr>LRPIN : {LRPIN}<br>UDPIN : {UDPIN}<br>UDValue : {UDValue}<br>LRValue : {LRValue}<br>Flipped : {flipped}<hr>"
    return render_template("index.html")

@app.route("/up")
def up():
    (UDValue,LRValue,flipped) = loadconfig()
    UD.ChangeDutyCycle(UDValue) #to ensure movement
    sleep(0.1)
    if UDValue > 3.0 :
        UDValue -= 0.25
    UD.ChangeDutyCycle(UDValue) #to ensure movement
    sleep(0.5)
    UD.ChangeDutyCycle(0) #to stop random jitters
    saveconfig(UDValue,LRValue,flipped)
    return redirect("/")
    
@app.route("/down")
def down():
    (UDValue,LRValue,flipped) = loadconfig()
    UD.ChangeDutyCycle(UDValue) #to ensure movement
    sleep(0.1)
    if UDValue < 12.5 :
        UDValue += 0.25
    UD.ChangeDutyCycle(UDValue) #to ensure movement
    sleep(0.5)
    UD.ChangeDutyCycle(0) #to stop random jitters
    saveconfig(UDValue,LRValue,flipped)
    return redirect("/")

@app.route("/right")
def right():
    (UDValue,LRValue,flipped) = loadconfig()
    LR.ChangeDutyCycle(LRValue) #to ensure movement
    sleep(0.1)
    if LRValue > 3.0 :
        LRValue -= 0.25
    LR.ChangeDutyCycle(LRValue) #to ensure movement
    sleep(0.5)
    LR.ChangeDutyCycle(0) #to stop random jitters
    saveconfig(UDValue,LRValue,flipped)
    return redirect("/")

@app.route("/left")
def left():
    (UDValue,LRValue,flipped) = loadconfig()
    LR.ChangeDutyCycle(LRValue) #to ensure movement
    sleep(0.1)
    if LRValue < 12.5 :
        LRValue += 0.25
    LR.ChangeDutyCycle(LRValue) #to ensure movement
    sleep(0.5)
    LR.ChangeDutyCycle(0) #to stop random jitters
    saveconfig(UDValue,LRValue,flipped)
    return redirect("/")

@app.route("/flip")
def flip():
    (UDValue, LRValue, flipped) = loadconfig()
    if not flipped:
        os.system('killall mjpeg*')
        os.system('./mjpeg2.py vflip &')
        flipped = True
    else:
        os.system('killall mjpeg*')
        os.system('./mjpeg2.py &')
        flipped = False
    saveconfig(UDValue,LRValue,flipped)
    return redirect("/")

def loadconfig():
    try:
        with open ("config.json", "r") as config:
            values = json.load(config)
            UDValue = values["UDValue"]
            LRValue = values["LRValue"]
            flipped = values["flipped"]
            return (UDValue, LRValue, flipped)
    except OSError as e:
        saveconfig(7.5,7.5,False)
        loadconfig()

def saveconfig(UDValue, LRValue, flipped):
    with open ("config.json", "w") as config:
        data = {"UDValue" : UDValue,"LRValue" : LRValue,"flipped" : bool(flipped)}
        json.dump(data, config)

if __name__ == '__main__':
    os.system('./mjpeg2.py &')
    app.run(host='0.0.0.0', port=5000, debug=False)
