"""
URL configuration for book_recommendation_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
# 移除不兼容的文档导入
# from rest_framework.documentation import include_docs_urls

# 导入drf-yasg相关组件
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# 简单的API根路径视图函数
def api_root(request):
    """提供API根目录信息"""
    return JsonResponse({
        'message': '欢迎使用图书推荐系统API',
        'api_endpoints': {
            'users': '/api/users/',
            'books': '/api/books/',
            'categories': '/api/books/categories/',
            'comments': '/api/books/comments/',
        },
        'admin': '/admin/',
        'api_docs': {
            'swagger': '/swagger/',
            'redoc': '/redoc/',
        }
    })

# 配置Swagger文档视图
schema_view = get_schema_view(
    openapi.Info(
        title="图书推荐系统API",
        default_version='v1',
        description="智能图书推荐系统的API文档",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # API根路径
    path('', api_root, name='api-root'),
    # Swagger文档URL
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # REST框架登录界面
    path('api-auth/', include('rest_framework.urls')),
    # 应用API
    path('api/users/', include('users.urls')),
    path('api/books/', include('books.urls')),
]

# 在开发环境中提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
