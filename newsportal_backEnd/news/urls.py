# newsportal_backEnd/news/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CategoryViewSet, CommentListCreateView

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    # Default DRF endpoints for Articles and Categories
    path('', include(router.urls)),
    
    # 👈 Custom endpoint for Comments: /api/articles/{id}/comments/
    path('articles/<int:article_id>/comments/', 
         CommentListCreateView.as_view(), 
         name='article-comments'),
]