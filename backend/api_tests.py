"""
集成API测试脚本

这个脚本提供了对后端API的端到端测试功能，专注于交互模块的API。
该脚本替换了以前分散的测试脚本（login_test.py, interaction_test.py, conversation_test.py等）。
"""

import requests
import json
import sys
import time
import os

# 基础URL
BASE_URL = "http://localhost:5000/api"

# 测试用户
TEST_USERS = {
    "user1": {
        "email": "lsm1248845597@163.com",
        "username": "Chris",
        "password": "Ok123456789"
    },
    "user2": {
        "email": "1248845597@163.com",
        "username": "Chris66",
        "password": "Ok123456789"
    }
}

# 存储token的文件
TOKEN_FILES = {
    "user1": "token_user1.txt",
    "user2": "token_user2.txt"
}

# Token存储
tokens = {}

def login_and_get_token(user_key):
    """登录并获取token"""
    print(f"\n登录用户 {user_key}...")
    
    response = requests.post(
        f"{BASE_URL}/user/login",
        json={
            "email": TEST_USERS[user_key]["email"],
            "password": TEST_USERS[user_key]["password"]
        }
    )
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        if "access_token" in data:
            token = data["access_token"]
            tokens[user_key] = token
            
            # 保存token到文件
            with open(TOKEN_FILES[user_key], "w") as f:
                f.write(token)
                
            print(f"获取到token: {token[:20]}...")
            return token
    
    print(f"登录失败: {response.text}")
    return None

def get_token(user_key):
    """获取用户token，如果文件存在则从文件读取，否则登录获取"""
    # 如果已经在内存中，直接返回
    if user_key in tokens:
        return tokens[user_key]
        
    # 尝试从文件读取
    try:
        if os.path.exists(TOKEN_FILES[user_key]):
            with open(TOKEN_FILES[user_key], "r") as f:
                token = f.read().strip()
                tokens[user_key] = token
                return token
    except:
        pass
        
    # 登录获取
    return login_and_get_token(user_key)

