import React from 'react';
import './PracticalCards.css';
import { Chart } from "react-google-charts";
// import { Sankey, Tooltip } from 'recharts';

const cards = [
  { title: 'TestBlock 1' },
  { title: 'TestBlock 2' },
  { title: 'TestBlock 3' },
];

const sankeyData = [
  ["From", "To", "Weight"],
  ["Bug", "AT-CTI", 6],
  ["Bug", "MongoDB Clusters", 10],
  ["Bug", "NoSQL", 4],
  ["Bug", "P2", 1],
  ["Bug", "bug", 4],
  ["Feature", "AT-CTI", 6],
  ["Feature", "MongoDB Clusters", 9],
  ["Feature", "Mongo", 1],
  ["Feature", "P2", 1],
  ["Task", "MongoDB Clusters", 1],
  ["AT-CTI", "P1", 7],
  ["MongoDB Clusters", "P0", 2],
  ["MongoDB Clusters", "P1", 7],
  ["MongoDB Clusters", "P2", 6],
  ["NoSQL", "P1", 4],
  ["bug", "P1", 4],
  ["Mongo", "P1", 1],
  ["P0", "0.26.0", 2],
  ["P0", "0.26.1", 2],
  ["P1", "0.26.0", 5],
  ["P1", "0.26.1", 7],
  ["P1", "0.26.2", 1],
  ["P1", "Backlog", 2],
  ["P2", "0.26.0", 5],
  ["P2", "0.26.1", 7],
  ["0.26.0", "tnaum-ms", 5],
  ["0.26.0", "bk201-", 4],
  ["0.26.1", "tnaum-ms", 7],
  ["0.26.1", "bk201-", 5],
  ["0.26.2", "bk201-", 1],
  ["Backlog", "sevoku", 2]
];

const sankeyOptions = {
  sankey: {
    node: {
      colors: [
        '#6366f1', // Feature
        '#38bdf8', // Bug
        '#34d399', // Task
        '#fde047', // P1
        '#f87171', // P0
        '#a78bfa', // P2
        '#fbbf24', // Backlog
        '#818cf8', // Mongo
        '#f472b6', // AT-CTI
        '#facc15', // NoSQL
        '#4ade80', // MongoDB Clusters
        '#22d3ee', // tnaum-ms
        '#f43f5e', // sevoku
        '#0ea5e9', // bk201-
      ],
      label: {
        fontName: 'Poppins',
        fontSize: 18,
        color: '#fff',
        bold: true,
      },
      nodePadding: 28,
      width: 16,
    },
    link: {
      colorMode: 'gradient',
      colors: ['#818cf8', '#38bdf8', '#34d399', '#fde047', '#f87171', '#a78bfa', '#fbbf24'],
      fillOpacity: 0.22,
    },
  },
  backgroundColor: { fill: 'transparent' },
  chartArea: { left: 0, top: 0, width: '100%', height: '100%' },
};

const PracticalCards = () => (
  <div className="practical-section">
    <div className="practical-title">Overall Flow</div>
    <div
      style={{
        width: '100%',
        background: 'rgba(30, 30, 40, 0.55)', 
        borderRadius: 32,
        padding: 18,
        backdropFilter: 'blur(12px)',
        border: '2px solid rgba(120,120,180,0.18)',
        position: 'relative',
        marginBottom: 32,
      }}
    >
      <Chart
        chartType="Sankey"
        width="100%"
        height="340px"
        data={sankeyData}
        options={sankeyOptions}
      />
    </div>
    <div className="practical-cards-list">
      {cards.map((card, i) => (
        <div key={i} className="practical-card">
          <div className="practical-card-title">{card.title}</div>
        </div>
      ))}
    </div>
  </div>
);

export default PracticalCards; 