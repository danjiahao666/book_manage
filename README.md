# 智能图书推荐系统

这是一个基于Django和Vue.js开发的智能图书推荐系统，提供图书管理、用户管理、评论管理以及基于用户行为的图书推荐功能。
开发人员：淡嘉浩、韦荣健、韦贻元

## 系统架构

### 前端技术栈
- Vue 3 - 渐进式JavaScript框架
- Vue Router - 官方路由管理器
- Pinia - 状态管理库
- Element Plus - UI组件库
- Axios - HTTP客户端
- Tailwind CSS - 实用工具优先的CSS框架
- ECharts - 数据可视化图表库

### 后端技术栈
- Django - Python Web框架
- Django REST Framework - RESTful API工具包
- MySQL - 关系型数据库
- JWT - 用户认证
- Swagger/OpenAPI - API文档

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

## 系统功能详情

### 首页
首页展示系统统计信息和最新图书，包括图书总数、分类总数、热门分类等。页面顶部还提供了随机图书推荐功能。

### 图书列表
图书列表页面提供所有图书的详细信息，支持以下功能:
- 搜索图书：根据书名、作者等关键词搜索
- 筛选图书：按分类筛选
- 排序图书：按书名、价格、出版日期等排序
- 查看详情：查看图书的详细信息和评论
- 添加/编辑/删除图书：管理图书信息

### 分类管理
分类管理页面用于管理图书分类，提供以下功能:
- 查看所有分类及其包含的图书数量
- 添加新分类
- 编辑分类信息
- 删除空分类（只有没有关联图书的分类才能删除）
- 查看分类下的所有图书

### 关于页面
关于页面提供系统相关信息，包括:
- 系统介绍
- 技术架构
- 功能说明
- 开发团队
- 联系方式
- API文档链接
- 版本信息

## 安装与运行

### 环境要求

- Python 3.8+
- MySQL 8.0+
- NodeJS 22.0+

### 后端安装部署

1. 克隆项目

```bash
git clone https://github.com/danjiahao666/book_manage.git
cd book_recommendation_system
```

2. 创建并激活虚拟环境

```bash
# Windows
rmdir /s /q venv
python -m venv venv
.\venv\Scripts\Activate.ps1  # PowerShell
# 或
.\venv\Scripts\activate.bat  # CMD

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 配置数据库(确保mysql在8.0以上)

编辑 `book_recommendation_system/settings.py` 文件中的数据库配置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'book_recommendation',  # 数据库名称
        'USER': 'root',                # 数据库用户名
        'PASSWORD': '123456',        # 数据库密码
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

在可视化软件上运行insert_books_data.sql，导入书籍数据
```

7. 创建超级用户

```bash
python manage.py createsuperuser
```

8. 运行开发服务器

```bash
python manage.py runserver
```

### 前端安装部署

1. 安装依赖:
```bash
cd frotend/vue_project
npm install
```

2. 启动开发服务器:
```bash
npm run dev
```

3. 构建生产版本:
```bash
npm run build
```

## API接口文档

启动服务器后，可以通过以下地址访问API文档：

```
http://127.0.0.1:8000/swagger
http://127.0.0.1:8000/redoc
```

### 常用URL

基础URL
- 首页: http://127.0.0.1:8000/
- 管理后台: http://127.0.0.1:8000/admin/
- REST框架登录: http://127.0.0.1:8000/api-auth/

API文档
- Swagger文档: http://127.0.0.1:8000/swagger/
- ReDoc文档: http://127.0.0.1:8000/redoc/
- JSON格式文档: http://127.0.0.1:8000/swagger.json

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

每个列表API还支持以下参数：
- 分页：?page=2（获取第2页数据）
- 每页显示数：?page_size=20（每页显示20条记录）
- 排序：?ordering=name（按名称升序）或?ordering=-name（降序）

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
├── frotend/                     # 前端目录
│   └── vue_project/             # Vue项目目录
├── media/                       # 媒体文件目录
├── static/                      # 静态文件目录
├── manage.py                    # Django管理脚本
└── README.md                    # 项目说明文档
```

## 贡献

欢迎贡献代码或提出建议，请遵循以下步骤:
1. Fork 本仓库
2. 创建新的分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证。详情请参阅LICENSE文件。

## 联系方式

如有任何问题或建议，请联系:
- 邮箱: 390482691@qq.com 
