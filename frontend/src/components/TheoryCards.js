import React from 'react';
import './TheoryCards.css';

const cards = [
  { title: 'TestBlock 1' },
  { title: 'TestBlock 2' },
  { title: 'TestBlock 3' },
];

const TheoryCards = () => (
  <div className="theory-section">
    <div className="theory-title">Blockers & Anomaly Detection</div>
    <div className="theory-cards-list">
      {cards.map((card, i) => (
        <div key={i} className="theory-card">
          {/* <span className="theory-card-icon">{card.icon}</span> */}
          <div className="theory-card-title">{card.title}</div>
        </div>
      ))}
    </div>
  </div>
);

export default TheoryCards; 