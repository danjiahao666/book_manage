from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    """
    图书分类模型
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='分类描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '图书分类'
        verbose_name_plural = '图书分类'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Book(models.Model):
    """
    图书模型
    """
    title = models.CharField(max_length=200, verbose_name='书名')
    author = models.CharField(max_length=200, verbose_name='作者')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', verbose_name='分类')
    cover = models.ImageField(upload_to='covers/', null=True, blank=True, verbose_name='封面')
    isbn = models.CharField(max_length=13, unique=True, verbose_name='ISBN')
    description = models.TextField(verbose_name='图书描述')
    publisher = models.CharField(max_length=200, verbose_name='出版社')
    publish_date = models.DateField(verbose_name='出版日期')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    pages = models.PositiveIntegerField(verbose_name='页数')
    language = models.CharField(max_length=50, verbose_name='语言')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '图书'
        verbose_name_plural = '图书'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    @property
    def average_rating(self):
        """计算图书的平均评分"""
        ratings = self.comments.all().values_list('rating', flat=True)
        if ratings:
            return sum(ratings) / len(ratings)
        return 0

class Comment(models.Model):
    """
    图书评论模型
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments', verbose_name='图书')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='用户')
    content = models.TextField(verbose_name='评论内容')
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name='评分'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '图书评论'
        verbose_name_plural = '图书评论'
        ordering = ['-created_at']
        # 一个用户只能对一本书评论一次
        unique_together = ['book', 'user']
    
    def __str__(self):
        return f"{self.user.username}对{self.book.title}的评论"

class UserBookInteraction(models.Model):
    """
    用户与图书的交互记录，用于推荐系统
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_interactions', verbose_name='用户')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='user_interactions', verbose_name='图书')
    viewed_at = models.DateTimeField(auto_now_add=True, verbose_name='浏览时间')
    view_count = models.PositiveIntegerField(default=1, verbose_name='浏览次数')
    
    class Meta:
        verbose_name = '用户图书交互'
        verbose_name_plural = '用户图书交互'
        unique_together = ['user', 'book']
    
    def __str__(self):
        return f"{self.user.username}与{self.book.title}的交互"
