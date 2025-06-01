import React from 'react';
import './TheoryCards.css';
import { AlertTriangle, TrendingDown, TrendingUp, Clock, Link2, GitBranch, Target } from 'lucide-react';

const BlockersCard = ({ criticalIssues, blockers }) => {
  // Use placeholder data if backend does not provide detailed info
  const issues = blockers.blocked_issues || [
    {
      id: 2416,
      title: blockers.blocked_issue_titles?.[0] || 'Query Metrics are empty for the last page',
      priority: 'P0',
      assignee: 'tnaum-ms',
      days_stuck: 5,
    },
    {
      id: 2422,
      title: blockers.blocked_issue_titles?.[1] || 'NoSQL Query Editor shows empty result',
      priority: 'P1',
      assignee: 'tnaum-ms',
      days_stuck: 8,
    },
  ];

  const priorityColors = {
    P0: { bg: '#fee2e2', color: '#b91c1c' },
    P1: { bg: '#fef3c7', color: '#b45309' },
    P2: { bg: '#dbeafe', color: '#2563eb' },
  };

  return (
    <div style={{
      background: 'rgba(230, 57, 70, 0.13)',
      borderRadius: 32,
      padding: 32,
      marginBottom: 32,
      maxWidth: 250,
      margin: '0 auto 32px auto',
      color: '#23272f',
      position: 'relative',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12, fontWeight: 600, fontSize: '1.2rem', color: '#23272f' }}>
        <AlertTriangle color="#e63946" size={22} style={{ marginRight: 8 }} />
        <span style={{ color: '#f3f4f6' }}>Critical Blockers</span>
        <TrendingDown color="#e63946" size={20} style={{ marginLeft: 'auto' }} />
      </div>
      <div style={{ fontSize: '2rem', fontWeight: 700, margin: '14px 0 0 0', color: '#f3f4f6' }}>{criticalIssues.critical_open} P0</div>
      <div style={{ fontSize: '1.1rem', color: '#f3f4f6', marginBottom: 14 }}>blocking development</div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
        {issues.map((issue, i) => (
          <div key={i} style={{
            background: 'rgba(230, 57, 70, 0.13)',
            borderRadius: 18,
            padding: 14,
            display: 'flex',
            flexDirection: 'column',
            marginBottom: 0,
            color: '#fff',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: 4 }}>
              <a href="#" style={{ color: '#fff', fontWeight: 700, fontSize: '1rem', marginRight: 8, textDecoration: 'underline' }}>#{issue.id}</a>
              <span style={{ background: priorityColors[issue.priority]?.bg || '#eee', color: priorityColors[issue.priority]?.color || '#222', borderRadius: 16, padding: '2px 10px', fontWeight: 700, fontSize: '0.98rem', marginLeft: 'auto' }}>{issue.priority}</span>
            </div>
            <div style={{ color: '#fff', fontSize: '1rem', marginBottom: 2 }}>{issue.title}</div>
            <div style={{ color: '#e0e0e0', fontSize: '0.98rem', marginBottom: 0 }}>{issue.assignee}</div>
            <div style={{ color: '#fff', fontWeight: 700, fontSize: '1rem', marginLeft: 'auto', marginTop: 2, textAlign: 'right' }}>{issue.days_stuck} days stuck</div>
          </div>
        ))}
      </div>
    </div>
  );
};

