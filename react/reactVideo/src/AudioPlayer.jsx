import React, { useEffect, useRef, useState } from 'react';
import Hls from 'hls.js';
import stream from "./stream.m3u8";

export default function AudioPlayer({ showFull }) {
  const videoRef = useRef();
  const [isPlaying, setIsPlaying] = useState(false);
  const [hls, setHls] = useState(null);

  useEffect(() => {
    if (Hls.isSupported()) {
      const hlsInstance = new Hls();
      const video = videoRef.current;

      hlsInstance.attachMedia(video);
      hlsInstance.on(Hls.Events.MEDIA_ATTACHED, function () {
        console.log("video and hls.js are now bound together !");
        setHls(hlsInstance);
      });
    }
  }, []);

  const togglePlay = () => {
    if (isPlaying) {
      hls.stopLoad();
      // videoRef.current.pause();
      setIsPlaying(false);
    } else {
      hls.loadSource({stream});
      hls.on(Hls.Events.MANIFEST_PARSED, function (event, data) {
        console.log("manifest loaded, found " + data.levels.length + " quality level");
        setTimeout(() => {
          videoRef.current.play();
          setTimeout(() => {
            videoRef.current.currentTime = videoRef.current.duration + 1;
          }, 2000);
        }, 1000);
      });
      setIsPlaying(true);
    }
  };

  useEffect(() => {
    if (isPlaying) {
      const interval = setInterval(() => {
        videoRef.current.currentTime = videoRef.current.duration;
      }, 120000);
      return () => clearInterval(interval);
    }
  }, [isPlaying]);

  return (
    <div>
    <audio ref={videoRef} {...(showFull ? { controls: true } : {})}>
      {/* style={{ display: 'none' }}> */}
        Your browser does not support the audio tag.
      </audio>
      <button onClick={togglePlay}>
        {isPlaying ? 'Stop' : 'Start'}
      </button>
    </div>
  );
}
