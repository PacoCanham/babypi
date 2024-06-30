import vlc
import threading
import io
import numpy as np
from PIL import Image


class CustomAudioPlayer:
    def __init__(self):
        self.instance = vlc.Instance('--input-repeat=-1')
        self.player = self.instance.media_player_new()
        self.playing = False
        self.current_track = None

    def play(self, track):
        if not self.playing:
            self.playing = True
            self.current_track = self.instance.media_new(track)
            self.player.set_media(self.current_track)
            self.player.play()

    def pause(self):
        if self.playing:
            self.playing = False
            self.player.pause()

    def resume(self):
        if not self.playing and self.current_track:
            self.playing = True
            self.player.play()

    def stop(self):
        if self.playing:
            self.playing = False
            self.player.stop()

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = threading.Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

    def save(self, filename):
        if self.frame is not None:
            image = Image.open(io.BytesIO(self.frame))
            image.save(filename)
        else:
            print("No frame available")

    def return_bytes(self):
        if self.frame is not None:
            return io.BytesIO(self.frame)
        else:
            print("No frame available")
            return None

    def return_array(self):
        if self.frame is not None:
            image = Image.open(io.BytesIO(self.frame))
            return np.array(image)
        else:
            print("No frame available")
            return None