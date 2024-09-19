import "./contactUs.css";
import Footer from "../Footer/footer";

function ContactForm() {
    return (
        <>
        <div className="form-container">
            <h1 className="form-title">Send A Message</h1>
            <form className="form">
                <input
                    type="text"
                    id="name"
                    className="form-input"
                    placeholder="Your Name"
                />

                <input
                    type="email"
                    id="email"
                    className="form-input"
                    placeholder="Your Email"
                />

                <input
                    type="text"
                    id="subject"
                    className="form-input"
                    placeholder="Subject"
                />

                <textarea
                    id="description"
                    className="form-textarea"
                    rows="4"
                    placeholder="Your Message"
                />

                <button
                    type="submit"
                    className="form-button"
                >
                    Send Message
                </button>
            </form>

            <div className="social-info">
                <p className="social-text">Follow us on Instagram:</p>
                <a href="https://www.instagram.com/" className="social-link">
                    @vdocter_healtunveiled
                </a>
            </div>

            <div className="contact-info">
                <p className="contact-text">Call us:</p>
                <a href="tel:+91 7862954487" className="contact-link">
                    +91 7862954487
                </a>
            </div>
        </div>
        <Footer/>
    </>
    );
}

export default ContactForm;
