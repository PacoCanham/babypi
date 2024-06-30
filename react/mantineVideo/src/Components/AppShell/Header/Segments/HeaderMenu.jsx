import { Flex, Menu, Button, rem, Modal} from "@mantine/core";
import { useMediaQuery, useDisclosure } from "@mantine/hooks";

import {
    IconSettings,
    IconSunHigh,
    IconArrowsMove,
    IconEar,
    IconPlaylist,
    IconLogout,
    IconUserPlus,
    IconDeviceCctv,
    IconMicrophone2,
  } from '@tabler/icons-react';
import VideoNotificationModal from "./VideoNotificationModal";
import AudioNotificationModal from "./AudioNotificationModal";

  
  export default function HeaderMenu(props){    
    const [notificationsModal, {open, close}] = useDisclosure(false);
    const [isVideo, changeVideo] = useDisclosure(true)
    const isMobile = useMediaQuery('(max-width: 50em)');

    function handleAccount(e){
        e.preventDefault()
        const url = e.currentTarget.id
        window.location.assign(url)
    }

    function closeVideo(){
        setVideoOpened.close()
    }
    return(
    <Flex
        mih={50}
        gap="md"
        justify="flex-end"
        align="center"
        direction="row"
        wrap="wrap"
        >
        <Menu shadow="md" width={200}>
        <Menu.Target>
            <Button w={100}><IconSettings/></Button>
        </Menu.Target>

        <Menu.Dropdown>
            <Menu.Label>Camera Options</Menu.Label>
            <Menu.Item onClick={()=>{props.setDisplayed({leds:!props.displayed.leds});fetch('/led_on_off')}} leftSection={<IconSunHigh style={{ width: rem(14), height: rem(14) }} />}>
            IR Light {(props.displayed.leds)?'Off':'On'}
            </Menu.Item>
            <Menu.Item onClick={()=>{props.setDisplayed({controls:!props.displayed.controls})}} leftSection={<IconArrowsMove style={{ width: rem(14), height: rem(14) }} />}>
            {(props.displayed.controls)?'Hide':'Show'} Controls
            </Menu.Item>
            <Menu.Item onClick={()=>{props.setDisplayed({microphone:!props.displayed.microphone})}} leftSection={<IconEar style={{ width: rem(14), height: rem(14) }} />}>
            {(props.displayed.microphone)?'Hide':'Show'} Audio Controls
            </Menu.Item>
            <Menu.Item onClick={()=>{props.setDisplayed({player:!props.displayed.player})}} leftSection={<IconPlaylist style={{ width: rem(14), height: rem(14) }} />}>
            {(props.displayed.player)?'Hide':'Show'} Music Player
            </Menu.Item>
            <Menu.Divider />

            <Menu.Label>Notification Settings</Menu.Label>
            <Menu.Item onClick={()=>{open(), changeVideo.open()}} leftSection={<IconDeviceCctv style={{ width: rem(14), height: rem(14) }} />}>
            Video Notifications
            </Menu.Item>
            <Menu.Item onClick={()=>{open(), changeVideo.close()}} leftSection={<IconMicrophone2 style={{ width: rem(14), height: rem(14) }} />}>
            Audio Notification
            </Menu.Item>
            <Menu.Divider />

            <Menu.Label>Account Settings</Menu.Label>
            <Menu.Item id="/logout" onClick={handleAccount} color='red' leftSection={<IconLogout style={{ width: rem(14), height: rem(14) }} />}>
            Logout
            </Menu.Item>
            <Menu.Item id="/register" onClick={handleAccount} color="green" leftSection={<IconUserPlus style={{ width: rem(14), height: rem(14) }} />}>
            Create New Account
            </Menu.Item>
        </Menu.Dropdown>
        </Menu>
        <Modal
            opened={notificationsModal}
            onClose={close}
            title={`${(isVideo)?"Video":"Audio"} Notification Settings`}
            size="xl"
            fullScreen={isMobile}
            transitionProps={{ transition: 'fade', duration: 200 }}
        >
        {isVideo ? <VideoNotificationModal/>: <AudioNotificationModal/>}
</Modal>
        </Flex>
    )
}