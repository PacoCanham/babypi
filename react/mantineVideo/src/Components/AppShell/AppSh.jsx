import { AppShell, Burger } from '@mantine/core';
import { useDisclosure, useSetState } from '@mantine/hooks';
import Header from './Header/Header';
import MainPage from './Main/MainPage';
import { useEffect } from 'react';

export default function AppSh(){
  const [opened, { toggle }] = useDisclosure();
  const [settings, setSettings] = useSetState({username:"", ledBool:true, temp:21, volume:10, viewers:0, notifications:true, playstate:false})
  const [notificationSettings, setNotificationSettings] = useSetState({vee:{},paco:{}})

  const [displayed, setDisplayed] = useSetState({
    leds:false,
    controls:false,
    microphone:false,
    player:false,
  })

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
    setSettings({username:dictionary.username, ledBool:dictionary.led, temp:dictionary.temp, volume:dictionary.volume, playstate:dictionary.playstate})
    })};

const getUpdates = () => {
    fetch('/updates')
        .then(response => response.json())
        .then(data => setSettings({viewers:data.viewers, temp:data.temp}))
    };

  return (
    <AppShell
      header={{ height: 60 }}
      padding="xl"
    >
      <AppShell.Header>
        <Header displayed={displayed} setDisplayed={setDisplayed} settings={settings} setSettings={setSettings}/>
      </AppShell.Header>
      <AppShell.Main><MainPage settings={settings} setSettings={setSettings} displayed={displayed}/></AppShell.Main>
    </AppShell>
  );
}


{/* <Burger
opened={opened}
onClick={toggle}
hiddenFrom="sm"
size="sm"
/> */}