def get_user_id(user_key):
    """获取用户ID"""
    token = get_token(user_key)
    if not token:
        return None
        
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(
        f"{BASE_URL}/user/profile",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        return data.get("id")
    
    return None

def print_response(response, description=None):
    """格式化打印响应"""
    if description:
        print(f"\n>> {description}")
    
    print(f"状态码: {response.status_code}")
    try:
        data = response.json()
        print(f"响应内容: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except:
        print(f"响应内容: {response.text}")
    
    return response.status_code

# 测试函数
def test_comment_functionality():
    """测试评论功能"""
    print("\n===== 测试评论功能 =====")
    
    token = get_token("user1")
    if not token:
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 发表评论
    response = requests.post(
        f"{BASE_URL}/interaction/comment",
        headers=headers,
        json={
            "novel_id": 1,
            "content": "这是一条API测试评论"
        }
    )
    comment_result = print_response(response, "发表评论") == 201
    
    if comment_result and response.json().get("comment", {}).get("id"):
        comment_id = response.json()["comment"]["id"]
    else:
        comment_id = None
    
    # 获取小说评论
    response = requests.get(
        f"{BASE_URL}/interaction/comments/1"
    )
    comments_result = print_response(response, "获取小说评论") == 200
    
    # 删除评论（如果创建成功）
    if comment_id:
        response = requests.delete(
            f"{BASE_URL}/interaction/comment/{comment_id}",
            headers=headers
        )
        delete_result = print_response(response, "删除评论") == 200
    else:
        delete_result = False
        print("无法删除评论，因为未获取到评论ID")
    
    return comment_result and comments_result and delete_result

def test_collection_functionality():
    """测试收藏功能"""
    print("\n===== 测试收藏功能 =====")
    
    token = get_token("user1")
    if not token:
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 收藏小说
    response = requests.post(
        f"{BASE_URL}/interaction/collection",
        headers=headers,
        json={
            "novel_id": 1
        }
    )
    collect_result = print_response(response, "收藏/取消收藏小说") in [200, 201]
    
    # 获取收藏状态
    response = requests.get(
        f"{BASE_URL}/interaction/collection/status/1",
        headers=headers
    )
    status_result = print_response(response, "获取收藏状态") == 200
    
    # 获取收藏列表
    response = requests.get(
        f"{BASE_URL}/interaction/collection",
        headers=headers
    )
    list_result = print_response(response, "获取收藏列表") == 200
    
    return collect_result and status_result and list_result

def test_follow_functionality():
    """测试关注功能"""
    print("\n===== 测试关注功能 =====")
    
    token1 = get_token("user1")
    token2 = get_token("user2")
    if not token1 or not token2:
        return False
    
    user1_id = get_user_id("user1")
    user2_id = get_user_id("user2")
    if not user1_id or not user2_id:
        print("无法获取用户ID")
        return False
    
    headers1 = {
        "Authorization": f"Bearer {token1}",
        "Content-Type": "application/json"
    }
    
    headers2 = {
        "Authorization": f"Bearer {token2}",
        "Content-Type": "application/json"
    }
    
    # 用户1关注用户2
    response = requests.post(
        f"{BASE_URL}/interaction/follow",
        headers=headers1,
        json={
            "user_id": user2_id
        }
    )
    follow1_result = print_response(response, f"用户1关注用户2 (ID: {user2_id})") == 200
    
    # 用户2关注用户1
    response = requests.post(
        f"{BASE_URL}/interaction/follow",
        headers=headers2,
        json={
            "user_id": user1_id
        }
    )
    follow2_result = print_response(response, f"用户2关注用户1 (ID: {user1_id})") == 200
    
    # 获取关注状态
    response = requests.get(
        f"{BASE_URL}/interaction/follow/status/{user2_id}",
        headers=headers1
    )
    status_result = print_response(response, "获取关注状态") == 200
    
    # 获取粉丝列表
    response = requests.get(
        f"{BASE_URL}/interaction/followers/{user1_id}"
    )
    followers_result = print_response(response, f"获取用户1的粉丝列表") == 200
    
    # 获取关注列表
    response = requests.get(
        f"{BASE_URL}/interaction/following/{user1_id}"
    )
    following_result = print_response(response, f"获取用户1的关注列表") == 200
    
    return follow1_result and follow2_result and status_result and followers_result and following_result

def test_message_functionality():
    """测试私信功能"""
    print("\n===== 测试私信功能 =====")
    
    token1 = get_token("user1")
    token2 = get_token("user2")
    if not token1 or not token2:
        return False
    
    user1_id = get_user_id("user1")
    user2_id = get_user_id("user2")
    if not user1_id or not user2_id:
        print("无法获取用户ID")
        return False
    
    headers1 = {
        "Authorization": f"Bearer {token1}",
        "Content-Type": "application/json"
    }
    
    headers2 = {
        "Authorization": f"Bearer {token2}",
        "Content-Type": "application/json"
    }
    
    # 用户1发送私信给用户2
    response = requests.post(
        f"{BASE_URL}/interaction/message",
        headers=headers1,
        json={
            "recipient_id": user2_id,
            "content": "你好，这是用户1发送的测试私信！"
        }
    )
    send1_result = print_response(response, f"用户1发送私信给用户2") in [200, 201]
    
    # 用户2发送私信给用户1
    response = requests.post(
        f"{BASE_URL}/interaction/message",
        headers=headers2,
        json={
            "recipient_id": user1_id,
            "content": "你好，这是用户2的回复私信！"
        }
    )
    send2_result = print_response(response, f"用户2发送私信给用户1") in [200, 201]
    
    # 获取收件箱
    response = requests.get(
        f"{BASE_URL}/interaction/inbox",
        headers=headers1
    )
    inbox_result = print_response(response, "获取用户1的收件箱") == 200
    
    # 获取与特定用户的对话
    response = requests.get(
        f"{BASE_URL}/interaction/conversation/{user2_id}",
        headers=headers1
    )
    conversation_result = print_response(response, f"获取用户1与用户2的对话") == 200
    
    # 如果有消息，标记为已读
    if inbox_result and response.json().get("messages"):
        message_id = response.json()["messages"][0]["id"]
        response = requests.post(
            f"{BASE_URL}/interaction/message/{message_id}/read",
            headers=headers1
        )
        read_result = print_response(response, "标记消息为已读") == 200
    else:
        read_result = False
        print("无法标记消息为已读，因为未获取到消息ID")
    
    return send1_result and send2_result and inbox_result and conversation_result and read_result

def test_reading_history():
    """测试阅读历史功能"""
    print("\n===== 测试阅读历史功能 =====")
    
    token = get_token("user1")
    if not token:
        return False
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 获取阅读历史
    response = requests.get(
        f"{BASE_URL}/interaction/history",
        headers=headers
    )
    history_result = print_response(response, "获取阅读历史") == 200
    
    # 获取阅读进度
    response = requests.get(
        f"{BASE_URL}/interaction/progress/1",
        headers=headers
    )
    progress_result = print_response(response, "获取阅读进度") == 200
    
    return history_result and progress_result

def run_tests():
    """运行所有API测试"""
    results = {}
    
    try:
        results["评论功能"] = test_comment_functionality()
    except Exception as e:
        print(f"评论功能测试异常: {e}")
        results["评论功能"] = False
    
    try:
        results["收藏功能"] = test_collection_functionality()
    except Exception as e:
        print(f"收藏功能测试异常: {e}")
        results["收藏功能"] = False
    
    try:
        results["关注功能"] = test_follow_functionality()
    except Exception as e:
        print(f"关注功能测试异常: {e}")
        results["关注功能"] = False
    
    try:
        results["私信功能"] = test_message_functionality()
    except Exception as e:
        print(f"私信功能测试异常: {e}")
        results["私信功能"] = False
    
    try:
        results["阅读历史"] = test_reading_history()
    except Exception as e:
        print(f"阅读历史测试异常: {e}")
        results["阅读历史"] = False
    
    # 打印测试结果汇总
    print("\n\n======= API测试结果汇总 =======")
    for test_name, success in results.items():
        print(f"{test_name}: {'✅ 成功' if success else '❌ 失败'}")
    
    # 计算成功率
    success_count = sum(1 for result in results.values() if result)
    total_count = len(results)
    success_rate = (success_count / total_count) * 100 if total_count > 0 else 0
    
    print(f"\n总体成功率: {success_rate:.1f}% ({success_count}/{total_count})")
    
    return all(results.values())

if __name__ == "__main__":
    print("===== 运行后端API集成测试 =====")
    success = run_tests()
    sys.exit(0 if success else 1) 