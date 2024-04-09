import VideoPlayer from "./VideoPlayer.jsx";
import './App.css'
import CameraButtons from "./CameraButtons.jsx";
import AudioPlayer from "./AudioPlayer.jsx";
import Header from "./Header.jsx";
import NotifyTest from "./NotifyTest.jsx";
import React, { useState, useEffect } from 'react';
import NoisePlayer from "./NoisePlayer.jsx";

export default function App() {
  const [showControls, setShowControls] = useState(false);
  const [showNoise, setShowNoise] = useState(false);
  const [paddingTop, setPaddingTop] = useState('1');

  useEffect(() => {
    const mql = window.matchMedia('(orientation: portrait)');

    function checkOrientation(e) {
      setPaddingTop(e.matches ? '1vh' : '8vh');
    }

    mql.addEventListener('change', checkOrientation);
    checkOrientation(mql); // initial check

    return () => mql.removeEventListener('change', checkOrientation);
  }, []);

  return (
    <div style={{ margin: '0', padding: '0', width: '100vw' }}>
      <div style={{ margin: '0', padding: '1', width: '100vw', height: '10vh' }}>
        <Header showControls={showControls} setShowControls={setShowControls} showNoise={showNoise} setShowNoise={setShowNoise} />
      </div>
      <div style={{ margin: 'auto', paddingTop: paddingTop, width: '100vw' }}>
        <VideoPlayer streamUrl="/video.mjpg" />
        <hr />
        <AudioPlayer streamUrl="/audio" />
        
        {showControls && <><hr /><CameraButtons/></>}
        {/* <NotifyTest /> */}
        {showNoise && <><hr/><NoisePlayer/></>}
        <hr/>
      </div>
    </div>
  );
}
