#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
用户模块API测试脚本

根据 doc/API/用户模块API文档.md 进行全面测试
测试内容包括:
1. 用户注册
2. 用户登录
3. 获取个人信息
4. 修改个人信息
5. 修改密码
6. 用户注销

测试结束后会自动清理创建的测试账户
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
TEST_USERNAME = f"testuser_{random.randint(1000, 9999)}"
TEST_PASSWORD = "TestPassword123"
TEST_NEW_PASSWORD = "NewPassword123"
TEST_EMAIL = f"test_{random.randint(1000, 9999)}@example.com"
TEST_PHONE = f"1{random.randint(10000000, 99999999)}"  # 随机生成手机号

# 存储全局变量
USER_ID = None
ACCESS_TOKEN = None

# 定义报告输出目录
REPORT_DIR = "../doc/test_report"

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

def test_register():
    """测试用户注册"""
    print_header("用户注册")
    
    url = f"{BASE_URL}/user/register"
    payload = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
        "email": TEST_EMAIL,
        "phone": TEST_PHONE
    }
    
    print(f"注册用户: {TEST_USERNAME}, 邮箱: {TEST_EMAIL}, 手机: {TEST_PHONE}")
    response = requests.post(url, json=payload)
    print_response(response)
    
    if response.status_code == 201 or response.status_code == 200:
        data = response.json()
        if data.get("success"):
            global USER_ID
            USER_ID = data.get("user", {}).get("id")
            print_result(True, f"用户注册成功，用户ID: {USER_ID}")
            return True
        else:
            print_result(False, data.get("error", "未知错误"))
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_duplicate_register():
    """测试重复注册"""
    print_header("重复注册测试")
    
    url = f"{BASE_URL}/user/register"
    payload = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD,
        "email": TEST_EMAIL
    }
    
    print(f"尝试重复注册用户: {TEST_USERNAME}")
    response = requests.post(url, json=payload)
    print_response(response)
    
    # 应该返回错误，因为用户名已存在
    if response.status_code == 400:
        data = response.json()
        if "already exists" in data.get("error", "").lower() or "已存在" in data.get("error", ""):
            print_result(True, "重复注册测试通过，系统正确拒绝")
            return True
        else:
            print_result(False, "系统拒绝，但错误消息不符合预期")
            return False
    else:
        print_result(False, f"请求状态码错误: {response.status_code}，应当返回400")
        return False

