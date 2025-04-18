#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
后端修复验证工具

该脚本用于验证小说平台后端服务中已知问题是否已修复，并生成验证报告。
"""

import os
import sys
import json
import time
import requests
import platform
from datetime import datetime

# 配置项
BASE_URL = "http://localhost:5000"
TIMEOUT = 10  # 秒
REPORT_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_FILE = os.path.join(REPORT_DIR, "fix_verification_report.md")

# 已知问题列表及其验证方法
KNOWN_ISSUES = [
    {
        "id": "ISSUE-001",
        "title": "用户登录失败时返回500错误而非400错误",
        "description": "当用户登录提供的凭据不正确时，后端应返回400状态码而非500状态码",
        "severity": "中",
        "verification": {
            "endpoint": "/api/user/login",
            "method": "POST",
            "payload": {"username": "nonexistentuser", "password": "wrongpassword"},
            "expected_status": 400,
            "unexpected_status": 500
        }
    },
    {
        "id": "ISSUE-002",
        "title": "小说列表API返回结果没有分页",
        "description": "小说列表API应支持分页参数page和limit，并返回总页数和总条目数",
        "severity": "低",
        "verification": {
            "endpoint": "/api/novels",
            "method": "GET",
            "params": {"page": 1, "limit": 10},
            "check_fields": ["total", "total_pages", "items"]
        }
    },
    {
        "id": "ISSUE-003",
        "title": "小说搜索返回不区分中英文大小写",
        "description": "小说搜索功能应支持不区分中英文大小写的搜索",
        "severity": "低",
        "verification": {
            "endpoint": "/api/search/novel",
            "method": "GET",
            "params": {"keyword": "test"},
            "alternative_params": {"keyword": "TEST"},
            "check_equality": True
        }
    },
    {
        "id": "ISSUE-004",
        "title": "评论发表接口不验证内容长度",
        "description": "评论发表接口应验证内容长度，不允许空评论或超长评论",
        "severity": "中",
        "verification": {
            "endpoint": "/api/comments",
            "method": "POST",
            "auth_required": True,
            "payload": {"content": ""},
            "expected_status": 400
        }
    },
    {
        "id": "ISSUE-005",
        "title": "用户资料更新后缓存未更新",
        "description": "用户资料更新后，相关缓存应立即更新",
        "severity": "高",
        "verification": {
            "endpoint": "/api/user/profile",
            "method": "PUT",
            "auth_required": True,
            "payload": {"nickname": f"Test User {int(time.time())}"},
            "check_method": "cache_update"
        }
    },
    {
        "id": "ISSUE-006",
        "title": "API响应缺少CORS头",
        "description": "所有API响应应包含正确的CORS头以支持前端跨域请求",
        "severity": "高",
        "verification": {
            "endpoint": "/api/health",
            "method": "GET",
            "check_headers": ["Access-Control-Allow-Origin"]
        }
    },
    {
        "id": "ISSUE-007",
        "title": "API健康检查缺少数据库连接状态",
        "description": "API健康检查应包含数据库连接状态信息",
        "severity": "中",
        "verification": {
            "endpoint": "/api/health",
            "method": "GET",
            "check_fields": ["database_status"]
        }
    },
    {
        "id": "ISSUE-008",
        "title": "作者信息API异常大小写名称",
        "description": "作者信息API在作者名称大小写不同时应能识别为同一作者",
        "severity": "低",
        "verification": {
            "endpoint": "/api/author/{author_name}",
            "method": "GET",
            "params_template": {"author_name": "testauthor"},
            "alternative_params_template": {"author_name": "TestAuthor"},
            "check_equality": True
        }
    },
    {
        "id": "ISSUE-009",
        "title": "接口响应时间过长",
        "description": "小说列表接口响应时间应在500毫秒内",
        "severity": "高",
        "verification": {
            "endpoint": "/api/novels",
            "method": "GET",
            "check_response_time": 0.5
        }
    },
    {
        "id": "ISSUE-010",
        "title": "API文档Swagger路径无效",
        "description": "API文档Swagger路径应能正常访问",
        "severity": "低",
        "verification": {
            "endpoint": "/api/docs",
            "method": "GET",
            "expected_status": 200
        }
    }
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

def get_auth_token():
    """获取认证令牌用于需要认证的接口测试"""
    try:
        test_credentials = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = requests.post(
            f"{BASE_URL}/api/user/login",
            json=test_credentials,
            timeout=TIMEOUT
        )
        if response.status_code == 200:
            data = response.json()
            if "token" in data:
                return data["token"]
            elif "access_token" in data:
                return data["access_token"]
        return None
    except Exception:
        return None

def verify_issue(issue, auth_token=None):
    """
    验证单个问题是否已修复
    
    参数:
        issue (dict): 问题定义及验证方法
        auth_token (str): 认证令牌（如需要）
    
    返回:
        dict: 验证结果
    """
    verification = issue["verification"]
    endpoint = verification["endpoint"]
    method = verification["method"]
    
    # 处理模板参数
    if "params_template" in verification:
        endpoint = endpoint.format(**verification["params_template"])
    
    url = f"{BASE_URL}{endpoint}"
    
    # 准备请求参数
    kwargs = {"timeout": TIMEOUT}
    
    if "params" in verification:
        kwargs["params"] = verification["params"]
    
    if "payload" in verification:
        kwargs["json"] = verification["payload"]
    
    if verification.get("auth_required", False) and auth_token:
        kwargs["headers"] = {"Authorization": f"Bearer {auth_token}"}
    
    # 记录开始时间（用于检查响应时间）
    start_time = time.time()
    
    try:
        # 发送请求
        if method == "GET":
            response = requests.get(url, **kwargs)
        elif method == "POST":
            response = requests.post(url, **kwargs)
        elif method == "PUT":
            response = requests.put(url, **kwargs)
        elif method == "DELETE":
            response = requests.delete(url, **kwargs)
        else:
            return {
                "status": "未验证",
                "fixed": False,
                "reason": f"不支持的HTTP方法: {method}",
                "details": None
            }
        
        response_time = time.time() - start_time
        
        # 验证预期状态码
        if "expected_status" in verification:
            if response.status_code != verification["expected_status"]:
                return {
                    "status": "未修复",
                    "fixed": False,
                    "reason": f"状态码不符，期望 {verification['expected_status']}，实际 {response.status_code}",
                    "details": None
                }
        
        # 验证非预期状态码
        if "unexpected_status" in verification:
            if response.status_code == verification["unexpected_status"]:
                return {
                    "status": "未修复",
                    "fixed": False,
                    "reason": f"返回了非预期状态码 {verification['unexpected_status']}",
                    "details": None
                }
        
        # 检查响应字段
        if "check_fields" in verification:
            try:
                data = response.json()
                for field in verification["check_fields"]:
                    if field not in data:
                        return {
                            "status": "未修复",
                            "fixed": False,
                            "reason": f"响应中缺少必要字段: {field}",
                            "details": f"现有字段: {', '.join(data.keys())}"
                        }
            except ValueError:
                return {
                    "status": "未修复",
                    "fixed": False,
                    "reason": "响应不是有效的JSON格式",
                    "details": None
                }
        
        # 检查响应头
        if "check_headers" in verification:
            for header in verification["check_headers"]:
                if header not in response.headers:
                    return {
                        "status": "未修复",
                        "fixed": False,
                        "reason": f"响应头中缺少: {header}",
                        "details": f"现有响应头: {', '.join(response.headers.keys())}"
                    }
        
        # 检查响应时间
        if "check_response_time" in verification:
            max_time = verification["check_response_time"]
            if response_time > max_time:
                return {
                    "status": "未修复",
                    "fixed": False,
                    "reason": f"响应时间过长: {response_time:.2f}秒，超过了 {max_time:.2f}秒",
                    "details": None
                }
        
        # 检查两个不同请求的响应是否相同（大小写不敏感的测试）
        if "check_equality" in verification and verification["check_equality"]:
            # 保存第一个响应
            first_response = response
            first_data = first_response.json() if first_response.headers.get('content-type', '').startswith('application/json') else None
            
            # 准备第二个请求
            if "alternative_params" in verification:
                kwargs["params"] = verification["alternative_params"]
            elif "alternative_params_template" in verification:
                alt_url = f"{BASE_URL}{verification['endpoint'].format(**verification['alternative_params_template'])}"
                url = alt_url
            
            # 发送第二个请求
            if method == "GET":
                second_response = requests.get(url, **kwargs)
            elif method == "POST":
                second_response = requests.post(url, **kwargs)
            elif method == "PUT":
                second_response = requests.put(url, **kwargs)
            elif method == "DELETE":
                second_response = requests.delete(url, **kwargs)
            
            # 比较两个响应
            if first_response.status_code != second_response.status_code:
                return {
                    "status": "未修复",
                    "fixed": False,
                    "reason": "两个请求的状态码不同",
                    "details": f"{first_response.status_code} vs {second_response.status_code}"
                }
            
            # 比较JSON响应（如果有）
            if first_data:
                try:
                    second_data = second_response.json()
                    # 简单比较，可能需要更复杂的逻辑来处理顺序不同的列表等情况
                    if first_data != second_data:
                        return {
                            "status": "未修复",
                            "fixed": False,
                            "reason": "两个请求的响应内容不同",
                            "details": "JSON响应不一致"
                        }
                except ValueError:
                    return {
                        "status": "未修复",
                        "fixed": False,
                        "reason": "第二个响应不是有效的JSON格式",
                        "details": None
                    }
        
        # 如果所有检查都通过，则认为问题已修复
        return {
            "status": "已修复",
            "fixed": True,
            "reason": "所有验证检查都通过",
            "details": None
        }
    
    except requests.exceptions.Timeout:
        return {
            "status": "未修复",
            "fixed": False,
            "reason": f"请求超时（{TIMEOUT}秒）",
            "details": None
        }
    except requests.exceptions.ConnectionError:
        return {
            "status": "未验证",
            "fixed": False,
            "reason": "无法连接到服务器",
            "details": None
        }
    except Exception as e:
        return {
            "status": "未验证",
            "fixed": False,
            "reason": f"验证过程异常: {str(e)}",
            "details": None
        }

def verify_all_issues():
    """验证所有已知问题"""
    print(f"{TerminalColors.BOLD}开始验证后端修复状态...{TerminalColors.ENDC}")
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"后端服务: {BASE_URL}")
    print("-" * 60)
    
    # 检查API服务是否在线
    print("正在检查API服务状态...")
    if not check_api_health():
        print(f"{TerminalColors.RED}API服务不可用！请确认服务已启动且可以访问 {BASE_URL}{TerminalColors.ENDC}")
        sys.exit(1)
    
    # 获取认证令牌（用于需要认证的测试）
    auth_token = get_auth_token()
    if auth_token:
        print(f"{TerminalColors.GREEN}已成功获取认证令牌{TerminalColors.ENDC}")
    else:
        print(f"{TerminalColors.YELLOW}未能获取认证令牌，需要认证的接口测试可能会失败{TerminalColors.ENDC}")
    
    print("\n开始验证已知问题修复状态...\n")
    
    results = []
    for issue in KNOWN_ISSUES:
        print(f"正在验证 {issue['id']}: {issue['title']}...")
        print(f"  严重程度: {issue['severity']}")
        print(f"  描述: {issue['description']}")
        
        # 验证问题
        result = verify_issue(issue, auth_token)
        result["issue"] = issue
        results.append(result)
        
        # 显示结果
        status = result["status"]
        if status == "已修复":
            status_colored = f"{TerminalColors.GREEN}{status}{TerminalColors.ENDC}"
        elif status == "未修复":
            status_colored = f"{TerminalColors.RED}{status}{TerminalColors.ENDC}"
        else:
            status_colored = f"{TerminalColors.YELLOW}{status}{TerminalColors.ENDC}"
        
        print(f"  结果: {status_colored}")
        print(f"  原因: {result['reason']}")
        if result["details"]:
            print(f"  详情: {result['details']}")
        print("-" * 60)
    
    return results

def generate_report(results):
    """生成修复验证报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 计算统计数据
    total = len(results)
    fixed = sum(1 for r in results if r["fixed"])
    not_fixed = sum(1 for r in results if not r["fixed"] and r["status"] == "未修复")
    not_verified = sum(1 for r in results if r["status"] == "未验证")
    
    # 按严重程度分组统计
    severity_stats = {
        "高": {"total": 0, "fixed": 0, "not_fixed": 0, "not_verified": 0},
        "中": {"total": 0, "fixed": 0, "not_fixed": 0, "not_verified": 0},
        "低": {"total": 0, "fixed": 0, "not_fixed": 0, "not_verified": 0}
    }
    
    for result in results:
        severity = result["issue"]["severity"]
        severity_stats[severity]["total"] += 1
        
        if result["fixed"]:
            severity_stats[severity]["fixed"] += 1
        elif result["status"] == "未修复":
            severity_stats[severity]["not_fixed"] += 1
        else:
            severity_stats[severity]["not_verified"] += 1
    
    # 生成报告内容
    report = [
        "# 小说平台后端修复验证报告",
        "",
        f"**生成时间**: {now}",
        f"**后端服务**: {BASE_URL}",
        f"**验证环境**: Python {platform.python_version()} on {platform.system()} {platform.release()}",
        "",
        "## 总体修复状态",
        "",
        f"**总问题数**: {total}",
        f"**已修复**: {fixed} ({fixed/total*100:.1f}%)",
        f"**未修复**: {not_fixed} ({not_fixed/total*100:.1f}%)",
        f"**未验证**: {not_verified} ({not_verified/total*100:.1f}%)",
        "",
        "## 按严重程度统计",
        "",
        "| 严重程度 | 总问题数 | 已修复 | 未修复 | 未验证 | 修复率 |",
        "|---------|----------|--------|--------|--------|--------|"
    ]
    
    for severity, stats in severity_stats.items():
        fix_rate = stats["fixed"] / stats["total"] * 100 if stats["total"] > 0 else 0
        report.append(f"| {severity} | {stats['total']} | {stats['fixed']} | {stats['not_fixed']} | {stats['not_verified']} | {fix_rate:.1f}% |")
    
    # 详细问题状态
    report.extend([
        "",
        "## 详细问题修复状态",
        ""
    ])
    
    # 未修复的高优先级问题
    high_priority_not_fixed = [r for r in results if not r["fixed"] and r["issue"]["severity"] == "高" and r["status"] == "未修复"]
    if high_priority_not_fixed:
        report.extend([
            "### ⚠️ 未修复的高优先级问题",
            ""
        ])
        
        for result in high_priority_not_fixed:
            issue = result["issue"]
            report.extend([
                f"#### {issue['id']}: {issue['title']}",
                "",
                f"- **描述**: {issue['description']}",
                f"- **验证结果**: {result['status']}",
                f"- **原因**: {result['reason']}",
                ""
            ])
    
    # 按状态分组列出所有问题
    for status_group in ["未修复", "已修复", "未验证"]:
        filtered_results = [r for r in results if r["status"] == status_group]
        if filtered_results:
            report.extend([
                f"### {status_group}问题 ({len(filtered_results)})",
                "",
                "| 问题ID | 标题 | 严重程度 | 原因 |",
                "|--------|------|----------|------|"
            ])
            
            for result in filtered_results:
                issue = result["issue"]
                report.append(f"| {issue['id']} | {issue['title']} | {issue['severity']} | {result['reason']} |")
            
            report.append("")
    
    # 添加建议事项
    report.extend([
        "## 建议事项",
        ""
    ])
    
    if not_fixed > 0:
        report.append("### 优先修复建议")
        report.append("")
        
        # 按严重程度优先级排序未修复的问题
        severity_order = {"高": 0, "中": 1, "低": 2}
        not_fixed_issues = [r for r in results if not r["fixed"] and r["status"] == "未修复"]
        not_fixed_issues.sort(key=lambda r: severity_order[r["issue"]["severity"]])
        
        for i, result in enumerate(not_fixed_issues):
            issue = result["issue"]
            report.append(f"{i+1}. {issue['severity']}优先级: **{issue['id']}** - {issue['title']}")
        
        report.append("")
    
    if not_verified > 0:
        report.append("### 未验证问题说明")
        report.append("")
        report.append("以下问题由于各种原因未能验证，建议手动检查：")
        report.append("")
        
        not_verified_issues = [r for r in results if r["status"] == "未验证"]
        for result in not_verified_issues:
            issue = result["issue"]
            report.append(f"- **{issue['id']}**: {issue['title']} - {result['reason']}")
        
        report.append("")
    
    # 如果全部修复，添加祝贺信息
    if fixed == total:
        report.extend([
            "## 🎉 恭喜!",
            "",
            "所有已知问题都已修复，后端服务状态良好。",
            ""
        ])
    
    return "\n".join(report)

