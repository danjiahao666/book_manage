from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt

from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@csrf_exempt
def token_auth(request):
    """
    Token认证视图 - 用于前端登录
    """
    print("接收到登录请求:", request.data)
    
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        print("缺少用户名或密码")
        return Response(
            {"detail": "请提供用户名和密码"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(username=username, password=password)
    
    if not user:
        print(f"认证失败: {username}")
        return Response(
            {"detail": "用户名或密码错误"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    # 获取或创建Token
    token, created = Token.objects.get_or_create(user=user)
    
    # 返回用户信息和Token
    serializer = UserSerializer(user)
    response_data = {
        'user': serializer.data,
        'token': token.key
    }
    
    print("认证成功，返回数据:", response_data)
    return Response(response_data)

class UserViewSet(viewsets.ModelViewSet):
    """
    用户视图集，处理用户的CRUD操作
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        根据不同的操作设置不同的权限
        - 注册用户不需要认证
        - 获取和更新用户信息需要认证
        - 只有管理员可以列出所有用户
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
    
    def retrieve(self, request, pk=None):
        """
        获取用户信息，普通用户只能获取自己的信息
        """
        if pk == 'me' or pk == str(request.user.id):
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        
        # 只有管理员可以获取其他用户的信息
        if request.user.is_staff:
            return super().retrieve(request, pk)
        
        return Response(
            {"detail": "您没有权限查看其他用户的信息"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    def update(self, request, pk=None):
        """
        更新用户信息，普通用户只能更新自己的信息
        """
        if pk == 'me' or pk == str(request.user.id):
            instance = request.user
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        
        # 只有管理员可以更新其他用户的信息
        if request.user.is_staff:
            return super().update(request, pk)
        
        return Response(
            {"detail": "您没有权限更新其他用户的信息"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def login(self, request):
        """
        用户登录
        """
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {"detail": "请提供用户名和密码"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if not user:
            return Response(
                {"detail": "用户名或密码错误"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        login(request, user)
        
        # 返回用户信息
        serializer = self.get_serializer(user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """
        用户注销
        """
        logout(request)
        return Response({"detail": "成功注销"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get', 'put', 'patch'], permission_classes=[permissions.IsAuthenticated])
    def profile(self, request, pk=None):
        """
        获取或更新用户配置文件
        """
        # 确保用户只能访问自己的配置文件
        if pk != 'me' and pk != str(request.user.id) and not request.user.is_staff:
            return Response(
                {"detail": "您没有权限访问其他用户的配置文件"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 如果是 'me'，使用当前用户
        if pk == 'me':
            user = request.user
        else:
            user = self.get_object()
        
        # 获取或创建用户配置文件
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        if request.method == 'GET':
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        
        # 更新配置文件
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
