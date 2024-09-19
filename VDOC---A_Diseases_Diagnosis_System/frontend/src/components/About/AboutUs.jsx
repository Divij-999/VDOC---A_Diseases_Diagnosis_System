import "./AboutUs.css";
// import Navbar from "../components/Navbar";
import img1 from '../../assets/aboutUs.jpg'
import Footer from "../Footer/footer";

function AboutUs() {
  return (<>
    <div className="about-container">
      <img src={img1}/>
      <h1>
      About VDOC
      </h1>
      <p>
      Welcome to VDOC, an advanced Disease Diagnosis System designed to support healthcare professionals and individuals in identifying and understanding potential health conditions. Our system leverages cutting-edge technology and a comprehensive database to offer accurate, real-time diagnostic support.
      </p>
      <h2>
      Our Mission
      </h2>
      <p>
      At VDOC, our mission is to enhance healthcare by providing a reliable, user-friendly platform that aids in the early detection and diagnosis of diseases. We strive to empower users with valuable insights while ensuring the highest standards of accuracy and reliability.
      </p>
      <h3>
      How It Works
      </h3>
      <p>
      <strong>VDOC</strong> uses a sophisticated randomstate algorithm to analyze symptoms and compare them against a vast database of diseases. The system provides a list of potential conditions based on the input symptoms, helping users and healthcare professionals make informed decisions.
      </p>
      <h3>
      Key Features
      </h3>
      <p>
        <ul>
          <li>
            <strong>Comprehensive Database : </strong>Access to a wide range of diseases and symptoms for thorough analysis.
          </li>
          <li>
            <strong>Real-Time Analysis : </strong>Instant feedback on potential conditions based on user inputs.
          </li>
          <li>
            <strong>User-Friendly Interface : </strong>Intuitive design for easy navigation and efficient use.
          </li>
        </ul>
      </p>
      <h3>Important Note</h3>
      <p>
        <strong>While VDOC is a powerful tool for understanding potential health issues, it is not a substitute for professional medical advice. We encourage users to consult with a healthcare professional for accurate diagnosis and treatment options.</strong>
      </p>
      <h3>
      Our Commitment
      </h3>
      <p>
      We are committed to continually improving our system to ensure it meets the evolving needs of the healthcare community. Your feedback is invaluable to us as we work towards providing the best diagnostic support available.
      </p>
      <h6>
      Thank you for choosing VDOC. We are here to assist you in your journey towards better health.
      </h6>
      
    </div>
    <Footer/>
    </>
  );
}

export default AboutUs;
