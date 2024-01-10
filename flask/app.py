from flask import Flask, redirect
import RPi.GPIO as GPIO

LRPIN = 12
UDPIN = 33
UDPerc = 50
LRPerc = 50


def startup():
    GPIO.setmode(GPIO.BOARD)

def UDStart():
    print(UDPIN)
    print(UDPerc)
    GPIO.setup(UDPIN, GPIO.OUT)
    UD = GPIO.PWM(UDPIN, 50)
    UD.start(0)

def UDStop():
    UD.ChangeDutyCycle(0)
    UD.stop()
    GPIO.setup(UDPIN, GPIO.IN)

def LRStop():
    LR.ChangeDutyCycle(0)
    LR.stop()
    GPIO.setup(LRPIN, GPIO.IN)


def LRStart():
    print(LRPIN)
    print(LRPerc)
    GPIO.setup(LRPIN, GPIO.OUT)
    LR = GPIO.PWM(LRPIN, 50)
    LR.start(0)

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
    UDStart()
    UDPerc += 5
    rawValue = ((UDPerc/10) + 2)
    UD.ChangeDutyCycle(rawValue)
    UDStop()
    # UD.stop()
    return redirect("/")
    
@app.route("/down")
def down():
    UDStart()
    UDPerc -= 5
    rawValue = ((UDPerc/10) + 2)
    UD.ChangeDutyCycle(rawValue)
    UDStop()
    return redirect("/")

@app.route("/left")
def left():
    LRStart()
    LRPerc -= 5
    rawValue = ((LRPerc/10) + 2)
    LR.ChangeDutyCycle(rawValue)
    LRStop()
    return redirect("/")

@app.route("/right")
def right():
    LRStart()
    LRPerc += 5
    rawValue = ((LRPerc/10) + 2)
    LR.ChangeDutyCycle(rawValue)
    LRStop()
    return redirect("/")

if __name__ == '__main__':
    startup()
    app.run(host='0.0.0.0', port=5000, debug=False)