const IssueAgeAnalysisCard = ({ currentSprint }) => (
  <div style={{
    background: 'rgba(230, 57, 70, 0.13)',
    borderRadius: 32,
    padding: 32,
    margin: '0 auto 32px auto',
    maxWidth: 250,
    minHeight: 480,
    color: '#f3f4f6',
    position: 'relative',
  }}>
    <div style={{ display: 'flex', alignItems: 'center', fontWeight: 600, fontSize: '1.2rem', color: '#23272f', marginBottom: 8 }}>
      <Clock color="#f59e42" size={22} style={{ marginRight: 8 }} />
      <span style={{ color: '#fff' }}>Issue Age Analysis</span>
      <TrendingUp color="#22c55e" size={20} style={{ marginLeft: 'auto' }} />
    </div>
    <div style={{ fontSize: '2.2rem', fontWeight: 700, margin: '8px 0 0 0', color: '#fff', display: 'flex', alignItems: 'center' }}>
      {currentSprint.milestone_open} <TrendingUp color="#e63946" size={18} style={{ marginLeft: 6 }} />
    </div>
    <div style={{ fontSize: '1.1rem', color: '#fff', marginBottom: 18 }}>issues stuck &gt;14 days</div>
    <div style={{ background: 'rgba(230, 57, 70, 0.13)', borderRadius: 18, padding: 18, marginBottom: 18, display: 'flex', flexDirection: 'column', gap: 8 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>Average Resolution</span>
        <span style={{ color: '#ea580c', fontWeight: 700, fontSize: '1.1rem' }}>{currentSprint.completion_percentage}%</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>Longest Stuck</span>
        <span style={{ color: '#e63946', fontWeight: 700, fontSize: '1.1rem' }}>{currentSprint.milestone_open} days</span>
      </div>
    </div>
    <div style={{ color: '#fff', fontSize: '1rem', textAlign: 'center' }}>AI suggests {currentSprint.milestone_open} for re-assignment</div>
  </div>
);

const DependencyRisksCard = ({ blockers }) => {
  // Use placeholder data if backend does not provide detailed info
  const dependencyChains = blockers.dependency_chains || [
    {
      from: '#2416',
      to: '#2567',
      label: 'blocking',
      labelColor: '#e63946',
      labelBg: '#fee2e2',
      desc: 'MongoDB features delayed',
    },
    {
      from: '#2503',
      to: '#2582',
      label: 'prerequisite',
      labelColor: '#b45309',
      labelBg: '#fef3c7',
      desc: 'Performance features chain',
    },
  ];

  return (
    <div style={{
      background: 'rgba(230, 57, 70, 0.13)',
      borderRadius: 32,
      padding: 32,
      margin: '0 auto 32px auto',
      maxWidth: 250,
      minHeight: 480,
      color: '#f3f4f6',
      position: 'relative',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', fontWeight: 600, fontSize: '1.2rem', color: '#23272f', marginBottom: 8 }}>
        <GitBranch color="#a78bfa" size={22} style={{ marginRight: 8 }} />
        <span style={{ color: '#fff' }}>Dependency Risks</span>
        <TrendingDown color="#e63946" size={20} style={{ marginLeft: 'auto' }} />
      </div>
      <div style={{ fontSize: '2rem', fontWeight: 700, margin: '8px 0 0 0', color: '#fff' }}>High Risk</div>
      <div style={{ fontSize: '1.1rem', color: '#fff', marginBottom: 18 }}>dependency chain detected</div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 14, marginBottom: 18 }}>
        {dependencyChains.map((chain, i) => (
          <div key={i} style={{
            background: 'rgba(230, 57, 70, 0.13)',
            borderRadius: 18,
            padding: 14,
            display: 'flex',
            flexDirection: 'column',
            marginBottom: 0,
            color: '#23272f',
          }}>
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: 4 }}>
              <a href="#" style={{ color: '#fff', fontWeight: 700, fontSize: '0.92rem', marginRight: 6, textDecoration: 'underline' }}>{chain.from}</a>
              <span style={{ color: '#fff', fontSize: 16 }}>›</span>
              <a href="#" style={{ color: '#fff', fontWeight: 700, fontSize: '0.92rem', marginLeft: 6, textDecoration: 'underline' }}>{chain.to}</a>
            </div>
            <span style={{ background: chain.labelBg, color: chain.labelColor, borderRadius: 16, padding: '2px 14px', fontWeight: 700, fontSize: '0.98rem', marginTop: 6, alignSelf: 'flex-start', display: 'inline-block' }}>{chain.label}</span>
            <div style={{ color: '#fff', fontSize: '1rem', marginBottom: 2, marginLeft: 4 }}>{chain.desc}</div>
          </div>
        ))}
      </div>
      <div style={{ color: '#fff', fontSize: '1rem', textAlign: 'center' }}>1 critical path identified</div>
    </div>
  );
};

