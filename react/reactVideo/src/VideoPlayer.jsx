import { Box, Typography } from '@mui/material'
import React, { useState } from 'react'


export default function VideoPlayer({streamUrl}){
    return (
    <Box sx={{width: "95%",textAlign:"center", margin:"auto", padding:2}}>
    <img src={streamUrl} width={"75%"} style={{border:"2px solid black", margin:"auto", padding:"0", borderRadius:"5%"}}/>   
    </Box>
    )
}
