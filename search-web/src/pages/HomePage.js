import React from 'react';
import SearchForm from '../components/SearchForm';
import mainIcon from '../assets/231.png';  // 이미지 파일 import

const HomePage = ({ setResults }) => {
  return (
    <div className="main">
      <header className="header">
        <img src={mainIcon} alt="Logo" className="logo" />
      </header>
      <SearchForm setResults={setResults} />
    </div>
  );
};

export default HomePage;
