import * as React from 'react';
import { TextField, FormHelperText, Box, Button, FormControl } from '@mui/material';
import { useState } from 'react';
import AccountCircle from '@mui/icons-material/AccountCircle';

export default function LoginForm() {


    const [form, setForm] = useState({username:'', password:''});
    
    function handleChange(e){
      e.preventDefault()
      const name = e.target.name;
      const value = e.target.value;
      
      setForm((previous_value) => {
        return {
          ...previous_value,
          [name]: value
        }
      })
    };

    async function postForm(){
        const response = await fetch('/login', {
            method: 'POST',
            body: JSON.stringify(form),
            headers: {
            'Content-Type': 'application/json'
            }
        })
        const data = await response.json()
        return (data)
//        .then(response => {
//          const data = response.json()
//          return data
//        })
    }

    async function handleSubmit(e){
        e.preventDefault();
        const data = await postForm()
        if (data.url){
            window.location.assign(data.url)
        } else if (data.error){
            alert(data.error)
        }
    }

  return (
    <FormControl
      sx={{
      bgcolor: 'background.paper',
      boxShadow: 1,
      borderRadius: 5,
      p: 2,
      minWidth: 300,
    }}>
      <FormHelperText id="form_helper Text">Please enter Account information</FormHelperText>
    <Box
          component="form"
          sx={{
            '& .MuiTextField-root': { m: 1, width: '25ch' },
          }}
          noValidate
          autoComplete="off"
          onSubmit={handleSubmit}
        >
        <Box sx={{ display: 'flex', alignItems: 'flex-end' }}>
          <AccountCircle sx={{ 
            color:(form.username == "") ? "red" : "blue", mr: 1, my: 0.5 }}
          />
          <TextField
            required
            id="username-input"
            name = "username"
            label="Username"
            error = {(form.username === "")?true:false}
            color = "success"
            value = {form.username}
            onChange={handleChange}
          />        
        </Box>
        <Box sx={{ display: 'flex', alignItems: 'flex-end' }}>
            <AccountCircle 
            sx={{ 
              color:(form.password == "") ? "red" : "blue", mr: 1, my: 0.5 }}
            />
            <TextField
            required
            id="password-input"
            name = "password"
            label="Password"
            type="password"
            autoComplete="current-password"
            error = {(form.password === "")?true:false}
            color = "success"
            value = {form.password}
            onChange={handleChange}
        />
        </Box>

  
        <Button
        type="submit"
        variant="contained"
        color={((form.username == "" || form.password == "")? "error": "success")}
        disabled={((form.username == "" || form.password == "")? true: false)}
        size='large'
        sx={{marginLeft:5, marginRight:5}}>
          Log in
        </Button>


    </Box>
    </FormControl>

  );
}
