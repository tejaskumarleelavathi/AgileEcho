import React from 'react';
import './App.css';
import Header from './components/Header';
import LevelHeader from './components/LevelHeader';
// import Calendar from './components/Calendar';
import Objectives from './components/Objectives';
// import MentorCall from './components/MentorCall';
import PracticalCards from './components/PracticalCards';
import TheoryCards from './components/TheoryCards';
import ChatBox from './components/ChatBox';
// import ChatBubble from './components/ChatBubble';

function App() {
  return (
    <div className="App">
      <Header />
      <LevelHeader />
      {/* <Calendar /> */}
      <Objectives />
      {/* <MentorCall /> */}
      <PracticalCards />
      <TheoryCards />
      <ChatBox />
      {/* <ChatBubble /> */}
    </div>
  );
}

export default App;
