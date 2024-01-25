import React from 'react';
import { Route, Routes, Navigate } from 'react-router-dom';
import App from './App';
import Dashboard from './Dashboard';
import { useNavigate } from 'react-router-dom';

const AppRouter = () => {
  const navigate = useNavigate();
  const [loggedIn, setLoggedIn] = React.useState(false);


  const handleLogin = (status) => {
    setLoggedIn(status);
    console.log('Logged in state:', status);

    try{
      if (status) {
        navigate('/dashboard');
      }
    }
    catch(error){
      console.log("Did not redirect")
    }
  };

  return (
      <Routes>
        <Route
          path="/dashboard"
          element={loggedIn ? <Dashboard /> : <Navigate to="/" replace />}
        />
        <Route
          path="/"
          element={<App onLogin={handleLogin} />}
        />
      </Routes>  
  );
};

export default AppRouter;
