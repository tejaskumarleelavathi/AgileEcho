import React from 'react';
import './Header.css';

const Header = () => (
  <>
    <div style={{
      width: '100%',
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      marginTop: 24,
      marginBottom: 8,
    }}>
      <span style={{
        fontFamily: 'Poppins, sans-serif',
        fontWeight: 700,
        fontSize: '2.8rem',
        letterSpacing: '-2px',
        lineHeight: 1.05,
        textAlign: 'center',
      }}>
        <span style={{ color: '#e6ffe6' }}>Agile</span>
        <span style={{ color: '#2563eb' }}>Echo</span>
      </span>
    </div>
    <div className="header-container">
      {/* Header content here, Tabs moved to page level */}
    </div>
  </>
);

export default Header; 