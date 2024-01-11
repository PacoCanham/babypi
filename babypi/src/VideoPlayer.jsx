import { VolumeDown, VolumeUp } from '@mui/icons-material';
import { Box, Grid, Slider, Stack, Typography } from '@mui/material'
import React, { useState } from 'react'
import ReactPlayer from 'react-player'


export default function VideoPlayer(){
    const {videoVolume, setVideoVolume} = useState(50);

    const handleChange = (e) => {
        setVideoVolume(e.target.value);
    }

    return (
    <>
    <Box sx={{width: "50%",textAlign:"center", margin:"auto", padding:1}}>
    <img src={"http://babycam.local:8000/stream.mjpg"} width={"100%"}/>   
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
                    sx={{width:"30vw"}}
                />
            <VolumeUp />
    </Stack>
    </Box>
</>
    )
}
