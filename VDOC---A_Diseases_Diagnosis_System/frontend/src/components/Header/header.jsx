import React from 'react';
import logo from '../../assets/logo.png';
import './header.css';
import { Link } from 'react-router-dom'; // Correct import

const Header = () => {
  return (
    <header className="navbar" style={{padding:'15px 30px 15px 30px'}}>

      <div className="logo">
        <Link to='/'>
          <img src={logo} alt="Logo" />
        </Link>
      </div>

      <nav className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/chat">Services</Link>
        <Link to="/articles">Articles</Link>
        <Link to="/about">About</Link>
        <Link to="/contact">Contact</Link>
      </nav>
    </header>
  );
};

export default Header;
