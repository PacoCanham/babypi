import {Box, Divider, Image, Modal } from "@mantine/core";
import Controls from "./Components/Controls";
import AudioPlayer from "./Components/AudioPlayer";
import NoisePlayer from "./Components/NoisePlayer";
import { useDisclosure } from "@mantine/hooks";
// {volume, setVolume, playstate, setPlaystate}
export default function MainPage(props){
    
    return(<>
        <Image
        src={"/video.mjpg"}
        radius={25}
        fallbackSrc="static/loading.jpg"
        p={25}
        />
        {(props.displayed.controls) && <><Divider p={20} size='xl' label="Controls"/><Controls/></>}
        {(props.displayed.microphone) && <><Divider p={20} size='xl' label="AudioStream Details"/></>}<AudioPlayer showFull={props.displayed.microphone}/>
        {(props.displayed.player) && <><Divider p={20} size='xl' label="Audio Player"/><NoisePlayer settings={props.settings} setSettings={props.setSettings}/></>}
        </>
)
}