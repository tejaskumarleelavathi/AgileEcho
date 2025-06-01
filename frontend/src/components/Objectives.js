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

const Objectives = ({ insightData, loading, error }) => {
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  let openVsClosed, criticalIssues, currentSprint;
  if (insightData && insightData.issue_analysis) {
    openVsClosed = insightData.issue_analysis.open_vs_closed;
    criticalIssues = insightData.issue_analysis.critical_issues_status;
    currentSprint = insightData.issue_analysis.current_sprint_status;
  } else {
    openVsClosed = { open_issues: 65, total_issues: 107 };
    criticalIssues = { critical_open: 5, total_critical: 14 };
    currentSprint = { total_milestone_issues: 12, milestone: '0.26.1' };
  }

  return (
    <div className="objectives-section">
      <div className="objectives-title">Current Project Health</div>
      <div className="objectives-list strict-issue-layout">
        <div className="strict-issue-card warning-card">
          <div className="strict-issue-header">
            <span className="strict-issue-icon"><GithubIssueIcon /></span>
            <span className="strict-issue-title">Open vs Closed Issues</span>
          </div>
          <div className="strict-issue-main">{openVsClosed.open_issues} <b>Open</b></div>
          <div className="strict-issue-footer">{openVsClosed.total_issues} total issues</div>
          <span className="strict-issue-dot"></span>
        </div>
        <div className="strict-issue-card warning-card">
          <div className="strict-issue-header">
            <span className="strict-issue-icon"><AlertTriangle color="#101820" fill="#d3d4d6" size={28} strokeWidth={2.2} /></span>
            <span className="strict-issue-title">Critical Issues</span>
          </div>
          <div className="strict-issue-main">{criticalIssues.critical_open} P0</div>
          <div className="strict-issue-footer">{criticalIssues.total_critical} critical issues pending</div>
          <span className="strict-warning-arrow"><TrendingDown color="#c1121f" size={32} strokeWidth={3} /></span>
        </div>
        <div className="strict-issue-card activity-card">
          <div className="strict-issue-header">
            <span className="strict-issue-icon"><Clock color="#101820" fill="#d3d4d6" size={28} strokeWidth={2.2} /></span>
            <span className="strict-issue-title">Recent Activity</span>
          </div>
          <div className="strict-issue-main">{currentSprint.total_milestone_issues} <b>items</b></div>
          <div className="strict-issue-footer">in current sprint ({currentSprint.milestone})</div>
          <span className="strict-activity-arrow"><TrendingUp color="#15803d" size={28} strokeWidth={3} /></span>
        </div>
      </div>
    </div>
  );
};

export default Objectives; 