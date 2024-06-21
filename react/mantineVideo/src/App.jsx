import { useState } from 'react'
import { MantineProvider } from '@mantine/core';
import '@mantine/core/styles.css';
import AppSh from './Components/AppShell/AppSh';
import './App.css'

function App() {

  return (
 <MantineProvider defaultColorScheme="dark">
    <AppSh/>
 </MantineProvider>
  )
}

export default App
