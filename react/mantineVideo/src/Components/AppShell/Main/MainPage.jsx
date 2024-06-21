import {Divider, Image } from "@mantine/core";
import Controls from "./Components/Controls";
import AudioPlayer from "./Components/AudioPlayer";

export default function MainPage(props){
    return(<>
        <Image
        src={"/video.mjpeg"}
        radius={25}
        fallbackSrc="static/maxresdefault.jpg"
        p={25}
        />
        {(props.displayed.controls) && <><Divider label="Controls"/><Controls/></>}
        {(props.displayed.microphone) && <><Divider label="AudioStream Details"/></>}<AudioPlayer showFull={props.displayed.microphone}/>
        {(props.displayed.player) && <><Divider label="Audio Player"/></>}
        </>
)
}