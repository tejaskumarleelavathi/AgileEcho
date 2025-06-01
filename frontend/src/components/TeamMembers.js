import React, { useEffect, useState } from 'react';

const API_URL = 'http://127.0.0.1:8000/latest-contributors?owner=microsoft&repo=vscode-cosmosdb';
const STANDUP_URL = 'http://127.0.0.1:8000/standup/';

const TeamMembers = () => {
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [popup, setPopup] = useState(null); // { loading, error, data, user }

  useEffect(() => {
    setLoading(true);
    fetch(API_URL)
      .then(res => res.json())
      .then(data => {
        setMembers(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const handleCardClick = (user) => {
    setPopup({ loading: true, error: null, data: null, user });
    fetch(STANDUP_URL + user)
      .then(async res => {
        if (!res.ok) throw new Error('Not submitted');
        return res.json();
      })
      .then(data => setPopup({ loading: false, error: null, data, user }))
      .catch(() => setPopup({ loading: false, error: 'Standup not submitted', data: null, user }));
  };

  const closePopup = () => setPopup(null);

  return (
    <div style={{ width: '100%', maxWidth: 900, margin: '0 auto 24px auto', padding: '0 12px' }}>
      <div style={{ fontSize: '1.2rem', fontWeight: 600, color: '#e6ffe6', marginBottom: 12 }}>Team Members</div>
      {loading ? (
        <div style={{ color: '#bfc0c0', fontSize: '1.1rem', padding: 24 }}>Loading...</div>
      ) : (
        <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap', justifyContent: 'center', alignItems: 'center', paddingBottom: 8 }}>
          {members.map((m, i) => (
            <div
              key={i}
              style={{
                background: 'rgba(40,40,40,0.35)',
                borderRadius: 22,
                minWidth: 180,
                maxWidth: 220,
                padding: '28px 20px',
                color: '#fff',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                boxShadow: '0 4px 24px 0 rgba(60,60,60,0.13)',
                marginBottom: 18,
                border: '1.5px solid rgba(255,255,255,0.18)',
                backdropFilter: 'blur(18px)',
                WebkitBackdropFilter: 'blur(18px)',
                transition: 'box-shadow 0.18s, border 0.18s',
                cursor: 'pointer',
                outline: 'none',
              }}
              tabIndex={0}
              onClick={() => handleCardClick(m.username)}
            >
              <img src={m.avatar_url} alt={m.username} style={{ width: 56, height: 56, borderRadius: '50%', objectFit: 'cover', marginBottom: 12, border: '2px solid #e6ffe6', boxShadow: '0 2px 8px 0 rgba(0,0,0,0.10)' }} />
              <div style={{ fontWeight: 700, fontSize: '1.08rem', marginBottom: 4 }}>{m.username}</div>
              <div style={{ color: '#bfc0c0', fontSize: '1rem', fontWeight: 500, marginBottom: 4 }}>Last Contribution</div>
              <div style={{ color: '#e6ffe6', fontSize: '0.98rem', fontWeight: 500 }}>{new Date(m.last_contribution_date).toLocaleDateString()}</div>
            </div>
          ))}
        </div>
      )}
      {popup && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          background: 'rgba(10,10,20,0.32)',
          zIndex: 9999,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
        }} onClick={closePopup}>
          <div
            style={{
              minWidth: 340,
              maxWidth: 420,
              background: 'rgba(40,40,40,0.38)',
              borderRadius: 28,
              boxShadow: '0 8px 32px 0 rgba(0,0,0,0.22)',
              border: '1.5px solid rgba(255,255,255,0.18)',
              backdropFilter: 'blur(18px)',
              WebkitBackdropFilter: 'blur(18px)',
              padding: '36px 32px 28px 32px',
              color: '#fff',
              position: 'relative',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              cursor: 'auto',
            }}
            onClick={e => e.stopPropagation()}
          >
            <button onClick={closePopup} style={{ position: 'absolute', top: 18, right: 18, background: 'none', border: 'none', color: '#fff', fontSize: 22, cursor: 'pointer', opacity: 0.7 }}>×</button>
            <div style={{ fontWeight: 700, fontSize: '1.2rem', marginBottom: 12 }}>{popup.user}'s Standup</div>
            {popup.loading && <div style={{ color: '#bfc0c0', fontSize: '1.1rem' }}>Loading...</div>}
            {popup.error && (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 16 }}>
                <div style={{ color: '#ffb4b4', fontSize: '1.1rem' }}>{popup.error}</div>
                <button
                  style={{
                    background: 'rgba(255,255,255,0.13)',
                    color: '#fff',
                    fontWeight: 700,
                    fontSize: '1rem',
                    border: '1.5px solid rgba(255,255,255,0.22)',
                    borderRadius: 14,
                    padding: '10px 28px',
                    cursor: 'pointer',
                    boxShadow: '0 2px 12px 0 rgba(60,60,60,0.10)',
                    marginTop: 8,
                    backdropFilter: 'blur(8px)',
                    WebkitBackdropFilter: 'blur(8px)',
                    transition: 'background 0.18s, border 0.18s',
                  }}
                  onClick={() => {
                    alert(`Request sent to ${popup.user} to submit their standup!`);
                  }}
                >
                  Ask to Submit Standup
                </button>
              </div>
            )}
            {popup.data && (
              <div style={{ width: '100%' }}>
                <div style={{ fontWeight: 600, color: '#e6ffe6', marginBottom: 8 }}>Yesterday</div>
                <div style={{ marginBottom: 8 }}>{popup.data.yesterday.summary}</div>
                <ul style={{ margin: 0, paddingLeft: 18, marginBottom: 8 }}>
                  {popup.data.yesterday.details.map((d, i) => (
                    <li key={i} style={{ color: '#bfc0c0', fontSize: '0.98rem', marginBottom: 2 }}>
                      PR #{d.pr_number}: {d.description}
                    </li>
                  ))}
                </ul>
                <div style={{ color: '#bfc0c0', fontSize: '0.98rem', marginBottom: 8 }}>
                  Commits: {popup.data.yesterday.commits} | Additions: {popup.data.yesterday.additions} | Deletions: {popup.data.yesterday.deletions} | Files Changed: {popup.data.yesterday.files_changed}
                </div>
                <div style={{ fontWeight: 600, color: '#e6ffe6', marginBottom: 8 }}>Today</div>
                <ul style={{ margin: 0, paddingLeft: 18, marginBottom: 8 }}>
                  {popup.data.today.focus.map((f, i) => (
                    <li key={i} style={{ color: '#bfc0c0', fontSize: '0.98rem', marginBottom: 2 }}>{f}</li>
                  ))}
                </ul>
                {popup.data.blockers && popup.data.blockers.length > 0 && (
                  <>
                    <div style={{ fontWeight: 600, color: '#e6ffe6', marginBottom: 8 }}>Blockers</div>
                    <ul style={{ margin: 0, paddingLeft: 18, marginBottom: 8 }}>
                      {popup.data.blockers.map((b, i) => (
                        <li key={i} style={{ color: '#ffb4b4', fontSize: '0.98rem', marginBottom: 2 }}>{b}</li>
                      ))}
                    </ul>
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default TeamMembers; 