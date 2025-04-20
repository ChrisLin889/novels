#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
小说模块 API 测试脚本

测试小说创建、查询、管理等功能
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

# 测试账户信息 - 从sign.txt获取
AUTHOR_USERNAME = "testauthor"
AUTHOR_PASSWORD = "password123"
AUTHOR_ID = 5

# 辅助函数
def random_string(length=8):
    """生成随机字符串"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_timestamp():
    """获取当前时间戳字符串"""
    return datetime.now().strftime("%Y%m%d%H%M%S")

class TestNovelAPI(unittest.TestCase):
    """小说API测试类"""
    
    @classmethod
    def setUpClass(cls):
        """测试类开始前执行，登录并获取测试用户的token"""
        print("\n=== 准备测试环境 ===")
        
        try:
            # 使用已有的作者账号登录
            login_response = requests.post(
                f"{BASE_URL}{API_PREFIX}/user/login", 
                json={"username": AUTHOR_USERNAME, "password": AUTHOR_PASSWORD}
            )
            
            if login_response.status_code != 200:
                print(f"作者登录失败: {login_response.text}")
                raise Exception("作者登录失败")
                
            login_data = login_response.json()
            # 从返回中获取token，API文档显示应该是access_token而不是token
            cls.author_token = login_data.get("access_token")
            if not cls.author_token:
                # 如果没有找到access_token，尝试使用token字段
                cls.author_token = login_data.get("token")
            
            if not cls.author_token:
                print(f"无法从登录响应中获取令牌: {login_data}")
                raise Exception("无法获取登录令牌")
                
            cls.author_id = AUTHOR_ID
                        
            # 创建测试小说列表
            cls.test_novels = []
            
            print(f"测试环境准备完成。使用作者用户ID: {cls.author_id}")
        except RequestException as e:
            print(f"测试环境准备失败: {str(e)}")
            raise
    
    @classmethod
    def tearDownClass(cls):
        """测试结束后清理创建的测试数据"""
        print("\n=== 清理测试环境 ===")
        # 删除创建的测试小说
        for novel_id in cls.test_novels:
            try:
                # 尝试删除小说
                response = requests.delete(
                    f"{BASE_URL}{API_PREFIX}/novel/{novel_id}/delete",
                    headers={"Authorization": f"Bearer {cls.author_token}"}
                )
                print(f"删除小说 {novel_id}: {'成功' if response.status_code == 200 else '失败'}")
            except Exception as e:
                print(f"删除小说 {novel_id} 时出错: {str(e)}")
        
        print("测试环境清理完成")
    
    def setUp(self):
        """每个测试方法开始前执行"""
        # 验证我们有有效的token
        self.assertTrue(hasattr(self.__class__, 'author_token') and self.__class__.author_token, 
                        "没有有效的作者token，无法进行测试")
    
    def test_01_add_novel(self):
        """测试添加小说功能"""
        print("\n--- 测试添加小说 ---")
        
        # 准备小说数据
        novel_data = {
            "title": f"测试小说 {random_string()} {get_timestamp()}",
            "category": "奇幻",
            "intro": "这是一本用于API测试的小说",  # 小说简介
            "cover": "https://example.com/default-cover.jpg",
            "status": "ongoing",  # 小说状态
            "tags": ["测试", "奇幻"]  # 添加标签字段
        }
        
        # 发送添加小说请求
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/novel/add",
            headers={"Authorization": f"Bearer {self.__class__.author_token}"},
            json=novel_data
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 201, f"添加小说失败，响应: {response.text}")  # 修改期望状态码为201
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("message", response_data, "响应中没有返回message字段")
        self.assertIn("novel_id", response_data, "响应中没有返回novel_id字段")
        
        # 保存小说ID用于后续测试和清理
        novel_id = response_data.get("novel_id")
        self.__class__.test_novels.append(novel_id)
        self.__class__.current_test_novel_id = novel_id
        
        print(f"成功创建测试小说，ID: {novel_id}")
    
    def test_02_get_novel_detail(self):
        """测试获取小说详情功能"""
        print("\n--- 测试获取小说详情 ---")
        
        # 确保有测试小说可用
        self.assertTrue(hasattr(self.__class__, 'current_test_novel_id'), "没有可用的测试小说ID")
        
        # 发送获取小说详情请求
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/novel/detail/{self.__class__.current_test_novel_id}",  # 修改路径
            headers={"Authorization": f"Bearer {self.__class__.author_token}"}
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"获取小说详情失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("novel", response_data, "响应中没有返回novel对象")
        self.assertIn("chapters", response_data, "响应中没有返回chapters列表")
        
        novel = response_data.get("novel")
        self.assertEqual(novel.get("id"), self.__class__.current_test_novel_id, "返回的小说ID不匹配")
        
        print(f"成功获取小说详情: {novel.get('title')}")
    
    def test_03_update_novel(self):
        """测试更新小说信息功能"""
        print("\n--- 测试更新小说信息 ---")
        
        # 确保有测试小说可用
        self.assertTrue(hasattr(self.__class__, 'current_test_novel_id'), "没有可用的测试小说ID")
        
        # 准备更新数据
        update_data = {
            "title": f"更新后的测试小说 {random_string()} {get_timestamp()}",
            "category": "科幻",
            "intro": "这是更新后的小说描述",  # 修改 description 为 intro
            "status": "ongoing"  # 添加状态字段
        }
        
        # 发送更新小说请求
        response = requests.put(
            f"{BASE_URL}{API_PREFIX}/novel/{self.__class__.current_test_novel_id}",
            headers={"Authorization": f"Bearer {self.__class__.author_token}"},
            json=update_data
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"更新小说失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("message", response_data, "响应中没有返回message字段")
        self.assertTrue(response_data.get("success", False), "响应中success字段不为True")
        
        # 获取更新后的小说详情进行验证
        detail_response = requests.get(
            f"{BASE_URL}{API_PREFIX}/novel/detail/{self.__class__.current_test_novel_id}",  # 修改路径
            headers={"Authorization": f"Bearer {self.__class__.author_token}"}
        )
        
        if detail_response.status_code == 200:
            novel = detail_response.json().get("novel", {})
            self.assertEqual(novel.get("title"), update_data["title"], "小说标题未更新")
            self.assertEqual(novel.get("intro"), update_data["intro"], "小说简介未更新")  # 修改验证字段
            
            print(f"成功更新小说信息: {novel.get('title')}")
        else:
            self.fail(f"获取更新后的小说详情失败: {detail_response.text}")
    
    def test_04_add_chapter(self):
        """测试添加小说章节功能"""
        print("\n--- 测试添加小说章节 ---")
        
        # 确保有测试小说可用
        self.assertTrue(hasattr(self.__class__, 'current_test_novel_id'), "没有可用的测试小说ID")
        
        # 准备章节数据
        chapter_data = {
            "title": f"测试章节 {random_string()}",
            "content": f"这是一个测试章节的内容。\n\n这是第二段。\n\n这是第三段，包含了一些随机字符: {random_string(32)}",
            "chapter_number": 1
        }
        
        # 发送添加章节请求
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/novel/{self.__class__.current_test_novel_id}/chapters",  # 修改路径
            headers={"Authorization": f"Bearer {self.__class__.author_token}"},
            json=chapter_data
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 201, f"添加章节失败，响应: {response.text}")  # 修改期望状态码为201
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("message", response_data, "响应中没有返回message字段")
        self.assertIn("chapter_id", response_data, "响应中没有返回chapter_id字段")
        
        # 保存章节ID用于后续测试
        self.__class__.current_test_chapter_id = response_data.get("chapter_id")
        
        print(f"成功添加测试章节，ID: {self.__class__.current_test_chapter_id}")
    
    def test_05_get_chapter_detail(self):
        """测试获取章节详情功能"""
        print("\n--- 测试获取章节详情 ---")
        
        # 确保有测试章节可用
        self.assertTrue(hasattr(self.__class__, 'current_test_chapter_id'), "没有可用的测试章节ID")
        
        # 发送获取章节详情请求
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/novel/chapters/{self.__class__.current_test_chapter_id}",  # 修改路径
            headers={"Authorization": f"Bearer {self.__class__.author_token}"}
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"获取章节详情失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("chapter", response_data, "响应中没有返回chapter对象")
        
        chapter = response_data.get("chapter")
        self.assertEqual(chapter.get("id"), self.__class__.current_test_chapter_id, "返回的章节ID不匹配")
        
        print(f"成功获取章节详情: {chapter.get('title')}")
    
    def test_06_update_chapter(self):
        """测试更新章节信息功能"""
        print("\n--- 测试更新章节信息 ---")
        
        # 确保有测试章节可用
        self.assertTrue(hasattr(self.__class__, 'current_test_chapter_id'), "没有可用的测试章节ID")
        
        # 准备更新数据
        update_data = {
            "title": f"更新后的测试章节 {random_string()}",
            "content": f"这是更新后的章节内容。\n\n包含了更多的随机字符: {random_string(50)}"
        }
        
        # 发送更新章节请求
        response = requests.put(
            f"{BASE_URL}{API_PREFIX}/novel/chapters/{self.__class__.current_test_chapter_id}",  # 修改路径
            headers={"Authorization": f"Bearer {self.__class__.author_token}"},
            json=update_data
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"更新章节失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("message", response_data, "响应中没有返回message字段")
        self.assertTrue(response_data.get("success", False), "响应中success字段不为True")
        
        # 获取更新后的章节详情进行验证
        detail_response = requests.get(
            f"{BASE_URL}{API_PREFIX}/novel/chapters/{self.__class__.current_test_chapter_id}",  # 修改路径
            headers={"Authorization": f"Bearer {self.__class__.author_token}"}
        )
        
        if detail_response.status_code == 200:
            chapter = detail_response.json().get("chapter", {})
            self.assertEqual(chapter.get("title"), update_data["title"], "章节标题未更新")
            
            print(f"成功更新章节信息: {chapter.get('title')}")
        else:
            self.fail(f"获取更新后的章节详情失败: {detail_response.text}")
    
    def test_07_get_all_chapters(self):
        """测试获取小说所有章节功能"""
        print("\n--- 测试获取小说所有章节 ---")
        
        # 确保有测试小说可用
        self.assertTrue(hasattr(self.__class__, 'current_test_novel_id'), "没有可用的测试小说ID")
        
        # 发送获取所有章节请求
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/novel/{self.__class__.current_test_novel_id}/chapters",
            headers={"Authorization": f"Bearer {self.__class__.author_token}"}
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"获取所有章节失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("chapters", response_data, "响应中没有返回chapters列表")
        
        chapters = response_data.get("chapters")
        self.assertIsInstance(chapters, list, "chapters不是一个列表")
        self.assertGreater(len(chapters), 0, "章节列表为空")
        
        print(f"成功获取小说的所有章节，共 {len(chapters)} 章")
    
    def test_08_delete_chapter(self):
        """测试删除章节功能"""
        print("\n--- 测试删除章节 ---")
        
        # 确保有测试章节可用
        self.assertTrue(hasattr(self.__class__, 'current_test_chapter_id'), "没有可用的测试章节ID")
        
        # 发送删除章节请求
        response = requests.delete(
            f"{BASE_URL}{API_PREFIX}/novel/chapters/{self.__class__.current_test_chapter_id}",  # 修改路径
            headers={"Authorization": f"Bearer {self.__class__.author_token}"}
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"删除章节失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("message", response_data, "响应中没有返回message字段")
        
        # 尝试获取已删除的章节，应该返回错误
        verify_response = requests.get(
            f"{BASE_URL}{API_PREFIX}/novel/chapters/{self.__class__.current_test_chapter_id}",  # 修改路径
            headers={"Authorization": f"Bearer {self.__class__.author_token}"}
        )
        
        # 验证章节已被删除
        self.assertEqual(verify_response.status_code, 404, "章节应该已被删除，期望返回404")
        
        print(f"成功删除测试章节，ID: {self.__class__.current_test_chapter_id}")
    
    def test_09_search_novels(self):
        """测试搜索小说功能"""
        print("\n--- 测试搜索小说 ---")
        
        # 发送搜索小说请求
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/search/novels?q=测试小说",
            headers={"Authorization": f"Bearer {self.__class__.author_token}"}
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"搜索小说失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("results", response_data, "响应中没有返回results列表")
        
        novels = response_data.get("results")
        self.assertIsInstance(novels, list, "results不是一个列表")
        
        print(f"成功搜索小说，找到 {len(novels)} 本相关小说")
    
    def test_10_get_author_novels(self):
        """测试获取作者的所有小说功能"""
        print("\n--- 测试获取作者的所有小说 ---")
        
        # 发送获取作者小说请求
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/novel/author/novels",  # 修改路径
            headers={"Authorization": f"Bearer {self.__class__.author_token}"}
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"获取作者小说失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("novels", response_data, "响应中没有返回novels列表")
        self.assertIn("total", response_data, "响应中没有返回total字段")
        self.assertIn("pages", response_data, "响应中没有返回pages字段")
        self.assertIn("current_page", response_data, "响应中没有返回current_page字段")
        
        novels = response_data.get("novels")
        self.assertIsInstance(novels, list, "novels不是一个列表")
        
        print(f"成功获取作者的所有小说，共 {len(novels)} 本")
    
    def test_11_delete_novel(self):
        """测试删除小说功能"""
        print("\n--- 测试删除小说 ---")
        
        # 确保有测试小说可用
        self.assertTrue(hasattr(self.__class__, 'current_test_novel_id'), "没有可用的测试小说ID")
        
        # 发送删除小说请求
        response = requests.delete(
            f"{BASE_URL}{API_PREFIX}/novel/{self.__class__.current_test_novel_id}/delete",  # 修改路径
            headers={"Authorization": f"Bearer {self.__class__.author_token}"}
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"删除小说失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("message", response_data, "响应中没有返回message字段")
        
        # 尝试获取已删除的小说，应该返回错误
        verify_response = requests.get(
            f"{BASE_URL}{API_PREFIX}/novel/detail/{self.__class__.current_test_novel_id}",  # 修改路径
            headers={"Authorization": f"Bearer {self.__class__.author_token}"}
        )
        
        self.assertEqual(verify_response.status_code, 404, "小说应该已被删除，期望返回404")
        
        # 从待清理列表中移除已删除的小说
        if self.__class__.current_test_novel_id in self.__class__.test_novels:
            self.__class__.test_novels.remove(self.__class__.current_test_novel_id)
            
        print(f"成功删除测试小说，ID: {self.__class__.current_test_novel_id}")
    
    def test_12_get_categories(self):
        """测试获取小说分类列表功能"""
        print("\n--- 测试获取小说分类列表 ---")
        
        # 发送获取分类列表请求
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/novel/categories"
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"获取小说分类列表失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("categories", response_data, "响应中没有返回categories列表")
        
        categories = response_data.get("categories")
        self.assertIsInstance(categories, list, "categories不是一个列表")
        
        print(f"成功获取小说分类列表，共 {len(categories)} 个分类")
    
    def test_13_get_novels_by_category(self):
        """测试获取分类小说列表功能"""
        print("\n--- 测试获取分类小说列表 ---")
        
        # 发送获取分类小说请求
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/novel/list?category=奇幻&page=1&per_page=10"
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"获取分类小说列表失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("novels", response_data, "响应中没有返回novels列表")
        self.assertIn("total", response_data, "响应中没有返回total字段")
        self.assertIn("pages", response_data, "响应中没有返回pages字段")
        self.assertIn("current_page", response_data, "响应中没有返回current_page字段")
        
        novels = response_data.get("novels")
        self.assertIsInstance(novels, list, "novels不是一个列表")
        
        print(f"成功获取分类小说列表，共 {len(novels)} 本")
        
    def test_14_get_popular_novels(self):
        """测试获取热门小说功能"""
        print("\n--- 测试获取热门小说 ---")
        
        # 发送获取热门小说请求
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/novel/popular?limit=5"
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"获取热门小说失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("novels", response_data, "响应中没有返回novels列表")
        
        novels = response_data.get("novels")
        self.assertIsInstance(novels, list, "novels不是一个列表")
        
        print(f"成功获取热门小说，共 {len(novels)} 本")
        
    def test_15_get_latest_novels(self):
        """测试获取最新小说功能"""
        print("\n--- 测试获取最新小说 ---")
        
        # 发送获取最新小说请求
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/novel/latest?limit=5"
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"获取最新小说失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("novels", response_data, "响应中没有返回novels列表")
        
        novels = response_data.get("novels")
        self.assertIsInstance(novels, list, "novels不是一个列表")
        
        print(f"成功获取最新小说，共 {len(novels)} 本")

    def test_16_get_all_tags(self):
        """测试获取所有标签列表功能"""
        print("\n--- 测试获取所有标签列表 ---")
        
        # 发送获取标签列表请求
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/novel/tags?sort_by=count&order=desc&limit=20"
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"获取标签列表失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("tags", response_data, "响应中没有返回tags列表")
        
        tags = response_data.get("tags")
        self.assertIsInstance(tags, list, "tags不是一个列表")
        
        print(f"成功获取所有标签列表，共 {len(tags)} 个标签")
    
    def test_17_add_novel_with_tags(self):
        """测试添加带标签的小说功能"""
        print("\n--- 测试添加带标签的小说功能 ---")
        
        # 准备小说数据（包含标签）
        novel_data = {
            "title": f"带标签的测试小说 {random_string()} {get_timestamp()}",
            "category": "奇幻",
            "intro": "这是一本用于测试标签功能的小说",
            "cover": "https://example.com/default-cover.jpg",
            "status": "ongoing",
            "tags": ["标签测试", "奇幻", "冒险"]
        }
        
        # 发送添加小说请求
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/novel/add",
            headers={"Authorization": f"Bearer {self.__class__.author_token}"},
            json=novel_data
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 201, f"添加小说失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("novel_id", response_data, "响应中没有返回novel_id字段")
        
        # 保存小说ID用于后续测试和清理
        novel_id = response_data.get("novel_id")
        self.__class__.test_novels.append(novel_id)
        self.__class__.tag_test_novel_id = novel_id
        
        print(f"成功创建带标签的测试小说，ID: {novel_id}")
    
    def test_18_get_novel_tags(self):
        """测试获取小说标签功能"""
        print("\n--- 测试获取小说标签 ---")
        
        # 确保有测试小说可用
        self.assertTrue(hasattr(self.__class__, 'tag_test_novel_id'), "没有可用的带标签测试小说ID")
        
        # 发送获取小说标签请求
        response = requests.get(
            f"{BASE_URL}{API_PREFIX}/novel/{self.__class__.tag_test_novel_id}/tags"
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"获取小说标签失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("tags", response_data, "响应中没有返回tags列表")
        
        tags = response_data.get("tags")
        self.assertIsInstance(tags, list, "tags不是一个列表")
        self.assertGreater(len(tags), 0, "小说标签列表为空")
        
        # 保存第一个标签ID用于后续移除标签测试
        if len(tags) > 0:
            self.__class__.test_tag_id = tags[0].get('id')
        
        print(f"成功获取小说标签，共 {len(tags)} 个标签")
    
    def test_19_add_tags_to_novel(self):
        """测试为小说添加标签功能"""
        print("\n--- 测试为小说添加标签 ---")
        
        # 确保有测试小说可用
        self.assertTrue(hasattr(self.__class__, 'tag_test_novel_id'), "没有可用的带标签测试小说ID")
        
        # 准备新标签数据
        tag_data = {
            "tags": [f"新标签{random_string(4)}", f"新标签{random_string(4)}"]
        }
        
        # 发送添加标签请求
        response = requests.post(
            f"{BASE_URL}{API_PREFIX}/novel/{self.__class__.tag_test_novel_id}/tags",
            headers={"Authorization": f"Bearer {self.__class__.author_token}"},
            json=tag_data
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"添加标签失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("message", response_data, "响应中没有返回message字段")
        self.assertIn("added_tags", response_data, "响应中没有返回added_tags字段")
        
        added_tags = response_data.get("added_tags")
        self.assertIsInstance(added_tags, list, "added_tags不是一个列表")
        self.assertEqual(len(added_tags), len(tag_data["tags"]), "添加的标签数量不匹配")
        
        print(f"成功为小说添加标签，添加了 {len(added_tags)} 个标签")
    
    def test_20_remove_tag_from_novel(self):
        """测试从小说中移除标签功能"""
        print("\n--- 测试从小说中移除标签 ---")
        
        # 确保有测试小说和标签可用
        self.assertTrue(hasattr(self.__class__, 'tag_test_novel_id'), "没有可用的带标签测试小说ID")
        self.assertTrue(hasattr(self.__class__, 'test_tag_id'), "没有可用的测试标签ID")
        
        # 发送移除标签请求
        response = requests.delete(
            f"{BASE_URL}{API_PREFIX}/novel/{self.__class__.tag_test_novel_id}/tags/{self.__class__.test_tag_id}",
            headers={"Authorization": f"Bearer {self.__class__.author_token}"}
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"移除标签失败，响应: {response.text}")
        
        # 验证响应内容
        response_data = response.json()
        self.assertIn("message", response_data, "响应中没有返回message字段")
        
        print(f"成功从小说中移除标签，ID: {self.__class__.test_tag_id}")
        
    def test_21_delete_tag_test_novel(self):
        """测试删除用于标签测试的小说"""
        print("\n--- 测试删除用于标签测试的小说 ---")
        
        # 确保有测试小说可用
        self.assertTrue(hasattr(self.__class__, 'tag_test_novel_id'), "没有可用的带标签测试小说ID")
        
        # 发送删除小说请求
        response = requests.delete(
            f"{BASE_URL}{API_PREFIX}/novel/{self.__class__.tag_test_novel_id}/delete",
            headers={"Authorization": f"Bearer {self.__class__.author_token}"}
        )
        
        # 验证响应状态码
        self.assertEqual(response.status_code, 200, f"删除小说失败，响应: {response.text}")
        
        # 从待清理列表中移除已删除的小说
        if self.__class__.tag_test_novel_id in self.__class__.test_novels:
            self.__class__.test_novels.remove(self.__class__.tag_test_novel_id)
            
        print(f"成功删除用于标签测试的小说，ID: {self.__class__.tag_test_novel_id}")


def main():
    """主函数"""
    print("\n=========================================")
    print("      小说模块 API 测试脚本开始执行      ")
    print("=========================================\n")
    
    # 创建测试套件
    suite = unittest.TestSuite()
    
    # 按顺序添加测试用例
    test_methods = [
        'test_01_add_novel',
        'test_02_get_novel_detail',
        'test_03_update_novel',
        'test_04_add_chapter',
        'test_05_get_chapter_detail',
        'test_06_update_chapter',
        'test_07_get_all_chapters',
        'test_08_delete_chapter',
        'test_09_search_novels',
        'test_10_get_author_novels',
        'test_11_delete_novel',
        'test_12_get_categories',
        'test_13_get_novels_by_category',
        'test_14_get_popular_novels',
        'test_15_get_latest_novels',
        'test_16_get_all_tags',
        'test_17_add_novel_with_tags',
        'test_18_get_novel_tags',
        'test_19_add_tags_to_novel',
        'test_20_remove_tag_from_novel',
        'test_21_delete_tag_test_novel'
    ]
    
    for test_name in test_methods:
        suite.addTest(TestNovelAPI(test_name))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出测试统计
    print("\n=========================================")
    print("           测试执行完成                 ")
    print(f"总测试用例数: {result.testsRun}")
    print(f"通过测试数: {result.testsRun - len(result.errors) - len(result.failures)}")
    print(f"失败测试数: {len(result.failures)}")
    print(f"错误测试数: {len(result.errors)}")
    print("=========================================\n")
    
    # 返回退出代码
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(main()) 