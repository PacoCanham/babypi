from flask import jsonify, request
from __main__ import app

@app.route("/getAudioConfig")
@login_required
def getAudioConf():
    return jsonify({Vee: {
        delayLow: 600,
        delayHigh: 1800,
        volumeLow: 100,
        volumeHigh: 1000,
        sampleLength: 3,
        enabled : True

    },
    Paco: {
        delayLow: 600,
        delayHigh: 1800,
        volumeLow: 100,
        volumeHigh: 1000,
        sampleLength: 3,
        enabled : True

    }})

@app.route("/getVideoConfig")
@login_required
def getVideoConf():
      return {Vee: {
        movThres: 60,
        movNumLow: 3,
        movNumHigh: 30,
        notificationDelay: 600,
        enabled : True

    },
    Paco: {
        movThres: 250,
        movNumLow: 3,
        movNumHigh: 30,
        notificationDelay: 600,
        enabled : True
    }}

@app.route("/applyVideo", methods=["POST"])
@login_required
def applyVideo():
    data = request.json
    print(data)
    return "OK"

@app.route("/applyAudio", methods=["POST"])
@login_required
def applyAudio():
    data = request.json
    print(data)
    return "OK"

