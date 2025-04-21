#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
作者模块API测试脚本

根据 doc/API/作者模块API文档.md 进行全面测试
测试内容包括:
1. 作者申请
   - 提交作者申请
   - 获取作者申请历史
2. 管理员审核作者申请 (根据 doc/API/管理模块API文档.md)
3. 作者管理
   - 更新作者资料
   - 获取作者统计数据
4. 注销作者身份

测试使用 sign.txt 中的账户信息进行测试
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
    "username": "testuser",
    "password": "newpassword456",
    "id": 4
}

TEST_AUTHOR = {
    "username": "testauthor",
    "password": "password123",
    "id": 5,
    "author_id": 1
}

TEST_ADMIN = {
    "username": "newadmin",
    "password": "password123",
    "id": 6,
    "admin_id": 2
}

# 存储全局变量
USER_TOKEN = None
AUTHOR_TOKEN = None
ADMIN_TOKEN = None
APPLICATION_ID = None
PEN_NAME = f"笔名_{random.randint(1000, 9999)}"

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

def user_login():
    """测试用户登录"""
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

def author_login():
    """测试作者登录"""
    print_header("作者用户登录")
    
    url = f"{BASE_URL}/user/login"
    payload = {
        "username": TEST_AUTHOR["username"],
        "password": TEST_AUTHOR["password"]
    }
    
    print(f"登录作者: {TEST_AUTHOR['username']}")
    response = requests.post(url, json=payload)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            global AUTHOR_TOKEN
            AUTHOR_TOKEN = data.get("access_token")
            print_result(True, "作者用户登录成功")
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

