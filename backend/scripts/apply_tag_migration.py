#!/usr/bin/env python3
"""
标签迁移脚本 - 连接到MySQL数据库并应用标签相关的迁移
"""

import os
import sys
import mysql.connector
from mysql.connector import Error

def apply_migration():
    """应用标签迁移"""
    # 数据库连接配置
    db_config = {
        'host': 'localhost',
        'database': 'novel_db',
        'user': 'root',
        'password': 'ok123456'
    }
    
    # 尝试连接数据库
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        print("成功连接到数据库")
        
        # 读取迁移脚本
        migration_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                     'migrations', 'tag_migration.sql')
        
        if not os.path.exists(migration_path):
            print(f"错误: 迁移脚本不存在 - {migration_path}")
            return False
            
        with open(migration_path, 'r', encoding='utf-8') as f:
            migration_sql = f.read()
        
        # 按语句分割SQL文件
        sql_statements = migration_sql.split(';')
        
        # 执行每个SQL语句
        for statement in sql_statements:
            statement = statement.strip()
            if statement:  # 忽略空语句
                try:
                    cursor.execute(statement)
                    print(f"成功执行: {statement[:50]}...")
                except Error as e:
                    print(f"执行SQL语句时出错: {statement[:50]}...")
                    print(f"错误信息: {e}")
        
        # 提交更改
        conn.commit()
        print("标签迁移应用成功")
        return True
        
    except Error as e:
        print(f"连接数据库时出错: {e}")
        return False
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("数据库连接已关闭")

if __name__ == "__main__":
    success = apply_migration()
    sys.exit(0 if success else 1) 