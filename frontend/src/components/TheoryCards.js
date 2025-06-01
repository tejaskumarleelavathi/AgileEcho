import React from 'react';
import './TheoryCards.css';
import { AlertTriangle, TrendingDown, TrendingUp, Clock, Link2, GitBranch, Target } from 'lucide-react';



const BlockersCard = () => (
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
    <div style={{ fontSize: '2rem', fontWeight: 700, margin: '14px 0 0 0', color: '#f3f4f6' }}>4 P0</div>
    <div style={{ fontSize: '1.1rem', color: '#f3f4f6', marginBottom: 14 }}>blocking development</div>
    <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
      <div style={{
        background: 'rgba(230, 57, 70, 0.13)',
        borderRadius: 18,
        padding: 14,
        display: 'flex',
        flexDirection: 'column',
        marginBottom: 0,
        color: '#fff',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: 4 }}>
          <a href="#" style={{ color: '#fff', fontWeight: 700, fontSize: '1rem', marginRight: 8, textDecoration: 'underline' }}>#2416</a>
          <span style={{ background: '#fee2e2', color: '#b91c1c', borderRadius: 16, padding: '2px 10px', fontWeight: 700, fontSize: '0.98rem', marginLeft: 'auto' }}>P0</span>
        </div>
        <div style={{ color: '#fff', fontSize: '1rem', marginBottom: 2 }}>Fail to connect Azure Cosmos DB for MongoDB cluster with Firewall enabled</div>
        <div style={{ color: '#e0e0e0', fontSize: '0.98rem', marginBottom: 0 }}>tnaum-ms</div>
        <div style={{ color: '#fff', fontWeight: 700, fontSize: '1rem', marginLeft: 'auto', marginTop: 2, textAlign: 'right' }}>5 days stuck</div>
      </div>
      <div style={{
        background: 'rgba(230, 57, 70, 0.13)',
        borderRadius: 18,
        padding: 14,
        display: 'flex',
        flexDirection: 'column',
        marginBottom: 0,
        color: '#fff',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: 4 }}>
          <a href="#" style={{ color: '#fff', fontWeight: 700, fontSize: '1rem', marginRight: 8, textDecoration: 'underline' }}>#2422</a>
          <span style={{ background: '#fef3c7', color: '#b45309', borderRadius: 16, padding: '2px 10px', fontWeight: 700, fontSize: '0.98rem', marginLeft: 'auto' }}>P1</span>
        </div>
        <div style={{ color: '#fff', fontSize: '1rem', marginBottom: 2 }}>Error executing MongoDB Clusters: Remove Connection command</div>
        <div style={{ color: '#e0e0e0', fontSize: '0.98rem', marginBottom: 0 }}>tnaum-ms</div>
        <div style={{ color: '#fff', fontWeight: 700, fontSize: '1rem', marginLeft: 'auto', marginTop: 2, textAlign: 'right' }}>8 days stuck</div>
      </div>
    </div>
  </div>
);

const IssueAgeAnalysisCard = () => (
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
      3 <TrendingUp color="#e63946" size={18} style={{ marginLeft: 6 }} />
    </div>
    <div style={{ fontSize: '1.1rem', color: '#fff', marginBottom: 18 }}>issues stuck &gt;14 days</div>
    <div style={{ background: 'rgba(230, 57, 70, 0.13)', borderRadius: 18, padding: 18, marginBottom: 18, display: 'flex', flexDirection: 'column', gap: 8 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>Average Resolution</span>
        <span style={{ color: '#ea580c', fontWeight: 700, fontSize: '1.1rem' }}>8.5 days</span>
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>Longest Stuck</span>
        <span style={{ color: '#e63946', fontWeight: 700, fontSize: '1.1rem' }}>18 days</span>
      </div>
    </div>
    <div style={{ color: '#fff', fontSize: '1rem', textAlign: 'center' }}>AI suggests 2 for re-assignment</div>
  </div>
);

const dependencyChains = [
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

const DependencyRisksCard = () => (
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

const MilestoneRiskScoreCard = () => (
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
    <div style={{ fontSize: '2rem', fontWeight: 700, margin: '8px 0 0 0', color: '#fff' }}>65%</div>
    <div style={{ fontSize: '1.1rem', color: '#fff', marginBottom: 18 }}>confidence (0.27.0)</div>
    <div style={{ background: 'rgba(230, 57, 70, 0.13)', borderRadius: 18, padding: 18, marginBottom: 18, width: '100%', boxSizing: 'border-box' }}>
      <div style={{ fontWeight: 700, fontSize: '1.1rem', marginBottom: 4 }}>0.26.1</div>
      <div style={{ color: '#fff', fontSize: '1rem', marginBottom: 8 }}>9/12 completed</div>
      <div style={{ background: '#e5e7eb', borderRadius: 8, height: 8, width: '100%', marginBottom: 8, position: 'relative' }}>
        <div style={{ background: '#22c55e', borderRadius: 8, height: 8, width: '75%', position: 'absolute', left: 0, top: 0 }}></div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ background: '#bbf7d0', color: '#22c55e', borderRadius: 16, padding: '2px 14px', fontWeight: 700, fontSize: '1rem' }}>85%</span>
        <span style={{ color: '#22c55e', fontWeight: 700, fontSize: '1rem', marginLeft: 12 }}>low risk</span>
      </div>
    </div>
    <div style={{ background: 'rgba(230, 57, 70, 0.13)', borderRadius: 18, padding: 18, marginBottom: 18, width: '100%', boxSizing: 'border-box' }}>
      <div style={{ fontWeight: 700, fontSize: '1.1rem', marginBottom: 4 }}>0.27.0</div>
      <div style={{ color: '#fff', fontSize: '1rem', marginBottom: 8 }}>8/22 completed</div>
      <div style={{ background: '#e5e7eb', borderRadius: 8, height: 8, width: '100%', marginBottom: 8, position: 'relative' }}>
        <div style={{ background: '#fb923c', borderRadius: 8, height: 8, width: '36%', position: 'absolute', left: 0, top: 0 }}></div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <span style={{ background: '#fef3c7', color: '#fb923c', borderRadius: 16, padding: '2px 14px', fontWeight: 700, fontSize: '1rem' }}>65%</span>
        <span style={{ color: '#fb923c', fontWeight: 700, fontSize: '1rem', marginLeft: 12 }}>medium risk</span>
      </div>
    </div>
    <div style={{ color: '#fff', fontSize: '1.1rem', textAlign: 'center', width: '100%' }}>Based on current velocity</div>
  </div>
);

const TheoryCards = () => (
  <div className="theory-section">
    <div className="theory-title">Blockers & Anomaly Detection</div>
    <div className="theory-main-cards">
      <BlockersCard />
      <IssueAgeAnalysisCard />
      <DependencyRisksCard />
    </div>
    <MilestoneRiskScoreCard />
  </div>
);

export default TheoryCards; 