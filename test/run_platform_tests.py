#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
小说平台测试和验证工具启动脚本
提供一个统一的界面来运行不同的测试和验证脚本
"""

import os
import sys
import subprocess
import argparse
from datetime import datetime

# 测试脚本路径配置
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = {
    "api_status": os.path.join(SCRIPT_DIR, "check_api_status.py"),
    "verify_fixes": os.path.join(SCRIPT_DIR, "verify_backend_fixes.py"),
    # 将来可以添加更多测试脚本
    # "functional_tests": os.path.join(SCRIPT_DIR, "run_functional_tests.py"),
    # "performance_tests": os.path.join(SCRIPT_DIR, "run_performance_tests.py"),
}

def check_prerequisites():
    """检查运行测试的先决条件"""
    print("=" * 50)
    print("检查测试先决条件...")
    
    # 检查Python版本
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 6):
        print(f"❌ Python版本过低: {sys.version}")
        print("请安装Python 3.6或更高版本")
        return False
    
    print(f"✅ Python版本: {sys.version}")
    
    # 检查必要的包
    required_packages = ["requests"]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ 已安装包: {package}")
        except ImportError:
            print(f"❌ 缺少包: {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print("\n需要安装以下包才能继续:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    # 检查测试脚本是否存在
    missing_scripts = []
    for name, path in SCRIPTS.items():
        if not os.path.exists(path):
            print(f"❌ 测试脚本不存在: {path}")
            missing_scripts.append(name)
        else:
            print(f"✅ 测试脚本已找到: {name}")
    
    if missing_scripts:
        print(f"\n以下测试脚本未找到: {', '.join(missing_scripts)}")
        return False
    
    return True

def run_script(script_path, script_name):
    """运行指定的测试脚本"""
    print("\n" + "=" * 50)
    print(f"运行 {script_name} 测试...")
    print("=" * 50)
    
    try:
        # 记录开始时间
        start_time = datetime.now()
        
        # 运行脚本并捕获输出
        process = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=False
        )
        
        # 记录结束时间和运行时间
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # 显示脚本输出
        print(process.stdout)
        
        # 检查脚本是否成功运行
        if process.returncode == 0:
            print(f"✅ {script_name} 测试完成 (用时: {duration:.2f}秒)")
            return True
        else:
            print(f"❌ {script_name} 测试失败 (退出代码: {process.returncode})")
            if process.stderr:
                print("错误信息:")
                print(process.stderr)
            return False
            
    except Exception as e:
        print(f"❌ 运行 {script_name} 时发生错误: {str(e)}")
        return False

def run_all_tests():
    """运行所有测试脚本"""
    results = {}
    
    # 先运行API状态检查
    if "api_status" in SCRIPTS:
        results["api_status"] = run_script(SCRIPTS["api_status"], "API状态检查")
    
    # 再运行问题修复验证
    if "verify_fixes" in SCRIPTS:
        results["verify_fixes"] = run_script(SCRIPTS["verify_fixes"], "问题修复验证")
    
    # 根据前两个测试的结果，决定是否继续运行其他测试
    if "api_status" in results and "verify_fixes" in results:
        if not (results["api_status"] and results["verify_fixes"]):
            print("\n⚠️ API状态检查或问题修复验证失败，建议先解决这些问题再继续测试")
            return results
    
    # 运行其他测试脚本
    for name, path in SCRIPTS.items():
        if name not in results:  # 跳过已经运行的脚本
            results[name] = run_script(path, name)
    
    return results

def generate_test_summary(results):
    """生成测试结果摘要"""
    print("\n" + "=" * 50)
    print("测试结果摘要")
    print("=" * 50)
    
    # 计算统计数据
    total = len(results)
    passed = sum(1 for result in results.values() if result)
    failed = total - passed
    
    print(f"运行测试: {total}")
    print(f"通过测试: {passed}")
    print(f"失败测试: {failed}")
    print("-" * 50)
    
    # 显示详细结果
    for name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
    
    print("-" * 50)
    
    # 提供建议
    if failed == 0:
        print("✅ 所有测试都通过了！系统可以投入进一步测试或使用。")
    else:
        print("⚠️ 有些测试失败了。请查看各测试报告获取详细信息。")
        print("建议修复失败的问题后再继续测试流程。")

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="小说平台测试启动工具")
    
    # 添加可选参数来选择特定的测试
    parser.add_argument(
        "--test", 
        choices=list(SCRIPTS.keys()) + ["all"],
        default="all",
        help="指定要运行的测试 (默认: all)"
    )
    
    # 添加是否显示详细输出的选项
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细输出"
    )
    
    return parser.parse_args()

def main():
    """主函数"""
    print("=" * 50)
    print("小说平台测试启动工具")
    print("=" * 50)
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # 解析命令行参数
    args = parse_args()
    
    # 检查先决条件
    if not check_prerequisites():
        print("\n❌ 未满足所有先决条件，无法继续测试")
        sys.exit(1)
    
    # 根据参数运行测试
    if args.test == "all":
        results = run_all_tests()
    else:
        if args.test in SCRIPTS:
            script_path = SCRIPTS[args.test]
            results = {args.test: run_script(script_path, args.test)}
        else:
            print(f"❌ 未知的测试: {args.test}")
            print(f"可用的测试: {', '.join(SCRIPTS.keys())}")
            sys.exit(1)
    
    # 生成测试结果摘要
    generate_test_summary(results)
    
    # 设置退出代码
    if all(results.values()):
        print("\n✅ 所有测试通过")
        sys.exit(0)
    else:
        print("\n❌ 部分测试失败")
        sys.exit(1)

if __name__ == "__main__":
    main() 