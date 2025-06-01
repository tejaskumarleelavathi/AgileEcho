import React, { useState, useEffect } from 'react';
import './ChatBox.css';

const ASK_API_URL = 'http://127.0.0.1:8000/ask';

const ChatBox = () => {
  const [input, setInput] = useState('');
  const [answerType, setAnswerType] = useState('brief');
  const [hasScrolled, setHasScrolled] = useState(false);
  const [popup, setPopup] = useState(null); // { loading, answer, error, question }

  useEffect(() => {
    const showChatbox = () => {
      if (!hasScrolled) setHasScrolled(true);
    };
    const handleScroll = () => {
      if (window.scrollY > 0 && !hasScrolled) setHasScrolled(true);
    };
    window.addEventListener('scroll', handleScroll);
    window.addEventListener('wheel', showChatbox, { passive: true });
    window.addEventListener('touchmove', showChatbox, { passive: true });
    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('wheel', showChatbox);
      window.removeEventListener('touchmove', showChatbox);
    };
  }, [hasScrolled]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setPopup({ loading: true, answer: null, error: null, question: input });
    try {
      const res = await fetch(ASK_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input })
      });
      if (!res.ok) throw new Error('Error fetching answer');
      const data = await res.json();
      setPopup({ loading: false, answer: data.answer, error: null, question: input });
    } catch {
      setPopup({ loading: false, answer: null, error: 'Error fetching answer', question: input });
    }
    setInput('');
  };

  const closePopup = () => setPopup(null);

  if (!hasScrolled) return null;

  return (
    <>
      {popup && (
        <div style={{
          position: 'fixed',
          left: 0,
          right: 0,
          bottom: 120,
          zIndex: 10000,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'flex-end',
          pointerEvents: 'none',
        }}>
          <div
            style={{
              minWidth: 320,
              maxWidth: 480,
              background: 'rgba(40,40,40,0.38)',
              borderRadius: 28,
              boxShadow: '0 8px 32px 0 rgba(0,0,0,0.22)',
              border: '1.5px solid rgba(255,255,255,0.18)',
              backdropFilter: 'blur(18px)',
              WebkitBackdropFilter: 'blur(18px)',
              padding: '32px 28px 24px 28px',
              color: '#fff',
              position: 'relative',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              pointerEvents: 'auto',
              marginBottom: 16,
            }}
          >
            <button onClick={closePopup} style={{ position: 'absolute', top: 18, right: 18, background: 'none', border: 'none', color: '#fff', fontSize: 22, cursor: 'pointer', opacity: 0.7 }}>×</button>
            <div style={{ fontWeight: 700, fontSize: '1.1rem', marginBottom: 10, color: '#e6ffe6' }}>Your Question</div>
            <div style={{ color: '#fff', fontSize: '1.08rem', marginBottom: 18, textAlign: 'center' }}>{popup.question}</div>
            {popup.loading && <div style={{ color: '#bfc0c0', fontSize: '1.1rem' }}>Loading answer...</div>}
            {popup.error && <div style={{ color: '#ffb4b4', fontSize: '1.1rem' }}>{popup.error}</div>}
            {popup.answer && (
              <div style={{ marginTop: 10, width: '100%' }}>
                <div style={{ fontWeight: 700, color: '#e6ffe6', marginBottom: 8 }}>Answer</div>
                <div style={{ color: '#fff', fontSize: '1.08rem', textAlign: 'center' }}>{popup.answer}</div>
              </div>
            )}
          </div>
        </div>
      )}
      <div className={`chatbox-container chatbox-bar-center show`}>
        <form className="chatbox-bar-form" onSubmit={handleSend} style={{ width: '100%' }}>
          <div className="chatbox-bar-input-row" style={{ display: 'flex', alignItems: 'center', width: '100%', position: 'relative' }}>
            <input
              className="chatbox-bar-input"
              type="text"
              placeholder="Send a message..."
              value={input}
              onChange={e => setInput(e.target.value)}
              style={{ paddingRight: 56 }}
            />
            <button className="chatbox-bar-send" type="submit" aria-label="Send">
              <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M6 14H22M22 14L16 8M22 14L16 20" stroke="#888" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
        </form>
      </div>
    </>
  );
}

export default ChatBox; 