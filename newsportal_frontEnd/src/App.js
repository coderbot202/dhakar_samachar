// newsportal_frontEnd/src/App.js

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ArticleList from './components/ArticleList';
import ArticleDetail from './components/ArticleDetail';
import './App.css'; 

function App() {
  return (
    <Router>
      <div className="app-container">
        <header className="main-header">
          <nav>
            {/* Base URL (/) points to the Article List - the default user view */}
            <Link to="/" className="site-logo">📰 News Portal</Link>
          </nav>
        </header>

        <main className="content-area">
          <Routes>
            <Route path="/" element={<ArticleList />} />
            <Route path="/articles/:id" element={<ArticleDetail />} />
          </Routes>
        </main>

        <footer className="main-footer">
            © 2025 News Portal. All rights reserved.
        </footer>
      </div>
    </Router>
  );
}

export default App;