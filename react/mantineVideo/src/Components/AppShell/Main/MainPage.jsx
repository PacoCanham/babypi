import {Divider, Image } from "@mantine/core";
import Controls from "./Components/Controls";

export default function MainPage(props){
    return(<>
        <Image
        src={"/video.mjpeg"}
        radius={25}
        fallbackSrc="https://i.ytimg.com/vi/Y8G9_SexVjE/maxresdefault.jpg"
        />
        {(props.displayed.controls) && <><Divider label="Controls"/><Controls/></>}
        {(props.displayed.microphone) && <><Divider label="AudioStream Details"/></>}
        {(props.displayed.player) && <><Divider label="Audio Player"/></>}
        </>
)
}