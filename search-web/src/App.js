import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ResultsPage from './pages/ResultsPage';
import './App.css';

function App() {
  const [results, setResults] = useState([]);

  return (
    <Router>
      <div className="app">
        <Routes>
          <Route path="/" element={<HomePage setResults={setResults} />} />
          <Route path="/results" element={<ResultsPage results={results} setResults={setResults} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
