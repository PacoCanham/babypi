import { Box, Typography } from '@mui/material'
import React, { useState } from 'react'


export default function VideoPlayer({streamUrl}){
    return (
    <Box sx={{width: "80%" ,textAlign:"center", margin:"auto", padding:2}}>
    <img src={streamUrl} width={"100%"} style={{border:"2px solid black", margin:"auto", padding:"2px", borderRadius:"5%"}}/>   
    </Box>
    )
}
