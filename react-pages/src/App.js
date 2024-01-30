// src/App.js
import './styles/index.css';
import React, { useState } from 'react';
import axios from 'axios';
import { API_REGISTER, API_LOGIN} from './api';



function App({ onLogin }) {
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
      onLogin(true)
    } catch (error) {
      if (error.response) {
        console.error('Error logging in:', error.response.data.message);
      } else {
        console.error('Error logging in:', error.message);
      }
    }
  };
  

  return (
    <div className="container">
      <div className="form-container">
        <h1>Password Manager</h1>
        <div className="input-group">
          <label className="label" htmlFor="email">Email:</label>
          <input
            type="text"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="input-box"
          />
        </div>
        <div className="input-group">
          <label className="label" htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input-box"
          />
        </div>
        <div className="button-group">
          <button onClick={registerUser} className="button register-btn">
            Register
          </button>
          <button onClick={loginUser} className="button login-btn">
            Login
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
