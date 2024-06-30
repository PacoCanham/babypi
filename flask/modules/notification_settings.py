from flask import jsonify, request, session
import json
from __main__ import app, login_required, settings
from functools import wraps
from flask_session import Session


def saveconfig():
    with open ("config.json", "w") as config:
        json.dump(settings, config)
        
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

@app.route("/toggleNotifications")
@login_required
def toggleNotifications():
    settings['notifications']['video'][session['username'].capitalize()]['enabled'] = not settings['notifications']['video'][session['username'].capitalize()]['enabled']  
    settings['notifications']['audio'][session['username'].capitalize()]['enabled'] = not settings['notifications']['audio'][session['username'].capitalize()]['enabled']  

    saveconfig()

