# newsportal_backEnd/news/views.py

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import filters # <-- IMPORTANT: Import the filters module
from .models import Article, Category, Comment
from .serializers import ArticleSerializer, CategorySerializer, CommentSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    """
    Handles listing, retrieving, and (via Admin/Authentication) creating/updating articles.
    Implements search functionality.
    """
    queryset = Article.objects.all().order_by('-published_date')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # --- SEARCH IMPLEMENTATION (User Requirement: Search Articles) ---
    filter_backends = [filters.SearchFilter]
    # The frontend ArticleList.js sends the search query to the 'search' parameter.
    # We tell DRF which fields to search within.
    search_fields = ['title', 'content', 'category__name'] 
    # -----------------------------------------------------------------


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Handles listing categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating comments for a specific article.
    (User Requirement: View and Comment on articles)
    """
    serializer_class = CommentSerializer
    permission_classes = [AllowAny] # Allow any user (even anonymous) to post comments

    def get_queryset(self):
        # Retrieve the article_id from the URL (defined in news/urls.py)
        article_id = self.kwargs['article_id']
        # Filter comments to show only those belonging to the current article
        return Comment.objects.filter(article__id=article_id).order_by('created_on')

    def perform_create(self, serializer):
        # Automatically link the new comment to the correct Article instance
        article = Article.objects.get(pk=self.kwargs['article_id'])
        serializer.save(article=article)