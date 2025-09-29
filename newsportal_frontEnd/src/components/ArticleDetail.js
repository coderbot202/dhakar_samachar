// newsportal_frontEnd/src/components/ArticleDetail.js
// (Same code as previously provided, ensures full article and comments load)

import React, { useState, useEffect, useCallback } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import CommentForm from './commentForm';

function ArticleDetail() {
  const { id } = useParams(); 
  const [article, setArticle] = useState(null);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchArticleData = useCallback(() => {
    setLoading(true);
    api.get(`articles/${id}/`)
      .then(response => {
        setArticle(response.data);
        setComments(response.data.comments || []); 
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching article details:', error);
        setLoading(false);
      });
  }, [id]);

  useEffect(() => {
    fetchArticleData();
  }, [fetchArticleData]);

  if (loading) {
    return <div className="loading">Loading article...</div>;
  }

  if (!article) {
    return <div className="error">Article not found.</div>;
  }

  return (
    <div className="article-detail">
      <h1>{article.title}</h1>
      <p className="category-info">
        Category: **{article.category_name}** | Published: {new Date(article.published_date).toLocaleDateString()}
      </p>
      
      <div className="article-media">
        {article.image && (
          <img src={article.image} alt={article.title} className="main-image" />
        )}
        {!article.image && article.video && (
          <video src={article.video} controls className="main-video">
             Your browser does not support the video tag.
          </video>
        )}
      </div>
      
      <div className="article-content">
        <p>{article.content}</p> 
      </div>

      <hr />

      <div className="comments-section">
        <h2>Comments ({comments.length})</h2>
        
        <CommentForm articleId={id} onCommentSubmitted={fetchArticleData} /> 

        <div className="comment-list">
          {comments.length > 0 ? (
            comments.map(comment => (
              <div key={comment.id} className="comment-item">
                <p className="comment-body">{comment.body}</p>
                <small>
                  By: **{comment.author_name}** on {new Date(comment.created_on).toLocaleDateString()}
                </small>
              </div>
            ))
          ) : (
            <p>Be the first to comment!</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default ArticleDetail;