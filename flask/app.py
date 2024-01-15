#!/usr/bin/python3

from flask import Flask, redirect, render_template
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import RPi.GPIO as GPIO
from time import sleep
import os
import json
import sqlite3

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
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = sqlite3.connect("babycam.db")
db = db.cursor()

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/data")
@login_required
def data():
    (UDValue,LRValue,flipped) = loadconfig()
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
@login_required
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
@login_required
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
@login_required
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
@login_required
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

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username").lower())
        rows = rows.fetchall()
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)
        session["user_id"] = rows[0]["id"]
        user_id = session["user_id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username").lower()
        passwordhash = generate_password_hash(request.form.get("password"))
        usernamecheck = db.execute("SELECT 1 FROM users WHERE username = ?", username)
        usernamecheck = usernamecheck.fetchall()
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match")
        if usernamecheck:
            return apology("Username Taken")
        elif not request.form.get("password"):
            return apology("Please enter a password")
        elif not request.form.get("username"):
            return apology("Please enter a username")
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, passwordhash)
            session["user_id"] = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username").lower())[0]["id"]
            user_id = session["user_id"]
            return redirect("/")
    else:
        return render_template("register.html")

if __name__ == '__main__':
    os.system('./mjpeg2.py &')
    app.run(host='0.0.0.0', port=5000, debug=False)
