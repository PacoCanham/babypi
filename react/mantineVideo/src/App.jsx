import { useState } from 'react'
import '@mantine/core/styles.css';
import './App.css'
import { MantineProvider } from '@mantine/core';
import AppSh from './Components/AppShell/AppSh';

function App() {
  const [count, setCount] = useState(0)

  return (
 <MantineProvider>
    <AppSh/>
 </MantineProvider>
  )
}

export default App
