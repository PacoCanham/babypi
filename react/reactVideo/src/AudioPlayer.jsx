  // import React, { useEffect, useRef } from 'react';
  // import Hls from 'hls.js'; // Import hls.js

  // const AudioPlayer = ({ streamUrl }) => {
  //   const audioRef = useRef(null);

  //   useEffect(() => {
  //     const audio = audioRef.current;
  //     if (!audio) return;

  //     // Initialize hls.js
  //     if (Hls.isSupported()) {
  //       const hls = new Hls();
  //       hls.loadSource(streamUrl);
  //       hls.attachMedia(audio);
  //     } else if (audio.canPlayType('application/vnd.apple.mpegurl')) {
  //       // For Safari, use native HLS support
  //       audio.src = streamUrl;
  //     } else {
  //       console.error('HLS is not supported in this browser.');
  //     }


  //   const handleCanPlayThrough = () => {
  //   // Seek to a position slightly before the end
  //       const seekTime = Math.max(audio.duration - 1, 0); // Seek 2 seconds before the end
  //       audio.currentTime = seekTime;
  //       audio.play().catch((error) => console.error('Error playing audio:', error));
  //   };

      











  //     audio.addEventListener('canplaythrough', handleCanPlayThrough);

  //     // Cleanup event listener
  //     return () => {
  //       audio.removeEventListener('canplaythrough', handleCanPlayThrough);
  //     };
  //   }, [streamUrl]);

  //   return (
  //     <audio ref={audioRef} controls preload="none">
  //       {/* Use the HLS source */}
  //       <source src={streamUrl} type="application/x-mpegURL" />
  //       Your browser does not support the audio element.
  //     </audio>
  //   );
  // };

  // export default AudioPlayer;

import React from 'react';
import ReactHlsPlayer from 'react-hls-player';

const AudioPlayer = ({ streamUrl }) => {
  return (
    <ReactHlsPlayer
      src={streamUrl}
      autoPlay={false} // Set to true if you want autoplay
      controls={true} // Show playback controls
      width="100%"
      height="5%"
      hlsConfig={{
        maxLoadingDelay: 4,
        minAutoBitrate: 0,
        lowLatencyMode: true,
        backBufferLength: 5,
        liveSyncDurationCount: 1,
        hls_time: 0.5
      }}
    />
  );
};

export default AudioPlayer;

