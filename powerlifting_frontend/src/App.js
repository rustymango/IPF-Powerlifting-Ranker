// import logo from './logo.svg';
import './App.css';
import React, { Component } from 'react';
import PostStats from './Components/stats_post';
import PostRank from './Components/rank_post';

function App() {
  return (

    <div className="App">
      <PostStats />
      <PostRank />
    </div>
  );

}

export default App;
