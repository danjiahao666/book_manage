# 智能图书推荐系统

这是一个基于Django和Django REST Framework开发的智能图书推荐系统的后端API。该系统提供图书管理、用户管理、评论管理以及基于用户行为的图书推荐功能。

## 功能特点

1. **用户管理**
   - 用户注册、登录和注销
   - 用户个人资料管理

2. **图书管理**
   - 图书信息的增删改查
   - 图书分类管理
   - 图书封面上传

3. **评论系统**
   - 用户可对图书发表评论和评分
   - 评论管理功能

4. **搜索功能**
   - 支持按书名、作者、内容搜索
   - 高级搜索功能（按分类、价格、评分等筛选）

5. **推荐系统**
   - 基于用户浏览历史的图书推荐
   - 基于用户评分的图书推荐

## 技术栈

- **后端框架**: Django 5.2
- **API框架**: Django REST Framework 3.16
- **数据库**: MySQL
- **认证**: Django Session认证

## 安装与运行

### 环境要求

- Python 3.8+
- MySQL 5.7+

### 安装步骤

1. 克隆项目

```bash
git clone <项目地址>
cd book_recommendation_system
```

2. 创建并激活虚拟环境

```bash
rmdir /s /q venv
python -m venv venv
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 配置数据库

编辑 `book_recommendation_system/settings.py` 文件中的数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'book_recommendation',  # 数据库名称
        'USER': 'root',                # 数据库用户名
        'PASSWORD': 'password',        # 数据库密码
        'HOST': 'localhost',           # 数据库主机
        'PORT': '3306',                # 数据库端口
    }
}
```

5. 创建数据库

```bash
mysql -u root -p
```

```sql
CREATE DATABASE book_recommendation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

6. 执行数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

7. 创建超级用户

```bash
python manage.py createsuperuser
```

8. 运行开发服务器

```bash
python manage.py runserver
```

## API接口文档

启动服务器后，可以通过以下地址访问API文档：

```
http://localhost:8000/docs/
```

### 主要API端点

#### 用户相关

- `POST /api/users/users/`: 创建新用户
- `POST /api/users/users/login/`: 用户登录
- `POST /api/users/users/logout/`: 用户注销
- `GET /api/users/users/me/`: 获取当前用户信息
- `PUT /api/users/users/me/`: 更新当前用户信息
- `GET /api/users/users/me/profile/`: 获取用户配置文件
- `PUT /api/users/users/me/profile/`: 更新用户配置文件

#### 图书相关

- `GET /api/books/books/`: 获取图书列表
- `POST /api/books/books/`: 创建新图书（仅管理员）
- `GET /api/books/books/{id}/`: 获取图书详情
- `PUT /api/books/books/{id}/`: 更新图书信息（仅管理员）
- `DELETE /api/books/books/{id}/`: 删除图书（仅管理员）
- `GET /api/books/books/search/`: 搜索图书
- `GET /api/books/books/recommended/`: 获取推荐图书

#### 分类相关

- `GET /api/books/categories/`: 获取分类列表
- `POST /api/books/categories/`: 创建新分类（仅管理员）
- `GET /api/books/categories/{id}/`: 获取分类详情
- `PUT /api/books/categories/{id}/`: 更新分类信息（仅管理员）
- `DELETE /api/books/categories/{id}/`: 删除分类（仅管理员）

#### 评论相关

- `GET /api/books/comments/`: 获取评论列表
- `POST /api/books/comments/`: 创建新评论
- `GET /api/books/comments/{id}/`: 获取评论详情
- `PUT /api/books/comments/{id}/`: 更新评论（仅评论作者）
- `DELETE /api/books/comments/{id}/`: 删除评论（仅评论作者或管理员）

## 项目结构

```
book_recommendation_system/
├── book_recommendation_system/  # 项目配置目录
│   ├── __init__.py
│   ├── settings.py              # 项目设置
│   ├── urls.py                  # 主URL路由
│   ├── asgi.py
│   └── wsgi.py
├── books/                       # 图书应用
│   ├── __init__.py
│   ├── admin.py                 # 管理后台配置
│   ├── apps.py
│   ├── models.py                # 数据模型
│   ├── serializers.py           # 序列化器
│   ├── urls.py                  # URL路由
│   └── views.py                 # 视图
├── users/                       # 用户应用
│   ├── __init__.py
│   ├── admin.py                 # 管理后台配置
│   ├── apps.py
│   ├── models.py                # 数据模型
│   ├── serializers.py           # 序列化器
│   ├── signals.py               # 信号处理
│   ├── urls.py                  # URL路由
│   └── views.py                 # 视图
├── media/                       # 媒体文件目录
├── static/                      # 静态文件目录
├── manage.py                    # Django管理脚本
└── README.md                    # 项目说明文档
```

123

## 许可证

本项目采用MIT许可证。详情请参阅LICENSE文件。 


首页: http://127.0.0.1:8000/
管理后台: http://127.0.0.1:8000/admin/
用户API: http://127.0.0.1:8000/api/users/
图书API: http://127.0.0.1:8000/api/books/


Swagger文档：在浏览器中打开 http://127.0.0.1:8000/swagger/
这是一个交互式文档，可以直接在网页中测试API
ReDoc文档：在浏览器中打开 http://127.0.0.1:8000/redoc/
这是另一种格式的文档，布局更干净，适合阅读
JSON格式文档：http://127.0.0.1:8000/swagger.json
这是API规范的原始JSON表示，可用于其他工具导入

基础URL
首页: http://127.0.0.1:8000/
管理后台: http://127.0.0.1:8000/admin/
REST框架登录: http://127.0.0.1:8000/api-auth/

API文档
Swagger文档: http://127.0.0.1:8000/swagger/
ReDoc文档: http://127.0.0.1:8000/redoc/
JSON格式文档: http://127.0.0.1:8000/swagger.json

用户相关API
用户列表: http://127.0.0.1:8000/api/users/users/
用户详情: http://127.0.0.1:8000/api/users/users/{id}/
当前用户: http://127.0.0.1:8000/api/users/users/me/
用户登录: http://127.0.0.1:8000/api/users/users/login/
用户注销: http://127.0.0.1:8000/api/users/users/logout/
用户资料: http://127.0.0.1:8000/api/users/users/{id}/profile/

图书相关API
图书列表: http://127.0.0.1:8000/api/books/books/
图书详情: http://127.0.0.1:8000/api/books/books/{id}/
图书分类列表: http://127.0.0.1:8000/api/books/categories/
图书分类详情: http://127.0.0.1:8000/api/books/categories/{id}/
图书评论列表: http://127.0.0.1:8000/api/books/comments/
图书评论详情: http://127.0.0.1:8000/api/books/comments/{id}/

每个列表API还支持以下参数：
分页：?page=2（获取第2页数据）
每页显示数：?page_size=20（每页显示20条记录）
排序：?ordering=name（按名称升序）或?ordering=-name（降序）
您可以在Swagger文档中查看每个API的详细参数和使用方法，包括请求体格式和响应格式。