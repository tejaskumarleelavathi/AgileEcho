import React, { useState, useEffect, useRef } from 'react';
import './App.css';

const META_LLAMA_GIF = 'https://about.fb.com/wp-content/uploads/2024/04/Meta-AI-Expasion_Header.gif';
const INSIGHT_API_URL = 'http://127.0.0.1:8000/insight-analysis';

function SplashScreen({ onFinish }) {
  const [gifLoaded, setGifLoaded] = useState(false);
  const [showWelcome, setShowWelcome] = useState(false);

  useEffect(() => {
    if (gifLoaded) {
      const welcomeTimeout = setTimeout(() => setShowWelcome(true), 600);
      const finishTimeout = setTimeout(() => onFinish(), 2200);
      return () => {
        clearTimeout(welcomeTimeout);
        clearTimeout(finishTimeout);
      };
    }
  }, [gifLoaded, onFinish]);

  return (
    <div style={{
      position: 'fixed',
      zIndex: 99999,
      inset: 0,
      width: '100vw',
      height: '100vh',
      overflow: 'hidden',
      background: '#101820',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
    }}>
      <img
        src={META_LLAMA_GIF}
        alt="Meta Llama Loading"
        style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          objectFit: 'cover',
          zIndex: 1,
        }}
        onLoad={() => setGifLoaded(true)}
      />
      {showWelcome && (
        <div style={{
          position: 'relative',
          zIndex: 2,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
        }}>
          <div style={{ fontSize: 64, marginBottom: 24 }}>🦙</div>
          <div style={{
            color: '#fff',
            fontSize: '2rem',
            fontWeight: 700,
            marginTop: 0,
            opacity: 1,
            transition: 'opacity 0.6s',
            letterSpacing: '0.01em',
            textAlign: 'center',
            textShadow: '0 2px 16px #222',
          }}>
            Welcome Back, Tnaum-ms!
          </div>
        </div>
      )}
    </div>
  );
}

function AgileEchoHeader() {
  return (
    <div style={{
      width: '100%',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      marginTop: 32,
      marginBottom: 24,
    }}>
      <span style={{
        fontFamily: 'Poppins, sans-serif',
        fontWeight: 700,
        fontSize: '2.8rem',
        letterSpacing: '-2px',
        lineHeight: 1.05,
        textAlign: 'center',
      }}>
        <span style={{ color: '#e6ffe6' }}>Agile</span>
        <span style={{ color: '#2563eb' }}>Echo</span>
      </span>
    </div>
  );
}

const BOT_AVATAR = '🦙';
const USER_AVATAR = '🧑‍💻';

function GlassButton({ children, selected, onClick, style }) {
  return (
    <button
      onClick={onClick}
      style={{
        background: selected ? 'rgba(37,99,235,0.22)' : 'rgba(40,40,40,0.38)',
        color: selected ? '#2563eb' : '#e6ffe6',
        border: selected ? '2px solid #2563eb' : '1.5px solid rgba(255,255,255,0.18)',
        borderRadius: 18,
        fontWeight: 700,
        fontSize: '1.08rem',
        padding: '10px 28px',
        margin: '0 8px',
        boxShadow: '0 2px 12px 0 rgba(60,60,60,0.10)',
        backdropFilter: 'blur(12px)',
        WebkitBackdropFilter: 'blur(12px)',
        cursor: 'pointer',
        outline: 'none',
        transition: 'all 0.18s',
        ...style,
      }}
    >
      {children}
    </button>
  );
}

