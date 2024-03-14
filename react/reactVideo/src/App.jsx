import VideoPlayer from "./VideoPlayer.jsx";
import './App.css'
import CameraButtons from "./CameraButtons.jsx";
import AudioPlayer from "./AudioPlayer.jsx";
import Header from "./Header.jsx";
import { useState } from "react";
import MjpegPlayer from "./MjpegPlayer.jsx";

export default function App(){
	const [showControls, setShowControls] = useState(false)
	return (
		<div style={{margin:"0", padding:"0", width:"100vw"}}>
		<div style={{margin:"0", paddingBottom:"5", width:"100vw"}}>
			<Header showControls={showControls} setShowControls={setShowControls}/>
		</div>
		<div style={{margin:"auto", paddingTop:"5", width:"100vw"}}>
			<MjpegPlayer url={"/video.mjpg"} />
			<hr/>
			<AudioPlayer streamUrl="/audio" />
			<hr/>
			{showControls && <CameraButtons/>}
		</div>
		</div>
	);
}
