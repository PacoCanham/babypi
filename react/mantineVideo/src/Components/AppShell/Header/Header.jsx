import { Container, Flex, Grid, Group, SimpleGrid, Text, Title  } from "@mantine/core";
import { useDisclosure, useSetState } from "@mantine/hooks";
import { useEffect } from "react"
import HeaderMenu from "./Segments/HeaderMenu";
import { IconBell, IconBellOff, IconEye, IconNotification } from "@tabler/icons-react";

// playstate from parent
// volume from parent

export default function Header(props){
    

    return(
    <Container fluid h={"100%"} bg="var(--mantine-color-blue-light)">
       <Flex
      mih={50}
      gap="md"
      justify="space-between"
      align="center"
      direction="row"
      wrap="nowrap">
        <Group>
            <Title flex="flex-start" order={1}>Hello {props.settings.username}</Title>
        </Group>
        <Group>
            <Text onClick={()=>{props.setSettings({notifications:!props.settings.notifications})}}>
            {(props.settings.notifications)?<IconBell/>:<IconBellOff/>}</Text>
            <Text size="xl" fw={500}>{props.settings.temp}°C </Text>
            <Text size='xl'>{props.settings.viewers}</Text>
            <IconEye size={32}/>
            <HeaderMenu displayed={props.displayed} setDisplayed={props.setDisplayed} settings={props.settings} setSettings={props.setSettings}/>
        </Group>
    </Flex>
    </Container>
    )
}