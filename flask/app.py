#!/usr/bin/python3

from flask import Flask, redirect, render_template, session, request, jsonify
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
    return {'error':reason}

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/viewers")
@login_required
def viewers():
    ip_pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
    viewers = 0
    iplist = set()
    with open ("./logs/ip.log", "r") as file:
        for line in file:
            if "GET" in line:
                ipadd = ip_pattern.search(line)
                if ipadd:
                    ipadd = ipadd.group()
                    if ipadd not in iplist:
                        iplist.add(ipadd)
            elif "Errno" in line:
                ipadd = ip_pattern.search(line)
                if ipadd:
                    ipadd = ipadd.group()
                    if ipadd in iplist:
                        iplist.remove(ipadd)
    viewers = len(iplist)
    return {'viewers' : viewers}

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
        os.system('./video.sh vflip')
        flipped = True
    else:
        os.system('killall mjpeg*')
        os.system('./video.sh')
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
        print(rows)
        if len(rows) != 1 or not check_password_hash(rows[0][2], password):
            return apology("invalid username and/or password")
        session["user_id"] = rows[0][0]
        user_id = session["user_id"]
        conn.close()
        return {'url':'/'}
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if request.method == "POST":
        conn = sqlite3.connect("babycam.db")
        cur = conn.cursor()
        data = request.json
        username = data.get("username").lower()
        print(type(username))
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
#            session["user_id"] = db.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username").lower(),)).fetchall()[0][0]
#            user_id = session["user_id"]
            conn.commit()
            conn.close()
            return {'url' : '/login'}
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
	session.clear()
	return redirect("/")

if __name__ == '__main__':
    os.system('./video.sh')
    app.run(host='0.0.0.0', port=80, debug=False)
