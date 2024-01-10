from flask import Flask
import RPi.GPIO as GPIO

UDPerc = 50
LRPerc = 50
#set gpio pin numbering to boad
GPIO.setmode(GPIO.BOARD)
#set Left and Right pin number
LRPIN = 12
UDPIN = 33
# set lr pin to output
GPIO.setup(LRPIN, GPIO.OUT)
GPIO.setup(UDPIN, GPIO.OUT)
#set lr pin as pwm
LR = GPIO.PWM(LRPIN, 50)
UD = GPIO.PWM(UDPIN, 50)

app = Flask(__name__)

@app.route("/")
def index():
    return f"App Loaded\nLRPIN : {LRPIN}\nUDPIN : {UDPIN}\n UDperc : {UDPerc}\n LRperc : {LRPerc}\n"


@app.route("/up")
def up():
    global UDPerc
    rawValue = (((5/100)* UDPerc) + 5)
    UD.start(rawValue)
    UDPerc += 5
    # 1 frequency = 20ms
    # (1/20*100) = 0
    
    #left = 5
    #middle = 7.5
    #right = 10
    #(5/100 * perc)+5
    # 100% = 10    - 5 
    # 75% = 8.25   - 3.25
    # 50% = 7.5    - 2.5
    # 25% = 6.25   - 1.25
    # 0% = 5       - 0
    rawValue = (((5/100)* UDPerc) + 5)
    UD.ChangeDutyCycle(rawValue)
    UD.stop()
    return "up"
    
@app.route("/down")
def down():
    global UDPerc
    rawValue = (((5/100)* UDPerc) + 5)
    UD.start(rawValue)
    UDPerc -= 5
    rawValue = (((5/100)* UDPerc) + 5)
    UD.ChangeDutyCycle(rawValue)
    UD.stop()
    return "down"

@app.route("/left")
def left():
    global LRPerc
    rawValue = (((5/100)* LRPerc) + 5)
    LR.start(rawValue)
    LRPerc += 5
    rawValue = (((5/100)* LRPerc) + 5)
    LR.ChangeDutyCycle(rawValue)
    LR.stop()
    return "left"

@app.route("/right")
def right():
    global LRPerc
    rawValue = (((5/100)* LRPerc) + 5)
    LR.start(rawValue)
    LRPerc -= 5
    rawValue = (((5/100)* LRPerc) + 5)
    LR.ChangeDutyCycle(rawValue)
    LR.stop()
    return "right"
