import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import {
  API_SAVE_CREDENTIALS,
  API_VIEW_CREDENTIALS,
  API_LOGOUT,
  API_DELETE_CREDENTIALS
} from './api';

function Dashboard() {
  const [credentials, setCredentials] = useState([]);
  const [newCredential, setNewCredential] = useState({
    website: '',
    username: '',
    password: '',
  });
  const navigate = useNavigate();

  useEffect(() => {
    // Fetch credentials on component mount
    handleViewCredentials();
  }, []);

  // Example function to save credentials
  const handleSaveCredentials = async (credentials) => {
    try {
      const response = await axios.post(API_SAVE_CREDENTIALS, credentials, { withCredentials: true });
      console.log('Credentials saved successfully:', response.data);
      // Handle success
    } catch (error) {
      console.error('Error saving credentials:', error.message);
      // Handle error
    }
  };

  const handleViewCredentials = async () => {
    try {
      const response = await axios.get(API_VIEW_CREDENTIALS, { withCredentials: true });
      const credentialsArray = Object.entries(response.data).map(([website, credential]) => ({
        website,
        ...credential,
      }));
      setCredentials(credentialsArray);
    } catch (error) {
      console.error('Error fetching credentials:', error.message);
      // Handle error
    }
  };

  const handleDeleteCredential = async (website) => {
    try {
      await axios.post(API_DELETE_CREDENTIALS, { website }, { withCredentials: true });
  
      // After deletion, refresh the credentials
      handleViewCredentials();
    } catch (error) {
      console.error('Error deleting credential:', error.message);
      // Handle error
    }
  };

  const handleLogout = async () => {
    try {
      await axios.post(API_LOGOUT, null, { withCredentials: true });
      console.log('Logged out successfully');

      // Redirect to the login/register page after successful logout
      navigate('/', { replace: true });
    } catch (error) {
      console.error('Error logging out:', error.message);
      // Handle error
    }
  };

  // Example function to add new credential
  const handleAddCredential = async () => {
    try {
      // Save the new credential
      await handleSaveCredentials(newCredential);

      setNewCredential({
        website: '',
        username: '',
        password: '',
      });
  
      // Refetch all credentials including the new one
      await handleViewCredentials();
    } catch (error) {
      console.error('Error adding credential:', error.message);
      // Handle error
    }
  };

  return (
    <div>
      <h1>Dashboard</h1>
      <button onClick={handleLogout}>Logout</button>
  
      <h2 className='credtitle ADD'>Add New Credentials</h2>
      <form>
        <label className='inputbox'>
          Website:
          <input
            type="text"
            value={newCredential.website}
            onChange={(e) => setNewCredential({ ...newCredential, website: e.target.value })}
          />
        </label>
        <label className='inputbox'>
          Username:
          <input
            type="text"
            value={newCredential.username}
            onChange={(e) => setNewCredential({ ...newCredential, username: e.target.value })}
          />
        </label>
        <label className='inputbox'>
          Password:
          <input
            type="password"
            value={newCredential.password}
            onChange={(e) => setNewCredential({ ...newCredential, password: e.target.value })}
          />
        </label>
        <button type="button" onClick={handleAddCredential}>
          +
        </button>
      </form>
  
      <h2 className='credtitle'>Credentials</h2>
      <table>
        <thead>
          <tr>
            <th>Website</th>
            <th>Username</th>
            <th>Password</th>
            <th>Delete</th>
          </tr>
        </thead>
        <tbody>
          {credentials.map((credential, index) => (
            <tr key={index}>
              <td>{credential.website}</td>
              <td>{credential.username}</td>
              <td>{credential.password}</td>
              <td>
                <button type="button" onClick={() => handleDeleteCredential(credential.website)}>
                  -
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}  

export default Dashboard;

