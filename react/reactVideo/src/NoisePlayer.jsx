import * as React from 'react';
import {Box} from '@mui/material';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import PauseIcon from '@mui/icons-material/Pause';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import { useState } from 'react';
import { useEffect } from 'react';


export default function NoisePlayer(){
    const [playing, setPlaying] = useState(false)
    const [noiseList, setNoiselist] = useState([])
    const [noise, setNoise] = useState('Select Track')

    useEffect(() => {
        async function get_noiselist() {
            await fetch('/noiselist')
                .then((response) => response.json())
                .then((data) => {
                    setNoiselist(data.noiselist)
                    setPlaying(data.playstate)
                    setNoise(data.trackname)
                })
            }
        get_noiselist()
    }, [])

    async function playfunction(e){
        e.preventDefault();
        await fetch('/noise');
        setPlaying(!playing)
        }
    
    async function noiseChange(e){
        const noiseName = e.target.value;
        setNoise(noiseName);
        const url = '/change_noise/' + noiseName ;
        await fetch(url);

    }

    return (
      <Box sx={{width: "40%" ,textAlign:"center", margin:"auto", padding:2}}>
        <Stack spacing={2} direction="row">
          <FormControl fullWidth>
          <InputLabel id="WhiteNoise-Select-Label">Select Track</InputLabel>
          <Select
            labelId="WhiteNoise-Select-Label"
            id="WhiteNoise-Select-Label"
            value={noise}
            label="Select Track"
            onChange={noiseChange}
          >
              {noiseList.map((noiseName)=>{
                  return (
                      <MenuItem value={noiseName}>{noiseName}</MenuItem>
                  )
              })}
          </Select>
          </FormControl>
          <IconButton
          onClick={playfunction}>
              {!playing ? <PlayArrowIcon/> : <PauseIcon/>}
          </IconButton>
        </Stack>
      </Box>
    );
}