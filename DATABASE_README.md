# 数据库配置与导入指南

本文档提供了如何配置MySQL数据库并导入示例数据到智能图书推荐系统的详细说明。

## 文件说明

- `book_recommendation.sql`: 包含数据库结构和示例数据的SQL文件
- `import_data.py`: 用于导入SQL数据到MySQL的Python脚本

## 导入步骤

### 1. 配置MySQL数据库

确保您的系统已安装MySQL数据库(5.7+版本)，并且已经启动MySQL服务。

### 2. 更新数据库配置

编辑Django项目的`book_recommendation_system/settings.py`文件，确保数据库配置正确：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'book_recommendation',  # 数据库名称
        'USER': 'root',                # 修改为您的MySQL用户名
        'PASSWORD': 'password',        # 修改为您的MySQL密码
        'HOST': 'localhost',           # 数据库主机
        'PORT': '3306',                # 数据库端口
    }
}
```

### 3. 导入数据方式一：使用Python脚本

运行提供的Python导入脚本：

```bash
python import_data.py [用户名] [密码]
```

如果不提供用户名和密码参数，脚本会交互式地请求您输入。

### 4. 导入数据方式二：直接使用MySQL命令

如果您更喜欢直接使用MySQL命令，可以执行以下操作：

```bash
# 登录MySQL
mysql -u 用户名 -p

# 创建数据库（如果SQL文件中没有CREATE DATABASE语句）
CREATE DATABASE IF NOT EXISTS book_recommendation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 退出MySQL命令行
EXIT;

# 导入SQL文件
mysql -u 用户名 -p book_recommendation < book_recommendation.sql
```

## 示例数据说明

SQL文件中包含以下示例数据：

1. **用户数据**:
   - 管理员账户 (用户名: admin)
   - 3个普通用户账户 (user1, user2, user3)

2. **图书分类**:
   - 科幻小说、悬疑推理、文学经典、历史
   - 计算机与编程、哲学思想、传记、商业管理

3. **图书数据**:
   - 包含15本不同类别的图书

4. **评论数据**:
   - 用户对图书的评论和评分

5. **交互数据**:
   - 用户与图书的浏览记录

## 默认账户

系统中预设了以下账户，可用于测试：

1. **管理员**:
   - 用户名: admin
   - 密码: admin123 (注意：实际密码是加密存储的)

2. **普通用户**:
   - 用户名: user1, user2, user3
   - 密码: password123 (注意：实际密码是加密存储的)

## 注意事项

1. SQL文件中的示例数据仅供开发和测试使用，不建议在生产环境中使用。

2. SQL文件中的用户密码是使用Django的密码哈希算法生成的，密码原文为:
   - 管理员: admin123
   - 普通用户: password123

3. 在生产环境中，请确保使用更强的密码，并更改默认的管理员账户密码。

4. 导入后，您可以使用Django的管理命令查看数据：

   ```bash
   python manage.py shell
   
   # 在Python shell中执行
   from books.models import Book, Category, Comment
   from django.contrib.auth.models import User
   
   # 查看数据
   print(User.objects.all())
   print(Book.objects.all())
   print(Category.objects.all())
   ``` 