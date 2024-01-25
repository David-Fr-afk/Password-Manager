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
    <div className="min-h-screen flex items-center justify-center">
      <div className="bg-white p-8 rounded shadow-md w-96 text-center">
        <h1 className="text-2xl font-bold mb-4 title">Password Manager</h1>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">Email:</label>
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500"
          />
        </div>
        <div className="mb-4">
          <label className="block text-gray-700 text-sm font-bold mb-2">Password:</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500"
          />
        </div>
        <div className="mb-4 flex justify-between">
          <button onClick={registerUser} className="bg-blue-500 text-white px-4 py-2 rounded focus:outline-none register-btn">
            Register
          </button>
          <button onClick={loginUser} className="bg-green-500 text-white px-4 py-2 rounded focus:outline-nonelogin-btn">
            Login
          </button>
        </div>
      </div>
    </div>
    </div>
  );
}

export default App;