function GlassPopup({ title, insights, onClose }) {
  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, width: '100vw', height: '100vh',
      background: 'rgba(10,10,20,0.32)',
      zIndex: 9999,
      display: 'flex', alignItems: 'center', justifyContent: 'center',
    }} onClick={onClose}>
      <div
        style={{
          minWidth: 340, maxWidth: 480,
          background: 'rgba(40,40,40,0.38)',
          borderRadius: 28,
          boxShadow: '0 8px 32px 0 rgba(0,0,0,0.22)',
          border: '1.5px solid rgba(255,255,255,0.18)',
          backdropFilter: 'blur(18px)',
          WebkitBackdropFilter: 'blur(18px)',
          padding: '36px 32px 28px 32px',
          color: '#fff',
          position: 'relative',
          display: 'flex', flexDirection: 'column', alignItems: 'flex-start',
          cursor: 'auto',
        }}
        onClick={e => e.stopPropagation()}
      >
        <button onClick={onClose} style={{ position: 'absolute', top: 18, right: 18, background: 'none', border: 'none', color: '#fff', fontSize: 22, cursor: 'pointer', opacity: 0.7 }}>×</button>
        <div style={{ fontWeight: 700, fontSize: '1.2rem', color: '#e6ffe6', marginBottom: 12 }}>{title}</div>
        <ul style={{ color: '#bfc0c0', fontSize: '1.08rem', paddingLeft: 18 }}>
          {insights && insights.map((ins, i) => <li key={i} style={{ marginBottom: 6 }}>{ins}</li>)}
        </ul>
      </div>
    </div>
  );
}

