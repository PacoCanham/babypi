import subprocess
from pydub import AudioSegment
import time


print(time.strftime("%H:%M:%S"))
# Start the ffmpeg process
ffmpeg_command = [
    'ffmpeg',
    '-i', 'flask/static/stream.m3u8',  # Replace with your input file
    '-f', 's16le',       # PCM format
    '-ar', '44100',      # Sample rate
    '-ac', '1',          # Mono
    'pipe:1'             # Output to stdout
]

process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

rms = []
spike_array = []


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

    latest_volume = audio_segment.rms

    if len(rms) > 0:
        average_rms = int(sum(rms)/len(rms))
        if len(spike_array) > 0 :
            spike_level = int(sum(spike_array)/len(spike_array))
        else:
            spike_level = 0
        high_spike_threshold = average_rms*10
        low_spike_threshold = average_rms*5
    else:    
        rms.append(latest_volume)
        continue

    
    # Calculate the RMS (Root Mean Square) value
    if len(rms) < 30:
            rms.append(latest_volume)
    else:
        if latest_volume > low_spike_threshold:
            if len(spike_array) > 3:
                spike_array.pop(0)
            spike_array.append(latest_volume)
        else:
            spike_array = []
            rms.pop(0)
            rms.append(latest_volume)
    

    if  len(spike_array) > 2 :
        if (sum(spike_array)/len(spike_array))>high_spike_threshold:
            with open("alertlog.log", 'a+') as f:
                f.write(f"\n\n\n\n\n\n{time.strftime('%H:%M:%S')}\n HIGH ALERT THRESHOLD\n")
                f.write(f"{time.strftime('%H:%M:%S')}\nRMS: {rms}\nAverage {average_rms}\nSpike_Array {spike_array}\nSpike Thresh (x10) = {high_spike_threshold}\nSpike level = {spike_level}\n\n")

            spike_array = []
        elif (sum(spike_array)/len(spike_array))>low_spike_threshold:
            with open("alertlog.log", 'a+') as f:
                f.write(f"\n\n\n\n\n\n{time.strftime('%H:%M:%S')}\n LOW ALERT THRESHOLD\n")
                f.write(f"{time.strftime('%H:%M:%S')}\nRMS: {rms}\nAverage {average_rms}\nSpike_Array {spike_array}\nSpike Thresh (x5) = {low_spike_threshold}\nSpike level = {spike_level}\n\n")

            spike_array = []




    # print(f"length of sum[:-3]  {len(rms[-3:])}")
    print(f'RMS: {rms}')
    print(f"Average {average_rms}")
    print(f"High Spike Thresh (x10) = {high_spike_threshold}")
    print(f"Spike Thresh (x5) = {low_spike_threshold}")

    print(f"Spike Array Length = {len(spike_array)}")
    # if spike_level:
    print(f"Spike level = {spike_level}\n")
    # if spike_level > low_spike_threshold :
    #     with open("alertlog.log", 'a+') as f:
    #         f.write(f"{time.strftime('%H:%M:%S')}\nRMS: {rms}\nAverage {average_rms}\nSpike_Array {spike_array}\nSpike Thresh (x5) = {low_spike_threshold}\nSpike level = {spike_level}\n\n")
        # print("ALERT")
