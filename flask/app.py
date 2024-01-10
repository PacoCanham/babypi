#!/usr/bin/python3

from flask import Flask, redirect
import RPi.GPIO as GPIO
from time import sleep

LRPIN = 12
UDPIN = 33
UDValue = 7.5
LRPerc = 7.5

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(UDPIN, GPIO.OUT)
GPIO.setup(LRPIN, GPIO.OUT)
UD = GPIO.PWM(UDPIN, 50)
LR = GPIO.PWM(LRPIN, 50)



app = Flask(__name__)

@app.route("/")
def index():
    return f"App Loaded<hr>LRPIN : {LRPIN}<br>UDPIN : {UDPIN}<br>UDValue : {UDValue}<br>LRperc : {LRPerc}<hr>"


@app.route("/up")
def up():
    global UDValue
    if UDValue > 3.0 :
        UDValue -= 0.25
    print(UDValue)
    UD.start(UDValue)
    sleep(0.05)
    UD.ChangeDutyCycle(UDValue) #to ensure movement
    UD.ChangeDutyCycle(0) #to stop random jitters
    return redirect("/")
    
@app.route("/down")
def down():
    global UDValue
    if UDValue < 12.5 :
        UDValue += 0.25
    print(UDValue)
    UD.start(UDValue)
    # sleep(0.05)
    UD.ChangeDutyCycle(UDValue) #to ensure movement
    UD.ChangeDutyCycle(0) #to stop random jitters
    return redirect("/")

@app.route("/left")
def left():
    global LRValue
    if LRValue > 3.0 :
        LRValue -= 0.25
    print(LRValue)
    UD.start(LRValue)
    # sleep(0.05)
    UD.ChangeDutyCycle(LRValue) #to ensure movement
    UD.ChangeDutyCycle(0) #to stop random jitters
    return redirect("/")

@app.route("/right")
def right():
    global LRValue
    if LRValue < 12.5 :
        LRValue += 0.25
    print(LRValue)
    UD.start(LRValue)
    # sleep(0.05)
    UD.ChangeDutyCycle(LRValue) #to ensure movement
    UD.ChangeDutyCycle(0) #to stop random jitters
    return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
