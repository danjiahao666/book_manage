from rest_framework import serializers
from .models import Category, Book, Comment, UserBookInteraction
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    """
    图书分类序列化器
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['created_at']

class UserBasicSerializer(serializers.ModelSerializer):
    """
    用户基本信息序列化器（用于评论显示）
    """
    class Meta:
        model = User
        fields = ['id', 'username']

class CommentSerializer(serializers.ModelSerializer):
    """
    图书评论序列化器
    """
    user = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'book', 'user', 'content', 'rating', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        """
        创建评论，自动关联当前用户
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class BookSerializer(serializers.ModelSerializer):
    """
    图书序列化器
    """
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    average_rating = serializers.ReadOnlyField()
    comments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'category', 'category_id', 'cover', 'isbn',
            'description', 'publisher', 'publish_date', 'price', 'pages',
            'language', 'created_at', 'updated_at', 'average_rating', 'comments_count'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_comments_count(self, obj):
        """获取评论数量"""
        return obj.comments.count()

class BookDetailSerializer(BookSerializer):
    """
    图书详情序列化器，包含评论信息
    """
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + ['comments']

class UserBookInteractionSerializer(serializers.ModelSerializer):
    """
    用户图书交互序列化器
    """
    class Meta:
        model = UserBookInteraction
        fields = ['id', 'user', 'book', 'viewed_at', 'view_count']
        read_only_fields = ['viewed_at'] 