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
    list_display = ['book', 'user', 'rating', 'formatted_created_at']
    search_fields = ['book__title', 'user__username', 'content']
    list_filter = ['rating']
    
    def formatted_created_at(self, obj):
        """格式化显示创建时间，避免时区问题"""
        if obj.created_at:
            return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')
        return '未知'
    formatted_created_at.short_description = '创建时间'

@admin.register(UserBookInteraction)
class UserBookInteractionAdmin(admin.ModelAdmin):
    """用户图书交互管理"""
    list_display = ['user', 'book', 'formatted_viewed_at', 'view_count']
    search_fields = ['user__username', 'book__title']
    list_filter = ['view_count']
    
    def formatted_viewed_at(self, obj):
        """格式化显示浏览时间，避免时区问题"""
        if obj.viewed_at:
            return obj.viewed_at.strftime('%Y-%m-%d %H:%M:%S')
        return '未知'
    formatted_viewed_at.short_description = '浏览时间'
