#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
搜索模块 API 测试脚本

测试小说搜索、标签搜索、相似小说推荐、热门标签获取等功能
"""

import sys
import os
import unittest
import json
import random
import string
import time
from datetime import datetime, timedelta

# 将项目根目录添加到 Python 路径中，保证能够导入到 backend 包
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入测试工具
import requests
from requests.exceptions import RequestException

# 测试配置
BASE_URL = "http://localhost:5000"
API_PREFIX = "/api"

# 测试账户信息
USER_USERNAME = "testuser"
USER_PASSWORD = "password123"

# 定义报告输出目录
REPORT_DIR = "../doc/test_report"

def ensure_report_dir():
    """确保报告目录存在"""
    os.makedirs(REPORT_DIR, exist_ok=True)

# 辅助函数
def random_string(length=8):
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_timestamp():
    """获取当前时间戳字符串"""
    return datetime.now().strftime("%Y%m%d%H%M%S")

class TestSearchAPI(unittest.TestCase):
    """搜索API测试类"""
    
    @classmethod
    def setUpClass(cls):
        """测试类开始前执行，登录并获取测试用户的token"""
        print("\n=== 准备测试环境 ===")
        
        try:
            # 登录获取token
            login_response = requests.post(
                f"{BASE_URL}{API_PREFIX}/user/login", 
                json={"username": USER_USERNAME, "password": USER_PASSWORD}
            )
            
            if login_response.status_code != 200:
                print(f"用户登录失败: {login_response.text}")
                # 尝试以游客身份继续测试
                cls.user_token = None
            else:
                login_data = login_response.json()
                # 从返回中获取token
                cls.user_token = login_data.get("access_token") or login_data.get("token")
                
            # 获取一些小说数据用于测试
            try:
                novels_response = requests.get(f"{BASE_URL}{API_PREFIX}/novel/popular")
                if novels_response.status_code == 200:
                    novels_data = novels_response.json().get("novels", [])
                    if novels_data:
                        cls.test_novel_id = novels_data[0].get("id")
                        cls.test_novel_title = novels_data[0].get("title")
                    else:
                        cls.test_novel_id = None
                        cls.test_novel_title = None
                        print("无法获取测试小说数据，某些测试可能会失败")
                else:
                    cls.test_novel_id = None
                    cls.test_novel_title = None
                    print("获取热门小说失败，某些测试可能会失败")
            except Exception as e:
                cls.test_novel_id = None
                cls.test_novel_title = None
                print(f"获取测试小说时出错: {str(e)}")
            
            # 获取一些标签数据用于测试
            try:
                tags_response = requests.get(f"{BASE_URL}{API_PREFIX}/search/tags/hot")
                if tags_response.status_code == 200:
                    tags_data = tags_response.json().get("tags", [])
                    if tags_data:
                        cls.test_tag = tags_data[0].get("name")
                    else:
                        cls.test_tag = "玄幻"  # 默认标签
                        print("无法获取热门标签，使用默认标签")
                else:
                    cls.test_tag = "玄幻"  # 默认标签
                    print("获取热门标签失败，使用默认标签")
            except Exception as e:
                cls.test_tag = "玄幻"  # 默认标签
                print(f"获取测试标签时出错: {str(e)}")
                
            print(f"测试环境准备完成。测试小说ID: {cls.test_novel_id}, 测试标签: {cls.test_tag}")
        except RequestException as e:
            print(f"测试环境准备失败: {str(e)}")
            raise
    
    def test_01_search_novels(self):
        """测试小说搜索功能"""
        print("\n--- 测试小说搜索 ---")
        
        # 如果有可用的小说标题，则使用；否则使用通用关键词
        search_query = self.__class__.test_novel_title if hasattr(self.__class__, 'test_novel_title') and self.__class__.test_novel_title else "小说"
        
        # 发送搜索请求
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/search/novels",
            params={"q": search_query, "page": 1, "per_page": 10}
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"小说搜索失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("total", response_data, "响应中没有返回total字段")
        self.assertIn("page", response_data, "响应中没有返回page字段")
        self.assertIn("per_page", response_data, "响应中没有返回per_page字段")
        self.assertIn("results", response_data, "响应中没有返回results字段")
        
        # 打印结果数量
        print(f"搜索关键词 '{search_query}' 返回 {response_data.get('total')} 个结果")
        
        # 验证分页功能
        if response_data.get('total', 0) > 10:
            # 测试第二页
            response_page2 = requests.get(
                f"{BASE_URL}{API_PREFIX}/search/novels",
                params={"q": search_query, "page": 2, "per_page": 10}
            )
            self.assertEqual(response_page2.status_code, 200, "分页搜索失败")
            page2_data = response_page2.json()
            self.assertEqual(page2_data.get('page'), 2, "返回的页码不正确")
            print("分页功能测试通过")
        
        # 测试无效搜索
        invalid_response = requests.get(
            f"{BASE_URL}{API_PREFIX}/search/novels",
            params={"q": random_string(20), "page": 1, "per_page": 10}  # 使用随机字符串，期望找不到结果
        )
        self.assertEqual(invalid_response.status_code, 200, "无效搜索请求应该返回200状态码")
        invalid_data = invalid_response.json()
        self.assertEqual(invalid_data.get('total', 0), 0, "无效搜索应返回0个结果")
        print("无效搜索测试通过")
    
    def test_02_tag_search(self):
        """测试标签搜索功能"""
        print("\n--- 测试标签搜索 ---")
        
        # 确保有测试标签可用
        self.assertTrue(hasattr(self.__class__, 'test_tag'), "没有可用的测试标签")
        
        # 发送标签搜索请求
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/search/novels/tag/{self.__class__.test_tag}",
            params={"page": 1, "per_page": 10}
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"标签搜索失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("total", response_data, "响应中没有返回total字段")
        self.assertIn("page", response_data, "响应中没有返回page字段")
        self.assertIn("per_page", response_data, "响应中没有返回per_page字段")
        self.assertIn("results", response_data, "响应中没有返回results字段")
        
        # 打印结果数量
        print(f"标签 '{self.__class__.test_tag}' 搜索返回 {response_data.get('total')} 个结果")
        
        # 测试无效标签
        invalid_tag = random_string(20)  # 使用随机字符串作为不太可能存在的标签
        invalid_response = requests.get(
            f"{BASE_URL}{API_PREFIX}/search/novels/tag/{invalid_tag}",
            params={"page": 1, "per_page": 10}
        )
        self.assertEqual(invalid_response.status_code, 200, "无效标签搜索应该返回200状态码")
        invalid_data = invalid_response.json()
        self.assertEqual(invalid_data.get('total', 0), 0, "无效标签搜索应返回0个结果")
        print("无效标签搜索测试通过")
    
    def test_03_similar_novels(self):
        """测试相似小说推荐功能"""
        print("\n--- 测试相似小说推荐 ---")
        
        # 确保有测试小说ID可用
        if not hasattr(self.__class__, 'test_novel_id') or not self.__class__.test_novel_id:
            self.skipTest("没有可用的测试小说ID，跳过相似小说推荐测试")
        
        # 发送相似小说请求
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/search/similar/{self.__class__.test_novel_id}",
            params={"limit": 5}
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"相似小说推荐失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("similar_novels", response_data, "响应中没有返回similar_novels字段")
        
        # 检查返回的小说列表
        similar_novels = response_data.get("similar_novels", [])
        self.assertLessEqual(len(similar_novels), 5, "返回的相似小说数量超过了请求的限制")
        
        print(f"成功获取 {len(similar_novels)} 个相似小说推荐")
        
        # 测试无效小说ID
        invalid_id = 99999999  # 使用一个很大的ID，期望它不存在
        invalid_response = requests.get(
            f"{BASE_URL}{API_PREFIX}/search/similar/{invalid_id}",
            params={"limit": 5}
        )
        # 可能返回404或空列表，都是有效的
        if invalid_response.status_code == 404:
            print("无效小说ID返回404状态码，测试通过")
        else:
            self.assertEqual(invalid_response.status_code, 200, "无效小说ID应该返回200或404状态码")
            invalid_data = invalid_response.json()
            similar_count = len(invalid_data.get("similar_novels", []))
            self.assertEqual(similar_count, 0, "对于无效小说ID，应返回0个相似小说")
            print("无效小说ID测试通过")
    
    def test_04_hot_tags(self):
        """测试获取热门标签功能"""
        print("\n--- 测试获取热门标签 ---")
        
        # 发送获取热门标签请求
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/search/tags/hot",
            params={"limit": 10}
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"获取热门标签失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("tags", response_data, "响应中没有返回tags字段")
        
        # 检查返回的标签列表
        tags = response_data.get("tags", [])
        self.assertLessEqual(len(tags), 10, "返回的热门标签数量超过了请求的限制")
        
        print(f"成功获取 {len(tags)} 个热门标签")
        
        # 测试类别过滤
        # 从返回的标签中获取一个类别ID
        if tags and "category_id" in tags[0]:
            category_id = tags[0]["category_id"]
            
            # 使用该类别ID进行过滤测试
            filtered_response = requests.get(
                f"{BASE_URL}{API_PREFIX}/search/tags/hot",
                params={"limit": 10, "category_id": category_id}
            )
            self.assertEqual(filtered_response.status_code, 200, "类别过滤热门标签请求失败")
            filtered_data = filtered_response.json()
            filtered_tags = filtered_data.get("tags", [])
            
            # 验证所有返回的标签都属于请求的类别
            if filtered_tags:
                for tag in filtered_tags:
                    self.assertEqual(tag.get("category_id"), category_id, "返回的标签类别与请求的不匹配")
                
                print(f"类别过滤测试通过，成功获取类别ID {category_id} 的 {len(filtered_tags)} 个标签")

def generate_report(result, start_time, end_time):
    """生成测试报告"""
    ensure_report_dir()
    
    # 计算执行时间
    total_time = end_time - start_time
    
    # 收集测试结果
    test_results = []
    for test, err in result.errors:
        test_results.append({
            "name": test._testMethodName,
            "result": "失败",
            "error": err
        })
    
    for test, err in result.failures:
        test_results.append({
            "name": test._testMethodName,
            "result": "失败",
            "error": err
        })
    
    for test in result.successes:
        test_results.append({
            "name": test._testMethodName,
            "result": "通过",
            "error": None
        })
    
    # 按测试方法名称排序
    test_results.sort(key=lambda x: x["name"])
    
    # 统计测试结果
    total_tests = len(test_results)
    passed_tests = sum(1 for test in test_results if test["result"] == "通过")
    
    # 生成报告文件名
    timestamp = get_timestamp()
    report_filename = f"搜索模块_api_test_report_{timestamp}.md"
    report_path = os.path.join(REPORT_DIR, report_filename)
    
    # 写入报告
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write("# 搜索模块 API 测试报告\n\n")
        report_file.write(f"**测试时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_file.write(f"**测试脚本**: test_search_api.py\n")
        report_file.write(f"**测试结果概述**: {passed_tests}/{total_tests} 通过\n")
        report_file.write(f"**总执行时间**: {total_time:.2f}秒\n\n")
        
        report_file.write("## 测试结果详情\n\n")
        report_file.write("| 测试名称 | 结果 |\n")
        report_file.write("|---------|------|\n")
        
        for test in test_results:
            test_name = test["name"][5:]  # 去掉 "test_" 前缀
            if test_name.startswith("0"):
                test_name = test_name[3:]  # 去掉序号和下划线
            
            # 将下划线替换为空格并首字母大写
            test_name = test_name.replace("_", " ").strip()
            
            # 添加表情符号
            result_emoji = "✅" if test["result"] == "通过" else "❌"
            report_file.write(f"| {test_name} | {result_emoji} {test['result']} |\n")
        
        # 添加错误详情部分
        has_errors = any(test["result"] == "失败" for test in test_results)
        if has_errors:
            report_file.write("\n## 错误详情\n\n")
            for test in test_results:
                if test["result"] == "失败":
                    test_name = test["name"][5:]
                    if test_name.startswith("0"):
                        test_name = test_name[3:]
                    test_name = test_name.replace("_", " ").strip()
                    
                    report_file.write(f"### {test_name}\n\n")
                    report_file.write("```\n")
                    report_file.write(test["error"])
                    report_file.write("\n```\n\n")
    
    print(f"\n测试报告已生成: {report_path}")
    return report_path

def main():
    """主函数，运行测试并生成报告"""
    # 创建测试套件
    test_suite = unittest.TestSuite()
    
    # 添加测试用例
    test_suite.addTest(unittest.makeSuite(TestSearchAPI))
    
    # 记录开始时间
    start_time = time.time()
    
    # 初始化测试结果收集器
    result = unittest.TestResult()
    result.successes = []
    
    # 原始的addSuccess方法不收集成功的测试用例，所以我们需要扩展它
    original_add_success = result.addSuccess
    def add_success_with_storage(test):
        original_add_success(test)
        result.successes.append(test)
    result.addSuccess = add_success_with_storage
    
    # 运行测试
    print("\n开始运行搜索模块 API 测试...\n")
    test_suite.run(result)
    
    # 记录结束时间
    end_time = time.time()
    
    # 打印测试结果
    print("\n\n=== 测试结果摘要 ===")
    print(f"总测试数: {result.testsRun}")
    print(f"成功: {len(result.successes)}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")
    print(f"跳过: {len(getattr(result, 'skipped', []))}")
    print(f"总执行时间: {end_time - start_time:.2f} 秒")
    
    # 生成报告
    report_path = generate_report(result, start_time, end_time)
    
    # 返回测试结果
    return len(result.failures) + len(result.errors) == 0

if __name__ == "__main__":
    # 确保报告目录存在
    ensure_report_dir()
    
    # 运行测试
    success = main()
    
    # 使用测试结果作为退出码
    sys.exit(0 if success else 1) 