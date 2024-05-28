import React, { useState } from 'react';
import SearchForm from '../components/SearchForm';
import SearchResults from '../components/SearchResults';
import { useLocation } from 'react-router-dom';

const ResultsPage = ({ results, setResults }) => {
  const location = useLocation();
  const [query, setQuery] = useState(location.state.query || '');

  return (
    <div className="main">
      <header className="header">
        <img src="https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png" alt="Logo" className="logo" />
      </header>
      <SearchForm setResults={setResults} initialQuery={query} />
      <SearchResults results={results} />
    </div>
  );
};

export default ResultsPage;
