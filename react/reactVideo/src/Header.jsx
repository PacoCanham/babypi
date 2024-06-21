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
import EditNotificationsIcon from '@mui/icons-material/EditNotifications';

export default function Header({showControls, setShowControls, showNoise, setShowNoise, setVolume, setPlaystate, showFull, setShowFull}) {
  const [username, setUsername] = useState(null);
  const [anchorEl, setAnchorEl] = useState(null);
  const [viewers, setViewers] = useState(1);
  const [ledBool, setLedBool] = useState(false)
  const [temp, setTemp] = useState(null)
  const [alert, setAlert] = useState("")
  const [open, setOpen] = useState(false);
  const [showAlert, setShowAlert] = useState(false);


  // get username and viewers on launch
  useEffect(()=>{
    const getOnce = () => {
      fetch("/getOnce")
       .then(response => response.json())
       .then(dictionary => {
        setUsername(dictionary.username)
        setLedBool(dictionary.led)
        setTemp(dictionary.temp)
        setVolume(dictionary.volume)
        setPlaystate(dictionary.playstate)
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

  
  const restart_cam = () => {
    fetch('/restart_cam')
    closeMenu()
  }
  
  useEffect(() => {
    const newCam = () => {
      fetch('/restart_cam')
    };
    newCam();
    const intervalId = setInterval(newCam, 600000);
    return () => clearInterval(intervalId);
  }, []);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleLEDs = () => {
    fetch('/led_on_off')
    setLedBool(!ledBool)
    closeMenu()
  };

  const handleNav = (e) => {
    e.preventDefault()
    const url = e.currentTarget.id
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
        <EditNotificationsIcon fontSize="large" onclick=""/>
          {temp}°C <VisibilityOutlined /> {viewers}
            <div>
              <IconButton
                onClick={handleMenu}
                size="large"
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
                onClose={closeMenu}
              >
                <MenuItem onClick={handleLEDs}>Turn LED's {(ledBool)?"Off":"On"}</MenuItem>
                <MenuItem onClick={restart_cam}>Restart Camera</MenuItem>                
                <MenuItem onClick={()=>{setShowControls(!showControls);closeMenu()}}>{(showControls)?"Hide":"Show"} Controls</MenuItem>
                <MenuItem onClick={()=>{setShowFull(!showFull);closeMenu()}}>{(showFull)?"Hide":"Show"} Audio Player</MenuItem>
                <MenuItem onClick={()=>{setShowNoise(!showNoise);closeMenu()}}>{(showNoise)?"Hide":"Show"} Noise Player</MenuItem>
                <MenuItem id="/register" onClick={handleNav}>Register</MenuItem>
                <MenuItem id="/logout" onClick={handleNav}>Logout</MenuItem>
                {/* <MenuItem onClick={closeMenu}>Close Menu</MenuItem> */}
              </Menu>
            </div>
        </Toolbar>
      </AppBar>
      {showAlert && <AlertDialog title={"Notification Setrtings"} setShowAlert={setShowAlert} alert={alert}/>}
    </Box>
  );
}
