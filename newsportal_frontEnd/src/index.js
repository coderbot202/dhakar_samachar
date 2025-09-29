// newsportal_frontEnd/src/index.js

import React from 'react';
// -------------------------------------------------------------
// CRITICAL: Ensure you are importing the modern client renderer
import ReactDOM from 'react-dom/client'; 
// -------------------------------------------------------------

// CRITICAL: Ensure the name of the file being imported matches (App.jsx)
import App from './App.js'; 
import './App.css'; // Make sure this path is correct if you use it
// You also have theme.css, make sure it's imported if needed

const rootElement = document.getElementById('root');

if (rootElement) {
    const root = ReactDOM.createRoot(rootElement);
    root.render(
      <React.StrictMode>
        <App />
      </React.StrictMode>
    );
} else {
    // If you see this in the browser console, index.html is still broken
    console.error("Failed to find the root element with id='root' in the DOM.");
}