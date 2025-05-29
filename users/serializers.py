from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    """
    用户配置文件序列化器
    """
    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'birth_date', 'favorite_genres']

class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器
    """
    profile = UserProfileSerializer(required=False)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'profile']
        
    def create(self, validated_data):
        """
        创建用户及其配置文件
        """
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password')
        
        # 创建用户
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        
        # 创建用户配置文件
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        else:
            UserProfile.objects.create(user=user)
            
        return user
    
    def update(self, instance, validated_data):
        """
        更新用户及其配置文件
        """
        profile_data = validated_data.pop('profile', None)
        password = validated_data.pop('password', None)
        
        # 更新用户信息
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        if password:
            instance.set_password(password)
        
        instance.save()
        
        # 更新用户配置文件
        if profile_data and hasattr(instance, 'profile'):
            for attr, value in profile_data.items():
                setattr(instance.profile, attr, value)
            instance.profile.save()
            
        return instance 