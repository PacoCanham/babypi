import { VolumeDown, VolumeUp } from '@mui/icons-material';
import { Box, Grid, Slider, Stack, Typography } from '@mui/material'
import React, { useState } from 'react'
import ReactPlayer from 'react-player'


export default function VideoPlayer(){
    const {videoVolume, setVideoVolume} = useState(50);

    const handleChange = (e) => {
        setVideoVolume(e.target.value);
    }

    const stream = window.location.protocol + "//" + window.location.hostname + ":8000/stream.mjpg";

    return (
    <>
    <Box sx={{width: "95%",textAlign:"center", margin:"auto", padding:2}}>
    <img src={stream} width={"75%"} style={{border:"2px solid black", margin:"auto", padding:"0"}}/>   
     <Typography gutterBottom>
            Volume
     </Typography>
    <Stack spacing={2} direction="row" alignItems={"center"}>
            <VolumeDown />
                <Slider
                    aria-label="Volume"
                    defaultValue={videoVolume}
                    onChange={handleChange}
                    valueLabelDisplay="auto"
                    step={10}
                    marks
                    min={0}
                    max={100}
                    sx={{width:"40vw", margin:"auto"}}
                />
            <VolumeUp />
    </Stack>
    </Box>
</>
    )
}
