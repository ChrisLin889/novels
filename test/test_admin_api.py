#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
管理模块API测试脚本

根据 doc/API/管理模块API文档.md 进行全面测试
测试内容包括:
1. 仪表盘统计
2. 用户管理
   - 获取用户列表
   - 更新用户角色
   - 管理用户状态
   - 获取用户操作历史
3. 敏感词管理
   - 获取敏感词列表
   - 添加敏感词
   - 删除敏感词
4. 内容管理
   - 获取待审核内容
   - 审核内容
5. 作者申请管理
   - 获取待处理作者申请
   - 处理作者申请(拒绝和批准)

测试使用 sign.txt 中的管理员账户进行测试
"""

import requests
import json
import time
import random
import string
import sys
import os
import io
from datetime import datetime

# 测试配置
BASE_URL = "http://localhost:5000/api"

# 定义报告输出目录
REPORT_DIR = "../doc/test_report"

# 测试账户信息
TEST_USER = {
    "username": f"testuser_{random.randint(1000, 9999)}",
    "password": "TestPassword123",
    "email": f"test_user_{random.randint(1000, 9999)}@example.com",
    "phone": f"1{random.randint(10000000, 99999999)}"  # 随机生成手机号
}

TEST_AUTHOR_USER = {
    "username": f"testauthor_{random.randint(1000, 9999)}",
    "password": "AuthorPassword123",
    "email": f"test_author_{random.randint(1000, 9999)}@example.com",
    "phone": f"1{random.randint(10000000, 99999999)}"  # 随机生成手机号
}

TEST_ADMIN = {
    "username": "newadmin",
    "password": "password123",
    "id": 6,
    "admin_id": 2
}

# 存储全局变量
USER_TOKEN = None
USER_ID = None
AUTHOR_USER_TOKEN = None
AUTHOR_USER_ID = None
ADMIN_TOKEN = None
AUTHOR_APP_ID = None
SECOND_AUTHOR_APP_ID = None
TEST_SENSITIVE_WORD_ID = None

def ensure_report_dir():
    """确保报告目录存在"""
    os.makedirs(REPORT_DIR, exist_ok=True)

def print_header(title):
    """打印带有格式的标题"""
    print("\n" + "=" * 80)
    print(f"测试: {title}")
    print("=" * 80)

def print_result(status, message):
    """打印测试结果"""
    if status:
        print(f"✅ 成功: {message}")
    else:
        print(f"❌ 失败: {message}")
        
def print_response(response):
    """打印请求响应"""
    print(f"状态码: {response.status_code}")
    try:
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except:
        print(f"响应内容: {response.text}")

def test_register_user():
    """测试注册普通用户"""
    print_header("注册普通用户")
    
    url = f"{BASE_URL}/user/register"
    payload = {
        "username": TEST_USER["username"],
        "password": TEST_USER["password"],
        "email": TEST_USER["email"],
        "phone": TEST_USER["phone"]
    }
    
    print(f"注册用户: {TEST_USER['username']}, 邮箱: {TEST_USER['email']}, 手机: {TEST_USER['phone']}")
    response = requests.post(url, json=payload)
    print_response(response)
    
    if response.status_code == 201 or response.status_code == 200:
        data = response.json()
        if data.get("success"):
            global USER_ID
            USER_ID = data.get("user", {}).get("id")
            TEST_USER["id"] = USER_ID
            print_result(True, f"用户注册成功，用户ID: {USER_ID}")
            return True
        else:
            print_result(False, data.get("error", "未知错误"))
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_register_author_user():
    """测试注册将成为作者的用户"""
    print_header("注册将成为作者的用户")
    
    url = f"{BASE_URL}/user/register"
    payload = {
        "username": TEST_AUTHOR_USER["username"],
        "password": TEST_AUTHOR_USER["password"],
        "email": TEST_AUTHOR_USER["email"],
        "phone": TEST_AUTHOR_USER["phone"]
    }
    
    print(f"注册用户: {TEST_AUTHOR_USER['username']}, 邮箱: {TEST_AUTHOR_USER['email']}, 手机: {TEST_AUTHOR_USER['phone']}")
    response = requests.post(url, json=payload)
    print_response(response)
    
    if response.status_code == 201 or response.status_code == 200:
        data = response.json()
        if data.get("success"):
            global AUTHOR_USER_ID
            AUTHOR_USER_ID = data.get("user", {}).get("id")
            TEST_AUTHOR_USER["id"] = AUTHOR_USER_ID
            print_result(True, f"用户注册成功，用户ID: {AUTHOR_USER_ID}")
            return True
        else:
            print_result(False, data.get("error", "未知错误"))
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_user_login():
    """测试普通用户登录"""
    print_header("普通用户登录")
    
    url = f"{BASE_URL}/user/login"
    payload = {
        "username": TEST_USER["username"],
        "password": TEST_USER["password"]
    }
    
    print(f"登录用户: {TEST_USER['username']}")
    response = requests.post(url, json=payload)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            global USER_TOKEN
            USER_TOKEN = data.get("access_token")
            print_result(True, "普通用户登录成功")
            return True
        else:
            print_result(False, data.get("error", "未知错误"))
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_author_user_login():
    """测试将成为作者的用户登录"""
    print_header("将成为作者的用户登录")
    
    url = f"{BASE_URL}/user/login"
    payload = {
        "username": TEST_AUTHOR_USER["username"],
        "password": TEST_AUTHOR_USER["password"]
    }
    
    print(f"登录用户: {TEST_AUTHOR_USER['username']}")
    response = requests.post(url, json=payload)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            global AUTHOR_USER_TOKEN
            AUTHOR_USER_TOKEN = data.get("access_token")
            print_result(True, "用户登录成功")
            return True
        else:
            print_result(False, data.get("error", "未知错误"))
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def admin_login():
    """测试管理员登录"""
    print_header("管理员登录")
    
    url = f"{BASE_URL}/user/login"
    payload = {
        "username": TEST_ADMIN["username"],
        "password": TEST_ADMIN["password"]
    }
    
    print(f"登录管理员: {TEST_ADMIN['username']}")
    response = requests.post(url, json=payload)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            global ADMIN_TOKEN
            ADMIN_TOKEN = data.get("access_token")
            print_result(True, "管理员登录成功")
            return True
        else:
            print_result(False, data.get("error", "未知错误"))
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_dashboard():
    """测试获取管理员仪表盘数据"""
    print_header("获取管理员仪表盘数据")
    
    url = f"{BASE_URL}/admin/dashboard"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    
    print("获取仪表盘数据...")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if ("user_stats" in data and 
            "content_stats" in data and 
            "activity_stats" in data):
            print_result(True, "成功获取仪表盘数据")
            return True
        else:
            print_result(False, "返回数据结构不完整")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_get_user_list():
    """测试获取用户列表"""
    print_header("获取用户列表")
    
    url = f"{BASE_URL}/admin/users?page=1&per_page=20"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    
    print("获取用户列表...")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if "users" in data and isinstance(data["users"], list):
            found_new_user = False
            for user in data["users"]:
                if user.get("id") == USER_ID:
                    found_new_user = True
                    break
            
            if found_new_user:
                print_result(True, "成功获取用户列表，且包含新注册的用户")
            else:
                print_result(True, "成功获取用户列表，但未找到新注册的用户")
            return True
        else:
            print_result(False, "返回数据结构不符合预期")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_submit_first_author_application():
    """测试提交第一次作者申请（将被拒绝）"""
    print_header("提交第一次作者申请")
    
    url = f"{BASE_URL}/author/application"
    headers = {"Authorization": f"Bearer {AUTHOR_USER_TOKEN}"}
    payload = {
        "pen_name": f"笔名_{random.randint(1000, 9999)}",
        "bio": "这是一个测试作者简介，用于测试作者申请功能。",
        "reason": "这是第一次申请，将被拒绝。"
    }
    
    print(f"申请作者: {payload['pen_name']}")
    response = requests.post(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 201:
        data = response.json()
        if "application" in data:
            global AUTHOR_APP_ID
            AUTHOR_APP_ID = data["application"]["id"]
            print_result(True, f"作者申请提交成功，申请ID: {AUTHOR_APP_ID}")
            return True
        else:
            print_result(False, "申请提交成功但未返回申请ID")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_admin_get_author_applications():
    """测试管理员获取待处理作者申请"""
    print_header("管理员获取待处理作者申请")
    
    url = f"{BASE_URL}/admin/author-applications"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    
    print("管理员获取待处理作者申请...")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        application_found = False
        
        if "applications" in data and len(data["applications"]) > 0:
            for app in data["applications"]:
                if app["id"] == AUTHOR_APP_ID:
                    application_found = True
                    break
            
            if application_found:
                print_result(True, "成功获取作者申请列表，且包含新提交的申请")
                return True
            else:
                print_result(False, "成功获取作者申请列表，但未找到新提交的申请")
                return False
        else:
            print_result(False, "未找到任何待处理作者申请")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_admin_reject_author_application():
    """测试管理员拒绝作者申请"""
    print_header("管理员拒绝作者申请")
    
    url = f"{BASE_URL}/admin/author-applications/{AUTHOR_APP_ID}"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    payload = {
        "action": "reject",
        "comment": "测试拒绝作者申请，请完善申请资料后再次提交"
    }
    
    print(f"拒绝作者申请 ID: {AUTHOR_APP_ID}")
    response = requests.post(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("message") and "拒绝" in data.get("message"):
            print_result(True, "成功拒绝作者申请")
            return True
        else:
            print_result(False, "响应成功但消息不符合预期")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_submit_second_author_application():
    """测试提交第二次作者申请（将被批准）"""
    print_header("提交第二次作者申请")
    
    url = f"{BASE_URL}/author/application"
    headers = {"Authorization": f"Bearer {AUTHOR_USER_TOKEN}"}
    payload = {
        "pen_name": f"优秀笔名_{random.randint(1000, 9999)}",
        "bio": "这是一个更详细的作者简介，包含我的写作经历和风格特点。",
        "reason": "这是第二次申请，已根据管理员意见完善了申请资料。"
    }
    
    print(f"再次申请作者: {payload['pen_name']}")
    response = requests.post(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 201:
        data = response.json()
        if "application" in data:
            global SECOND_AUTHOR_APP_ID
            SECOND_AUTHOR_APP_ID = data["application"]["id"]
            print_result(True, f"第二次作者申请提交成功，申请ID: {SECOND_AUTHOR_APP_ID}")
            return True
        else:
            print_result(False, "申请提交成功但未返回申请ID")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_admin_approve_author_application():
    """测试管理员批准作者申请"""
    print_header("管理员批准作者申请")
    
    url = f"{BASE_URL}/admin/author-applications/{SECOND_AUTHOR_APP_ID}"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    payload = {
        "action": "approve",
        "comment": "申请资料完整，批准成为作者"
    }
    
    print(f"批准作者申请 ID: {SECOND_AUTHOR_APP_ID}")
    response = requests.post(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("message") and "批准" in data.get("message"):
            print_result(True, "成功批准作者申请")
            return True
        else:
            print_result(False, "响应成功但消息不符合预期")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_update_user_role():
    """测试更新用户角色"""
    print_header("更新用户角色")
    
    url = f"{BASE_URL}/admin/users/{USER_ID}/role"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    payload = {
        "role": "author"
    }
    
    print(f"将用户 {USER_ID} 角色更新为作者")
    response = requests.put(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data["user"]["role"] == "author":
            print_result(True, "成功更新用户角色为作者")
            return True
        else:
            print_result(False, "响应成功但角色更新可能未成功")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_manage_user_status():
    """测试管理用户状态（禁用与解禁）"""
    print_header("管理用户状态")
    
    # 首先禁用用户
    ban_url = f"{BASE_URL}/admin/users/{USER_ID}"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    ban_payload = {
        "action": "ban",
        "reason": "测试禁用功能",
        "duration": 1  # 禁用1天
    }
    
    print(f"禁用用户 {USER_ID}，时长1天")
    ban_response = requests.post(ban_url, json=ban_payload, headers=headers)
    print_response(ban_response)
    
    ban_success = False
    if ban_response.status_code == 200:
        data = ban_response.json()
        if data.get("success") and "banned" in data.get("message", ""):
            ban_success = True
            print_result(True, "成功禁用用户")
        else:
            print_result(False, "响应成功但禁用可能未成功")
    else:
        print_result(False, f"禁用请求失败，状态码: {ban_response.status_code}")
    
    time.sleep(1)  # 短暂延迟
    
    # 然后解禁用户
    unban_url = f"{BASE_URL}/admin/users/{USER_ID}"
    unban_payload = {
        "action": "unban",
        "reason": "测试解禁功能"
    }
    
    print(f"解禁用户 {USER_ID}")
    unban_response = requests.post(unban_url, json=unban_payload, headers=headers)
    print_response(unban_response)
    
    if unban_response.status_code == 200:
        data = unban_response.json()
        if data.get("success") and "unbanned" in data.get("message", ""):
            print_result(True, "成功解禁用户")
            return ban_success and True
        else:
            print_result(False, "响应成功但解禁可能未成功")
            return False
    else:
        print_result(False, f"解禁请求失败，状态码: {unban_response.status_code}")
        return False

def test_get_user_actions():
    """测试获取用户操作历史"""
    print_header("获取用户操作历史")
    
    url = f"{BASE_URL}/admin/user-actions?user_id={USER_ID}"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    
    print(f"获取用户 {USER_ID} 的操作历史")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if "actions" in data and isinstance(data["actions"], list):
            found_ban_action = False
            for action in data["actions"]:
                if action.get("target_user_id") == USER_ID and action.get("action_type") == "ban":
                    found_ban_action = True
                    break
            
            if found_ban_action:
                print_result(True, "成功获取用户操作历史，且包含禁用操作记录")
            else:
                print_result(False, "成功获取用户操作历史，但未找到禁用操作记录")
            return True
        else:
            print_result(False, "返回数据结构不符合预期")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_get_sensitive_words():
    """测试获取敏感词列表"""
    print_header("获取敏感词列表")
    
    url = f"{BASE_URL}/admin/sensitive-words"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    
    print("获取敏感词列表...")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if "words" in data and isinstance(data["words"], list):
            print_result(True, f"成功获取敏感词列表，共 {len(data['words'])} 条")
            return True
        else:
            print_result(False, "返回数据结构不符合预期")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_add_sensitive_word():
    """测试添加敏感词"""
    print_header("添加敏感词")
    
    # 生成随机敏感词，避免冲突
    test_word = f"test_sensitive_{random.randint(1000, 9999)}"
    
    url = f"{BASE_URL}/admin/sensitive-words"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    payload = {
        "action": "add",
        "word": test_word,
        "level": 2,
        "category": "profanity"
    }
    
    print(f"添加敏感词: {test_word}")
    response = requests.post(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data.get("word", {}).get("word") == test_word:
            global TEST_SENSITIVE_WORD_ID
            TEST_SENSITIVE_WORD_ID = data["word"]["id"]
            print_result(True, f"成功添加敏感词，ID: {TEST_SENSITIVE_WORD_ID}")
            return True
        else:
            print_result(False, "响应成功但添加可能未成功")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_delete_sensitive_word():
    """测试删除敏感词"""
    print_header("删除敏感词")
    
    url = f"{BASE_URL}/admin/sensitive-words"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    payload = {
        "action": "delete",
        "word_id": TEST_SENSITIVE_WORD_ID
    }
    
    print(f"删除敏感词 ID: {TEST_SENSITIVE_WORD_ID}")
    response = requests.post(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and "deleted" in data.get("message", ""):
            print_result(True, "成功删除敏感词")
            return True
        else:
            print_result(False, "响应成功但删除可能未成功")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_get_pending_content():
    """测试获取待审核内容"""
    print_header("获取待审核内容")
    
    # 测试三种内容类型
    content_types = ["novel", "chapter", "comment"]
    overall_result = True
    
    for content_type in content_types:
        url = f"{BASE_URL}/admin/content/{content_type}"
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        
        print(f"获取待审核的 {content_type} 内容...")
        response = requests.get(url, headers=headers)
        print_response(response)
        
        if response.status_code == 200:
            data = response.json()
            if "content" in data and "content_type" in data and data["content_type"] == content_type:
                print_result(True, f"成功获取待审核的 {content_type} 内容列表")
            else:
                print_result(False, f"获取 {content_type} 内容返回数据结构不符合预期")
                overall_result = False
        else:
            if response.status_code == 404 or response.status_code == 204:
                print_result(True, f"目前没有待审核的 {content_type} 内容")
            else:
                print_result(False, f"获取 {content_type} 内容请求失败，状态码: {response.status_code}")
                overall_result = False
    
    return overall_result

def test_resign_author():
    """测试将成为作者的用户注销作者身份"""
    print_header("注销作者身份")
    
    url = f"{BASE_URL}/author/resign"
    headers = {"Authorization": f"Bearer {AUTHOR_USER_TOKEN}"}
    payload = {
        "reason": "测试注销作者身份功能",
        "confirm": True
    }
    
    print("注销作者身份...")
    response = requests.post(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print_result(True, "成功注销作者身份")
            return True
        else:
            print_result(False, data.get("error", "未知错误"))
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_deactivate_author_account():
    """测试注销作者用户账户"""
    print_header("注销作者用户账户")
    
    url = f"{BASE_URL}/user/deactivate"
    headers = {"Authorization": f"Bearer {AUTHOR_USER_TOKEN}"}
    payload = {
        "password": TEST_AUTHOR_USER["password"],
        "reason": "测试账户注销功能",
        "confirm": True
    }
    
    print("注销作者用户账户...")
    response = requests.post(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print_result(True, "成功注销作者用户账户")
            return True
        else:
            print_result(False, data.get("error", "未知错误"))
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_deactivate_user_account():
    """测试注销普通用户账户"""
    print_header("注销普通用户账户")
    
    url = f"{BASE_URL}/user/deactivate"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}
    payload = {
        "password": TEST_USER["password"],
        "reason": "测试账户注销功能",
        "confirm": True
    }
    
    print("注销普通用户账户...")
    response = requests.post(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print_result(True, "成功注销普通用户账户")
            return True
        else:
            print_result(False, data.get("error", "未知错误"))
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def run_all_tests():
    """运行所有测试"""
    tests = [
        ("注册普通用户", test_register_user),
        ("普通用户登录", test_user_login),
        ("注册未来作者用户", test_register_author_user),
        ("未来作者用户登录", test_author_user_login),
        ("管理员登录", admin_login),
        ("获取管理员仪表盘数据", test_dashboard),
        ("获取用户列表", test_get_user_list),
        ("提交第一次作者申请", test_submit_first_author_application),
        ("管理员获取待处理作者申请", test_admin_get_author_applications),
        ("管理员拒绝作者申请", test_admin_reject_author_application),
        ("提交第二次作者申请", test_submit_second_author_application),
        ("管理员批准作者申请", test_admin_approve_author_application),
        ("更新用户角色", test_update_user_role),
        ("管理用户状态", test_manage_user_status),
        ("获取用户操作历史", test_get_user_actions),
        ("获取敏感词列表", test_get_sensitive_words),
        ("添加敏感词", test_add_sensitive_word),
        ("删除敏感词", test_delete_sensitive_word),
        ("获取待审核内容", test_get_pending_content),
        ("注销作者身份", test_resign_author),
        ("注销作者用户账户", test_deactivate_author_account),
        ("注销普通用户账户", test_deactivate_user_account),
    ]
    
    # 准备报告
    ensure_report_dir()
    report_filename = f"admin_api_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_path = os.path.join(REPORT_DIR, report_filename)
    
    # 备份原始打印函数
    original_print = print
    
    try:
        # 创建同时输出到控制台和文件的打印函数
        report_file = open(report_path, 'w', encoding='utf-8')
        
        def tee_print(*args, **kwargs):
            # 输出到控制台
            original_print(*args, **kwargs)
            # 输出到文件
            kwargs_copy = kwargs.copy()
            kwargs_copy.pop('flush', None)  # 移除文件不支持的参数
            kwargs_copy.pop('file', None)   # 移除file参数，防止重复
            original_print(*args, file=report_file, **kwargs_copy)
        
        # 替换全局打印函数
        globals()['print'] = tee_print
        
        # 写入报告头部
        print(f"# 管理模块 API 测试报告\n")
        print(f"**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        print(f"**测试脚本**: test_admin_api.py\n")
        print("## 测试结果汇总\n")
        
        # 运行测试并记录结果
        success_count = 0
        for test_name, test_func in tests:
            try:
                if test_func():
                    success_count += 1
            except Exception as e:
                print(f"❌ 测试执行出错: {str(e)}")
        
        # 打印汇总信息
        print("\n## 汇总信息\n")
        print(f"- 总测试数: {len(tests)}")
        print(f"- 成功测试数: {success_count}")
        print(f"- 测试通过率: {success_count / len(tests) * 100:.2f}%")
        
        report_file.close()
        original_print(f"\n测试报告已保存至: {report_path}")
        
        return success_count == len(tests)
    
    except Exception as e:
        original_print(f"测试过程中发生错误: {str(e)}")
        return False
    
    finally:
        # 恢复原始打印函数
        globals()['print'] = original_print

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 