#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
后端服务状态检查脚本
用于在运行测试前验证后端服务是否正常运行，以及测试账户是否可用
"""

import requests
import sys
import time
import json
from urllib.parse import urljoin

# 配置参数
BASE_URL = "http://localhost:5000"
MAX_RETRIES = 3
RETRY_INTERVAL = 2  # 秒

# 测试账户
TEST_ACCOUNTS = [
    {"username": "testuser", "password": "password123", "role": "普通用户"},
    {"username": "testauthor", "password": "password123", "role": "作者"},
    {"username": "testadmin", "password": "password123", "role": "管理员"}
]

def check_service_health():
    """检查后端服务是否在运行"""
    print("正在检查后端服务状态...")
    
    try:
        # 尝试访问根路径
        response = requests.get(BASE_URL, timeout=5)
        
        # 验证服务是否响应
        if response.status_code < 500:  # 只要不是服务器错误，就认为服务在运行
            print(f"✅ 后端服务运行正常 (状态码: {response.status_code})")
            return True
        else:
            print(f"❌ 后端服务返回错误 (状态码: {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务，请确认服务已启动")
        return False
    except requests.exceptions.Timeout:
        print("❌ 连接后端服务超时，请检查服务状态")
        return False
    except Exception as e:
        print(f"❌ 检查服务状态时出错: {str(e)}")
        return False

def check_authentication():
    """测试账户认证"""
    print("\n正在测试账户认证...")
    
    login_url = urljoin(BASE_URL, "/api/user/login")
    success_count = 0
    
    for account in TEST_ACCOUNTS:
        account_str = f"{account['username']} ({account['role']})"
        print(f"\n正在测试账户: {account_str}")
        
        for retry in range(MAX_RETRIES):
            try:
                response = requests.post(
                    login_url, 
                    json={"username": account["username"], "password": account["password"]},
                    timeout=5
                )
                
                # 输出响应状态和内容以便调试
                print(f"  响应状态码: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if data.get("access_token"):
                            print(f"✅ {account_str} 登录成功，获取到有效token")
                            success_count += 1
                            break
                        else:
                            print(f"❌ {account_str} 登录返回200，但未获取到有效token")
                    except json.JSONDecodeError:
                        print(f"❌ {account_str} 登录返回200，但响应不是有效JSON")
                elif response.status_code == 404:
                    print(f"❌ {account_str} 登录路径不存在，API可能未实现或路径错误")
                    print(f"  响应内容: {response.text[:200]}")
                    break
                else:
                    print(f"❌ {account_str} 登录失败，状态码: {response.status_code}")
                    try:
                        print(f"  错误信息: {response.json().get('error', '未知错误')}")
                    except:
                        print(f"  响应内容: {response.text[:200]}")
                
                if retry < MAX_RETRIES - 1:
                    print(f"  尝试重试 ({retry+1}/{MAX_RETRIES})...")
                    time.sleep(RETRY_INTERVAL)
            except Exception as e:
                print(f"❌ {account_str} 测试出错: {str(e)}")
                if retry < MAX_RETRIES - 1:
                    print(f"  尝试重试 ({retry+1}/{MAX_RETRIES})...")
                    time.sleep(RETRY_INTERVAL)
    
    print(f"\n账户认证测试完成: {success_count}/{len(TEST_ACCOUNTS)} 成功")
    return success_count == len(TEST_ACCOUNTS)

def check_api_endpoints():
    """检查核心API端点是否可访问"""
    print("\n正在检查核心API端点...")
    
    # 核心API列表
    endpoints = [
        {"path": "/api/user/profile", "method": "GET", "auth_required": True, "name": "用户信息"},
        {"path": "/api/novel/list", "method": "GET", "auth_required": False, "name": "小说列表"},
        {"path": "/api/author/profile/testauthor", "method": "GET", "auth_required": False, "name": "作者信息"},
        {"path": "/api/search/novel", "method": "GET", "auth_required": False, "name": "小说搜索", "params": {"keyword": "测试"}},
        {"path": "/api/admin/dashboard", "method": "GET", "auth_required": True, "admin_only": True, "name": "管理仪表盘"}
    ]
    
    # 先获取token
    tokens = {}
    login_url = urljoin(BASE_URL, "/api/user/login")
    
    for account in TEST_ACCOUNTS:
        try:
            response = requests.post(
                login_url, 
                json={"username": account["username"], "password": account["password"]},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("access_token"):
                    tokens[account["role"]] = data["access_token"]
        except:
            pass
    
    if "普通用户" not in tokens:
        print("❌ 无法获取用户token，跳过需要认证的API检查")
        
    if "管理员" not in tokens:
        print("❌ 无法获取管理员token，跳过管理员API检查")
    
    success_count = 0
    
    for endpoint in endpoints:
        url = urljoin(BASE_URL, endpoint["path"])
        method = endpoint["method"]
        name = endpoint["name"]
        
        # 跳过无法测试的管理员API
        if endpoint.get("admin_only") and "管理员" not in tokens:
            print(f"⚠️ 跳过 {name} API (需要管理员权限)")
            continue
            
        # 跳过无法测试的需要认证的API
        if endpoint.get("auth_required") and "普通用户" not in tokens and "管理员" not in tokens:
            print(f"⚠️ 跳过 {name} API (需要认证)")
            continue
            
        print(f"\n检查 {name} API...")
        
        # 准备请求参数
        kwargs = {"timeout": 5}
        if endpoint.get("params"):
            kwargs["params"] = endpoint["params"]
            
        # 添加认证头
        headers = {}
        if endpoint.get("auth_required"):
            token_type = "管理员" if endpoint.get("admin_only") else "普通用户"
            if token_type in tokens:
                headers["Authorization"] = f"Bearer {tokens[token_type]}"
            
        if headers:
            kwargs["headers"] = headers
            
        try:
            # 根据请求方法发送请求
            if method == "GET":
                response = requests.get(url, **kwargs)
            elif method == "POST":
                response = requests.post(url, **kwargs)
            else:
                print(f"❌ 不支持的请求方法: {method}")
                continue
                
            # 验证响应
            if response.status_code in [200, 201, 202]:
                print(f"✅ {name} API 正常访问 (状态码: {response.status_code})")
                success_count += 1
            elif response.status_code == 404:
                print(f"❌ {name} API 路径不存在，可能未实现 (状态码: 404)")
                print(f"  URL: {url}")
            else:
                print(f"❌ {name} API 返回错误 (状态码: {response.status_code})")
                try:
                    error = response.json().get("error", "未知错误")
                    print(f"  错误信息: {error}")
                except:
                    print(f"  响应内容: {response.text[:200]}")
                    
        except Exception as e:
            print(f"❌ 检查 {name} API 时出错: {str(e)}")
    
    print(f"\nAPI端点检查完成: {success_count}/{len(endpoints)} 成功")
    return success_count > 0

def main():
    """主函数"""
    print("=" * 50)
    print("小说平台后端服务检查工具")
    print("=" * 50)
    print(f"后端URL: {BASE_URL}")
    print("-" * 50)
    
    # 检查服务健康状态
    service_ok = check_service_health()
    if not service_ok:
        print("\n⚠️ 后端服务状态异常，请检查服务是否已启动")
        print("如果服务未启动，请先启动服务后再运行测试")
        sys.exit(1)
    
    # 测试认证
    auth_ok = check_authentication()
    
    # 检查API端点
    api_ok = check_api_endpoints()
    
    # 总结结果
    print("\n" + "=" * 50)
    print("检查结果总结:")
    print("-" * 50)
    print(f"后端服务状态: {'✅ 正常' if service_ok else '❌ 异常'}")
    print(f"账户认证状态: {'✅ 正常' if auth_ok else '❌ 异常'}")
    print(f"API端点状态: {'✅ 部分可用' if api_ok else '❌ 大部分不可用'}")
    
    if not auth_ok or not api_ok:
        print("\n⚠️ 后端服务可能存在问题，测试可能会失败")
        print("建议先修复后端服务问题，再运行测试")
    else:
        print("\n✅ 后端服务状态良好，可以开始测试")
    
if __name__ == "__main__":
    main() 