import React from 'react';
import './LevelHeader.css';

const LevelHeader = () => (
  <div className="level-header-row">
    <div className="level-header-title">Repo:<br/>vscode-cosmosdb</div>
    <div className="level-header-tasks-group-vertical">
      <span className="level-header-objectives-label">objectives</span>
      <span className="level-header-tasks">04/05</span>
    </div>
  </div>
);

export default LevelHeader; 