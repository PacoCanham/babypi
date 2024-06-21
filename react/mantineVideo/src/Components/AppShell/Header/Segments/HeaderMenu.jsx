import { Flex, Menu, Button, rem} from "@mantine/core";

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

export default function HeaderMenu(props){
    function handleAccount(e){
        e.preventDefault()
        const url = e.currentTarget.id
        window.location.assign(url)
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
            <Menu.Item onClick={()=>{props.setDisplayed({leds:!props.displayed.leds})}} leftSection={<IconSunHigh style={{ width: rem(14), height: rem(14) }} />}>
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
            <Menu.Item leftSection={<IconDeviceCctv style={{ width: rem(14), height: rem(14) }} />}>
            Video Notifications
            </Menu.Item>
            <Menu.Item leftSection={<IconMicrophone2 style={{ width: rem(14), height: rem(14) }} />}>
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
        </Flex>
    )
}