import React from 'react';

const SearchResults = ({ results }) => {
  return (
    <div className="results">
      {results.map((result, index) => (
        <div key={index} className="result-item">
          <a href={result.url} target="_blank" rel="noopener noreferrer">
            <h3>{result.title}</h3>
            <p>{result.snippet}</p>
          </a>
        </div>
      ))}
    </div>
  );
};

export default SearchResults;
