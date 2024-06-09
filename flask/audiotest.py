#!/home/paco/.babycamvenv/bin/python3
import subprocess
from pydub import AudioSegment
import requests
from io import BytesIO
from time import time

# Command to get the FFmpeg process output

# Function to process audio from FFmpeg's stdout
def process_audio_from_ffmpeg():
    time400 = time()
    time150 = time()
    ffmpeg_command = [
        'ffmpeg',
        '-i', 'static/stream.m3u8',  # Replace with your input file
        '-f', 's16le',       # PCM format
        '-ar', '44100',      # Sample rate
        '-ac', '1',          # Stereo
        'pipe:1'             # Output to stdout
    ]
    # Start the FFmpeg process
    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE)
    add = 0
    count = 0
    while True:
        # Read 44100*2*2 bytes from stdout (1 second of audio)
        audio_data = process.stdout.read(44100 * 2 * 2)
        if not audio_data:
            break

        # Create an audio segment from the raw data
        audio_segment = AudioSegment(
            data=audio_data,
            sample_width=2,  # PCM 16-bit
            frame_rate=44100,
            channels=1
        )
        rms = audio_segment.rms
        print(f'\nRMS value: {rms}\n')
        add += rms
        count += 1
        average = (add/count)
        currentTime = time()
        # print(f"Current Time : {currentTime}")
        # print(f"Time Delta : {currentTime - time400}")
        if rms > 600 :
            print(f"Time Delta : {(currentTime - time400)}")
            if (currentTime - time400) > 10:
                print("RMS OVER 500")
                requests.post("https://192.168.4.182:8181/babycamtest",
                    data="Blanca is Really Screaming!.",
                    headers={
                        "Title": "Blanca",
                        "Priority": "urgent",
                        "Tags": "warning",
                        "Actions":"view, Open Camera, https://pacocanham.ddns.net/",
                    })
                time400 = time()
        elif rms > 250 :
            if (currentTime - time150) > 10:
                print("RMS OVER 150")
                requests.post("https://192.168.4.182:8181/babycamtest",
                    data="Blanca is making noise 😢".encode(encoding='utf-8'),
                    headers={
                        "Title":"Blanca",
                        "Priority":"3",
                        "Tags":"baby,sob,warning",
                        "Actions":"view, Open Camera, https://pacocanham.ddns.net/",
                    })
                time150 = time()
            # data="Blanca is being loud",
            # headers={ "Actions": "view, Open Camera, https://pacocanham.ddns.net/, clear=true; body='{\"temperature\": 65}'" })
            # print("LOUD"*1000)
        # print(f"Average = {average}")

process_audio_from_ffmpeg()