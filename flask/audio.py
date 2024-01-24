import pyaudio
import numpy as np
import socket

# Set up the PyAudio instance
p = pyaudio.PyAudio()

# Open the stream
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

# Set up the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 8087))
s.listen(1)

print("Waiting for a connection...")
conn, addr = s.accept()
print("Connected to: ", addr)

try:
    while True:
        # Read data from the audio input stream
        data = stream.read(1024)
        
        # Send data over the socket
        conn.send(data)
except KeyboardInterrupt:
    # Stop the stream and close the socket when the script is interrupted
    print("Interrupted... stopping stream and closing socket.")
    stream.stop_stream()
    stream.close()
    conn.close()
