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

export default function App() {
  const [username, setUsername] = useState(null);
  const [anchorEl, setAnchorEl] = useState(null);
  const [viewers, setViewers] = useState(1);
  useEffect(()=>{(
    async function getUsername()
    {const response = await fetch("/username").then (setUsername(response));}
  )}, []); 

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
    console.log("logout")
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
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
              </Menu>
            </div>
        </Toolbar>
      </AppBar>
    </Box>
  );
}