import React, { useEffect, useRef, useState, useCallback } from 'react';
import Hls from 'hls.js';
import { Center, Switch } from '@mantine/core';

export default function AudioPlayer(props) {
  const videoRef = useRef();
  const [isPlaying, setIsPlaying] = useState(false);
  const [hls, setHls] = useState(null);
  const [useLowLatency, setChecked] = useState(true);
  

  useEffect(() => {
    if (Hls.isSupported()) {
      const hlsInstance = new Hls({
        liveSyncDuration: 5, // Set the sync duration for live streams
        liveBackBufferLength: 2, // Set the live back buffer length});
        maxBufferLength: useLowLatency ? 10 : 30, // Adjust buffer length dynamically
        maxMaxBufferLength: useLowLatency ? 30 : 600, // Adjust max buffer length for live streams
      });
      hlsInstance.attachMedia(videoRef.current);
      hlsInstance.on(Hls.Events.MEDIA_ATTACHED, () => {
        setHls(hlsInstance);
      });
    }
  }, []);

  const startPlayback = useCallback(() => {
    hls.loadSource('./stream.m3u8');
    hls.on(Hls.Events.MANIFEST_PARSED, () => {
      videoRef.current.play();
    });
    setIsPlaying(true);
  }, [hls]);

  const stopPlayback = useCallback(() => {
    hls.stopLoad();
    setIsPlaying(false);
  }, [hls]);

  useEffect(() => {
    if (isPlaying && useLowLatency) {
      const interval = setInterval(() => {
        videoRef.current.currentTime = videoRef.current.duration;
      }, 120000);
      return () => clearInterval(interval);
    }
  }, [isPlaying, useLowLatency]);

  return (
    <div>
      <audio ref={videoRef} {...(props.showFull ? { controls: true } : {})}>
        Your browser does not support the audio tag.
      </audio>
      <br />
      <button onClick={isPlaying ? stopPlayback : startPlayback}>
        {isPlaying ? 'Stop' : 'Start'}
      </button>
      <Center>
      <Switch
        label="Delay"
        checked={useLowLatency}
        onChange={() => setChecked(!useLowLatency)}
      />
      </Center>

    </div>
  );
}
