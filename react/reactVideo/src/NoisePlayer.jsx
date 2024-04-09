import * as React from 'react';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import PauseIcon from '@mui/icons-material/Pause';
import InputLabel from '@mui/material/InputLabel';
import NativeSelect from '@mui/material/NativeSelect';
import { useState } from 'react';
import { useEffect } from 'react';


export default function NoisePlayer(){
    const [playing, setPlaying] = useState(false)
    const [noiselist, setNoiselist] = useState([])
    useEffect(() => {
        async function get_noiselist() {
            await fetch('/noiselist')
                .then((response) => response.json())
                .then((data) => {
                    setNoiselist(data.noiselist)
                })
            }
        get_noiselist()
    }, [])

    async function playfunction(e){
        e.preventDefault();
        await fetch('/noise');
        setPlaying(!playing)
        }
    
    return (
      <Stack spacing={1} direction="row">
        <InputLabel variant="standard" htmlFor="noiseList">
          Select Track
        </InputLabel>
        <NativeSelect
          defaultValue={noiselist[0]}
          inputProps={{
            name: 'noiseList',
            id: 'noiseList',
          }}
        >
            {tracklist.map((track, trackIndex)=>{
                return (
                    <option value={trackIndex}>{track}</option>
                )
            })}
        </NativeSelect>
        <IconButton
        onClick={playfunction}>
            {playing ? <PlayArrowIcon/> : <PauseIcon/>}
        </IconButton>
      </Stack>
    );
}