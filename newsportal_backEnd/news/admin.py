# D:\news-portal\newsportal_backEnd\news\admin.py

from django.contrib import admin
from .models import Article, Category, Comment  # <--- CORRECTED: Changed 'NewsArticle' to 'Article'

# You should also make sure the registration lines are there:
admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Comment)