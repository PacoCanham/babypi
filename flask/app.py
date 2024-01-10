#!/usr/bin/python3

from flask import Flask, redirect
import RPi.GPIO as GPIO
from time import sleep

LRPIN = 12
UDPIN = 33
UDValue = 7.5
LRPerc = 50

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(UDPIN, GPIO.OUT)
GPIO.setup(LRPIN, GPIO.OUT)
UD = GPIO.PWM(UDPIN, 50)
LR = GPIO.PWM(LRPIN, 50)



app = Flask(__name__)

@app.route("/")
def index():
    return f"App Loaded<hr>LRPIN : {LRPIN}<br>UDPIN : {UDPIN}<br>UDperc : {UDPerc}<br>LRperc : {LRPerc}<hr>"


@app.route("/up")
def up():
    global UDValue
    if UDValue < 12.5 :
        UDValue += 0.5
    UD.start(UDValue)
    sleep(0.05)
    UD.ChangeDutyCycle(0) #to stop random jitters
    return redirect("/")
    
@app.route("/down")
def down():
    global UDValue
    if UDValue > 2.0 :
        UDValue -= 0.5
    UD.start(UDValue)
    sleep(0.05)
    UD.ChangeDutyCycle(0) #to stop random jitters
    return redirect("/")

@app.route("/left")
def left():
    global LRPerc
    LRPerc -= 5
    rawValue = ((LRPerc/9) + 2)
    LR.start(rawValue)
    sleep(0.05)
    LR.ChangeDutyCycle(0)
    return redirect("/")

@app.route("/right")
def right():
    global LRPerc
    LRPerc += 5
    rawValue = ((LRPerc/9) + 2)
    LR.start(rawValue)
    sleep(0.05)
    LR.ChangeDutyCycle(0)
    return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
