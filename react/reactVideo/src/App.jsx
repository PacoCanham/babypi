import VideoPlayer from "./VideoPlayer.jsx";
import './App.css'
import CameraButtons from "./CameraButtons.jsx";
import AudioPlayer from "./AudioPlayer.jsx";
import Header from "./Header.jsx";
import NotifyTest from "./NotifyTest.jsx";
import React, { useState, useEffect } from 'react';
import NoisePlayer from "./NoisePlayer.jsx";
import NoSleep from 'nosleep.js';


export default function App() {
  const [showControls, setShowControls] = useState(false);
  const [showNoise, setShowNoise] = useState(false);
  const [paddingTop, setPaddingTop] = useState('1');
  const [volume, setVolume] = useState(20);
  const [playstate, setPlaystate] = useState(false);
  const [showFull, setShowFull] = useState(false);

  useEffect(() => {
    const noSleep = new NoSleep();

    const enableNoSleep = () => {
      noSleep.enable();
      document.removeEventListener('touchstart', enableNoSleep, false);
    };

    // Enable wake lock on touchstart
    document.addEventListener('touchstart', enableNoSleep, false);

    // Orientation change event listener
    const mql = window.matchMedia('(orientation: portrait)');
    const checkOrientation = (e) => {
      setPaddingTop(e.matches ? '1vh' : '8vh');
    };
    mql.addEventListener('change', checkOrientation);
    checkOrientation(mql); // initial check

    // Cleanup function for useEffect
    return () => {
      noSleep.disable(); // Disable wake lock
      document.removeEventListener('touchstart', enableNoSleep, false);
      mql.removeEventListener('change', checkOrientation);
    };
  }, []);


  return (
    <div style={{ margin: '0', padding: '0', width: '100vw' }}>
      <div style={{ margin: '0', padding: '1', width: '100vw', height: '10vh' }}>
        <Header showControls={showControls} setShowControls={setShowControls} showNoise={showNoise} setShowNoise={setShowNoise} setVolume={setVolume} setPlaystate={setPlaystate} showFull={showFull} setShowFull={setShowFull} />
      </div>
      <div style={{ margin: 'auto', paddingTop: paddingTop, width: '80vw' }}>
        <VideoPlayer streamUrl="/video.mjpg" />
        <hr />
        <AudioPlayer showFull={showFull} />
        {/* <AudioPlayer/> */}
        {showControls && <><hr /><CameraButtons/></>}
        {/* <NotifyTest /> */}
        {showNoise && <><hr/><NoisePlayer volume={volume} setVolume={setVolume} playstate={playstate} setPlaystate={setPlaystate}/></>}
        <hr/>
      </div>
    </div>
  );
}
