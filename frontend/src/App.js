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

function DailyPage() {
  return (
    <div>
      <Header />
      <Tabs />
      <LevelHeader />
      <TeamMembers />
      <TeamProgress />
      <div className="chatbox-bottom-spacer" />
    </div>
  );
}

function OverviewPage() {
  return (
    <>
      <Header />
      <Tabs />
      <LevelHeader />
      <Objectives />
      <PracticalCards />
      <TheoryCards />
      <ChatBox />
      <div className="chatbox-bottom-spacer" />
    </>
  );
}

function RetrospectivesPage() {
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
  const [showSplash, setShowSplash] = useState(true);
  useEffect(() => {
    if (!showSplash) return;
  }, [showSplash]);
  return (
    <>
      {showSplash && <SplashScreen onFinish={() => setShowSplash(false)} />}
      {!showSplash && (
        <Router>
          <Routes>
            <Route path="/" element={<OverviewPage />} />
            <Route path="/daily" element={<DailyPage />} />
            <Route path="/retrospectives" element={<RetrospectivesPage />} />
          </Routes>
        </Router>
      )}
    </>
  );
}

export default App;
