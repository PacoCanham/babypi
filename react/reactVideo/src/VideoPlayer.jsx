import { Box, Typography } from '@mui/material'
import React, { useState } from 'react'
import CustomAudioPlayer from './CustomAudioPlayer';


export default function VideoPlayer(){
    // const {videoVolume, setVideoVolume} = useState(50);

    // const handleChange = (e) => {
    //     setVideoVolume(e.target.value);
    // }

    const stream = window.location.protocol + "//" + window.location.hostname + ":5147/stream.mjpg";

    return (
    <Box sx={{width: "95%",textAlign:"center", margin:"auto", padding:2}}>
    <img src={stream} width={"75%"} style={{border:"2px solid black", margin:"auto", padding:"0", borderRadius:"5%"}}/>   
    <CustomAudioPlayer src="plughw:3,0" capture />
     <Typography gutterBottom>
            Volume
     </Typography>
    </Box>
    )
}
