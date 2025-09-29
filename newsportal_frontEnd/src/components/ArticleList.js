// newsportal_frontEnd/src/components/ArticleList.js

import React, { useState, useEffect } from 'react';
import api from '../api';
import { Link, useSearchParams } from 'react-router-dom';

function ArticleList() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchParams, setSearchParams] = useSearchParams();
  
  const searchQuery = searchParams.get('q') || '';
  const [searchTerm, setSearchTerm] = useState(searchQuery);

  useEffect(() => {
    setLoading(true);
    
    // Use the 'search' parameter required by your Django ArticleViewSet
    const url = searchQuery 
      ? `articles/?search=${searchQuery}`
      : 'articles/';

    api.get(url)
      .then(response => {
        setArticles(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching articles:', error);
        setLoading(false);
      });
  }, [searchQuery]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
        setSearchParams({ q: searchTerm.trim() });
    } else {
        setSearchParams({}); 
    }
  };

  if (loading) {
    return <div className="loading">Loading news...</div>;
  }

  // --- Start Rendering ---
  return (
    <div className="article-list">
      <h2>Latest News</h2>
      
      {/* Search Bar */}
      <form onSubmit={handleSearchSubmit} className="search-form">
          <input
              type="text"
              placeholder="Search articles by title or content..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
          />
          <button type="submit">Search</button>
      </form>
      
      {searchQuery && (
          <p className="search-status">
              Showing results for: **"{searchQuery}"** ({articles.length} found)
          </p>
      )}

      {articles.length === 0 ? (
          <p className="no-results">No articles found matching your criteria.</p>
      ) : (
          articles.map(article => (
              <div key={article.id} className="article-preview">
                
                <div className="media-thumbnail">
                   {/* Defensive rendering to prevent crashes on null values */}
                   {article.image && ( <img src={article.image} alt={article.title} /> )}
                   {!article.image && article.video && ( <video src={article.video} controls muted /> )}
                   {!article.image && !article.video && ( <div className="no-media-placeholder">No Media</div> )}
                </div>

                <div className="article-info">
                  <span className="category-tag">
                    {/* Defensive rendering for category name */}
                    {article.category_name ? article.category_name : 'N/A'}
                  </span>
                  <h3><Link to={`/articles/${article.id}`}>{article.title}</Link></h3>
                  <p>{article.content ? article.content.substring(0, 150) : 'No content'}...</p> 
                  <small>Published: {new Date(article.published_date).toLocaleDateString()}</small>
                </div>
              </div>
          ))
      )}
    </div>
  );
}

export default ArticleList;