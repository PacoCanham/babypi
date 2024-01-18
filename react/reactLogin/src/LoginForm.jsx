import * as React from 'react';
import { styled, TextField, FormGroup, Box, Button } from '@mui/material';
import { useState } from 'react';

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
    <Box
          component="form"
          sx={{
            '& .MuiTextField-root': { m: 1, width: '25ch' },
          }}
          noValidate
          autoComplete="off"
          onSubmit={handleSubmit}
        >
          <FormGroup>
          <TextField
          focused
          required
          id="username-input"
          name = "username"
          label="Username"
          size="Large"
          error = {(form.username === "")?true:false}
          color = "success"
          value = {form.username}
          onChange={handleChange}
          sx={{ input: { color: 'white' } }}
        />
          <TextField
          focused
          id="password-input"
          name = "password"
          label="Password"
          type="password"
          autoComplete="current-password"
          size="Large"
          error = {(form.password === "")?true:false}
          color = "success"
          value = {form.password}
          onChange={handleChange}
          sx={{ input: { color: 'white' } }}
        />
        <Button
        type="submit"
        variant="contained"
        color={((form.username == "" || form.password == "")? "error": "success")}
        disabled={((form.username == "" || form.password == "")? true: false)}
        size='large'
        sx={{marginLeft:5, marginRight:5}}>
          Log in
        </Button>

        </FormGroup>
    </Box>

  );
}
