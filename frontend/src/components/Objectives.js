import React from 'react';
import { AlertTriangle, TrendingDown, Clock, TrendingUp } from 'lucide-react';
import './Objectives.css';

const GithubIssueIcon = () => (
  <svg width="28" height="28" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="14" cy="14" r="12" stroke="#2ea043" strokeWidth="2.5"/>
    <circle cx="14" cy="14" r="5" fill="#2ea043"/>
    <rect x="13" y="6" width="2" height="6" rx="1" fill="#2ea043"/>
    <rect x="13" y="16" width="2" height="6" rx="1" fill="#2ea043"/>
  </svg>
);

const Objectives = () => (
  <div className="objectives-section">
    <div className="objectives-title">Current Project Health</div>
    <div className="objectives-list strict-issue-layout">
      <div className="strict-issue-card warning-card">
        <div className="strict-issue-header">
          <span className="strict-issue-icon"><GithubIssueIcon /></span>
          <span className="strict-issue-title">Open vs Closed Issues</span>
        </div>
        <div className="strict-issue-main">58.8% <b>Open</b></div>
        <div className="strict-issue-footer">102 total issues</div>
        <span className="strict-issue-dot"></span>
      </div>
      <div className="strict-issue-card warning-card">
        <div className="strict-issue-header">
          <span className="strict-issue-icon"><AlertTriangle color="#101820" fill="#d3d4d6" size={28} strokeWidth={2.2} /></span>
          <span className="strict-issue-title">Critical Issues</span>
        </div>
        <div className="strict-issue-main">4 P0</div>
        <div className="strict-issue-footer">24 P1 issues pending</div>
        <span className="strict-warning-arrow"><TrendingDown color="#c1121f" size={32} strokeWidth={3} /></span>
      </div>
      <div className="strict-issue-card activity-card">
        <div className="strict-issue-header">
          <span className="strict-issue-icon"><Clock color="#101820" fill="#d3d4d6" size={28} strokeWidth={2.2} /></span>
          <span className="strict-issue-title">Recent Activity</span>
        </div>
        <div className="strict-issue-main">12 <b>items</b></div>
        <div className="strict-issue-footer">in current sprint (0.26.1)</div>
        <span className="strict-activity-arrow"><TrendingUp color="#15803d" size={28} strokeWidth={3} /></span>
      </div>
    </div>
  </div>
);

export default Objectives; 