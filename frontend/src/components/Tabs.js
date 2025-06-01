import React from 'react';
import './Tabs.css';
import { useLocation, useNavigate } from 'react-router-dom';

const Tabs = () => {
  const location = useLocation();
  const navigate = useNavigate();
  return (
    <div className="tabs-container">
      <div
        className={`tab${location.pathname === '/' ? ' selected' : ''}`}
        onClick={() => navigate('/')}
      >
        Overview
      </div>
      <div
        className={`tab${location.pathname === '/daily' ? ' selected' : ''}`}
        onClick={() => navigate('/daily')}
      >
        Daily
      </div>
      <div
        className={`tab${location.pathname === '/retrospectives' ? ' selected' : ''}`}
        onClick={() => navigate('/retrospectives')}
      >
        Retrospectives
      </div>
    </div>
  );
};

export default Tabs; 