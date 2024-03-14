import React, { useEffect, useRef } from 'react';

const AudioPlayer = ({ streamUrl }) => {
  const audioRef = useRef(null);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    // Event listener to play the latest chunk
    const handleCanPlayThrough = () => {
      // Seek to the latest part of the audio
      audio.currentTime = audio.duration;
      audio.play().catch((error) => console.error('Error playing audio:', error));
    };

    audio.addEventListener('canplaythrough', handleCanPlayThrough);

    // Cleanup event listener
    return () => {
      audio.removeEventListener('canplaythrough', handleCanPlayThrough);
    };
  }, [streamUrl]);

  return (
    <audio ref={audioRef} controls preload="none">
      <source src={streamUrl} type="audio/webm" />
      Your browser does not support the audio element.
    </audio>
  );
};

export default AudioPlayer;
