import { Container, Flex, Grid, Group, Text, Title  } from "@mantine/core";
import { useDisclosure, useSetState } from "@mantine/hooks";
import { useEffect } from "react"
import HeaderMenu from "./Segments/HeaderMenu";
import { IconBell, IconBellOff, IconEye, IconNotification } from "@tabler/icons-react";

// playstate from parent
// volume from parent

export default function Header(props){

    useEffect(()=>{
        getOnce();
        getUpdates();
    },[])

    useEffect(() => {
        getUpdates();
        const intervalId = setInterval(getUpdates, 30000);
        return () => clearInterval(intervalId);
      }, []);
    

    const getOnce = () => {
        fetch("/getOnce")
        .then(response => response.json())
        .then(dictionary => {
        props.setSettings({username:dictionary.username, ledBool:dictionary.led, temp:dictionary.temp})
        props.setVolume(dictionary.volume)
        props.setPlaystate(dictionary.playstate)
        })};

    const getUpdates = () => {
        fetch('/updates')
            .then(response => response.json())
            .then(data => props.setSettings({viewers:data.viewers, temp:data.temp}))
        };
    

    return(
        <Container fluid h={"100%"} bg="var(--mantine-color-blue-light)">
        <Grid>
            <Grid.Col span={10}><Group justify="Space-Between" align="Center" >
                <Title order={1}>Hello {props.username}</Title><Text onClick={()=>{props.setSettings({notifications:!props.settings.notifications})}}>
            {(props.settings.notifications)?<IconBell/>:<IconBellOff/>}</Text></Group></Grid.Col>
            <Grid.Col span={1} align="right"><Group justify="Space-between" align="center" ><Text size="xl" fw={500}>{props.settings.temp}°C </Text><Group align="center"><Text size='xl'>{props.settings.viewers}</Text><IconEye size={32}/></Group></Group></Grid.Col>
            <Grid.Col span={1} align="left"><HeaderMenu displayed={props.displayed} setDisplayed={props.setDisplayed} settings={props.settings} setSettings={props.setSettings}/></Grid.Col>
    </Grid>
    </Container>
    )
}