def test_login():
    """测试用户登录"""
    print_header("用户登录")
    
    url = f"{BASE_URL}/user/login"
    payload = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    }
    
    print(f"登录用户: {TEST_USERNAME}")
    response = requests.post(url, json=payload)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            global ACCESS_TOKEN
            ACCESS_TOKEN = data.get("access_token")
            print_result(True, "登录成功")
            return True
        else:
            print_result(False, data.get("error", "未知错误"))
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_get_profile():
    """测试获取个人信息"""
    print_header("获取个人信息")
    
    url = f"{BASE_URL}/user/profile"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    print("获取个人信息...")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("username") == TEST_USERNAME:
            print_result(True, "获取个人信息成功")
            return True
        else:
            print_result(False, "获取的用户信息不符合预期")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_update_profile():
    """测试修改个人信息"""
    print_header("修改个人信息")
    
    url = f"{BASE_URL}/user/profile"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    
    # 随机生成新的头像URL
    new_avatar = f"avatar_{random.randint(1000, 9999)}.jpg"
    payload = {
        "avatar": new_avatar
    }
    
    print(f"修改头像为: {new_avatar}")
    response = requests.put(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            user_data = data.get("user", {})
            if user_data.get("avatar") == new_avatar:
                print_result(True, "修改个人信息成功")
                return True
            else:
                print_result(False, "修改后的信息不符合预期")
                return False
        else:
            print_result(False, data.get("error", "未知错误"))
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_change_password():
    """测试修改密码"""
    global ACCESS_TOKEN
    print_header("修改密码")
    
    url = f"{BASE_URL}/user/change-password"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    payload = {
        "current_password": TEST_PASSWORD,
        "new_password": TEST_NEW_PASSWORD
    }
    
    print("修改密码...")
    response = requests.post(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("message") and "success" in data.get("message").lower():
            print_result(True, "修改密码成功")
            
            # 测试使用新密码登录
            print("\n测试使用新密码登录...")
            login_url = f"{BASE_URL}/user/login"
            login_payload = {
                "username": TEST_USERNAME,
                "password": TEST_NEW_PASSWORD
            }
            login_response = requests.post(login_url, json=login_payload)
            print_response(login_response)
            
            if login_response.status_code == 200 and login_response.json().get("success"):
                ACCESS_TOKEN = login_response.json().get("access_token")
                print_result(True, "使用新密码登录成功")
                return True
            else:
                print_result(False, "使用新密码登录失败")
                return False
        else:
            print_result(False, data.get("error", "未知错误"))
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_deactivate_account():
    """测试注销账户"""
    print_header("注销账户")
    
    url = f"{BASE_URL}/user/deactivate"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    payload = {
        "password": TEST_NEW_PASSWORD  # 使用最新的密码
    }
    
    print("注销账户...")
    response = requests.post(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print_result(True, "注销账户成功")
            
            # 验证账户是否已被删除 - 尝试登录
            print("\n验证账户是否已被删除...")
            login_url = f"{BASE_URL}/user/login"
            login_payload = {
                "username": TEST_USERNAME,
                "password": TEST_NEW_PASSWORD
            }
            login_response = requests.post(login_url, json=login_payload)
            print_response(login_response)
            
            if login_response.status_code == 401 or (login_response.status_code == 200 and not login_response.json().get("success")):
                print_result(True, "验证成功，账户已被删除")
                return True
            else:
                print_result(False, "账户似乎没有被删除")
                return False
        else:
            print_result(False, data.get("error", "未知错误"))
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def cleanup():
    """清理测试数据，确保测试账户被删除"""
    print_header("清理测试数据")
    
    if not ACCESS_TOKEN:
        print("无需清理，未创建有效会话")
        return
    
    # 如果前面的注销测试失败，尝试再次注销
    url = f"{BASE_URL}/user/deactivate"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    payload = {
        "password": TEST_NEW_PASSWORD
    }
    
    print("尝试强制注销账户...")
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200 and response.json().get("success"):
        print_result(True, "清理成功")
    else:
        print("清理失败，可能需要手动删除测试账户")
        print(f"测试用户名: {TEST_USERNAME}")

def run_all_tests():
    """运行所有测试"""
    # 创建缓冲区以捕获输出
    output_buffer = io.StringIO()
    
    # 确保报告目录存在
    ensure_report_dir()
    
    # 生成报告文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_filename = f"用户模块_api_test_report_{timestamp}.md"
    report_path = os.path.join(REPORT_DIR, report_filename)
    
    try:
        # 定义同时向控制台和缓冲区打印的函数
        def tee_print(*args, **kwargs):
            print(*args, **kwargs)
            print(*args, **kwargs, file=output_buffer)
        
        tee_print("\n📋 开始用户模块API测试")
        tee_print(f"测试用户名: {TEST_USERNAME}")
        tee_print(f"测试邮箱: {TEST_EMAIL}")
        tee_print(f"测试手机号: {TEST_PHONE}")
        
        # 保存原始print函数
        original_print_header = print_header
        original_print_result = print_result
        original_print_response = print_response
        
        # 重定义打印函数以同时输出到缓冲区
        def new_print_header(title):
            original_print_header(title)
            output_buffer.write("\n" + "=" * 80 + "\n")
            output_buffer.write(f"测试: {title}\n")
            output_buffer.write("=" * 80 + "\n")
        
        def new_print_result(status, message):
            original_print_result(status, message)
            if status:
                output_buffer.write(f"✅ 成功: {message}\n")
            else:
                output_buffer.write(f"❌ 失败: {message}\n")
        
        def new_print_response(response):
            original_print_response(response)
            output_buffer.write(f"状态码: {response.status_code}\n")
            try:
                output_buffer.write(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}\n")
            except:
                output_buffer.write(f"响应内容: {response.text}\n")
        
        # 替换打印函数
        globals()['print_header'] = new_print_header
        globals()['print_result'] = new_print_result
        globals()['print_response'] = new_print_response
        
        # 运行测试
        tests = [
            ("用户注册", test_register),
            ("重复注册测试", test_duplicate_register),
            ("用户登录", test_login),
            ("获取个人信息", test_get_profile),
            ("修改个人信息", test_update_profile),
            ("修改密码", test_change_password),
            ("注销账户", test_deactivate_account)
        ]
        
        results = []
        for name, test_func in tests:
            success = test_func()
            results.append((name, success))
            
            # 如果关键测试失败，可能无法继续
            if name in ["用户注册", "用户登录"] and not success:
                tee_print(f"\n⚠️ {name}失败，无法继续测试")
                break
                
        # 显示测试结果摘要
        summary = "\n" + "=" * 80 + "\n"
        summary += "测试结果摘要\n"
        summary += "=" * 80 + "\n"
        
        success_count = sum(1 for _, success in results if success)
        total_count = len(results)
        
        for name, success in results:
            status = "✅" if success else "❌"
            summary += f"{status} {name}\n"
            
        summary += f"\n总计: {success_count}/{total_count} 测试通过\n"
        
        if success_count == total_count:
            summary += "\n🎉 所有测试通过!\n"
        else:
            summary += "\n⚠️ 部分测试失败，请检查详细输出\n"
        
        tee_print(summary)
        
        # 还原打印函数
        globals()['print_header'] = original_print_header
        globals()['print_result'] = original_print_result
        globals()['print_response'] = original_print_response
        
        # 写入报告文件
        with open(report_path, 'w', encoding='utf-8') as report_file:
            report_file.write("# 用户模块 API 测试报告\n\n")
            report_file.write(f"**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            report_file.write(f"**测试脚本**: test_user_api.py\n")
            report_file.write(f"**描述**: 包括用户注册、登录、个人信息管理及注销功能测试\n\n")
            report_file.write("---\n\n")
            report_file.write("```\n")
            report_file.write(output_buffer.getvalue())
            report_file.write("```\n")
        
        print(f"\n测试报告已保存至: {report_path}")
            
    except Exception as e:
        print(f"\n❌ 测试过程中出现异常: {str(e)}")
    finally:
        # 无论测试是否成功，都尝试清理
        cleanup()
        
    # 返回测试结果，用于系统退出码
    return success_count == total_count

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 