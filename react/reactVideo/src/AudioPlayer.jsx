import React, { useEffect, useRef } from 'react';
import ReactHlsPlayer from 'react-hls-player';

const AudioPlayer = ({ streamUrl }) => {
  const playerRef = useRef(null);

  useEffect(() => {
    const intervalId = setInterval(() => {
      if (playerRef.current && playerRef.current.hls) {
        const hls = playerRef.current.hls;
        const liveEdge = hls.liveSyncPosition;
        const currentTime = playerRef.current.video.currentTime;

        if (liveEdge - currentTime > 3) {
          playerRef.current.video.currentTime = liveEdge;
        }
      }
    }, 1000); // Check every second

    return () => clearInterval(intervalId); // Clean up on unmount
  }, []);

  return (
    <ReactHlsPlayer
      playerRef={playerRef}
      src={streamUrl}
      autoPlay={true} // Autoplay is enabled
      controls={true} // Playback controls are shown
      width="100%"
      height="15px"
      startPosition={-1}
      hlsConfig={{
        maxLoadingDelay: 2, // Align with FFmpeg's low latency settings
        minAutoBitrate: 0, // No minimum bitrate, allowing for adaptive bitrate
        lowLatencyMode: true, // Enable low latency mode
        maxBufferLength: 0.5, // Set buffer length to 0.5s to match FFmpeg's segment time
        liveSyncDurationCount: 1, // Sync with the latest segment for low latency
      }}
    />
  );
};

export default AudioPlayer;
