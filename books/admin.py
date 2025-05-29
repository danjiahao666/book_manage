from django.contrib import admin
from .models import Category, Book, Comment, UserBookInteraction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """图书分类管理"""
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """图书管理"""
    list_display = ['title', 'author', 'category', 'isbn', 'publisher', 'publish_date', 'price']
    search_fields = ['title', 'author', 'isbn', 'publisher', 'description']
    list_filter = ['category', 'language', 'publish_date']
    date_hierarchy = 'publish_date'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """图书评论管理"""
    list_display = ['book', 'user', 'rating', 'created_at']
    search_fields = ['book__title', 'user__username', 'content']
    list_filter = ['rating', 'created_at']
    date_hierarchy = 'created_at'

@admin.register(UserBookInteraction)
class UserBookInteractionAdmin(admin.ModelAdmin):
    """用户图书交互管理"""
    list_display = ['user', 'book', 'viewed_at', 'view_count']
    search_fields = ['user__username', 'book__title']
    list_filter = ['viewed_at']
    date_hierarchy = 'viewed_at'
