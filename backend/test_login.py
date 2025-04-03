#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_login(email=None, phone=None, password=None):
    """测试登录API"""
    login_url = f"{BASE_URL}/user/login"
    
    # 构建登录数据
    login_data = {"password": password}
    if email:
        login_data["email"] = email
    elif phone:
        login_data["phone"] = phone
    
    print(f"尝试登录: {json.dumps(login_data, ensure_ascii=False)}")
    
    # 发送登录请求
    response = requests.post(login_url, json=login_data)
    
    # 打印响应
    print(f"状态码: {response.status_code}")
    try:
        print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
    except:
        print(f"响应内容: {response.text}")
    
    return response

# 测试管理员账户 (用邮箱)
print("\n=== 测试管理员账户 (邮箱) ===")
test_login(email="admin2@example.com", password="Admin123456")

# 测试管理员账户 (可能有的用户名，尝试使用邮箱登录)
print("\n=== 测试管理员账户 (尝试用户名) ===")
test_login(email="admin", password="Admin123456")

# 测试普通用户账户
print("\n=== 测试普通用户账户 ===")
test_login(email="lsm1248845597@163.com", password="Ok123456789")

# 测试使用不存在的账户
print("\n=== 测试不存在的账户 ===")
test_login(email="nonexistent@example.com", password="password123")

# 测试密码错误
print("\n=== 测试密码错误 ===")
test_login(email="admin2@example.com", password="WrongPassword") 