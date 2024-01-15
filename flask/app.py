#!/usr/bin/python3

from flask import Flask, redirect, render_template, session, request
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import RPi.GPIO as GPIO
from time import sleep
import os
import json
import subprocess
#from cs50 import SQL
import sqlite3
import re

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

vidlog = ""
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#db = SQL("sqlite:///babycam.db")
dbloc = sqlite3.connect("babycam.db",  check_same_thread=False)
db = dbloc.cursor()

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

def apology(reason):
    return "<html><head><title>Babycam</title></head><body style='text-align:center'><h1>Error</h1><h2>" + reason + "</h2><a href='/login'>Return to login</a></body></html>"

@app.route("/")
@login_required
def index():
    ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    viewers = 0
    iplist = set()
    with open ("out.log", "r") as file:
        for line in file:
            if "Errno" not in line:
                iplist.add(ip_pattern.search(line).group())
            else:
                iplist.remove(ip_pattern.search(line).group())
    viewers = len(iplist)
    with open ("out.log", "w") as ipl:
        for item in iplist:
            ipl.write(item)
    return render_template("index.html", viewers=viewers)

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
    return ('', 204)
    
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
    return ('', 204)

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
    return ('', 204)

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
    return ('', 204)

@app.route("/flip")
@login_required
def flip():
    (UDValue, LRValue, flipped) = loadconfig()
    if not flipped:
        os.system('killall mjpeg*')
        os.system('./mjpeg2.py vflip &> out.log')
        flipped = True
    else:
        os.system('killall mjpeg*')
        os.system('./mjpeg2.py &> out.log')
        flipped = False
    saveconfig(UDValue,LRValue,flipped)
    return ('', 204)

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

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("must provide username")
        elif not request.form.get("password"):
            return apology("must provide password")
        rows = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username").lower(),)).fetchall()
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password")
        session["user_id"] = rows[0][0]
        user_id = session["user_id"]
        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if request.method == "POST":
        username = request.form.get("username").lower()
        passwordhash = generate_password_hash(request.form.get("password"))
        usernamecheck = db.execute("SELECT 1 FROM users WHERE username = ?", (username,)).fetchone()
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match")
        if usernamecheck:
            return apology("Username Taken")
        elif not request.form.get("password"):
            return apology("Please enter a password")
        elif not request.form.get("username"):
            return apology("Please enter a username")
        else:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, passwordhash,))
#            session["user_id"] = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username").lower(),)).fetchall()[0][0]
#            user_id = session["user_id"]
            return redirect("/")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")

if __name__ == '__main__':
    os.system('./mjpeg2.py &> out.log')
#    vidcmd = "./mjpeg2.py"
#    vidlog = subprocess.check_output(vidcmd, stderr=subprocess.STDOUT, text=True, shell=True)
    app.run(host='0.0.0.0', port=5000, debug=False)
