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

  // get username and viewers on launch
  useEffect(()=>{
    const getUsername = () => {
      fetch("/username")
       .then(response => response.json())
       .then(username => setUsername(username.username))
      };
    const getViewers = () => {
      fetch('/viewers')
       .then(response => response.json())
       .then(viewers => setViewers(viewers.viewers))
      };
      getUsername();
      getViewers();
    },[]); 

  //get viewers every 30seconds
  useEffect(() => {
    const getViewers = () => {
      fetch('/viewers')
        .then(response => response.json())
        .then(data => setViewers(data.viewers))
    };
    getViewers();
    const intervalId = setInterval(getViewers, 30000);
    return () => clearInterval(intervalId);
  }, []);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleSettings = () => {
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
          <VisibilityOutlined /> {viewers}
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
                <MenuItem onClick={handleSettings}>Settings</MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
                <MenuItem onClick={handleSettings}>Close Menu</MenuItem>
              </Menu>
            </div>
        </Toolbar>
      </AppBar>
    </Box>
  );
}