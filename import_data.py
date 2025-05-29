#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
导入SQL数据到MySQL数据库的脚本
"""

import os
import subprocess
import getpass
import sys

def import_sql_file(sql_file, database, username=None, password=None, host="localhost"):
    """
    导入SQL文件到MySQL数据库
    
    参数:
    - sql_file: SQL文件路径
    - database: 数据库名称
    - username: MySQL用户名
    - password: MySQL密码
    - host: MySQL主机
    """
    # 如果未提供用户名，要求输入
    if username is None:
        username = input("请输入MySQL用户名（默认为root）: ") or "root"
    
    # 如果未提供密码，要求输入
    if password is None:
        password = getpass.getpass(f"请输入MySQL用户 {username} 的密码: ")
    
    # 构建MySQL命令
    mysql_cmd = f'mysql -h {host} -u {username}'
    if password:
        mysql_cmd += f' -p"{password}"'
    
    # 检查数据库是否存在
    check_db_cmd = f'{mysql_cmd} -e "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = \'{database}\'"'
    result = subprocess.run(check_db_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if database not in result.stdout:
        print(f"数据库 {database} 不存在，将会创建...")
    
    # 导入SQL文件
    import_cmd = f'{mysql_cmd} < {sql_file}'
    print(f"正在导入SQL文件 {sql_file} 到 MySQL...")
    
    try:
        subprocess.run(import_cmd, shell=True, check=True)
        print(f"成功导入SQL文件到数据库 {database}!")
    except subprocess.CalledProcessError as e:
        print(f"导入SQL文件失败: {e}")
        return False
    
    return True

def main():
    """
    主函数
    """
    # 检查SQL文件是否存在
    sql_file = "book_recommendation.sql"
    if not os.path.isfile(sql_file):
        print(f"错误: SQL文件 {sql_file} 不存在！")
        return False
    
    # 从SQL文件中获取数据库名称
    database = "book_recommendation"
    
    # 检查命令行参数
    username = None
    password = None
    
    if len(sys.argv) > 1:
        username = sys.argv[1]
    if len(sys.argv) > 2:
        password = sys.argv[2]
    
    # 导入SQL文件
    success = import_sql_file(sql_file, database, username, password)
    
    if success:
        print("""
数据导入成功！现在你可以使用以下命令启动Django服务器：
    
    python manage.py runserver
    
然后在浏览器访问:
    
    http://127.0.0.1:8000/admin/
    
使用以下默认管理员账号登录:
    用户名: admin
    密码: admin123
    
注意: 这是示例数据，仅用于开发和测试。在生产环境中，请使用更强的密码。
    """)
    
    return success

if __name__ == "__main__":
    main() 