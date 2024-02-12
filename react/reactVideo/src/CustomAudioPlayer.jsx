import { VolumeDown, VolumeUp } from "@mui/icons-material";
import { Slider, Stack } from "@mui/material";
import React, { useState, useEffect } from "react";
import AudioPlayer from "react-h5-audio-player";

// A custom component that wraps the AudioPlayer component and adds a volume slider
export default function CustomAudioPlayer({ src, capture }) {
  // A state variable to store the current volume value
  const [volume, setVolume] = useState(0.5);

  // A function to handle the change of the volume slider
  const handleVolumeChange = (event) => {
    // Get the new volume value from the event
    const newVolume = event.target.value;
    // Update the state variable
    setVolume(newVolume);
  };

  return (
    <div className="custom-audio-player">
      {/* Render the AudioPlayer component with the src and capture props */}
      <AudioPlayer src={src} capture={capture} volume={volume} />
      {/* Render a range input for the volume slider */}
        <Stack spacing={2} direction="row" alignItems={"center"}>
              <VolumeDown />
                  <Slider
                      aria-label="Volume"
                      value={volume}
                      onChange={handleVolumeChange}
                      valueLabelDisplay="auto"
                      step={0.1}
                      marks
                      min={0}
                      max={1}
                      className="volume-slider"
                      sx={{width:"40vw", margin:"auto"}}
                  />
              <VolumeUp />
      </Stack>
    </div>
  );
};