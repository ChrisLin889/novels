#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
import unittest

# 导入相对路径的配置
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

BASE_URL = "http://localhost:5000"

class NovelModuleTest(unittest.TestCase):
    """小说模块测试类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.base_url = BASE_URL
        # 测试账户信息
        self.test_user = {
            "username": "testuser",
            "password": "password123",
        }
        self.test_author = {
            "username": "testauthor",
            "password": "password123",
        }
        self.test_admin = {
            "username": "testadmin",
            "password": "password123",
        }
        # 登录并获取token
        self.user_token = self.get_token(self.test_user)
        self.author_token = self.get_token(self.test_author)
        self.admin_token = self.get_token(self.test_admin)
        
        # 创建测试小说
        self.create_test_novel()
    
    def get_token(self, user_data):
        """获取用户登录token"""
        login_url = f"{self.base_url}/api/user/login"
        response = requests.post(login_url, json=user_data)
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    
    def create_test_novel(self):
        """创建测试小说"""
        if not self.author_token:
            self.fail("作者账户登录失败，无法继续测试")
            
        create_url = f"{self.base_url}/api/novel"
        headers = {"Authorization": f"Bearer {self.author_token}"}
        
        # 检查是否已存在测试小说
        novels_url = f"{self.base_url}/api/novel/list"
        response = requests.get(novels_url, params={"author": "testauthor"})
        if response.status_code == 200:
            novels = response.json().get("novels", [])
            for novel in novels:
                if novel.get("title") == "测试小说":
                    self.test_novel_id = novel.get("id")
                    return
        
        # 创建新的测试小说
        novel_data = {
            "title": "测试小说",
            "description": "这是一个用于测试的小说",
            "category": "科幻",
            "tags": ["测试", "科幻"],
            "status": "连载中"
        }
        
        response = requests.post(create_url, headers=headers, json=novel_data)
        if response.status_code == 201:
            self.test_novel_id = response.json().get("novel", {}).get("id")
        else:
            self.fail(f"创建测试小说失败: {response.text}")
    
    def test_01_get_novel_list(self):
        """测试获取小说列表"""
        list_url = f"{self.base_url}/api/novel/list"
        
        # 获取所有小说
        response = requests.get(list_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("novels", data)
        self.assertIsInstance(data["novels"], list)
        
        # 按分类筛选
        response = requests.get(list_url, params={"category": "科幻"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for novel in data["novels"]:
            self.assertEqual(novel["category"], "科幻")
        
        # 按作者筛选
        response = requests.get(list_url, params={"author": "testauthor"})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for novel in data["novels"]:
            self.assertEqual(novel["author"]["username"], "testauthor")
    
    def test_02_get_novel_detail(self):
        """测试获取小说详情"""
        if not hasattr(self, 'test_novel_id'):
            self.fail("没有测试小说ID，无法继续测试")
            
        detail_url = f"{self.base_url}/api/novel/{self.test_novel_id}"
        
        # 获取小说详情
        response = requests.get(detail_url)
        self.assertEqual(response.status_code, 200)
        novel = response.json()
        self.assertEqual(novel["title"], "测试小说")
        self.assertEqual(novel["author"]["username"], "testauthor")
        
        # 获取不存在的小说
        response = requests.get(f"{self.base_url}/api/novel/999999")
        self.assertEqual(response.status_code, 404)
    
    def test_03_update_novel(self):
        """测试更新小说信息"""
        if not hasattr(self, 'test_novel_id'):
            self.fail("没有测试小说ID，无法继续测试")
            
        update_url = f"{self.base_url}/api/novel/{self.test_novel_id}"
        headers = {"Authorization": f"Bearer {self.author_token}"}
        
        # 作者更新小说
        update_data = {
            "description": "这是更新后的小说描述",
            "tags": ["测试", "科幻", "更新"]
        }
        response = requests.put(update_url, headers=headers, json=update_data)
        self.assertEqual(response.status_code, 200)
        novel = response.json().get("novel", {})
        self.assertEqual(novel["description"], update_data["description"])
        self.assertEqual(set(novel["tags"]), set(update_data["tags"]))
        
        # 普通用户尝试更新小说
        user_headers = {"Authorization": f"Bearer {self.user_token}"}
        response = requests.put(update_url, headers=user_headers, json=update_data)
        self.assertEqual(response.status_code, 403)
    
    def test_04_add_chapter(self):
        """测试添加章节"""
        if not hasattr(self, 'test_novel_id'):
            self.fail("没有测试小说ID，无法继续测试")
            
        chapter_url = f"{self.base_url}/api/novel/{self.test_novel_id}/chapter"
        headers = {"Authorization": f"Bearer {self.author_token}"}
        
        # 作者添加章节
        chapter_data = {
            "title": "测试章节",
            "content": "这是测试章节的内容，用于测试章节添加功能。",
            "chapter_number": 1
        }
        response = requests.post(chapter_url, headers=headers, json=chapter_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data.get("success"))
        self.test_chapter_id = data.get("chapter", {}).get("id")
        
        # 普通用户尝试添加章节
        user_headers = {"Authorization": f"Bearer {self.user_token}"}
        response = requests.post(chapter_url, headers=user_headers, json={
            "title": "非法章节",
            "content": "这是非法添加的章节内容。",
            "chapter_number": 2
        })
        self.assertEqual(response.status_code, 403)
    
    def test_05_get_chapters(self):
        """测试获取章节列表"""
        if not hasattr(self, 'test_novel_id'):
            self.fail("没有测试小说ID，无法继续测试")
            
        chapters_url = f"{self.base_url}/api/novel/{self.test_novel_id}/chapters"
        
        # 获取章节列表
        response = requests.get(chapters_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("chapters", data)
        self.assertIsInstance(data["chapters"], list)
        
        # 检查是否包含之前添加的章节
        if hasattr(self, 'test_chapter_id'):
            chapter_found = False
            for chapter in data["chapters"]:
                if chapter.get("id") == self.test_chapter_id:
                    chapter_found = True
                    self.assertEqual(chapter["title"], "测试章节")
                    break
            self.assertTrue(chapter_found, "未找到之前添加的章节")
    
    def test_06_read_chapter(self):
        """测试阅读章节"""
        if not hasattr(self, 'test_novel_id') or not hasattr(self, 'test_chapter_id'):
            self.fail("没有测试小说ID或章节ID，无法继续测试")
            
        chapter_url = f"{self.base_url}/api/novel/chapter/{self.test_chapter_id}"
        
        # 匿名用户阅读章节
        response = requests.get(chapter_url)
        self.assertEqual(response.status_code, 200)
        chapter = response.json()
        self.assertEqual(chapter["title"], "测试章节")
        self.assertIn("content", chapter)
        
        # 登录用户阅读章节
        headers = {"Authorization": f"Bearer {self.user_token}"}
        response = requests.get(chapter_url, headers=headers)
        self.assertEqual(response.status_code, 200)
    
    def test_07_update_chapter(self):
        """测试更新章节"""
        if not hasattr(self, 'test_novel_id') or not hasattr(self, 'test_chapter_id'):
            self.fail("没有测试小说ID或章节ID，无法继续测试")
            
        chapter_url = f"{self.base_url}/api/novel/chapter/{self.test_chapter_id}/update"
        headers = {"Authorization": f"Bearer {self.author_token}"}
        
        # 更新章节内容
        update_data = {
            "title": "更新后的测试章节",
            "content": "这是更新后的测试章节内容。"
        }
        response = requests.put(chapter_url, headers=headers, json=update_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        
        # 验证更新是否成功
        get_chapter_url = f"{self.base_url}/api/novel/chapter/{self.test_chapter_id}"
        response = requests.get(get_chapter_url)
        self.assertEqual(response.status_code, 200)
        chapter = response.json()
        self.assertEqual(chapter["title"], update_data["title"])
        self.assertEqual(chapter["content"], update_data["content"])
        
        # 普通用户尝试更新章节
        user_headers = {"Authorization": f"Bearer {self.user_token}"}
        response = requests.put(chapter_url, headers=user_headers, json={
            "title": "非法更新的章节",
            "content": "这是非法更新的内容。"
        })
        self.assertEqual(response.status_code, 403)
    
    def test_08_delete_chapter(self):
        """测试删除章节"""
        if not hasattr(self, 'test_novel_id') or not hasattr(self, 'test_chapter_id'):
            self.fail("没有测试小说ID或章节ID，无法继续测试")
            
        chapter_url = f"{self.base_url}/api/novel/chapter/{self.test_chapter_id}/delete"
        
        # 普通用户尝试删除章节
        user_headers = {"Authorization": f"Bearer {self.user_token}"}
        response = requests.delete(chapter_url, headers=user_headers)
        self.assertEqual(response.status_code, 403)
        
        # 作者删除章节
        author_headers = {"Authorization": f"Bearer {self.author_token}"}
        response = requests.delete(chapter_url, headers=author_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        
        # 验证删除是否成功
        get_chapter_url = f"{self.base_url}/api/novel/chapter/{self.test_chapter_id}"
        response = requests.get(get_chapter_url)
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main(verbosity=2) 