function GlassTable({ issues, selectedIds, onSelect, onRowClick }) {
  return (
    <div style={{
      width: '100%',
      maxWidth: 820,
      margin: '24px auto',
      background: 'rgba(40,40,40,0.38)',
      borderRadius: 22,
      boxShadow: '0 4px 24px 0 rgba(60,60,60,0.13)',
      border: '1.5px solid rgba(255,255,255,0.18)',
      backdropFilter: 'blur(18px)',
      WebkitBackdropFilter: 'blur(18px)',
      padding: '18px 0',
      color: '#fff',
      fontSize: '1.08rem',
      overflow: 'auto',
    }}>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ color: '#e6ffe6', fontWeight: 700, fontSize: '1.1rem' }}>
            <th style={{ padding: '8px 0' }}>Select</th>
            <th style={{ textAlign: 'left', padding: '8px 0' }}>Issue</th>
            <th style={{ padding: '8px 0' }}>#</th>
          </tr>
        </thead>
        <tbody>
          {issues.map(issue => (
            <tr key={issue.id} style={{ background: selectedIds.includes(issue.id) ? 'rgba(37,99,235,0.13)' : 'transparent', cursor: 'pointer' }} onClick={() => onRowClick(issue)}>
              <td style={{ textAlign: 'center' }}>
                <input
                  type="checkbox"
                  checked={selectedIds.includes(issue.id)}
                  onChange={e => { e.stopPropagation(); onSelect(issue.id); }}
                  style={{ width: 18, height: 18 }}
                />
              </td>
              <td style={{ padding: '8px 0', color: '#fff', fontWeight: 500 }}>{issue.title}</td>
              <td style={{ color: '#2563eb', fontWeight: 700 }}>#{issue.id}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function ChatUI() {
  const [step, setStep] = useState(0); // 0: initial, 1: select type, 2: select priority, 3: select issues
  const [messages, setMessages] = useState([
    { sender: 'bot', text: "Hi, You haven't submitted your today's standup." },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [selectedTypes, setSelectedTypes] = useState([]);
  const [priority, setPriority] = useState(null);
  const [selectedIssues, setSelectedIssues] = useState([]);
  const [typeNextClicked, setTypeNextClicked] = useState(false);
  const [issuesNextClicked, setIssuesNextClicked] = useState(false);
  const [popup, setPopup] = useState(null); // { title, insights }
  const [insightData, setInsightData] = useState(null);
  const [fetching, setFetching] = useState(true);
  const chatEndRef = useRef(null);

  useEffect(() => {
    setFetching(true);
    fetch(INSIGHT_API_URL)
      .then(res => res.json())
      .then(data => setInsightData(data))
      .finally(() => setFetching(false));
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, step]);

  // Step 1: After initial message, show type selection
  useEffect(() => {
    if (step === 0) {
      setTimeout(() => {
        setMessages(msgs => [
          ...msgs,
          { sender: 'bot', text: 'On what part do you want to work on today?', type: 'type-select' },
        ]);
        setStep(1);
      }, 900);
    }
  }, [step]);

  // Step 2: After type selection, ask about priority (only after Next is clicked)
  useEffect(() => {
    if (step === 1 && typeNextClicked && selectedTypes.length > 0) {
      setTimeout(() => {
        setMessages(msgs => [
          ...msgs,
          { sender: 'bot', text: 'Do you want to work on low priorities as well or mixed?', type: 'priority-select' },
        ]);
        setStep(2);
        setTypeNextClicked(false);
      }, 600);
    }
  }, [step, typeNextClicked, selectedTypes]);

  // Step 3: After priority selection, show table
  useEffect(() => {
    if (step === 2 && priority) {
      setTimeout(() => {
        setMessages(msgs => [
          ...msgs,
          { sender: 'bot', text: 'Here are the issues. Which ones do you want to work on?', type: 'table-select' },
        ]);
        setStep(3);
      }, 600);
    }
  }, [step, priority]);

  // Step 4: After issues selected and Next clicked, allow chat input
  useEffect(() => {
    if (step === 3 && issuesNextClicked && selectedIssues.length > 0) {
      setTimeout(() => {
        setMessages(msgs => [
          ...msgs,
          { sender: 'bot', text: `Great! You selected ${selectedIssues.length} issue(s). You can now chat with me about your work.` },
        ]);
        setStep(4);
        setIssuesNextClicked(false);
      }, 600);
    }
  }, [step, issuesNextClicked, selectedIssues]);

  const handleTypeSelect = (type) => {
    setSelectedTypes(prev => prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]);
  };

  const handlePrioritySelect = (p) => {
    setPriority(p);
  };

  const handleIssueSelect = (id) => {
    setSelectedIssues(prev => prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]);
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages((msgs) => [...msgs, { sender: 'user', text: input }]);
    setInput('');
    setLoading(true);
    setTimeout(() => {
      setMessages((msgs) => [...msgs, { sender: 'bot', text: 'This is a sample bot reply.' }]);
      setLoading(false);
    }, 800);
  };

  // For table issues, use critical_issues_status.critical_issue_titles if available, else fallback
  const issues = insightData?.issue_analysis?.critical_issues_status?.critical_issue_titles?.map((title, idx) => ({
    id: 2000 + idx,
    title,
    insights: insightData.issue_analysis.critical_issues_status.insights
  })) || [];

  // For type buttons, show insights from open_vs_closed, critical_issues_status, current_sprint_status
  const typeInsights = {
    Feature: insightData?.issue_analysis?.open_vs_closed?.insights || [],
    Bug: insightData?.issue_analysis?.critical_issues_status?.insights || [],
    Task: insightData?.issue_analysis?.current_sprint_status?.insights || [],
  };

  return (
    <div style={{
      width: '100%',
      maxWidth: 820,
      margin: '0 auto',
      minHeight: 480,
      display: 'flex',
      flexDirection: 'column',
      background: 'transparent',
      borderRadius: 0,
      boxShadow: 'none',
      border: 'none',
      padding: '0 0 90px 0',
      position: 'relative',
    }}>
      {fetching && (
        <div style={{ color: '#e6ffe6', fontWeight: 700, fontSize: '1.2rem', textAlign: 'center', marginTop: 48 }}>Loading...</div>
      )}
      {!fetching && (
        <>
          <div style={{
            flex: 1,
            overflowY: 'auto',
            padding: '32px 0 12px 0',
            display: 'flex',
            flexDirection: 'column',
            gap: 18,
            minHeight: 320,
            maxHeight: '60vh',
          }}>
            {messages.map((msg, i) => (
              <div key={i} style={{
                display: 'flex',
                flexDirection: msg.sender === 'user' ? 'row-reverse' : 'row',
                alignItems: 'flex-end',
                gap: 12,
                width: '100%',
              }}>
                <span style={{ fontSize: 28 }}>{msg.sender === 'bot' ? BOT_AVATAR : USER_AVATAR}</span>
                <div style={{
                  background: 'rgba(40,40,40,0.38)',
                  borderRadius: 18,
                  boxShadow: '0 2px 8px 0 rgba(60,60,60,0.10)',
                  border: '1.5px solid rgba(255,255,255,0.13)',
                  backdropFilter: 'blur(18px)',
                  WebkitBackdropFilter: 'blur(18px)',
                  color: msg.sender === 'bot' ? '#e6ffe6' : '#2563eb',
                  padding: '12px 18px',
                  fontSize: '1.08rem',
                  fontWeight: 500,
                  maxWidth: 600,
                  wordBreak: 'break-word',
                  marginBottom: 2,
                  position: 'relative',
                }}>
                  {msg.text}
                  {/* Step 1: Type selection buttons */}
                  {msg.type === 'type-select' && step === 1 && (
                    <div style={{ display: 'flex', marginTop: 18 }}>
                      {['Feature', 'Bug', 'Task'].map(type => (
                        <GlassButton
                          key={type}
                          selected={selectedTypes.includes(type)}
                          onClick={() => handleTypeSelect(type)}
                          style={{ position: 'relative' }}
                        >
                          {type}
                          <span
                            style={{
                              position: 'absolute',
                              top: -28,
                              right: 0,
                              fontSize: 18,
                              cursor: 'pointer',
                              color: '#e6ffe6',
                              marginLeft: 6,
                            }}
                            onClick={e => { e.stopPropagation(); setPopup({ title: type, insights: typeInsights[type] }); }}
                            title={`Show insights for ${type}`}
                          >
                            ℹ️
                          </span>
                        </GlassButton>
                      ))}
                      {selectedTypes.length > 0 && (
                        <GlassButton
                          style={{ marginLeft: 18, background: '#2563eb', color: '#e6ffe6' }}
                          onClick={() => setTypeNextClicked(true)}
                        >
                          Next
                        </GlassButton>
                      )}
                    </div>
                  )}
                  {/* Step 2: Priority selection buttons */}
                  {msg.type === 'priority-select' && step === 2 && (
                    <div style={{ display: 'flex', marginTop: 18 }}>
                      {['Low Priorities', 'Mixed'].map(p => (
                        <GlassButton
                          key={p}
                          selected={priority === p}
                          onClick={() => handlePrioritySelect(p)}
                        >
                          {p}
                        </GlassButton>
                      ))}
                    </div>
                  )}
                  {/* Step 3: Table selection */}
                  {msg.type === 'table-select' && step === 3 && (
                    <>
                      <GlassTable
                        issues={issues}
                        selectedIds={selectedIssues}
                        onSelect={handleIssueSelect}
                        onRowClick={issue => setPopup({ title: issue.title, insights: issue.insights })}
                      />
                      {selectedIssues.length > 0 && (
                        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 12 }}>
                          <GlassButton
                            style={{ background: '#2563eb', color: '#e6ffe6' }}
                            onClick={() => setIssuesNextClicked(true)}
                          >
                            Next
                          </GlassButton>
                        </div>
                      )}
                    </>
                  )}
                </div>
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>
          <form onSubmit={handleSend} style={{
            position: 'fixed',
            left: 0,
            right: 0,
            bottom: 0,
            margin: '0 auto',
            width: '100%',
            maxWidth: 820,
            display: 'flex',
            alignItems: 'center',
            gap: 12,
            padding: '18px 24px 24px 24px',
            background: 'transparent',
            zIndex: 10,
            justifyContent: 'center',
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
                background: 'rgba(40,40,40,0.38)',
                color: '#fff',
                outline: 'none',
                fontWeight: 500,
                boxShadow: '0 2px 8px 0 rgba(60,60,60,0.10)',
                border: '1.5px solid rgba(255,255,255,0.13)',
                backdropFilter: 'blur(18px)',
                WebkitBackdropFilter: 'blur(18px)',
              }}
              disabled={step < 4 || loading}
            />
            <button
              type="submit"
              disabled={step < 4 || loading || !input.trim()}
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
          {popup && (
            <GlassPopup title={popup.title} insights={popup.insights} onClose={() => setPopup(null)} />
          )}
        </>
      )}
    </div>
  );
}

function App() {
  const [showSplash, setShowSplash] = useState(true);
  return (
    <div style={{ minHeight: '100vh', background: 'transparent' }}>
      {showSplash && <SplashScreen onFinish={() => setShowSplash(false)} />}
      {!showSplash && (
        <>
          <AgileEchoHeader />
          <ChatUI />
        </>
      )}
    </div>
  );
}

export default App;
