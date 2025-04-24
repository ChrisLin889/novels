#!/usr/bin/env python3
import requests
import json
import sys
import time

# 设置API基础URL
BASE_URL = "http://localhost:5000/api"  # 根据实际环境修改

# 测试用户信息 - 使用普通用户和作者用户来测试
TEST_USERS = [
    {"email": "user@example.com", "password": "password123", "type": "普通用户"},
    {"email": "author@test.com", "password": "password123", "type": "作者用户"}
]

def print_separator():
    print("\n" + "-" * 50 + "\n")

def login_user(user_info):
    """登录用户并返回token和用户信息"""
    print(f"尝试登录 {user_info['type']} ({user_info['email']})...")
    
    url = f"{BASE_URL}/user/login"
    data = {
        "email": user_info["email"],
        "password": user_info["password"]
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        
        result = response.json()
        if "access_token" in result and "user" in result:
            print(f"登录成功! 用户ID: {result['user']['id']}, 角色: {result['user']['role']}")
            return {
                "token": result["access_token"],
                "user_id": result["user"]["id"],
                "username": result["user"]["username"],
                "role": result["user"]["role"]
            }
        else:
            print(f"登录失败: 响应格式错误 {result}")
            return None
    except Exception as e:
        print(f"登录请求异常: {str(e)}")
        return None

def get_novel_list(token):
    """获取小说列表"""
    print("获取小说列表...")
    
    url = f"{BASE_URL}/novel/list"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        if "novels" in result and len(result["novels"]) > 0:
            print(f"获取到 {len(result['novels'])} 本小说")
            return result["novels"]
        else:
            print("没有获取到小说列表")
            return []
    except Exception as e:
        print(f"获取小说列表异常: {str(e)}")
        return []

def get_novel_chapters(token, novel_id):
    """获取小说章节列表"""
    print(f"获取小说 ID: {novel_id} 的章节列表...")
    
    url = f"{BASE_URL}/novel/{novel_id}/chapters"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        if "chapters" in result and len(result["chapters"]) > 0:
            print(f"获取到 {len(result['chapters'])} 个章节")
            return result["chapters"]
        else:
            print("没有获取到章节")
            return []
    except Exception as e:
        print(f"获取章节列表异常: {str(e)}")
        return []

def read_chapter(token, chapter_id):
    """阅读章节内容"""
    print(f"阅读章节 ID: {chapter_id}...")
    
    url = f"{BASE_URL}/novel/chapters/{chapter_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        if "chapter" in result:
            print(f"成功获取章节内容: {result['chapter']['title']}")
            return result["chapter"]
        else:
            print("获取章节内容失败")
            return None
    except Exception as e:
        print(f"阅读章节异常: {str(e)}")
        return None

def check_reading_history(token, user_id):
    """检查用户阅读历史"""
    print(f"检查用户 ID: {user_id} 的阅读历史...")
    
    url = f"{BASE_URL}/interaction/history"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        print(f"阅读历史响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if "history" in result:
            if len(result["history"]) > 0:
                print(f"成功获取到 {len(result['history'])} 条阅读历史记录")
                return result["history"]
            else:
                print("阅读历史为空")
                return []
        else:
            print("获取阅读历史失败")
            return None
    except Exception as e:
        print(f"检查阅读历史异常: {str(e)}")
        return None

def inspect_request_headers(token, url):
    """检查请求头中的token"""
    print(f"检查请求头 (URL: {url})...")
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # 使用options请求只检查头部
        response = requests.options(url, headers=headers)
        print(f"请求头: {headers}")
        print(f"状态码: {response.status_code}")
        return True
    except Exception as e:
        print(f"检查请求头异常: {str(e)}")
        return False

def run_test():
    print_separator()
    print("开始测试阅读历史功能")
    print_separator()
    
    for user_info in TEST_USERS:
        # 登录用户
        print_separator()
        user_data = login_user(user_info)
        if not user_data:
            continue
        
        token = user_data["token"]
        user_id = user_data["user_id"]
        
        # 检查目标URL的请求头
        print_separator()
        test_url = f"{BASE_URL}/novel/chapters/1"  # 测试请求头
        inspect_request_headers(token, test_url)
        
        # 获取小说列表
        print_separator()
        novels = get_novel_list(token)
        if not novels:
            continue
        
        # 选择第一本小说
        novel = novels[0]
        novel_id = novel["id"]
        print(f"选择小说: {novel['title']} (ID: {novel_id})")
        
        # 获取章节列表
        print_separator()
        chapters = get_novel_chapters(token, novel_id)
        if not chapters:
            continue
        
        # 阅读第一章
        first_chapter = chapters[0]
        chapter_id = first_chapter["id"]
        
        # 先检查阅读历史
        print_separator()
        print("阅读前检查历史记录:")
        before_history = check_reading_history(token, user_id)
        
        # 阅读章节
        print_separator()
        chapter = read_chapter(token, chapter_id)
        if not chapter:
            continue
            
        # 等待一会儿确保后端处理完成
        print("等待2秒确保后端处理完成...")
        time.sleep(2)
        
        # 再次检查阅读历史
        print_separator()
        print("阅读后检查历史记录:")
        after_history = check_reading_history(token, user_id)
        
        # 分析结果
        print_separator()
        print("分析结果:")
        if not before_history and not after_history:
            print("错误: 阅读前后都无法获取阅读历史")
        elif not before_history and after_history:
            print("成功: 阅读后创建了历史记录")
        elif before_history and after_history:
            if len(after_history) > len(before_history):
                print("成功: 阅读后添加了新的历史记录")
            elif len(after_history) == len(before_history):
                # 检查是否为同一本小说
                updated = False
                for record in after_history:
                    if record["novel"]["id"] == novel_id:
                        print(f"成功: 更新了小说 {novel['title']} 的阅读历史")
                        updated = True
                        break
                
                if not updated:
                    print("错误: 阅读历史未更新")
            else:
                print("错误: 阅读后历史记录数量减少")
        else:
            print("错误: 阅读前有历史记录，阅读后无法获取")
        
        print_separator()

if __name__ == "__main__":
    run_test() 