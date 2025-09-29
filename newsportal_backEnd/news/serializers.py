# newsportal_backEnd/news/serializers.py

from rest_framework import serializers
from .models import Article, Category, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        # Allow user to input name and body
        fields = ['id', 'author_name', 'body', 'created_on'] 
        # The article field is set by the view, not the user input
        read_only_fields = ['created_on']

class ArticleSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    comments = CommentSerializer(many=True, read_only=True) # Nested comments
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'category', 'category_name', 
                  'image', 'video', 'published_date', 'comments']
        read_only_fields = ['published_date']