// src/App.js
import React, { useState } from 'react';
import axios from 'axios';
import { API_REGISTER, API_LOGIN, API_SAVE_CREDENTIALS, API_VIEW_CREDENTIALS, API_LOGOUT } from './api';

function App() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const registerUser = async () => {
    try {
      const response = await axios.post(API_REGISTER, { email, password });
      
      // Check if response is defined and if response.data is defined
      if (response && response.data) {
        console.log(response.data.message);
      } else {
        console.error('Error registering user: Unexpected response format');
      }
    } catch (error) {
      if (error.response) {
        console.error('Error registering user:', error.response.data.message);
      } else {
        console.error('Error registering user:', error.message);
      }
    }
  };

  const loginUser = async () => {
    try {
      const response = await axios.post(API_LOGIN, { email, password }, { withCredentials: true });
      console.log(response.data.message);
    } catch (error) {
      if (error.response) {
        console.error('Error logging in:', error.response.data.message);
      } else {
        console.error('Error logging in:', error.message);
      }
    }
  };
  
  const logoutUser = async () => {
    try {
      const response = await axios.post(API_LOGOUT, {}, { withCredentials: true });
      console.log(response.data.message);
    } catch (error) {
      if (error.response) {
        console.error('Error logging out:', error.response.data.message);
      } else {
        console.error('Error logging out:', error.message);
      }
    }
  };
  

  return (
    <div>
      <h1>React App</h1>
      <div>
        <label>Email:</label>
        <input type="text" value={email} onChange={(e) => setEmail(e.target.value)} />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      </div>
      <div>
        <button onClick={registerUser}>Register</button>
        <button onClick={loginUser}>Login</button>
        <button onClick={logoutUser}>Logout</button>
      </div>
    </div>
  );
}

export default App;
