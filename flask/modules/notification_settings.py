from flask import jsonify, request, session
import json
from __main__ import app, login_required, settings
from functools import wraps
from flask_session import Session


def saveconfig():
    with open ("config.json", "w") as config:
        json.dump(settings, config)

@app.route("/getNotificationEnabled")
@login_required
def userNotifcationState():
    if session['username'].lower() in ["paco", 'vee']:
        username= session['username'].capitalize()
        if settings['notifications']["audio"][username]['enabled'] == True and settings['notifications']["video"][username]['enabled'] == True :
            return jsonify({"both_enabled" : True})
        else:
            return jsonify({"both_enabled" : False})

@app.route("/toggleNotifications")
@login_required
def toggleNotifications():
    if session['username'].lower() in ["paco", 'vee']:
        username= session['username'].capitalize()
        if settings['notifications']["audio"][username]['enabled'] == True and settings['notifications']["video"][username]['enabled'] == True :
            settings['notifications']['video'][username]['enabled'] = False  
            settings['notifications']['audio'][username]['enabled'] = False
        else:
            settings['notifications']['video'][username]['enabled'] = True
            settings['notifications']['audio'][username]['enabled'] = True
        saveconfig()
    return "ok", 200
    
@app.route("/getAudioConfig")
@login_required
def getAudioConf():
    return jsonify(settings['notifications']["audio"])

@app.route("/getVideoConfig")
@login_required
def getVideoConf():
      return jsonify(settings['notifications']["video"])

@app.route("/applyVideo", methods=["POST"])
@login_required
def applyVideo():
    # data = request.json
    settings['notifications']['video'] = request.json 
    saveconfig()
    return "OK"

@app.route("/applyAudio", methods=["POST"])
@login_required
def applyAudio():
    settings['notifications']['audio'] = request.json 
    saveconfig()
    return "OK"


