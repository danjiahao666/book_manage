from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from django.shortcuts import get_object_or_404

from .models import Category, Book, Comment, UserBookInteraction
from .serializers import (
    CategorySerializer, BookSerializer, BookDetailSerializer,
    CommentSerializer, UserBookInteractionSerializer
)

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    自定义权限：
    - 管理员可以执行所有操作
    - 普通用户只能执行读操作
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class CategoryViewSet(viewsets.ModelViewSet):
    """
    图书分类视图集
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

class BookViewSet(viewsets.ModelViewSet):
    """
    图书视图集
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'description', 'isbn']
    ordering_fields = ['title', 'author', 'created_at', 'publish_date', 'price']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """
        根据操作选择不同的序列化器
        - 列表页使用 BookSerializer
        - 详情页使用 BookDetailSerializer
        """
        if self.action == 'retrieve':
            return BookDetailSerializer
        return BookSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """
        获取图书详情，同时记录用户浏览历史
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # 记录用户浏览历史（仅对已登录用户）
        if request.user.is_authenticated:
            interaction, created = UserBookInteraction.objects.get_or_create(
                user=request.user,
                book=instance
            )
            if not created:
                interaction.view_count += 1
                interaction.save()
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """
        高级搜索功能
        """
        query = request.query_params.get('q', '')
        category_id = request.query_params.get('category', None)
        min_price = request.query_params.get('min_price', None)
        max_price = request.query_params.get('max_price', None)
        min_rating = request.query_params.get('min_rating', None)
        
        queryset = self.get_queryset()
        
        # 基本搜索
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(description__icontains=query) |
                Q(isbn__icontains=query)
            )
        
        # 按分类筛选
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # 按价格范围筛选
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # 按评分筛选
        if min_rating:
            # 计算每本书的平均评分，并筛选出评分大于等于min_rating的书
            queryset = queryset.annotate(avg_rating=Avg('comments__rating')).filter(avg_rating__gte=min_rating)
        
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """
        获取推荐图书
        - 对于已登录用户，根据其浏览历史和评论推荐
        - 对于未登录用户，返回评分最高的图书
        """
        if request.user.is_authenticated:
            # 获取用户已浏览的图书分类
            user_categories = UserBookInteraction.objects.filter(
                user=request.user
            ).values_list('book__category', flat=True).distinct()
            
            # 获取用户已评论的图书的评分高于3的分类
            liked_categories = Comment.objects.filter(
                user=request.user, rating__gte=4
            ).values_list('book__category', flat=True).distinct()
            
            # 合并分类
            all_categories = set(list(user_categories) + list(liked_categories))
            
            if all_categories:
                # 推荐同类别但用户未浏览过的图书
                recommended_books = Book.objects.filter(
                    category__in=all_categories
                ).exclude(
                    user_interactions__user=request.user
                ).annotate(
                    avg_rating=Avg('comments__rating')
                ).order_by('-avg_rating')[:10]
                
                serializer = self.get_serializer(recommended_books, many=True)
                return Response(serializer.data)
        
        # 默认推荐：评分最高的图书
        top_rated_books = Book.objects.annotate(
            avg_rating=Avg('comments__rating'),
            num_ratings=Count('comments')
        ).filter(num_ratings__gte=1).order_by('-avg_rating')[:10]
        
        serializer = self.get_serializer(top_rated_books, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    """
    图书评论视图集
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """
        根据不同的操作设置不同的权限
        - 查看评论不需要认证
        - 创建、更新和删除评论需要认证
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        根据URL参数筛选评论
        - 可以按图书ID筛选
        - 可以按用户ID筛选
        """
        queryset = super().get_queryset()
        book_id = self.request.query_params.get('book', None)
        user_id = self.request.query_params.get('user', None)
        
        if book_id:
            queryset = queryset.filter(book_id=book_id)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
            
        return queryset
    
    def perform_create(self, serializer):
        """创建评论时自动关联当前用户"""
        serializer.save(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        """
        更新评论，确保用户只能更新自己的评论
        """
        instance = self.get_object()
        if instance.user != request.user and not request.user.is_staff:
            return Response(
                {"detail": "您没有权限修改其他用户的评论"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        删除评论，确保用户只能删除自己的评论
        """
        instance = self.get_object()
        if instance.user != request.user and not request.user.is_staff:
            return Response(
                {"detail": "您没有权限删除其他用户的评论"},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
