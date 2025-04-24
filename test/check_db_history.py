#!/usr/bin/env python3
import sys
import os
import mysql.connector
import datetime
from mysql.connector import Error

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'database': 'novel_db',
    'user': 'root',
    'password': 'ok123456'
}

def print_separator():
    print("\n" + "-" * 60 + "\n")

def connect_db():
    """连接到MySQL数据库"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print(f"成功连接到MySQL数据库: {DB_CONFIG['database']}")
        return conn
    except Error as e:
        print(f"数据库连接错误: {str(e)}")
        return None

def check_db_tables(conn):
    """检查数据库中的表结构"""
    print("检查数据库表结构...")
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        
        print(f"发现 {len(tables)} 个表:")
        for table in tables:
            table_name = list(table.values())[0]
            print(f" - {table_name}")
            
        # 特别检查 user_history 表
        cursor.execute("DESCRIBE user_history;")
        columns = cursor.fetchall()
        
        print("\n用户历史表 (user_history) 结构:")
        for col in columns:
            print(f" - {col['Field']} ({col['Type']})")
        
        cursor.close()
        return True
    except Error as e:
        print(f"检查表结构错误: {str(e)}")
        return False

def check_reading_history(conn):
    """检查阅读历史记录"""
    print("查询阅读历史记录...")
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                h.id, h.user_id, h.novel_id, h.chapter_id, h.last_read_time,
                u.username, n.title as novel_title, c.title as chapter_title
            FROM user_history h
            JOIN user u ON h.user_id = u.id
            JOIN novel n ON h.novel_id = n.id
            JOIN chapter c ON h.chapter_id = c.id
            ORDER BY h.last_read_time DESC
            LIMIT 20;
        """)
        
        records = cursor.fetchall()
        cursor.close()
        
        if not records:
            print("未找到阅读历史记录")
            return
        
        print(f"找到 {len(records)} 条最近的阅读历史记录:")
        for i, record in enumerate(records):
            print(f"\n记录 #{i+1}:")
            print(f"  ID: {record['id']}")
            print(f"  用户: {record['username']} (ID: {record['user_id']})")
            print(f"  小说: {record['novel_title']} (ID: {record['novel_id']})")
            print(f"  章节: {record['chapter_title']} (ID: {record['chapter_id']})")
            print(f"  最后阅读时间: {record['last_read_time']}")
    
    except Error as e:
        print(f"查询阅读历史错误: {str(e)}")

def check_users(conn):
    """检查用户表"""
    print("查询用户信息...")
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, username, email, status, created_at
            FROM user
            ORDER BY id
            LIMIT 10;
        """)
        
        users = cursor.fetchall()
        
        if not users:
            print("未找到用户记录")
            cursor.close()
            return
        
        print(f"找到 {len(users)} 个用户:")
        for user in users:
            print(f"  ID: {user['id']}, 用户名: {user['username']}, 邮箱: {user['email']}, 状态: {user['status']}")
            
        # 查询作者用户
        cursor.execute("""
            SELECT a.user_id, u.username, a.pen_name
            FROM author a
            JOIN user u ON a.user_id = u.id
            ORDER BY a.id
            LIMIT 10;
        """)
        
        authors = cursor.fetchall()
        cursor.close()
        
        if not authors:
            print("\n未找到作者记录")
        else:
            print(f"\n找到 {len(authors)} 个作者用户:")
            for author in authors:
                print(f"  用户ID: {author['user_id']}, 用户名: {author['username']}, 笔名: {author['pen_name']}")
    
    except Error as e:
        print(f"查询用户信息错误: {str(e)}")

def monitor_history_updates(conn, interval=5, duration=60):
    """监控阅读历史更新"""
    print(f"开始监控阅读历史更新 (每 {interval} 秒检查一次，总计 {duration} 秒)...")
    
    try:
        start_time = datetime.datetime.now()
        end_time = start_time + datetime.timedelta(seconds=duration)
        
        # 先获取初始记录数
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as count FROM user_history")
        initial_count = cursor.fetchone()['count']
        print(f"初始阅读历史记录数: {initial_count}")
        
        last_records = []
        cursor.execute("""
            SELECT h.id, h.user_id, h.novel_id, h.chapter_id, h.last_read_time
            FROM user_history h
            ORDER BY h.last_read_time DESC
            LIMIT 5;
        """)
        for row in cursor.fetchall():
            last_records.append((row['id'], row['user_id'], row['novel_id'], row['chapter_id'], row['last_read_time']))
        
        check_count = 0
        while datetime.datetime.now() < end_time:
            # 等待指定间隔
            import time
            time.sleep(interval)
            
            # 检查记录数变化
            cursor.execute("SELECT COUNT(*) as count FROM user_history")
            current_count = cursor.fetchone()['count']
            
            check_count += 1
            print(f"\n检查 #{check_count} ({datetime.datetime.now()}):")
            print(f"  当前阅读历史记录数: {current_count}")
            
            if current_count != initial_count:
                print(f"  记录数变化: {current_count - initial_count}")
            
            # 检查最新记录变化
            cursor.execute("""
                SELECT h.id, h.user_id, h.novel_id, h.chapter_id, h.last_read_time,
                       u.username, n.title as novel_title, c.title as chapter_title
                FROM user_history h
                JOIN user u ON h.user_id = u.id
                JOIN novel n ON h.novel_id = n.id
                JOIN chapter c ON h.chapter_id = c.id
                ORDER BY h.last_read_time DESC
                LIMIT 5;
            """)
            
            current_records = []
            current_ids = []
            for row in cursor.fetchall():
                current_records.append(row)
                current_ids.append((row['id'], row['user_id'], row['novel_id'], row['chapter_id'], row['last_read_time']))
            
            if not current_records:
                print("  未找到最近的阅读历史记录")
                continue
                
            # 检查新记录
            if current_ids != last_records:
                print("  检测到阅读历史变化:")
                for record in current_records:
                    record_tuple = (record['id'], record['user_id'], record['novel_id'], record['chapter_id'], record['last_read_time'])
                    if record_tuple not in last_records:
                        print(f"    新/更新记录: ID={record['id']}, 用户={record['username']}, 小说={record['novel_title']}, 章节={record['chapter_title']}, 时间={record['last_read_time']}")
                
                # 更新上次记录
                last_records = current_ids
            else:
                print("  未检测到阅读历史变化")
        
        cursor.close()
        print(f"\n监控结束，总计检查 {check_count} 次")
    
    except KeyboardInterrupt:
        print("\n监控被用户中断")
    except Error as e:
        print(f"\n监控出错: {str(e)}")

def run_checks():
    print_separator()
    print("MySQL数据库阅读历史检查工具")
    print_separator()
    print(f"数据库配置: {DB_CONFIG}")
    
    conn = connect_db()
    if not conn:
        return
        
    try:
        print_separator()
        check_db_tables(conn)
        
        print_separator()
        check_users(conn)
        
        print_separator()
        check_reading_history(conn)
        
        print_separator()
        answer = input("是否监控阅读历史更新? (y/n): ")
        if answer.lower() == 'y':
            monitor_history_updates(conn)
    finally:
        if conn:
            conn.close()
            print("数据库连接已关闭")
    
    print_separator()
    print("检查完成")
    
if __name__ == "__main__":
    run_checks() 