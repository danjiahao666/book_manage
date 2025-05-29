from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    用户配置文件模型
    扩展Django内置的User模型，添加额外的用户信息
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='用户')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name='头像')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    birth_date = models.DateField(null=True, blank=True, verbose_name='出生日期')
    favorite_genres = models.CharField(max_length=200, blank=True, verbose_name='喜爱的图书类型')
    
    class Meta:
        verbose_name = '用户配置文件'
        verbose_name_plural = '用户配置文件'
    
    def __str__(self):
        return f"{self.user.username}的个人资料"
