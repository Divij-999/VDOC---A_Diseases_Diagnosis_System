import React, { useState, useEffect } from "react";
import './Login.css';
import { GoogleLogin } from '@react-oauth/google';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { useNavigate, Link } from 'react-router-dom';
import axios from "axios";
import Cookies from 'js-cookie';  // Import js-cookie


// function Signup() {
    //   const [errorMessage, setErrorMessage] = useState('');
    //   const [successMessage, setSuccessMessage] = useState('');
    
    //   const navigate = useNavigate();

//   useEffect(() => {
//     // Fetch CSRF token when the component mounts
//     axios.get('http://127.0.0.1:8000/api/csrf-token/', { withCredentials: true })
//       .then(response => {
//         console.log("CSRF token fetched");
//       })
//       .catch(error => {
//         console.error("Failed to fetch CSRF token:", error);
//       });
//   }, []);

//   const handleSubmit = async (event) => {
//     event.preventDefault(); // Prevent the form from submitting

//     setErrorMessage('');
//     setSuccessMessage('');

//     const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
//     const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/;

//     if (!emailRegex.test(email)) {
//       setErrorMessage('Please enter a valid email address.');
//       return;
//     }

//     if (!passwordRegex.test(password)) {
//       setErrorMessage('Password must be at least 8 characters long, include one uppercase letter, one lowercase letter, and one number.');
//       return;
//     }

//     const csrfToken = getCSRFToken();

//     if (!csrfToken) {
    //       setErrorMessage('CSRF token not found. Please reload the page.');
    //       return;
//     }

//     try {
    //       const response = await axios.post(
//         'http://127.0.0.1:8000/api/signup/',
//         { username, email, password },
//         {
//           headers: {
    //             'Content-Type': 'application/json',
    //             'X-CSRFToken': csrfToken, // Include CSRF token in headers
//           },
//           withCredentials: true, // Include cookies in the request
//         }
//       );

//       if (response.status === 201) {
//         setSuccessMessage('Signup successful! Redirecting to login...');
//         setTimeout(() => {
//           navigate('/login');
//         }, 2000);
//       } else {
//         setErrorMessage('Signup failed. Please try again.');
//       }
//     } catch (error) {
//       setErrorMessage(error.response?.data?.error || 'An unexpected error occurred.');
//     }
//   };
function Signup({setIsAuthenticated}) {
    
    const [email, setEmail] = useState('');
    // const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    const [formData, setFormData] = useState({
      username: '',
      email: '',
      password: '',
      first_name: '',
      last_name: ''
    });
    const navigate = useNavigate(); // To navigate programmatically
  
    const handleChange = (e) => {
      setFormData({
        ...formData,
        [e.target.name]: e.target.value
      });
    };
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      try {
        setErrorMessage('');
        setSuccessMessage('');

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$/;

        if (!emailRegex.test(email)) {
        setErrorMessage('Please enter a valid email address.');
        return;
        }

        if (!passwordRegex.test(password)) {
        setErrorMessage('Password must be at least 8 characters long, include one uppercase letter, one lowercase letter, and one number.');
        return;
        }
        
        const response = await axios.post('http://127.0.0.1:8000/api/register/', formData);
        
        // Store the token in a cookie with a 7-day expiration
        Cookies.set('token', response.data.token, { expires: 7});
  
        setIsAuthenticated(true);
        // Redirect to the create chat page
        if (response.status === 201) {
            setSuccessMessage('Signup successful! Redirecting to login...');
            setTimeout(() => {
                navigate('/');
            }, 2000);
            }
        else {
            setErrorMessage('Signup failed. Please try again.');
        }
    } catch (error) {
        console.error('Error:', error);
        setErrorMessage(error.response?.data?.error || 'An unexpected error occurred.');
      }
    };
  

  return (
    <div id="login_background">
      <div className="login-card">
        <div className="button-group">
          <Link to='/register'>
            <button className="btn2 signup" style={{ backgroundColor: '#006E75', color: 'white' }}>Sign up</button>
          </Link>
          <Link to='/login'>
            <button className="btn2 login" style={{ backgroundColor: '#e8faff', color: 'black' }}>Log in</button>
          </Link>
        </div>

        <div style={{ display: 'flex', justifyContent: 'center' }} className="mt-4">
          <GoogleOAuthProvider clientId="YOUR_GOOGLE_CLIENT_ID">
            <GoogleLogin
              onSuccess={(credentialResponse) => {
                console.log(credentialResponse);
                // Handle Google login success
              }}
              onError={() => {
                console.log('Google Login Failed');
              }}
            />
          </GoogleOAuthProvider>
        </div>

        <div className="or-divider mt-4">
          <span>OR</span>
        </div>

        <h2 className="mb-4 mt-4" style={{ fontFamily: "lato" }}>Create a New Account</h2>

        <form id="signupForm" onSubmit={handleSubmit}>

          <div className="form-floating mb-3">
            <input
              type="text"
              className="form-control"
              id="floatingUsername"
              placeholder="Username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
            />
            <label htmlFor="floatingUsername">Username</label>
          </div>

          <div className="form-floating mb-3">
            <input
              type="email"
              className="form-control"
              id="floatingEmail"
              placeholder="name@example.com"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
            <label htmlFor="floatingEmail">Email Address</label>
          </div>

          <div className="form-floating mb-3">
            <input
              type="password"
              className="form-control"
              id="floatingPassword"
              placeholder="Password"
              name="password"
              value={formData.password}
              onChange={handleChange}
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
            Sign Up
          </button>
        </form>

        {/* Error Message Display */}
        {errorMessage && <p id="error-message" style={{ color: 'red', marginTop: '10px' }}>{errorMessage}</p>}
        {successMessage && <p id="success-message" style={{ color: 'green', marginTop: '10px' }}>{successMessage}</p>}
      </div>
    </div>
  );
}

export default Signup;
