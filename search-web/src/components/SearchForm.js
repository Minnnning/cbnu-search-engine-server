import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SearchForm.css';
import searchIcon from '../assets/search-icon.png';  // 이미지 파일 import

const SearchForm = ({ setResults, initialQuery = '' }) => {
  const [query, setQuery] = useState(initialQuery);
  const navigate = useNavigate();

  const handleSearch = async (e) => {
    e.preventDefault();
    if (query) {
      const response = await fetch(`https://api.example.com/search?q=${query}`);
      const data = await response.json();
      setResults(data.results); // assuming the API returns an object with a 'results' array
      navigate('/results', { state: { query } });
    }
  };

  return (
    <form className="search-form" onSubmit={handleSearch}>
      <input
        type="text"
        className="search-input"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
      />
      <button type="submit" className="search-button">
        <img src={searchIcon} alt="Search" className="search-icon" />
      </button>
    </form>
  );
};

export default SearchForm;