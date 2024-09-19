import React, { useState, useEffect } from "react";
import './Login.css';
import { GoogleLogin } from '@react-oauth/google';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { useNavigate, Link } from 'react-router-dom';
import axios from 'axios';
import Cookies from 'js-cookie';  // Import js-cookie


function Login({ setIsAuthenticated }) {
    
  const [errorMessage, setErrorMessage] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

    const [formData, setFormData] = useState({
      username: '',
      password: '',
    });
  
    const navigate = useNavigate();
  
    const handleChange = (e) => {
      setFormData({
        ...formData,
        [e.target.name]: e.target.value
      });
    };
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
      
        const response = await axios.post('http://127.0.0.1:8000/api/login/', formData);
        
        console.log('Response:', response.data);
        console.log(response.data.token);
      
        // Store the token in a cookie with a 7-day expiration
        Cookies.set('token', response.data.token, { expires: 7});
        setIsAuthenticated(true);
      
        // Redirect to the chat page upon successful login
        navigate('/');
      } catch (error) {
        console.error('Error:', error);
      }
    };
  
  return (
    <div id="login_background">
      <div className="login-card">
        <div className="button-group">
          <Link to='/register'>
            <button className="btn2 signup" style={{ backgroundColor: '#e8faff', color: 'black' }}>Sign up</button>
          </Link>
          <Link to='/login'>
            <button className="btn2 login" style={{ backgroundColor: '#006E75', color: 'white' }}>Log in</button>
          </Link>
        </div>

        <div style={{ display: 'flex', justifyContent: 'center' }} className="mt-4">
          <GoogleOAuthProvider clientId="YOUR_GOOGLE_CLIENT_ID">
            <GoogleLogin
              onSuccess={(credentialResponse) => {
                console.log(credentialResponse);
              }}
              onError={() => {
                console.log('Login Failed');
              }}
            />
          </GoogleOAuthProvider>
        </div>

        <div className="or-divider mt-4">
          <span>OR</span>
        </div>

        <h2 className="mb-4 mt-4" style={{ fontFamily: "lato" }}>Log in</h2>

        <form id="loginForm" onSubmit={handleSubmit}>
          <div className="form-floating mb-3">
            <input
              type="text"
              className="form-control"
              id="floatingInput"
              placeholder="Username"
              value={formData.username}
              onChange={handleChange}
              name="username"
              required
            />
            <label htmlFor="floatingInput">Username</label>
          </div>

          <div className="form-floating mb-3">
            <input
              type="password"
              className="form-control"
              id="floatingPassword"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              name="password"
              required
            />
            <label htmlFor="floatingPassword">Password</label>
          </div>

          <button
            className="btn btn-success"
            style={{
              width: '60%',
              backgroundColor: '#006E75',
              color: 'white',
              fontWeight: 'bold',
            }}
            type="submit"
          >
            Login
          </button>
        </form>

        {/* Error and Success Messages */}
        {errorMessage && <p id="error-message" style={{ color: 'red', marginTop: '10px' }}>{errorMessage}</p>}
        {successMessage && <p id="success-message" style={{ color: 'green', marginTop: '10px' }}>{successMessage}</p>}
      </div>
    </div>
  );
}

export default Login;
