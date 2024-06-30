from flask import jsonify, request
from __main__ import app, login_required, settings
from functools import wraps
from flask_session import Session



@app.route("/getAudioConfig")
@login_required
def getAudioConf():
    return jsonify({'Vee': {
        'delayLow': 600,
        'delayHigh': 1800,
        'volumeLow': 100,
        'volumeHigh': 1000,
        'sampleLength': 3,
        'enabled' : True
    },
    'Paco': {
        'delayLow': 600,
        'delayHigh': 1800,
        'volumeLow': 100,
        'volumeHigh': 1000,
        'sampleLength': 3,
        'enabled' : True
    }})

@app.route("/getVideoConfig")
@login_required
def getVideoConf():
      return {'Vee': {
        'movThres': 60,
        'movNumLow': 3,
        'movNumHigh': 30,
        'notificationDelay': 600,
        'enabled' : True
    },
    'Paco': {
        'movThres': 250,
        'movNumLow': 3,
        'movNumHigh': 30,
        'notificationDelay': 600,
        'enabled' : True
    }}

@app.route("/applyVideo", methods=["POST"])
@login_required
def applyVideo():
    # data = request.json
    settings['video'] = request.json 
    print(settings)
    return "OK"

@app.route("/applyAudio", methods=["POST"])
@login_required
def applyAudio():
    settings['audio'] = request.json 
    print(settings)
    return "OK"

