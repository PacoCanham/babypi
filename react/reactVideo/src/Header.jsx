import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';
import Settings from '@mui/icons-material/Settings';
import { useEffect } from 'react';
import { useState } from 'react';
import VisibilityOutlined from '@mui/icons-material/VisibilityOutlined';

export default function Header() {
  const [username, setUsername] = useState(null);
  const [anchorEl, setAnchorEl] = useState(null);
  const [viewers, setViewers] = useState(1);
  const [ledBool, setLedBool] = useState(true)
  const [temp, setTemp] = useState(null)

  // get username and viewers on launch
  useEffect(()=>{
    const getOnce = () => {
      fetch("/getOnce")
       .then(response => response.json())
       .then(dictionary => {
        setUsername(dictionary.username)
        setLedBool(dictionary.led)
        }
        )
      };
    const getUpdates = () => {
      fetch('/updates')
       .then(response => response.json())
       .then(viewers => setViewers(viewers.viewers))
      };
      getOnce();
      getUpdates();
    },[]); 

  //get viewers every 30seconds
  useEffect(() => {
    const getUpdates = () => {
      fetch('/updates')
        .then(response => response.json())
        .then(data => {
          setViewers(data.viewers)
          setTemp(data.temp)
        }
        )
    };
    getUpdates();
    const intervalId = setInterval(getUpdates, 30000);
    return () => clearInterval(intervalId);
  }, []);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleLEDs = () => {
    fetch('/led_on_off')
    setAnchorEl(null);
  };

  const handleLogout = () => {
    fetch('/logout')
     .then(response => response.json())
     .then(data => window.location.assign(data.url))
  }

  return (
    <Box sx={{ flexGrow: 1, position:"absolute", margin:0, padding:0, width:"100vw", top:0}}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Hello {username}
          </Typography>
          <VisibilityOutlined /> {viewers} - {temp}°C
            <div>
              <IconButton
                size="large"
                onClick={handleMenu}
                color="inherit"
              >
                <Settings/>
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorEl}
                anchorOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                keepMounted
                transformOrigin={{
                  vertical: 'top',
                  horizontal: 'right',
                }}
                open={Boolean(anchorEl)}
              >
                <MenuItem onClick={handleLEDs}>Turn LED's {(ledBool)?"ON":"OFF"}</MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
                <MenuItem onClick={()=>setAnchorEl(null)}>Close Menu</MenuItem>
              </Menu>
            </div>
        </Toolbar>
      </AppBar>
    </Box>
  );
}