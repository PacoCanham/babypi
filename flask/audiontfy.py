import subprocess
from pydub import AudioSegment
import time
import requests



# print(time.strftime("%H:%M:%S"))
# Start the ffmpeg process
def audioDetection():
    ffmpeg_command = [
        'ffmpeg',
        '-i', 'static/stream.m3u8',  # Replace with your input file
        '-f', 's16le',       # PCM format
        '-ar', '44100',      # Sample rate
        '-ac', '1',          # Mono
        'pipe:1'             # Output to stdout
    ]

    process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    rms, spike_array = [], []
    low_notification_time, high_notification_time = time.time() + 30, time.time() + 30
    low_notification_delay = 600
    high_notification_delay = 15


    while True:
        # Read 1 second of audio data
        audio_data = process.stdout.read(44100 * 2 * 1)
        if not audio_data:
            break

        # Create an audio segment from the raw data
        audio_segment = AudioSegment(
            data=audio_data,
            sample_width=2,  # PCM 16-bit
            frame_rate=44100,
            channels=1
        )

        # Calculate the RMS (Root Mean Square) value
        latest_volume = audio_segment.rms

        if len(rms) > 0:
            average_rms = int(sum(rms)/len(rms))
            if len(spike_array) > 0 :
                spike_level = int(sum(spike_array)/len(spike_array))
            else:
                spike_level = 0
            high_spike_threshold = average_rms*10
            low_spike_threshold = average_rms*3
        else:    
            rms.append(latest_volume)
            print(rms)
            continue

        
        if len(rms) < 30:
            print()
            rms.append(latest_volume)
        else:
            if latest_volume > low_spike_threshold:
                spike_array.append(latest_volume)
                if len(spike_array) > 1:
                    spike_array.pop(0)
            else:
                spike_array.clear()
                rms.pop(0)
                rms.append(latest_volume)
        

        if  len(spike_array) > 1 :
            if ((sum(spike_array)/len(spike_array))>high_spike_threshold) and ((time.time() - high_notification_time) > high_notification_delay):
                high_notification_time = time.time()
                with open("alertlog.log", 'a+') as f:
                    f.write(f"\n\n\n\n\n\n{time.strftime('%H:%M:%S')}\n HIGH ALERT THRESHOLD\n")
                    f.write(f"{time.strftime('%H:%M:%S')}\nRMS : {rms}\nAverage : {average_rms}\nSpike_Array : {spike_array}\nSpike Thresh (x10) : {high_spike_threshold}\nSpike level : {spike_level}\n\n")
                    f.write("\n60s Delay")
                requests.post("https://192.168.4.182:8181/babycamtest",
                    data="Blanca is Really Screaming!.",
                    headers={
                        "Title": "Blanca",
                        "Priority": "urgent",
                        "Tags": "warning",
                        "Actions":"view, Open Camera, https://pacocanham.ddns.net/",
                    })
                spike_array.clear()
            elif ((sum(spike_array)/len(spike_array))>low_spike_threshold) and ((time.time() - low_notification_time) > low_notification_delay):
                low_notification_time = time.time()
                with open("alertlog.log", 'a+') as f:
                    f.write(f"\n\n\n\n\n\n{time.strftime('%H:%M:%S')}\n LOW ALERT THRESHOLD\n")
                    f.write(f"{time.strftime('%H:%M:%S')}\nRMS : {rms}\nAverage : {average_rms}\nSpike_Array : {spike_array}\nSpike Thresh (x5) : {low_spike_threshold}\nSpike level : {spike_level}\n\n")
                    f.write("\n5 Minute delay\n")
                requests.post("https://192.168.4.182:8181/babycamtest",
                    data="Blanca is making noise 😢".encode(encoding='utf-8'),
                    headers={
                        "Title":"Blanca",
                        "Priority":"3",
                        "Tags":"baby,sob,warning",
                        "Actions":"view, Open Camera, https://pacocanham.ddns.net/",
                    })
                spike_array.clear()





        # print(f"length of sum[:-3]  {len(rms[-3:])}")
        if len(rms) < 30:
            print(rms)
        else:
            print(f'Current RMS : {latest_volume}')
            print(f"{len(rms)}s Average : {average_rms}")
            print(f"High Spike Thresh (x10) : {high_spike_threshold}")
            print(f"Spike Thresh (x3) : {low_spike_threshold}")

            print(f"Spike Array Length : {len(spike_array)}")
            print(f"Spike level : {spike_level}\n")


audioDetection()