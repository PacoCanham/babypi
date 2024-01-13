import { Box } from "@mui/material";
import Buttons from "./Buttons.jsx";
import VideoPlayer from "./VideoPlayer.jsx";
import './App.css'

export default function App(){
	return (
		<div style={{margin:"auto", padding:"1"}}>
			<VideoPlayer/>
			<hr/>
			<Buttons/>
		</div>

	);
}
