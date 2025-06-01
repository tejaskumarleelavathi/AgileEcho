import React from 'react';
import './LevelHeader.css';

const LevelHeader = () => (
  <div className="level-header-row">
    <div className="level-header-title">
      <span style={{ color: '#e6ffe6', fontWeight: 700 }}>Repo:</span><br/>
      <span style={{ color: '#2563eb', fontWeight: 700 }}>vscode-cosmosdb</span>
    </div>
    <div className="level-header-tasks-group-vertical">
      <span className="level-header-objectives-label" style={{ color: '#e6ffe6', fontWeight: 700 }}>objectives</span>
      <span className="level-header-tasks" style={{ color: '#2563eb', fontWeight: 700 }}>04/05</span>
    </div>
  </div>
);

export default LevelHeader; 