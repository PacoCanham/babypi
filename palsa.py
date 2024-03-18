#!/usr/bin/env python3
# -*- mode: python; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*-

## recordtest.py
##
## This is an example of a simple sound capture script.
##
## The script opens an ALSA pcm device for sound capture, sets
## various attributes of the capture, and reads in a loop,
## writing the data to standard out.
##
## To test it out do the following:
## python recordtest.py out.raw # talk to the microphone
## aplay -r 8000 -f S16_LE -c 1 out.raw

#!/usr/bin/env python

from __future__ import print_function

import sys
import time
import getopt
import alsaaudio
import io
import wave
# from pydub import AudioSegment

f = io.BytesIO()

inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK,
    channels=1, rate=44100, format=alsaaudio.PCM_FORMAT_S16_LE,
    periodsize=160, device="hw:2,0")
out = io.BytesIO()

loops = 5000
while loops > 0:
    loops = -1
    l, data = inp.read()
    if l < 0:
        print("Capture buffer overrun! Continuing nonetheless ...")
    elif l:
        f.write(data)
        time.sleep(.001)

print(f)

def bytes_to_wav(byte_data, filename):
    with wave.open(filename, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(44100)
        wav_file.writeframes(byte_data)

time.sleep(5)
x = f.getvalue()
bytes_to_wav(x, "test.wav")
