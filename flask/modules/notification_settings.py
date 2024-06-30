from flask import jsonify, request
from __main__ import app, login_required, settings
from functools import wraps
from flask_session import Session



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
    print(settings)
    return "OK"

@app.route("/applyAudio", methods=["POST"])
@login_required
def applyAudio():
    settings['notifications']['audio'] = request.json 
    print(settings)
    return "OK"

