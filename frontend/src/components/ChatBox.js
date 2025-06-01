import React, { useState, useEffect } from 'react';
import './ChatBox.css';

const ChatBox = () => {
  const [input, setInput] = useState('');
  const [show, setShow] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 80) {
        setShow(true);
      } else {
        setShow(false);
      }
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setInput('');
  };

  return (
    <form className={`chatbox-bar-center${show ? ' show' : ''}`} onSubmit={handleSend}>
      <input
        className="chatbox-bar-input"
        type="text"
        placeholder="Send a message..."
        value={input}
        onChange={e => setInput(e.target.value)}
      />
      <button className="chatbox-bar-send" type="submit" aria-label="Send">
        <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M6 14H22M22 14L16 8M22 14L16 20" stroke="#888" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
        </svg>
      </button>
    </form>
  );
};

export default ChatBox; 