const MilestoneRiskScoreCard = ({ currentSprint }) => (
  <div className="milestone-risk-score-card" style={{
    background: 'rgba(230, 57, 70, 0.13)',
    borderRadius: 32,
    padding: 32,
    margin: '18px auto 32px auto',
    width: '100%',
    maxWidth: '100%',
    color: '#f3f4f6',
    position: 'relative',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-start',
    boxSizing: 'border-box',
  }}>
    <div style={{ display: 'flex', alignItems: 'center', fontWeight: 600, fontSize: '1.2rem', color: '#23272f', marginBottom: 8 }}>
      <Target color="#888" size={22} style={{ marginRight: 8 }} />
      <span style={{ fontWeight: 700, color: '#fff' }}>Milestone Risk Score</span>
    </div>
    <div style={{ fontSize: '2rem', fontWeight: 700, margin: '8px 0 0 0', color: '#fff' }}>{currentSprint.completion_percentage}%</div>
    <div style={{ fontSize: '1.1rem', color: '#fff', marginBottom: 18 }}>confidence ({currentSprint.milestone})</div>
    <div style={{ background: 'rgba(230, 57, 70, 0.13)', borderRadius: 18, padding: 18, marginBottom: 18, width: '100%', boxSizing: 'border-box' }}>
      <div style={{ fontWeight: 700, fontSize: '1.1rem', marginBottom: 4 }}>{currentSprint.milestone}</div>
      <div style={{ color: '#fff', fontSize: '1rem', marginBottom: 8 }}>{currentSprint.milestone_closed}/{currentSprint.total_milestone_issues} completed</div>
      <div style={{ background: '#e5e7eb', borderRadius: 8, height: 8, width: '100%', marginBottom: 8, position: 'relative' }}>
        <div style={{ background: '#22c55e', borderRadius: 8, height: 8, width: `${currentSprint.completion_percentage}%`, position: 'absolute', left: 0, top: 0 }}></div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ background: '#bbf7d0', color: '#22c55e', borderRadius: 16, padding: '2px 14px', fontWeight: 700, fontSize: '1rem' }}>{currentSprint.completion_percentage}%</span>
        <span style={{ color: '#22c55e', fontWeight: 700, fontSize: '1rem', marginLeft: 12 }}>low risk</span>
      </div>
    </div>
  </div>
);

const TheoryCards = ({ insightData, loading, error }) => {
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  let criticalIssues, blockers, currentSprint;
  if (insightData && insightData.issue_analysis) {
    criticalIssues = insightData.issue_analysis.critical_issues_status;
    blockers = insightData.issue_analysis.external_blockers_impact;
    currentSprint = insightData.issue_analysis.current_sprint_status;
  } else {
    criticalIssues = { critical_open: 4 };
    blockers = { blocked_issues: null, blocked_issue_titles: [
      'Query Metrics are empty for the last page',
      'NoSQL Query Editor shows empty result',
    ] };
    currentSprint = { milestone_open: 9, completion_percentage: 18.18, milestone: '0.26.1', total_milestone_issues: 12, milestone_closed: 3 };
  }

  return (
    <div className="theory-section">
      <div className="theory-title">Blockers & Anomaly Detection</div>
      <div className="theory-main-cards">
        <BlockersCard criticalIssues={criticalIssues} blockers={blockers} />
        <IssueAgeAnalysisCard currentSprint={currentSprint} />
        <DependencyRisksCard blockers={blockers} />
      </div>
      <MilestoneRiskScoreCard currentSprint={currentSprint} />
    </div>
  );
};

export default TheoryCards; 