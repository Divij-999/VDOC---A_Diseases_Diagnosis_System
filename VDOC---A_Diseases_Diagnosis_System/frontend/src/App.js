import logo from './logo.svg';
import './App.css';
import React, { useState, useEffect } from 'react';
import HomePage from './components/HomePage/homePage'
// import 'bootstrap/dist/css/bootstrap.min.css';
import Header from './components/Header/header';
import Contact from './components/ContactUs/contactUs'
import Footer from './components/Footer/footer';
import About from './components/About/AboutUs';
import ChatPage from './components/ChatPage/ChatPage';
import Login from './components/Login_Register/Login';
import Signup from './components/Login_Register/Signup';
import Articles from './components/Articles/Articles';
import { BrowserRouter as Router,Routes,Route } from 'react-router-dom';
import Cookies from 'js-cookie'


function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = Cookies.get('token');
    if (token) {
      setIsAuthenticated(true);
    }
  }, []);

  return (
    <div>
      <Router>
        <Header/>
        <Routes>
            <Route path='/' element={<HomePage/>}/>
            <Route path='/contact' element={<Contact/>}/>
            <Route path='/about' element={<About/>}/>
            <Route path="/chat" element={<ChatPage />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Signup />} />
            <Route path="/articles" element={<Articles />} />
        </Routes>
        {/* <Footer/> */}
      </Router>
    </div>
    // <>
    //   <Router>
    //     <Header/>
    //     <Routes>
    //       {isAuthenticated
    //         ?
    //         (
    //           <>
    //             <Route path="/" element={<HomePage/>} />
    //             <Route path="/articles" element={<Articles />} />
    //             <Route path="/chat" element={<ChatPage />} />
    //           </>
    //         )
    //         :
    //         (<>
    //             <Route path='/' element={<HomePage/>}/>
    //              <Route path='/contact' element={<Contact/>}/>
    //              <Route path='/about' element={<About/>}/>
    //              <Route path="/login" element={<Login />} />
    //              <Route path="/register" element={<Signup />} />
    //           </>)}
    //     </Routes>
    //   </Router>
    // </>
  );
}

export default App;
