import React from 'react';
import ReactPlayer from 'react-player';

const MjpegPlayer = ({ url }) => {
  return (
      <ReactPlayer
        url={url}
        playing={true} // Auto-play the stream
        controls={false} // Show native player controls
        width="75%"
        height="auto"
      />
  );
};

export default MjpegPlayer;
