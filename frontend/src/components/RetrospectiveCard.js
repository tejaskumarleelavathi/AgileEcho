import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';

const API_URL = 'http://127.0.0.1:8000/retrospectives';
const CONTRIBUTORS_API = 'http://127.0.0.1:8000/latest-contributors?owner=microsoft&repo=vscode-cosmosdb';

const markdownStyles = {
  h1: { color: '#e6ffe6', fontWeight: 700, fontSize: '1.5rem', margin: '18px 0 8px 0' },
  h2: { color: '#2563eb', fontWeight: 700, fontSize: '1.2rem', margin: '16px 0 8px 0' },
  h3: { color: '#e6ffe6', fontWeight: 600, fontSize: '1.08rem', margin: '12px 0 6px 0' },
  p: { color: '#fff', fontSize: '1.08rem', margin: '8px 0' },
  ul: { color: '#bfc0c0', fontSize: '1.08rem', margin: '8px 0 8px 18px' },
  li: { marginBottom: 4 },
  strong: { color: '#e6ffe6', fontWeight: 700 },
  contributor: {
    background: '#2563eb',
    color: '#e6ffe6',
    borderRadius: 8,
    padding: '2px 10px',
    fontWeight: 700,
    cursor: 'pointer',
    textDecoration: 'none',
    transition: 'all 0.18s',
    margin: '0 2px',
    display: 'inline-block',
  },
  contributorHover: {
    background: '#e6ffe6',
    color: '#2563eb',
  },
};

function getGithubUrl(username) {
  return `https://github.com/${username}`;
}

function prettifyUsername(username) {
  // Convert 'tnaum-ms' -> 'Tnaum Ms', 'dmitriish' -> 'Dmitriish'
  return username
    .replace(/[-_]/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase());
}

const RetrospectiveCard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [contributors, setContributors] = useState([]);

  useEffect(() => {
    fetch(API_URL)
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch');
        return res.json();
      })
      .then(setData)
      .catch(() => setError('Could not load retrospective'))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    fetch(CONTRIBUTORS_API)
      .then(res => res.json())
      .then(setContributors)
      .catch(() => setContributors([]));
  }, []);

  // Build a map of display name to username for contributors (dynamic)
  const nameToUsername = {};
  contributors.forEach(c => {
    nameToUsername[c.username] = c.username;
    const pretty = prettifyUsername(c.username);
    nameToUsername[pretty] = c.username;
  });
  // Build a regex to match any contributor name or prettified name
  const contributorNames = Object.keys(nameToUsername).filter(Boolean).sort((a, b) => b.length - a.length); // longest first
  const contributorRegex = contributorNames.length > 0 ? new RegExp(`(${contributorNames.map(n => n.replace(/[-/\\^$*+?.()|[\]{}]/g, '\\$&')).join('|')})`, 'g') : null;

  // Custom renderer for text nodes to highlight contributor names
  function renderTextWithContributors(text) {
    if (!contributorRegex) return text;
    const parts = text.split(contributorRegex);
    return parts.map((part, i) => {
      const username = nameToUsername[part];
      if (username) {
        return (
          <a
            key={i}
            href={getGithubUrl(username)}
            target="_blank"
            rel="noopener noreferrer"
            style={markdownStyles.contributor}
            onMouseOver={e => {
              e.currentTarget.style.background = markdownStyles.contributorHover.background;
              e.currentTarget.style.color = markdownStyles.contributorHover.color;
            }}
            onMouseOut={e => {
              e.currentTarget.style.background = markdownStyles.contributor.background;
              e.currentTarget.style.color = markdownStyles.contributor.color;
            }}
          >
            {part}
          </a>
        );
      }
      return part;
    });
  }

  const components = {
    h1: ({node, ...props}) => <h1 style={markdownStyles.h1} {...props} />,
    h2: ({node, ...props}) => <h2 style={markdownStyles.h2} {...props} />,
    h3: ({node, ...props}) => <h3 style={markdownStyles.h3} {...props} />,
    p: ({node, ...props}) => <p style={markdownStyles.p} {...props} />,
    ul: ({node, ...props}) => <ul style={markdownStyles.ul} {...props} />,
    li: ({node, ...props}) => <li style={markdownStyles.li} {...props} />,
    strong: ({node, ...props}) => <strong style={markdownStyles.strong} {...props} />,
    text: ({node, value}) => renderTextWithContributors(value),
  };

  return (
    <div style={{
      background: 'rgba(40,40,40,0.38)',
      borderRadius: 28,
      boxShadow: '0 8px 32px 0 rgba(0,0,0,0.22)',
      border: '1.5px solid rgba(255,255,255,0.18)',
      backdropFilter: 'blur(18px)',
      WebkitBackdropFilter: 'blur(18px)',
      padding: '36px 32px 28px 32px',
      color: '#fff',
      maxWidth: 700,
      margin: '32px auto',
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'flex-start',
    }}>
      {data && (
        <div style={{ fontWeight: 700, fontSize: '2.2rem', color: '#e6ffe6', marginBottom: 12 }}>{data.milestone}</div>
      )}
      {loading && <div style={{ color: '#bfc0c0', fontSize: '1.1rem' }}>Loading...</div>}
      {error && <div style={{ color: '#ffb4b4', fontSize: '1.1rem' }}>{error}</div>}
      {data && (
        <div style={{ width: '100%' }}>
          <div style={{ color: '#bfc0c0', fontSize: '1rem', marginBottom: 8 }}>Generated on: {data.generated_on}</div>
          <div style={{ color: '#bfc0c0', fontSize: '1rem', marginBottom: 8 }}>Repository: {data.repository}</div>
          <div style={{ background: 'rgba(255,255,255,0.08)', borderRadius: 18, padding: 18, color: '#fff', fontSize: '1.08rem', marginTop: 8 }}>
            <ReactMarkdown components={components}>{data.retrospective}</ReactMarkdown>
          </div>
        </div>
      )}
    </div>
  );
};

export default RetrospectiveCard; 