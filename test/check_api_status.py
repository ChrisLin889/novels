#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API状态检查工具

该脚本用于检查小说平台的后端API服务状态，确保所有关键接口正常运行。
"""

import sys
import requests
import json
import time
from datetime import datetime

# 配置项
BASE_URL = "http://localhost:5000"
TIMEOUT = 5  # 秒
API_ENDPOINTS = [
    {"path": "/api/health", "method": "GET", "name": "健康检查"},
    {"path": "/api/novels", "method": "GET", "name": "小说列表接口"},
    {"path": "/api/categories", "method": "GET", "name": "分类列表接口"},
    {"path": "/api/authors", "method": "GET", "name": "作者列表接口"},
    {"path": "/api/users/status", "method": "GET", "name": "用户系统状态"}
]

class TerminalColors:
    """终端颜色定义"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def check_api_health():
    """检查API服务器是否在线"""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=TIMEOUT)
        if response.status_code == 200:
            return True
        return False
    except requests.exceptions.RequestException:
        return False

def test_endpoint(endpoint):
    """
    测试单个API端点
    
    参数:
        endpoint (dict): 包含路径、方法和名称的端点信息
    
    返回:
        dict: 测试结果
    """
    url = f"{BASE_URL}{endpoint['path']}"
    method = endpoint['method'].lower()
    start_time = time.time()
    
    try:
        if method == 'get':
            response = requests.get(url, timeout=TIMEOUT)
        elif method == 'post':
            response = requests.post(url, timeout=TIMEOUT)
        else:
            return {
                "endpoint": endpoint,
                "status": "错误",
                "message": f"不支持的HTTP方法: {method}",
                "response_time": 0,
                "status_code": 0
            }
        
        response_time = time.time() - start_time
        
        # 分析响应
        if response.status_code >= 200 and response.status_code < 300:
            status = "正常"
            message = "接口响应正常"
        elif response.status_code >= 400 and response.status_code < 500:
            status = "客户端错误"
            message = f"客户端错误: {response.status_code}"
        elif response.status_code >= 500:
            status = "服务器错误"
            message = f"服务器错误: {response.status_code}"
        else:
            status = "警告"
            message = f"非标准状态码: {response.status_code}"
            
        return {
            "endpoint": endpoint,
            "status": status,
            "message": message,
            "response_time": response_time,
            "status_code": response.status_code
        }
    except requests.exceptions.Timeout:
        return {
            "endpoint": endpoint,
            "status": "超时",
            "message": f"请求超时 (>{TIMEOUT}秒)",
            "response_time": TIMEOUT,
            "status_code": 0
        }
    except requests.exceptions.ConnectionError:
        return {
            "endpoint": endpoint,
            "status": "连接错误",
            "message": "无法连接到服务器",
            "response_time": 0,
            "status_code": 0
        }
    except Exception as e:
        return {
            "endpoint": endpoint,
            "status": "异常",
            "message": str(e),
            "response_time": 0,
            "status_code": 0
        }

def print_result(result):
    """以彩色格式打印测试结果"""
    endpoint = result["endpoint"]
    status = result["status"]
    message = result["message"]
    response_time = result["response_time"]
    status_code = result["status_code"]
    
    # 根据状态设置颜色
    if status == "正常":
        status_color = TerminalColors.GREEN
    elif status == "警告":
        status_color = TerminalColors.YELLOW
    else:
        status_color = TerminalColors.RED
    
    # 根据响应时间设置颜色
    if response_time < 0.3:
        time_color = TerminalColors.GREEN
    elif response_time < 1.0:
        time_color = TerminalColors.YELLOW
    else:
        time_color = TerminalColors.RED
    
    print(f"{TerminalColors.BOLD}{endpoint['name']} ({endpoint['method']} {endpoint['path']}){TerminalColors.ENDC}")
    print(f"  状态: {status_color}{status}{TerminalColors.ENDC}")
    print(f"  响应码: {status_code}")
    print(f"  响应时间: {time_color}{response_time:.3f}秒{TerminalColors.ENDC}")
    print(f"  信息: {message}")
    print("-" * 50)

def main():
    """主函数，运行API状态检查"""
    print(f"\n{TerminalColors.BOLD}小说平台 API 状态检查{TerminalColors.ENDC}")
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"基础URL: {BASE_URL}")
    print("-" * 50)
    
    # 首先确认API服务是否在线
    print("正在检查API服务状态...")
    if not check_api_health():
        print(f"{TerminalColors.RED}API服务不可用！请确认服务已启动且可以访问 {BASE_URL}{TerminalColors.ENDC}")
        sys.exit(1)
    
    print(f"{TerminalColors.GREEN}API服务在线，开始检查各个端点...{TerminalColors.ENDC}\n")
    
    # 测试所有端点
    results = []
    for endpoint in API_ENDPOINTS:
        result = test_endpoint(endpoint)
        print_result(result)
        results.append(result)
    
    # 统计结果
    total = len(results)
    success = sum(1 for r in results if r["status"] == "正常")
    warnings = sum(1 for r in results if r["status"] == "警告")
    errors = total - success - warnings
    
    print(f"\n{TerminalColors.BOLD}测试统计结果{TerminalColors.ENDC}")
    print(f"总计端点: {total}")
    print(f"正常: {TerminalColors.GREEN}{success}{TerminalColors.ENDC}")
    if warnings > 0:
        print(f"警告: {TerminalColors.YELLOW}{warnings}{TerminalColors.ENDC}")
    if errors > 0:
        print(f"错误: {TerminalColors.RED}{errors}{TerminalColors.ENDC}")
    
    # 返回适当的退出码
    if errors > 0:
        sys.exit(1)
    elif warnings > 0:
        sys.exit(2)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main() 