def test_submit_author_application():
    """测试提交作者申请"""
    print_header("提交作者申请")
    
    url = f"{BASE_URL}/author/application"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}
    payload = {
        "pen_name": PEN_NAME,
        "bio": "这是一个测试作者简介，用于测试作者申请功能。",
        "reason": "我希望成为一名作者，这是测试申请理由。"
    }
    
    print(f"申请作者: {PEN_NAME}")
    response = requests.post(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 201:
        data = response.json()
        if "application" in data:
            global APPLICATION_ID
            APPLICATION_ID = data["application"]["id"]
            print_result(True, f"作者申请提交成功，申请ID: {APPLICATION_ID}")
            return True
        else:
            print_result(False, "申请提交成功但未返回申请ID")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_get_author_applications():
    """测试获取作者申请历史"""
    print_header("获取作者申请历史")
    
    url = f"{BASE_URL}/author/applications"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}
    
    print("获取作者申请历史...")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if "applications" in data and len(data["applications"]) > 0:
            found = False
            for app in data["applications"]:
                if app["id"] == APPLICATION_ID:
                    found = True
                    break
            
            if found:
                print_result(True, "成功获取作者申请历史，且包含刚才提交的申请")
                return True
            else:
                print_result(False, "成功获取作者申请历史，但不包含刚才提交的申请")
                return False
        else:
            print_result(False, "未找到任何作者申请历史")
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
        if "applications" in data and len(data["applications"]) > 0:
            found = False
            for app in data["applications"]:
                if app["id"] == APPLICATION_ID:
                    found = True
                    break
            
            if found:
                print_result(True, "管理员成功获取待处理作者申请，且包含刚才提交的申请")
                return True
            else:
                print_result(False, "管理员成功获取待处理作者申请，但不包含刚才提交的申请")
                return False
        else:
            print_result(False, "未找到任何待处理作者申请")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_admin_approve_author_application():
    """测试管理员审批作者申请"""
    print_header("管理员审批作者申请")
    
    url = f"{BASE_URL}/admin/author-applications/{APPLICATION_ID}"
    headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
    payload = {
        "action": "approve",
        "comment": "管理员批准测试申请"
    }
    
    print(f"管理员审批作者申请 ID: {APPLICATION_ID}...")
    response = requests.post(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if "application" in data and data["application"]["status"] == "approved":
            print_result(True, "管理员成功批准作者申请")
            return True
        else:
            print_result(False, "申请状态未变更为approved")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_update_author_profile():
    """测试更新作者资料"""
    print_header("更新作者资料")
    
    # 重新登录获取作者身份的token
    user_login()
    
    url = f"{BASE_URL}/author/profile"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}
    payload = {
        "pen_name": f"{PEN_NAME}_更新",
        "bio": "这是更新后的作者简介，用于测试作者资料更新功能。",
        "contact_email": f"author_{random.randint(1000, 9999)}@example.com"
    }
    
    print("更新作者资料...")
    response = requests.put(url, json=payload, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data.get("author", {}).get("pen_name") == f"{PEN_NAME}_更新":
            print_result(True, "作者资料更新成功")
            return True
        else:
            print_result(False, "作者资料更新失败或笔名未更新")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_get_author_stats():
    """测试获取作者统计数据"""
    print_header("获取作者统计数据")
    
    url = f"{BASE_URL}/novel/author/stats"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}
    
    print("获取作者统计数据...")
    response = requests.get(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if "novel_count" in data:
            print_result(True, "获取作者统计数据成功")
            return True
        else:
            print_result(False, "获取作者统计数据失败，返回数据格式不正确")
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def test_resign_author():
    """测试注销作者身份"""
    print_header("注销作者身份")
    
    url = f"{BASE_URL}/author/resign"
    headers = {"Authorization": f"Bearer {USER_TOKEN}"}
    
    print("注销作者身份...")
    response = requests.post(url, headers=headers)
    print_response(response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            print_result(True, "注销作者身份成功")
            return True
        else:
            print_result(False, data.get("error", "未知错误"))
            return False
    else:
        print_result(False, f"请求失败，状态码: {response.status_code}")
        return False

def run_all_tests():
    """运行所有测试"""
    
    print("📋 开始作者模块API测试")
    
    # 重定向输出到字符串
    original_stdout = sys.stdout
    captured_output = io.StringIO()
    sys.stdout = captured_output
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # 定义替代的打印函数，同时输出到控制台和字符串
        def tee_print(*args, **kwargs):
            temp_stdout = sys.stdout
            sys.stdout = original_stdout
            print(*args, **kwargs)
            sys.stdout = captured_output
            print(*args, **kwargs)
        
        # 替换打印函数
        global print_header, print_result, print_response
        original_print_header = print_header
        original_print_result = print_result
        original_print_response = print_response
        
        def new_print_header(title):
            tee_print("\n" + "=" * 80)
            tee_print(f"测试: {title}")
            tee_print("=" * 80)
        
        def new_print_result(status, message):
            if status:
                tee_print(f"✅ 成功: {message}")
            else:
                tee_print(f"❌ 失败: {message}")
        
        def new_print_response(response):
            tee_print(f"状态码: {response.status_code}")
            try:
                tee_print(f"响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
            except:
                tee_print(f"响应内容: {response.text}")
        
        print_header = new_print_header
        print_result = new_print_result
        print_response = new_print_response
        
        # 记录测试结果
        results = {}
        
        # 执行测试
        tee_print("测试笔名:", PEN_NAME)
        
        results["用户登录"] = user_login()
        results["提交作者申请"] = test_submit_author_application()
        results["获取作者申请历史"] = test_get_author_applications()
        results["管理员登录"] = admin_login()
        results["管理员获取待处理作者申请"] = test_admin_get_author_applications()
        results["管理员审批作者申请"] = test_admin_approve_author_application()
        results["更新作者资料"] = test_update_author_profile()
        results["获取作者统计数据"] = test_get_author_stats()
        results["注销作者身份"] = test_resign_author()
        
        # 生成测试摘要
        tee_print("\n" + "=" * 80)
        tee_print("测试结果摘要")
        tee_print("=" * 80)
        
        all_passed = True
        for test_name, result in results.items():
            status = "✅" if result else "❌"
            tee_print(f"{status} {test_name}")
            if not result:
                all_passed = False
        
        tee_print(f"\n总计: {sum(results.values())}/{len(results)} 测试通过")
        
        if all_passed:
            tee_print("\n🎉 所有测试通过!")
        else:
            tee_print("\n❗ 部分测试失败，请检查详细输出。")
        
        # 保存测试报告
        ensure_report_dir()
        report_path = os.path.join(REPORT_DIR, f"作者模块_api_test_report_{timestamp}.md")
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# 作者模块 API 测试报告\n\n")
            f.write(f"**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("**测试脚本**: test_author_api.py\n")
            f.write("**描述**: 包括作者申请、管理员审核、作者资料管理及注销功能测试\n\n")
            f.write("---\n\n")
            f.write(captured_output.getvalue())
        
        tee_print(f"\n\n测试报告已保存至: {report_path}")
        
    finally:
        # 恢复输出和打印函数
        sys.stdout = original_stdout
        if 'original_print_header' in locals():
            print_header = original_print_header
            print_result = original_print_result
            print_response = original_print_response

if __name__ == "__main__":
    run_all_tests() 