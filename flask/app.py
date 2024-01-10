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

def LRStop(LR):
    LR.ChangeDutyCycle(0)
    LR.stop()
    GPIO.setup(LRPIN, GPIO.IN)

def LRStart():
    print(LRPIN)
    print(LRPerc)
    GPIO.setup(LRPIN, GPIO.OUT)
    LR = GPIO.PWM(LRPIN, 50)
    LR.start(0)
    return LR

app = Flask(__name__)

@app.route("/")
def index():
    return f"App Loaded<hr>LRPIN : {LRPIN}<br>UDPIN : {UDPIN}<br>UDperc : {UDPerc}<br>LRperc : {LRPerc}<hr>"


@app.route("/up")
def up():
    # global UDPerc
    # rawValue = (((5/100)* UDPerc) + 5)
    # rawValue = ((UDPerc/10) + 2)
    # UD.start(rawValue)
    # UDPerc += 5
    # 1 frequency = 20ms
    # (1/20*100) = 0
    # ((rawValue - 2)/(12-2))*100 = UDPerc
    # UDPerc/10 + 2 = rawValue
    
    #left = 5
    #middle = 7.5
    #right = 10
    #(0.1 * perc)+2
    # 100% = 12    - 5 
    # 75% = 8.25   - 3.25
    # 50% = 7.5    - 2.5
    # 25% = 6.25   - 1.25
    # 0% = 2       - 0
    # rawValue = (((5/100)* UDPerc) + 5)
    global UDPerc
    UD.start(0)
    UDPerc += 5
    rawValue = ((UDPerc/10) + 2)
    UD.ChangeDutyCycle(rawValue)
    UD.stop()
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
