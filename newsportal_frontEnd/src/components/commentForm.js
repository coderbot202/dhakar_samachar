// newsportal_frontEnd/src/components/CommentForm.js

import React, { useState } from 'react';
import api from '../api';

function CommentForm({ articleId, onCommentSubmitted }) {
  const [authorName, setAuthorName] = useState('');
  const [body, setBody] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (!authorName.trim() || !body.trim()) {
      setError('Name and comment body cannot be empty.');
      return;
    }

    try {
      // POST the new comment to the specific article's comments endpoint
      await api.post(`articles/${articleId}/comments/`, {
        author_name: authorName,
        body: body,
      });

      setSuccess('Comment submitted successfully!');
      setAuthorName('');
      setBody('');
      onCommentSubmitted(); // Trigger parent to re-fetch and update comment list
    } catch (err) {
      console.error('Error submitting comment:', err);
      setError('Failed to submit comment. Please try again.');
    }
  };

  return (
    <div className="comment-form-container">
      <h4>Leave a Comment</h4>
      <form onSubmit={handleSubmit}>
        {error && <p className="error-message">{error}</p>}
        {success && <p className="success-message">{success}</p>}
        
        <div className="form-group">
          <label htmlFor="name">Your Name:</label>
          <input
            type="text"
            id="name"
            value={authorName}
            onChange={(e) => setAuthorName(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="comment">Comment:</label>
          <textarea
            id="comment"
            value={body}
            onChange={(e) => setBody(e.target.value)}
            rows="4"
            required
          />
        </div>
        
        <button type="submit">Submit Comment</button>
      </form>
    </div>
  );
}

export default CommentForm;