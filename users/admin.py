from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """用户配置文件管理"""
    list_display = ['user', 'birth_date', 'favorite_genres']
    search_fields = ['user__username', 'user__email', 'favorite_genres']
    list_filter = ['birth_date']
