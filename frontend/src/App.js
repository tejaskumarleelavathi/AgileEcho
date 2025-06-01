import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
import LevelHeader from './components/LevelHeader';
import Objectives from './components/Objectives';
import PracticalCards from './components/PracticalCards';
import TheoryCards from './components/TheoryCards';
import ChatBox from './components/ChatBox';
import Tabs from './components/Tabs';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import TeamProgress from './components/TeamProgress';
import TeamMembers from './components/TeamMembers';
import RetrospectiveCard from './components/RetrospectiveCard';
// import TeamProcess from './components/TeamProcess';

const META_LLAMA_GIF = 'https://about.fb.com/wp-content/uploads/2024/04/Meta-AI-Expasion_Header.gif';

function SplashScreen({ onFinish }) {
  const [gifLoaded, setGifLoaded] = useState(false);
  const [showWelcome, setShowWelcome] = useState(false);

  useEffect(() => {
    if (gifLoaded) {
      const welcomeTimeout = setTimeout(() => setShowWelcome(true), 600); // show welcome after gif loads
      const finishTimeout = setTimeout(() => onFinish(), 2200); // total splash duration
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
          {/* Lottie emoji placeholder */}
          <div style={{ fontSize: 64, marginBottom: 24 }}>👋</div>
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
            Welcome Back Scrum Master
          </div>
        </div>
      )}
    </div>
  );
}

function DailyPage({ insightData, loading, error }) {
  return (
    <div>
      <Header />
      <Tabs />
      <LevelHeader />
      <TeamMembers />
      <TeamProgress insightData={insightData} loading={loading} error={error} />
      <div className="chatbox-bottom-spacer" />
    </div>
  );
}

function OverviewPage({ insightData, loading, error }) {
  return (
    <>
      <Header />
      <Tabs />
      <LevelHeader />
      <Objectives insightData={insightData} loading={loading} error={error} />
      <PracticalCards insightData={insightData} />
      <TheoryCards insightData={insightData} loading={loading} error={error} />
      <ChatBox />
      <div className="chatbox-bottom-spacer" />
    </>
  );
}

function RetrospectivesPage({ insightData, loading, error }) {
  return (
    <>
      <Header />
      <Tabs />
      <LevelHeader />
      <RetrospectiveCard />
      {/* <div className="chatbox-bottom-spacer" /> */}
    </>
  );
}

function App() {
  const [splashDone, setSplashDone] = useState(false);
  const [insightData, setInsightData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch data as soon as the app loads
  useEffect(() => {
    fetch('http://127.0.0.1:8000/insight-analysis')
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch insight data');
        return res.json();
      })
      .then(data => {
        setInsightData(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  // Only show dashboard when both splash and data are ready
  const ready = splashDone && !loading;

  return (
    <>
      {(!ready) && <SplashScreen onFinish={() => setSplashDone(true)} />}
      {ready && (
        <Router>
          <Routes>
            <Route path="/" element={<OverviewPage insightData={insightData} loading={loading} error={error} />} />
            <Route path="/daily" element={<DailyPage insightData={insightData} loading={loading} error={error} />} />
            <Route path="/retrospectives" element={<RetrospectivesPage insightData={insightData} loading={loading} error={error} />} />
          </Routes>
        </Router>
      )}
    </>
  );
}

export default App;
