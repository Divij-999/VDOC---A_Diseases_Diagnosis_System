import React from 'react';
import './homePage.css';  // Replace with actual path if needed
import doctor1 from '../../assets/doctor1.jpg';  // Image 1 for the grid
import doctor2 from '../../assets/doctor2.jpg';  // Image 2 for the grid
import doctor3 from '../../assets/doctor3.jpg';  // Image 3 for the grid
import doctor4 from '../../assets/doctor4.jfif'
import microscope from '../../assets/microscope.jpg'
import Footer from '../Footer/footer'
import Header from '../Header/header';
import 'bootstrap/dist/css/bootstrap.min.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowUpRightFromSquare , faBrain } from '@fortawesome/free-solid-svg-icons';
import { faHeart , faCircle } from '@fortawesome/free-regular-svg-icons';
import { Link } from 'react-router-dom';


const HomePage = () => {
  return (
    <div className="app">
      {/* Header Section */}
      {/* <Header/> */}

      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          {/* <h1 className='heroh1'>Extraordinary Care is Right Here</h1> */}
          <h1 style={{lineHeight:'1rem',fontWeight:'bold',lineHeight:'3rem'}}>"Where Symptoms Meet Solutions"</h1>

          <div className="hero-buttons">
          <Link to='/chat' style={{textDecoration:'none'}}>
            <button className="btn">Chat with Us &nbsp;<strong><FontAwesomeIcon icon={faArrowUpRightFromSquare}/></strong></button>
          </Link>
            {/* <button className="btn">Schedule an <strong>Appointment</strong></button>
            <button className="btn">Log In to <strong>MyChart</strong></button> */}
          </div>
        </div>
      </section>
      <marquee behavior="scroll" direction="left" scrollamount="12" style={{fontWeight:'bold'}}>
      "The database used to develop the model is a sample database. Please consult a doctor before attempting any medications or remedies."</marquee>

      {/* Medical Info Section */}
      <div className="medical-page-container">
        <div className="medical-header text-center">
          <h1>Every patient is different, every smile is unique</h1>
        </div>

        <div className="medical-info-section my-5">
          <div className="medical-info-column">
            <div className="medical-info-box">
              <div className="medical-icon">&#10003;</div>
              <div className="medical-info-content">
                <h4>Accurate Diagnosis</h4>
                <p>We provide highly accurate predictions based on advanced algorithms, medical data, and symptom analysis to help guide your healthcare decisions.</p>
              </div>
            </div>

            <div className="medical-info-box">
              <div className="medical-icon">&#10003;</div>
              <div className="medical-info-content">
                <h4>Data Privacy First</h4>
                <p>Your personal health data is safe. We prioritize your privacy with secure data handling and encryption at every step.</p>
              </div>
            </div>

            <div className="medical-info-box">
              <div className="medical-icon">&#10003;</div>
              <div className="medical-info-content">
                <h4>Comprehensive Symptom Tracking</h4>
                <p>Track symptoms easily and get insights on potential conditions, tailored to your unique health profile.</p>
              </div>
            </div>
          </div>

          <div className="medical-image-column">
            <div className="medical-image-grid">
              <img src={doctor1} alt="Doctor Image 1" className="medical-img img-fluid my-3" />
              <img src={doctor2} alt="Doctor Image 2" className="medical-img img-fluid my-3" />
              <img src={doctor3} alt="Doctor Image 3" className="medical-img img-fluid my-3" />
              <img src={doctor4} alt="Doctor Image 3" className="medical-img img-fluid my-3" />
            </div>
          </div>
        </div>
      </div>
      <div className="why-choose-us">
      {/* Left Section - Image */}
      <div className="left-section">
        <img src={microscope} alt="Microscope" className="microscope-image" />
      </div>

      {/* Right Section - Text and Icons */}
      <div className="right-section">
        <h2>Why Choose Us</h2>
        <p>Our disease diagnosis system is built with cutting-edge technology</p>
        
        <div className="features-grid">
          <div className="feature-item">
            <div className="icon">&#128213;</div>
            <div className="feature-content">
              <h4>Trusted Platform</h4>
              <p>Our system uses sample medical databases and AI algorithms to provide predictions and insights.</p>
            </div>
          </div>

          <div className="feature-item">
            <div className="icon">&#128106;</div>
            <div className="feature-content">
              <h4>User-Friendly Interface</h4>
              <p>We ensure a simple and intuitive platform, making it easy for anyone to use and receive health guidance.</p>
            </div>
          </div>

          <div className="feature-item">
            <div className="icon">&#128176;</div>
            <div className="feature-content">
              <h4>Affordable & Accessible</h4>
              <p>Our services are designed to be cost-effective, providing high-quality health assessments at an affordable rate.</p>
            </div>
          </div>

          <div className="feature-item">
            <div className="icon">&#128197;</div>
            <div className="feature-content">
              <h4>Quick Results</h4>
              <p>Receive accurate health insights quickly and conveniently, without waiting for long appointments.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer/>
    </div>
  );
};

export default HomePage;
