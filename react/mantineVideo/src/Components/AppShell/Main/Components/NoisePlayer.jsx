import * as React from 'react';
import { useState } from 'react';
import { useEffect } from 'react';
import { ActionIcon, Group, MultiSelect, Slider } from '@mantine/core';
import { IconPlayerPause, IconPlayerPlay } from '@tabler/icons-react';


export default function NoisePlayer(props){
    const [noiseList, setNoiselist] = useState([])
    const [noise, setNoise] = useState('Select Track')
    const [sliderVisibility, setSliderVisibility] = useState(true)



    useEffect(() => {
        async function get_noiselist() {
            await fetch('/noiselist')
                .then((response) => response.json())
                .then((data) => {
                    setNoiselist(data.noiselist)
                    props.setSettings({playstate:data.playstate, volume:data.volume})
                    setNoise(data.trackname)
                })
            }
        get_noiselist()
    }, [])

    function playfunction(e){
        e.preventDefault();
        console.log(props.settings)
        props.setSettings({playstate:!props.settings.playstate})
        fetch('/noise')
        }
    
    function noiseChange(selection){
        const noiseName = selection;
        setNoise(selection);
        const url = '/change_noise/' + noiseName ;
        fetch(url);
    }

    function chooseVolume(value){
        props.setSettings({volume:value})
        const url = "/setVolume/" + value;
        fetch(url);
    }

    return (
        <><Group justify="center" align="end">
          <MultiSelect
            label="Pick White noise track"
            placeholder="Please select a track"
            data={noiseList}
            p={10}
            w={'90%'}
            onChange={noiseChange}/>
           <ActionIcon variant="filled" color="gray" size="xl" radius="xl" aria-label="Settings" onClick={playfunction}>
              {props.playstate ? <IconPlayerPause/> : <IconPlayerPlay/>}
          </ActionIcon></Group>
          <Slider
          color='gray'
          marks={[
            {value : 0, label: '0%'},
            {value : 20, label: '20%'},
            {value : 40, label: '40%'},
            {value : 60, label: '60%'},
            {value : 80, label: '80%'},
            {value : 100, label: '100%'},
          ]}
          onChangeEnd={chooseVolume}
          p={10}>
          </Slider>
          </>
    );
}