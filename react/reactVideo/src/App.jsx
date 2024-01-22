import VideoPlayer from "./VideoPlayer.jsx";
import './App.css'
import CameraButtons from "./CameraButtons.jsx";
import Header from "./Header.jsx";

export default function App(){
	return (
		<div style={{margin:"auto", padding:"1"}}>
			<VideoPlayer/>
			<hr/>
			<CameraButtons/>
		</div>
	);
}
