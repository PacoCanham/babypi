import * as React from 'react';
import {Box} from '@mui/material';
import Stack from '@mui/material/Stack';
import IconButton from '@mui/material/IconButton';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import PauseIcon from '@mui/icons-material/Pause';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import Slider from '@mui/material/Slider';
import { useState } from 'react';
import { useEffect } from 'react';


export default function NoisePlayer({volume, setVolume, playstate, setPlaystate}){
    const [noiseList, setNoiselist] = useState([])
    const [noise, setNoise] = useState('Select Track')
    const [sliderVisibility, setSliderVisibility] = useState(true)



    useEffect(() => {
        async function get_noiselist() {
            await fetch('/noiselist')
                .then((response) => response.json())
                .then((data) => {
                    setNoiselist(data.noiselist)
                    setPlaystate(data.playstate)
                    setNoise(data.trackname)
                    setVolume(data.volume)
                })
            }
        get_noiselist()
    }, [])

    async function playfunction(e){
        e.preventDefault();
        await fetch('/noise');
        setPlaystate(!playstate)
        }
    
    async function noiseChange(e){
        const noiseName = e.target.value;
        setNoise(noiseName);
        const url = '/change_noise/' + noiseName ;
        await fetch(url);
    }

    async function chooseVolume(e){
        const newVolume = e.target.value;
        setVolume(newVolume);
        const url = "/setVolume/" + newVolume;
        await fetch(url);
    }

    return (
      <Box sx={{width: "auto" ,textAlign:"center", margin:"auto", padding:2}}>
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
              {!playstate ? <PlayArrowIcon/> : <PauseIcon/>}
          </IconButton>
          <IconButton
                onMouseEnter={() => setSliderVisibility(true)}
                onMouseOut={() => setSliderVisibility(false)}>
            {sliderVisibility ? <VolumeUpIcon/> : <Slider
        value={volume}
        valueLabelDisplay="auto"
        onChange={(e) => chooseVolume(e)}
        orientation="vertical"
        style={{ height: '75px' }}
      /> }
          </IconButton>
        </Stack>
      </Box>
    );
}