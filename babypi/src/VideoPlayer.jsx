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
    <ReactPlayer url='https://www.youtube.com/watch?v=LXb3EKWsInQ' volume={(videoVolume/100)} playing controls width={"75vw"}/>
    <Box sx={{width: "50%",textAlign:"center", margin:"auto", padding:1}}>
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