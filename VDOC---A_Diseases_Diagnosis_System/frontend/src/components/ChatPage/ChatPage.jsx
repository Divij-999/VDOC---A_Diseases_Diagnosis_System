import axios from 'axios';
import React, { useState, useEffect } from "react";
// import Navbar from "./Navbar";
import './ChatPage.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPenToSquare, faArrowUpFromBracket, faRobot } from '@fortawesome/free-solid-svg-icons';

function ChatPage() {
    const [text, setText] = useState('');
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        // Add a welcome message when the component is loaded
        setMessages([
            { date: new Date().toLocaleDateString(), message: 'Welcome! How can I assist you today?', messageFrom: 'server' }
        ]);
    }, []);

    useEffect(() => {
        // Scroll to bottom whenever messages change
        scrollToBottom();
    }, [messages]); // Run this effect whenever messages change

    const scrollToBottom = () => {
        const chatContainer = document.getElementById('chatpage_chat_content');
        if (chatContainer) {
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
    };

    const serverChat = (message) => {
        return (
            <div id='serverMessage' key={message.date + message.message}>
                <div id="serverMessageInner" className="btn">
                    <FontAwesomeIcon icon={faRobot} style={{ color: '#2C3E50', border: '2px solid black', padding: '9px', borderRadius: '50%', marginRight: '6px' }} />&nbsp;
                    <span style={{ textAlign: 'left', flex: 1 }}>
                        {message.message}
                    </span>
                </div>
            </div>
        );
    };

    const clientChat = (message) => {
        return (
            <div id='clientMessage' key={message.date + message.message}>
                <div id="clientMessageInner" className="btn">
                    {message.message}
                </div>
            </div>
        );
    };

    const addMessage = async () => {
        if (text !== '') {
            // Add the client's message to the messages array
            setMessages(prevMessages => [
                ...prevMessages,
                { date: new Date().toLocaleDateString(), message: text, messageFrom: 'client' }
            ]);

            try {
                console.log("Sending message to Rasa:", text); // Debugging line
                const response = await axios.post(process.env.REACT_APP_RASA_URL, {
                    sender: 'user',
                    message: text
                });

                // Add the server's response to the messages array
                setMessages(prevMessages => [
                    ...prevMessages,
                    { date: new Date().toLocaleDateString(), message: response.data[0].text, messageFrom: 'server' }
                ]);

                console.log("Received response from Rasa:", response.data[0].text);
            } catch (error) {
                console.error("Error sending message to Rasa:", error);
            }

            // Clear the text input
            setText('');
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            e.preventDefault(); // Prevent default behavior (e.g., form submission)
            addMessage(); // Call the function to add the message
        }
    };

    return (
        <div className="container-fluid" id='chatpage_body'>
            <main>
                <div id="chatpage_main_content" className="container-fluid" style={{ margin: 0, padding: 0 }}>
                    <div id="chatpage_history">
                        <div className="d-flex justify-content-center" style={{ height: '60px', padding: '10px' }}>
                            <button className="btn" style={{ backgroundColor: '#2C3E50', color: 'white', fontWeight: 'bold', width: '90%' }}>
                                New Chat &nbsp;<FontAwesomeIcon icon={faPenToSquare} style={{ fontSize: '20px' }} />
                            </button>
                        </div>
                    </div>
                    <div id="chatpage_chat_content">
                        <div className="container-fluid" id='chatpage_chat_content_display' style={{ color: 'black' ,paddingBottom:'120px'}}>
                            {
                                messages.map((message) => {
                                    return message.messageFrom === 'server' ? serverChat(message) : clientChat(message);
                                })
                            }
                            <div style={{ height: '90px' }}></div> {/* Extra space at the bottom */}
                        </div>
                        <div id='chat_prompt_space' className="container-fluid d-flex justify-content-center align-items-end pb-4">
                            <input
                                type="text"
                                id="promptText"
                                className="form-control"
                                onKeyDown={handleKeyDown}
                                value={text}
                                onChange={(e) => setText(e.target.value)}
                                placeholder="Enter your message"
                                style={{ width: '90%' }}
                            />
                            <button className="btn" style={{ backgroundColor: '#2C3E50', color: 'white', fontWeight: 'bold' }} onClick={addMessage}>
                                <FontAwesomeIcon icon={faArrowUpFromBracket} />
                            </button>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}

export default ChatPage;
