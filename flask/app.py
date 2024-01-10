#!/usr/bin/python3

from flask import Flask, redirect
import RPi.GPIO as GPIO

LRPIN = 12
UDPIN = 33
UDPerc = 50
LRPerc = 50

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(UDPIN, GPIO.OUT)
UD = GPIO.PWM(UDPIN, 50)
UD.start(7.5)


app = Flask(__name__)

@app.route("/")
def index():
    return f"App Loaded<hr>LRPIN : {LRPIN}<br>UDPIN : {UDPIN}<br>UDperc : {UDPerc}<br>LRperc : {LRPerc}<hr>"


@app.route("/up")
def up():
    # global UDPerc
    UD.start(0)
    # UDPerc += 5
    # rawValue = ((UDPerc/10) + 2)
    UD.ChangeDutyCycle(12)
    return redirect("/")
    
@app.route("/down")
def down():
    global UDPerc
    UDStart()
    UDPerc -= 5
    rawValue = ((UDPerc/10) + 2)
    UD.ChangeDutyCycle(rawValue)
    UDStop()
    return redirect("/")

@app.route("/left")
def left():
    global LRPerc
    LR = LRStart()
    LRPerc -= 5
    rawValue = ((LRPerc/10) + 2)
    print(f"rawValue : {rawValue}")
    LR.ChangeDutyCycle(rawValue)
    LRStop(LR)
    return redirect("/")

@app.route("/right")
def right():
    global LRPerc
    LR = LRStart()
    LRPerc += 5
    rawValue = ((LRPerc/10) + 2)
    LR.ChangeDutyCycle(rawValue)
    LRStop(LR)
    return redirect("/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
