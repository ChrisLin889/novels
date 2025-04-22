#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API测试主入口脚本

运行所有API测试模块，输出汇总结果
"""

import os
import sys
import time
import subprocess
from datetime import datetime

# 定义测试模块
TEST_MODULES = [
    {
        "name": "用户模块 API",
        "script": "test_user_api.py",
        "description": "包括用户注册、登录、个人信息管理及注销功能测试"
    },
    {
        "name": "小说模块 API",
        "script": "test_novel_api.py",
        "description": "包括小说创建、查询、更新、章节管理、标签管理等功能测试"
    },
    {
        "name": "作者模块 API",
        "script": "test_author_api.py",
        "description": "包括作者申请、管理员审核、作者资料管理及注销功能测试"
    },
    {
        "name": "互动模块 API",
        "script": "test_interaction_api.py",
        "description": "包括评论、关注、收藏、阅读进度及私信功能测试"
    }
]

# 定义报告输出目录
REPORT_DIR = "../doc/test_report"

def print_banner(text):
    """打印格式化标题"""
    border = "=" * 80
    print(f"\n{border}")
    print(f"{text.center(80)}")
    print(f"{border}\n")

def ensure_report_dir():
    """确保报告目录存在"""
    os.makedirs(REPORT_DIR, exist_ok=True)

def generate_report_filename(module_name):
    """生成报告文件名"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cleaned_name = module_name.replace(" ", "_").lower()
    return f"{cleaned_name}_test_report_{timestamp}.md"

def run_test(module):
    """运行单个测试模块"""
    print_banner(f"开始测试: {module['name']}")
    print(f"描述: {module['description']}")
    print(f"脚本: {module['script']}")
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # 生成报告文件名
    report_filename = generate_report_filename(module['name'])
    report_path = os.path.join(REPORT_DIR, report_filename)
    
    # 创建报告目录
    ensure_report_dir()
    
    # 运行测试并将输出保存到报告文件
    start_time = time.time()
    with open(report_path, 'w', encoding='utf-8') as report_file:
        # 写入报告标题
        report_file.write(f"# {module['name']} 测试报告\n\n")
        report_file.write(f"**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_file.write(f"**测试脚本**: {module['script']}\n")
        report_file.write(f"**描述**: {module['description']}\n\n")
        report_file.write("---\n\n")
        
        # 运行测试并捕获输出
        cmd = ["python3", module["script"]]
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            cwd=os.path.dirname(os.path.abspath(__file__)),
            text=True
        )
        
        # 实时写入报告
        for line in process.stdout:
            print(line, end='')
            report_file.write(line)
            
        result = process.wait()
        
    end_time = time.time()
    success = result == 0
    duration = end_time - start_time
    
    print("\n" + "="*80)
    status = "✅ 通过" if success else "❌ 失败"
    print(f"测试结果: {status}")
    print(f"执行时间: {duration:.2f} 秒")
    print(f"测试报告已保存至: {report_path}")
    print("="*80 + "\n")
    
    return {
        "name": module["name"],
        "success": success,
        "duration": duration,
        "report_path": report_path
    }

def main():
    """主函数，运行所有测试并显示汇总结果"""
    print_banner("API 测试套件")
    
    if len(TEST_MODULES) == 0:
        print("警告: 没有定义测试模块")
        return
    
    # 运行所有测试
    results = []
    for module in TEST_MODULES:
        try:
            result = run_test(module)
            results.append(result)
        except KeyboardInterrupt:
            print("\n测试被用户中断!")
            break
        except Exception as e:
            print(f"\n测试执行错误: {str(e)}")
            results.append({
                "name": module["name"],
                "success": False,
                "duration": 0,
                "error": str(e)
            })
    
    # 显示汇总结果
    print_banner("测试结果汇总")
    
    total_tests = len(results)
    passed_tests = sum(1 for r in results if r["success"])
    total_duration = sum(r["duration"] for r in results)
    
    # 创建汇总报告
    summary_report_path = os.path.join(REPORT_DIR, f"summary_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
    with open(summary_report_path, 'w', encoding='utf-8') as summary_file:
        summary_file.write("# API测试汇总报告\n\n")
        summary_file.write(f"**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        summary_file.write(f"**测试模块数**: {total_tests}\n")
        summary_file.write(f"**通过测试数**: {passed_tests}\n")
        summary_file.write(f"**总执行时间**: {total_duration:.2f}秒\n\n")
        
        summary_file.write("## 测试结果详情\n\n")
        for result in results:
            status = "✅ 通过" if result["success"] else "❌ 失败"
            summary_file.write(f"- {status} **{result['name']}** ({result['duration']:.2f}秒)\n")
            if "report_path" in result:
                report_filename = os.path.basename(result["report_path"])
                summary_file.write(f"  - [详细报告]({report_filename})\n")
        
        summary_file.write("\n\n")
        if passed_tests == total_tests:
            summary_file.write("🎉 **所有测试通过!**\n")
        else:
            summary_file.write("⚠️ **部分测试失败，请检查详细输出**\n")
    
    # 打印测试结果到控制台
    for result in results:
        status = "✅ 通过" if result["success"] else "❌ 失败"
        print(f"{status} - {result['name']} ({result['duration']:.2f}秒)")
    
    print("\n" + "-"*80)
    print(f"总计: {passed_tests}/{total_tests} 测试通过")
    print(f"总执行时间: {total_duration:.2f}秒")
    print(f"汇总报告已保存至: {summary_report_path}")
    print("-"*80)
    
    if passed_tests == total_tests:
        print("\n🎉 所有测试通过!")
        return 0
    else:
        print("\n⚠️ 部分测试失败，请检查详细输出")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 