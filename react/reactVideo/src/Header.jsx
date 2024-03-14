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

export default function Header({showControls, setShowControls}) {
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
    closeMenu()
  };

  const handleNav = (e) => {
    e.preventDefault()
    const url = e.currentTarget.name
    window.location.assign(url)
  }

  function closeMenu(){
    setAnchorEl(null);
  }

  return (
    <Box sx={{ flexGrow: 1, position:"absolute", margin:0, padding:0, paddingBottom:5, width:"100vw", top:0, left:0}}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, textAlign:"start" }}>
            Hello {username}
          </Typography>
          {temp}°C <VisibilityOutlined /> {viewers}
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
                <MenuItem onClick={()=>setShowControls(!showControls)}>{(showControls)?"Hide":"Show"} Controls</MenuItem>
                <MenuItem name="/register" onClick={handleNav}>Register</MenuItem>
                <MenuItem name="/logout" onClick={handleNav}>Logout</MenuItem>
                <MenuItem onClick={closeMenu}>Close Menu</MenuItem>
              </Menu>
            </div>
        </Toolbar>
      </AppBar>
    </Box>
  );
}