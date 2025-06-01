import React, { useState, useRef, useEffect } from 'react';

const ASK_API_URL = 'http://127.0.0.1:8000/ask';

const BOT_AVATAR = '🦙';
const USER_AVATAR = '🧑‍💻';

const initialMessages = [
  {
    sender: 'bot',
    text: "Hi, You haven't submitted your today's standup.",
  },
];

const ChatbotApp = () => {
  const [messages, setMessages] = useState(initialMessages);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg = { sender: 'user', text: input };
    setMessages((msgs) => [...msgs, userMsg]);
    setInput('');
    setLoading(true);
    try {
      const res = await fetch(ASK_API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: input })
      });
      const data = await res.json();
      setMessages((msgs) => [...msgs, { sender: 'bot', text: data.answer }]);
    } catch {
      setMessages((msgs) => [...msgs, { sender: 'bot', text: 'Sorry, there was an error.' }]);
    }
    setLoading(false);
  };

  return (
    <div style={{
      width: '100%',
      maxWidth: 600,
      margin: '0 auto',
      display: 'flex',
      flexDirection: 'column',
      height: '70vh',
      background: 'rgba(40,40,40,0.38)',
      borderRadius: 28,
      boxShadow: '0 8px 32px 0 rgba(0,0,0,0.22)',
      border: '1.5px solid rgba(255,255,255,0.18)',
      backdropFilter: 'blur(18px)',
      WebkitBackdropFilter: 'blur(18px)',
      padding: '0 0 18px 0',
      position: 'relative',
    }}>
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '32px 32px 12px 32px',
        display: 'flex',
        flexDirection: 'column',
        gap: 18,
      }}>
        {messages.map((msg, i) => (
          <div key={i} style={{
            display: 'flex',
            flexDirection: msg.sender === 'user' ? 'row-reverse' : 'row',
            alignItems: 'flex-end',
            gap: 12,
          }}>
            <span style={{ fontSize: 28 }}>{msg.sender === 'bot' ? BOT_AVATAR : USER_AVATAR}</span>
            <div style={{
              background: msg.sender === 'bot' ? 'rgba(37,99,235,0.18)' : 'rgba(230,255,230,0.18)',
              color: msg.sender === 'bot' ? '#e6ffe6' : '#2563eb',
              borderRadius: 18,
              padding: '12px 18px',
              fontSize: '1.08rem',
              fontWeight: 500,
              maxWidth: 380,
              wordBreak: 'break-word',
              boxShadow: '0 2px 8px 0 rgba(60,60,60,0.10)',
              border: '1.5px solid rgba(255,255,255,0.13)',
              marginBottom: 2,
            }}>{msg.text}</div>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <form onSubmit={handleSend} style={{
        display: 'flex',
        alignItems: 'center',
        gap: 12,
        padding: '0 24px',
        marginTop: 8,
      }}>
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message..."
          style={{
            flex: 1,
            borderRadius: 18,
            border: 'none',
            padding: '14px 18px',
            fontSize: '1.08rem',
            background: 'rgba(255,255,255,0.13)',
            color: '#fff',
            outline: 'none',
            fontWeight: 500,
            boxShadow: '0 2px 8px 0 rgba(60,60,60,0.10)',
          }}
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          style={{
            background: '#2563eb',
            color: '#e6ffe6',
            border: 'none',
            borderRadius: 18,
            padding: '12px 22px',
            fontWeight: 700,
            fontSize: '1.08rem',
            cursor: loading ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.7 : 1,
            transition: 'background 0.18s',
          }}
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatbotApp; 