def save_report(report_content):
    """将报告保存到文件"""
    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(report_content)
        print(f"{TerminalColors.GREEN}报告已保存到: {REPORT_FILE}{TerminalColors.ENDC}")
        return True
    except Exception as e:
        print(f"{TerminalColors.RED}保存报告失败: {str(e)}{TerminalColors.ENDC}")
        return False

def main():
    """主函数"""
    print(f"\n{TerminalColors.BOLD}小说平台后端修复验证工具{TerminalColors.ENDC}")
    print("-" * 60)
    
    # 验证所有问题
    results = verify_all_issues()
    
    # 计算统计数据
    total = len(results)
    fixed = sum(1 for r in results if r["fixed"])
    
    # 生成报告
    report_content = generate_report(results)
    save_report(report_content)
    
    # 打印总结
    print(f"\n{TerminalColors.BOLD}验证结果总结:{TerminalColors.ENDC}")
    print(f"总问题数: {total}")
    print(f"已修复: {TerminalColors.GREEN}{fixed}{TerminalColors.ENDC} ({fixed/total*100:.1f}%)")
    print(f"未修复或未验证: {TerminalColors.RED}{total-fixed}{TerminalColors.ENDC} ({(total-fixed)/total*100:.1f}%)")
    print(f"\n详细报告已保存到: {REPORT_FILE}")
    
    # 返回适当的退出码
    if fixed == total:
        print(f"\n{TerminalColors.GREEN}恭喜! 所有已知问题都已修复!{TerminalColors.ENDC}")
        sys.exit(0)
    else:
        print(f"\n{TerminalColors.YELLOW}存在未修复的问题，请查看详细报告。{TerminalColors.ENDC}")
        sys.exit(1)

if __name__ == "__main__":
    main() 