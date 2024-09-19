import React from "react";
import './footer.css'

import { Link } from "react-router-dom";

function Footer(){
    return(
        <footer className="footer">
            <div className="footer-section quick-links">
                <h4>Quick Links</h4>
                <ul>
                    <Link to='/' className="link"><li>Home</li></Link>
                    <Link to='/chat' className="link"><li>Services</li></Link>
                    <Link to='/articles' className="link"><li>Article</li></Link>
                    <Link to='/about' className="link"><li>About</li></Link>
                    <Link to='/contact' className="link"><li>Contact</li></Link>
                </ul>
            </div>
            <div className="footer-section contact-info">
                <h4>Contact Info</h4>
                <ul>
                    <li>+91 7862954487</li>
                    <li>+91 6355053655</li>
                    <li>vdocter@gmail.com</li>
                    <li>22002170410010@ljku.edu.in</li>
                    <li>Ahmedabad, India - 380006</li>
                </ul>
            </div>
            <div className="footer-section follow-us">
                <h4>Follow Us</h4>
                <ul>
                    <li>Facebook</li>
                    <li>Twitter</li>
                    <li>Instagram</li>
                    <li>LinkedIn</li>
                </ul>
            </div>
            <div className="footer-bottom">
                Created By VDOC | All Rights Reserved!
            </div>
        </footer>
    )
}

export default Footer