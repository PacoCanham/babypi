import { AppShell, Burger, Container, Flex } from '@mantine/core';
import { useDisclosure, useSetState } from '@mantine/hooks';
import Header from './Header/Header';
import MainPage from './Main/MainPage';

export default function AppSh(){
  const [opened, { toggle }] = useDisclosure();
  const [displayed, setDisplayed] = useSetState({
    leds:false,
    controls:false,
    microphone:false,
    player:false,
  })
  const [settings, setSettings] = useSetState({username:String,ledBool:Boolean,temp:21,volume:Number, viewers:0, notifications:true})



  return (
    <AppShell
      header={{ height: 60 }}
      padding="xl"
    >
      <AppShell.Header>
        <Burger
          opened={opened}
          onClick={toggle}
          hiddenFrom="sm"
          size="sm"
        />
        <Header displayed={displayed} setDisplayed={setDisplayed} settings={settings} setSettings={setSettings}/>
      </AppShell.Header>
      <AppShell.Main><MainPage displayed={displayed}/></AppShell.Main>
    </AppShell>
  );
}