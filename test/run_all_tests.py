#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest
import importlib
import time

# 导入相对路径的配置
sys.path.append(os.path.dirname(__file__))

# 测试模块列表
TEST_MODULES = [
    'test_user',
    'test_novel',
    'test_author',
    'test_interaction',
    'test_search',
    'test_admin'
]

def run_all_tests():
    """运行所有测试模块"""
    print("=" * 80)
    print("开始执行小说平台 API 接口测试")
    print("=" * 80)
    
    start_time = time.time()
    success = True
    
    for module_name in TEST_MODULES:
        try:
            # 动态导入测试模块
            module = importlib.import_module(module_name)
            
            # 创建测试套件
            suite = unittest.TestLoader().loadTestsFromModule(module)
            
            # 运行测试
            print(f"\n{'-' * 80}")
            print(f"正在执行 {module_name} 测试模块...")
            print(f"{'-' * 80}")
            
            result = unittest.TextTestRunner(verbosity=2).run(suite)
            
            # 打印测试结果
            print(f"\n{module_name} 测试结果:")
            print(f"  测试总数: {result.testsRun}")
            print(f"  通过数量: {result.testsRun - len(result.failures) - len(result.errors)}")
            print(f"  失败数量: {len(result.failures)}")
            print(f"  错误数量: {len(result.errors)}")
            
            # 检查是否有测试失败
            if result.failures or result.errors:
                success = False
                
        except Exception as e:
            print(f"\n加载 {module_name} 模块失败: {str(e)}")
            success = False
    
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "=" * 80)
    print(f"测试执行完成，总耗时: {duration:.2f} 秒")
    print(f"测试结果: {'成功' if success else '失败'}")
    print("=" * 80)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(run_all_tests()) 