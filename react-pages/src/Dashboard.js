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
    <div className="dashboard-container">
      <h1 className="dashboard-heading">Dashboard</h1>
      <button className="logout-btn" onClick={handleLogout}>
        Logout
      </button>
  
      <h2 className='add-credential-title'>Add New Credentials</h2>
      <form className="add-credential-form">
        <div className="input-group">
          <label className="input-label">Website:</label>
          <input
            type="text"
            value={newCredential.website}
            onChange={(e) => setNewCredential({ ...newCredential, website: e.target.value })}
            className="input-box"
          />
        </div>
        <div className="input-group">
          <label className="input-label">Username:</label>
          <input
            type="text"
            value={newCredential.username}
            onChange={(e) => setNewCredential({ ...newCredential, username: e.target.value })}
            className="input-box"
          />
        </div>
        <div className="input-group">
          <label className="input-label">Password:</label>
          <input
            type="password"
            value={newCredential.password}
            onChange={(e) => setNewCredential({ ...newCredential, password: e.target.value })}
            className="input-box"
          />
        </div>
        <button type="button" onClick={handleAddCredential} className="add-btn">
          Add
        </button>
      </form>
  
      
      <table className="credentials-table">
        <thead>
          <tr>
            <th>Website</th>
            <th>Username</th>
            <th>Password</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {credentials.map((credential, index) => (
            <tr key={index}>
              <td>{credential.website}</td>
              <td>{credential.username}</td>
              <td>{credential.password}</td>
              <td>
                <button className="delete-btn" onClick={() => handleDeleteCredential(credential.website)}>
                  Delete
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

