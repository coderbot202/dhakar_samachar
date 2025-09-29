# newsportal_backEnd/news/models.py

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Categories" # Fixes display in Admin
        
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    
    # NEW MEDIA FIELDS
    image = models.ImageField(upload_to='article_images/', blank=True, null=True)
    video = models.FileField(upload_to='article_videos/', blank=True, null=True)
    
    published_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100) # User who commented
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_on'] # Show comments from oldest to newest
    
    def __str__(self):
        return f'Comment by {self.author_name} on {self.article.title}'