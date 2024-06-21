import { Box } from '@mui/material';
import React from 'react';
import { Image } from '@mantine/core';

export default function VideoPlayer({ streamUrl }) {
  return (
    <Box sx={{
      width: "100%", // Take up full container width
      textAlign: "center",
      margin: "auto",
      padding: 2,
      paddingTop: "10vh", // Adjust this value to ensure it doesn't overlap with the header
      paddingBottom: "10vh", // Adjust this value to ensure it doesn't overlap with footer or other elements
    }}>
      <Image 
      radius="md"
      src={streamUrl}
      onError={()=>{window.location.reload(false)}}
      />

    </Box>
  );
}


// import { Box, Typography } from '@mui/material'
// import React, { useState } from 'react'


// export default function VideoPlayer({streamUrl}){
//     return (
//     <Box sx={{width: "80%" ,textAlign:"center", margin:"auto", padding:2}}>
//     <img src={streamUrl} width={"100%"} style={{border:"2px solid black", margin:"auto", padding:"2px", borderRadius:"5%"}}/>   
//     </Box>
//     )
// }

    //     src={streamUrl} 
    //     alt="Live stream" 
    //     style={{
    //       maxWidth: "100%", // Ensure it's responsive
    //       height: "auto", // Maintain aspect ratio
    //       border: "2px solid black",
    //       borderRadius: "5%",
    //       boxShadow: "0 4px 8px 0 rgba(0,0,0,0.2)" // Optional: Adds a subtle shadow for depth
    //     }} 
    //   />