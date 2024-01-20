import * as React from 'react';
import { styled, TextField, FormGroup, Box, Button, FormControl } from '@mui/material';
import { useState } from 'react';

export default function RegisterForm() {


    const [form, setForm] = useState({username:'', password:'',confirmation:''});
    
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
      const response = await fetch('/register', {
          method: 'POST',
          body: JSON.stringify(form),
          headers: {
          'Content-Type': 'application/json'
          }
      })
      const data = await response.json()
      return (data)
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
    <Box
          component="form"
          sx={{
            '& .MuiTextField-root': { m: 1, width: '25ch' },
          }}
          noValidate
          autoComplete="off"
          onSubmit={handleSubmit}
        >
          <FormGroup sx={{alignItems:'center'}}>
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
        />
        <TextField
          focused
          id="confirmation-input"
          name = "confirmation"
          label="Confirm Password"
          type="password"
          size="Large"
          error = {(form.confirmation == "" || form.confirmation != form.password)?true:false}
          color = "success"
          value = {form.confirmation}
          onChange={handleChange}
          sx={{ input: { color: 'white' } }}
        />
        <Button
        type='submit'
        variant="contained"
        color={((form.username == "" || form.password == "" || form.confirmation == "" || form.confirmation != form.password)? "error": "success")}
        disabled={((form.username == "" || form.password == "" || form.confirmation == "" || form.confirmation != form.password) ? true: false)}
        size='large'
        sx={{marginLeft:5, marginRight:5}}>
          Register
        </Button>

        </FormGroup>
    </Box>
    </FormControl>

  );
}