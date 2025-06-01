import React from 'react';
import { CheckCircle, ArrowRight, Clock, GitBranch } from 'lucide-react';

const TeamProgress = ({ insightData, loading, error }) => {
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  let resolvedIssues, newIssues, plannedWork, dependencies, typeColors, priorityColors;
  if (insightData && insightData.issue_analysis) {
    // You can map backend data here if available
    resolvedIssues = [];
    newIssues = [];
    plannedWork = [];
    dependencies = [];
  } else {
    resolvedIssues = [
      {
        id: 2697,
        type: 'Task',
        title: 'Finalize the work on pull/2685',
        users: ['Copilot'],
        version: '0.26.1',
      },
      {
        id: 2694,
        type: 'Bug',
        title: 'Re-insert the node on refresh in the cached tree provider',
        users: ['Copilot', 'tnaum-ms'],
        version: '0.26.1',
      },
      {
        id: 2542,
        type: 'Feature',
        title: 'Login with Managed Identity not possible',
        users: ['sevoku'],
        version: '0.27.0',
      },
    ];
    newIssues = [
      {
        id: 2689,
        type: 'Feature',
        priority: 'P1',
        title: 'Support basic keyboard shortcuts in Query Editor',
        users: ['bk201-'],
      },
      {
        id: 2682,
        type: 'Bug',
        title: 'Document Delete Success/Failure Notification Missing',
        users: ['bk201-'],
      },
      {
        id: 2675,
        type: 'Feature',
        priority: 'P1',
        title: '[Feat] NOSQL: Set throughput bucket for requests',
        users: ['sevoku'],
      },
    ];
    plannedWork = [
      {
        id: 2416,
        type: 'Bug',
        priority: 'P0',
        title: 'Fail to connect the Azure Cosmos DB for MongoDB cluster in VS Code with Firewall enabled',
        users: ['tnaum-ms'],
      },
      {
        id: 2549,
        type: 'Bug',
        priority: 'P1',
        title: 'Unable to Search for UUIDs in MongoDB Clusters',
        users: ['tnaum-ms'],
      },
      {
        id: 2503,
        type: 'Feature',
        priority: 'P1',
        title: 'Improve insert and upsert implementation',
        users: ['tnaum-ms'],
      },
    ];
    dependencies = [
      {
        from: { id: 2416, user: 'tnaum-ms' },
        to: { id: 2567, user: 'tnaum-ms' },
        label: 'blocking',
        labelColor: '#e63946',
        labelBg: '#fee2e2',
        desc: 'Firewall config needed for re-config on demand feature',
      },
      {
        from: { id: 2503, user: 'tnaum-ms' },
        to: { id: 2582, user: 'unassigned' },
        label: 'prerequisite',
        labelColor: '#b45309',
        labelBg: '#fef3c7',
        desc: 'Bulk import depends on improved insert implementation',
      },
    ];
  }
  typeColors = {
    Task: { color: '#22c55e', bg: '#dcfce7' },
    Bug: { color: '#e63946', bg: '#fee2e2' },
    Feature: { color: '#2563eb', bg: '#dbeafe' },
  };
  priorityColors = {
    P0: { color: '#dc2626', bg: '#fee2e2' },
    P1: { color: '#b45309', bg: '#fef3c7' },
    P2: { color: '#3b82f6', bg: '#dbeafe' },
  };

  return (
    <div style={{
      width: '100%',
      maxWidth: 900,
      margin: '0 auto 24px auto',
      padding: '0 12px',
    }}>
      <div style={{ fontSize: '1.2rem', fontWeight: 600, color: '#e6ffe6', marginBottom: 12 }}>Team Progress</div>
      <div style={{
        background: 'rgba(255,255,255,0.85)',
        borderRadius: 18,
        boxShadow: '0 2px 12px 0 rgba(0,0,0,0.10)',
        padding: 32,
        marginBottom: 24,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', fontWeight: 700, fontSize: '1.1rem', color: '#22c55e', marginBottom: 18 }}>
          <CheckCircle color="#22c55e" size={22} style={{ marginRight: 8 }} />
          Issues Resolved Yesterday
          <span style={{ marginLeft: 'auto', color: '#888', fontWeight: 600, fontSize: '1rem', background: '#f3f4f6', borderRadius: 12, padding: '2px 12px' }}>{resolvedIssues.length}</span>
        </div>
        {resolvedIssues.map((issue, i) => {
          const typeColor = typeColors[issue.type] || { color: '#888', bg: '#eee' };
          return (
            <div key={issue.id} style={{
              background: i % 2 === 0 ? 'rgba(243,244,246,0.7)' : 'transparent',
              borderRadius: 12,
              padding: '14px 18px',
              marginBottom: 8,
              display: 'flex',
              alignItems: 'flex-start',
              gap: 12,
            }}>
              <span style={{ width: 8, height: 8, borderRadius: '50%', background: typeColor.color, marginTop: 8, display: 'inline-block' }}></span>
              <a href="#" style={{ color: '#2563eb', fontWeight: 700, fontSize: '1.08rem', marginRight: 8, textDecoration: 'underline' }}>#{issue.id}</a>
              <span style={{
                background: typeColor.bg,
                color: typeColor.color,
                borderRadius: 8,
                padding: '2px 10px',
                fontWeight: 700,
                fontSize: '0.98rem',
                marginRight: 8,
              }}>{issue.type}</span>
              <span style={{ color: '#22223b', fontWeight: 500, fontSize: '1.08rem', flex: 1 }}>{issue.title}</span>
              <span style={{ color: '#888', fontWeight: 500, fontSize: '1rem', marginLeft: 8 }}>{issue.users.join(' & ')}</span>
              <span style={{ color: '#888', fontWeight: 600, fontSize: '1rem', marginLeft: 18 }}>{issue.version}</span>
            </div>
          );
        })}
      </div>
      <div style={{
        background: 'rgba(255,255,255,0.85)',
        borderRadius: 18,
        boxShadow: '0 2px 12px 0 rgba(0,0,0,0.10)',
        padding: 32,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', fontWeight: 700, fontSize: '1.1rem', color: '#2563eb', marginBottom: 18 }}>
          <ArrowRight color="#2563eb" size={22} style={{ marginRight: 8 }} />
          New Issues Assigned Today
          <span style={{ marginLeft: 'auto', color: '#888', fontWeight: 600, fontSize: '1rem', background: '#f3f4f6', borderRadius: 12, padding: '2px 12px' }}>{newIssues.length}</span>
        </div>
        {newIssues.map((issue, i) => {
          const typeColor = typeColors[issue.type] || { color: '#888', bg: '#eee' };
          return (
            <div key={issue.id} style={{
              background: i % 2 === 0 ? 'rgba(243,244,246,0.7)' : 'transparent',
              borderRadius: 12,
              padding: '14px 18px',
              marginBottom: 8,
              display: 'flex',
              alignItems: 'flex-start',
              gap: 12,
            }}>
              <span style={{ width: 8, height: 8, borderRadius: '50%', background: typeColor.color, marginTop: 8, display: 'inline-block' }}></span>
              <a href="#" style={{ color: '#2563eb', fontWeight: 700, fontSize: '1.08rem', marginRight: 8, textDecoration: 'underline' }}>#{issue.id}</a>
              {issue.priority && (
                <span style={{
                  background: priorityColors[issue.priority].bg,
                  color: priorityColors[issue.priority].color,
                  borderRadius: 8,
                  padding: '2px 10px',
                  fontWeight: 700,
                  fontSize: '0.98rem',
                  marginRight: 8,
                }}>{issue.priority}</span>
              )}
              <span style={{
                background: typeColor.bg,
                color: typeColor.color,
                borderRadius: 8,
                padding: '2px 10px',
                fontWeight: 700,
                fontSize: '0.98rem',
                marginRight: 8,
              }}>{issue.type}</span>
              <span style={{ color: '#22223b', fontWeight: 500, fontSize: '1.08rem', flex: 1 }}>{issue.title}</span>
              <span style={{ color: '#888', fontWeight: 500, fontSize: '1rem', marginLeft: 8 }}>{issue.users.join(' & ')}</span>
            </div>
          );
        })}
      </div>
      {/* Planned Work for Tomorrow */}
      <div style={{
        background: 'rgba(255,255,255,0.85)',
        borderRadius: 18,
        boxShadow: '0 2px 12px 0 rgba(0,0,0,0.10)',
        padding: 32,
        marginTop: 32,
        marginBottom: 24,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', fontWeight: 700, fontSize: '1.1rem', color: '#f59e42', marginBottom: 18 }}>
          <Clock color="#f59e42" size={22} style={{ marginRight: 8 }} />
          Planned Work for Tomorrow
          <span style={{ marginLeft: 'auto', color: '#888', fontWeight: 600, fontSize: '1rem', background: '#f3f4f6', borderRadius: 12, padding: '2px 12px' }}>{plannedWork.length}</span>
        </div>
        {plannedWork.map((issue, i) => {
          const typeColor = typeColors[issue.type] || { color: '#888', bg: '#eee' };
          return (
            <div key={issue.id} style={{
              background: i % 2 === 0 ? 'rgba(243,244,246,0.7)' : 'transparent',
              borderRadius: 12,
              padding: '14px 18px',
              marginBottom: 8,
              display: 'flex',
              alignItems: 'flex-start',
              gap: 12,
            }}>
              <span style={{ width: 8, height: 8, borderRadius: '50%', background: typeColor.color, marginTop: 8, display: 'inline-block' }}></span>
              <a href="#" style={{ color: '#2563eb', fontWeight: 700, fontSize: '1.08rem', marginRight: 8, textDecoration: 'underline' }}>#{issue.id}</a>
              {issue.priority && (
                <span style={{
                  background: priorityColors[issue.priority].bg,
                  color: priorityColors[issue.priority].color,
                  borderRadius: 8,
                  padding: '2px 10px',
                  fontWeight: 700,
                  fontSize: '0.98rem',
                  marginRight: 8,
                }}>{issue.priority}</span>
              )}
              <span style={{
                background: typeColor.bg,
                color: typeColor.color,
                borderRadius: 8,
                padding: '2px 10px',
                fontWeight: 700,
                fontSize: '0.98rem',
                marginRight: 8,
              }}>{issue.type}</span>
              <span style={{ color: '#22223b', fontWeight: 500, fontSize: '1.08rem', flex: 1 }}>{issue.title}</span>
              <span style={{ color: '#888', fontWeight: 500, fontSize: '1rem', marginLeft: 8 }}>{issue.users.join(' & ')}</span>
            </div>
          );
        })}
      </div>
      
    </div>
  );
};

export default TeamProgress; 