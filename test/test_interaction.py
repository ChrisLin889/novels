#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import requests
import unittest
import time

# 导入相对路径的配置
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

BASE_URL = "http://localhost:5000"

class InteractionModuleTest(unittest.TestCase):
    """互动模块测试类"""
    
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
        
        # 获取测试小说和章节ID
        self.get_test_resources()
    
    def get_token(self, user_data):
        """获取用户登录token"""
        login_url = f"{self.base_url}/api/user/login"
        response = requests.post(login_url, json=user_data)
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    
    def get_test_resources(self):
        """获取测试小说和章节ID"""
        # 获取测试作者的小说
        novels_url = f"{self.base_url}/api/author/novels/testauthor"
        response = requests.get(novels_url)
        if response.status_code == 200:
            novels = response.json().get("novels", [])
            if novels:
                self.test_novel_id = novels[0].get("id")
                
                # 获取章节
                chapters_url = f"{self.base_url}/api/novel/{self.test_novel_id}/chapters"
                response = requests.get(chapters_url)
                if response.status_code == 200:
                    chapters = response.json().get("chapters", [])
                    if chapters:
                        self.test_chapter_id = chapters[0].get("id")
    
    def test_01_add_comment(self):
        """测试添加评论"""
        if not hasattr(self, 'test_novel_id'):
            self.skipTest("没有测试小说，跳过评论测试")
            
        comment_url = f"{self.base_url}/api/interaction/comment"
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        # 对小说添加评论
        comment_data = {
            "target_type": "novel",
            "target_id": self.test_novel_id,
            "content": f"这是一条测试评论 {time.time()}"
        }
        
        response = requests.post(comment_url, headers=headers, json=comment_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data.get("success"))
        self.assertIn("comment", data)
        self.test_comment_id = data["comment"]["id"]
        
        # 未登录用户尝试评论
        response = requests.post(comment_url, json=comment_data)
        self.assertEqual(response.status_code, 401)
        
        # 对章节添加评论（如果有测试章节）
        if hasattr(self, 'test_chapter_id'):
            chapter_comment_data = {
                "target_type": "chapter",
                "target_id": self.test_chapter_id,
                "content": f"这是对章节的测试评论 {time.time()}"
            }
            
            response = requests.post(comment_url, headers=headers, json=chapter_comment_data)
            self.assertEqual(response.status_code, 201)
            data = response.json()
            self.assertTrue(data.get("success"))
    
    def test_02_get_comments(self):
        """测试获取评论列表"""
        if not hasattr(self, 'test_novel_id'):
            self.skipTest("没有测试小说，跳过评论测试")
            
        # 获取小说评论
        comments_url = f"{self.base_url}/api/interaction/comments"
        params = {
            "target_type": "novel",
            "target_id": self.test_novel_id
        }
        
        response = requests.get(comments_url, params=params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("comments", data)
        self.assertIsInstance(data["comments"], list)
        
        # 验证之前添加的评论是否存在
        if hasattr(self, 'test_comment_id'):
            comment_found = False
            for comment in data["comments"]:
                if comment.get("id") == self.test_comment_id:
                    comment_found = True
                    break
            self.assertTrue(comment_found, "未找到之前添加的评论")
    
    def test_03_reply_comment(self):
        """测试回复评论"""
        if not hasattr(self, 'test_comment_id'):
            self.skipTest("没有测试评论，跳过回复测试")
            
        reply_url = f"{self.base_url}/api/interaction/reply"
        headers = {"Authorization": f"Bearer {self.author_token}"}
        
        # 作者回复评论
        reply_data = {
            "parent_id": self.test_comment_id,
            "content": f"这是一条测试回复 {time.time()}"
        }
        
        response = requests.post(reply_url, headers=headers, json=reply_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data.get("success"))
        self.assertIn("reply", data)
        self.test_reply_id = data["reply"]["id"]
        
        # 验证回复是否成功
        comments_url = f"{self.base_url}/api/interaction/comment/{self.test_comment_id}/replies"
        response = requests.get(comments_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("replies", data)
        self.assertIsInstance(data["replies"], list)
        self.assertTrue(len(data["replies"]) > 0)
    
    def test_04_like_comment(self):
        """测试点赞评论"""
        if not hasattr(self, 'test_comment_id'):
            self.skipTest("没有测试评论，跳过点赞测试")
            
        like_url = f"{self.base_url}/api/interaction/like"
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        # 用户点赞评论
        like_data = {
            "target_type": "comment",
            "target_id": self.test_comment_id
        }
        
        response = requests.post(like_url, headers=headers, json=like_data)
        
        # 由于可能已经点赞过，所以需要处理两种情况
        if response.status_code == 400 and "已经点赞" in response.json().get("error", ""):
            print("用户已经点赞过该评论")
            
            # 取消点赞
            unlike_url = f"{self.base_url}/api/interaction/unlike"
            response = requests.post(unlike_url, headers=headers, json=like_data)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data.get("success"))
            
            # 再次点赞
            response = requests.post(like_url, headers=headers, json=like_data)
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 201)
            data = response.json()
            self.assertTrue(data.get("success"))
        
        # 未登录用户尝试点赞
        response = requests.post(like_url, json=like_data)
        self.assertEqual(response.status_code, 401)
    
    def test_05_collect_novel(self):
        """测试收藏小说"""
        if not hasattr(self, 'test_novel_id'):
            self.skipTest("没有测试小说，跳过收藏测试")
            
        collect_url = f"{self.base_url}/api/interaction/collect"
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        # 用户收藏小说
        collect_data = {
            "novel_id": self.test_novel_id
        }
        
        response = requests.post(collect_url, headers=headers, json=collect_data)
        
        # 由于可能已经收藏过，所以需要处理两种情况
        if response.status_code == 400 and "已经收藏" in response.json().get("error", ""):
            print("用户已经收藏过该小说")
            
            # 取消收藏
            uncollect_url = f"{self.base_url}/api/interaction/uncollect"
            response = requests.post(uncollect_url, headers=headers, json=collect_data)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data.get("success"))
            
            # 再次收藏
            response = requests.post(collect_url, headers=headers, json=collect_data)
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 201)
            data = response.json()
            self.assertTrue(data.get("success"))
        
        # 未登录用户尝试收藏
        response = requests.post(collect_url, json=collect_data)
        self.assertEqual(response.status_code, 401)
    
    def test_06_get_collections(self):
        """测试获取收藏列表"""
        collections_url = f"{self.base_url}/api/user/collections"
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        # 获取用户收藏列表
        response = requests.get(collections_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("collections", data)
        self.assertIsInstance(data["collections"], list)
        
        # 验证之前收藏的小说是否存在
        if hasattr(self, 'test_novel_id'):
            novel_found = False
            for collection in data["collections"]:
                if collection.get("novel", {}).get("id") == self.test_novel_id:
                    novel_found = True
                    break
            self.assertTrue(novel_found, "未找到之前收藏的小说")
    
    def test_07_rate_novel(self):
        """测试评分小说"""
        if not hasattr(self, 'test_novel_id'):
            self.skipTest("没有测试小说，跳过评分测试")
            
        rate_url = f"{self.base_url}/api/interaction/rate"
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        # 用户评分小说
        rate_data = {
            "novel_id": self.test_novel_id,
            "score": 4.5,  # 评分范围通常是1-5
            "comment": "这是一条评分评论"
        }
        
        response = requests.post(rate_url, headers=headers, json=rate_data)
        
        # 由于可能已经评分过，所以需要处理两种情况
        if response.status_code == 400 and "已经评分" in response.json().get("error", ""):
            print("用户已经评分过该小说")
            
            # 更新评分
            response = requests.put(rate_url, headers=headers, json=rate_data)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data.get("success"))
        else:
            self.assertEqual(response.status_code, 201)
            data = response.json()
            self.assertTrue(data.get("success"))
        
        # 未登录用户尝试评分
        response = requests.post(rate_url, json=rate_data)
        self.assertEqual(response.status_code, 401)
    
    def test_08_report_content(self):
        """测试举报内容"""
        if not hasattr(self, 'test_novel_id'):
            self.skipTest("没有测试小说，跳过举报测试")
            
        report_url = f"{self.base_url}/api/interaction/report"
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        # 用户举报小说
        report_data = {
            "target_type": "novel",
            "target_id": self.test_novel_id,
            "reason": "测试举报",
            "description": "这是一条测试举报，用于测试举报功能"
        }
        
        response = requests.post(report_url, headers=headers, json=report_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data.get("success"))
        
        # 未登录用户尝试举报
        response = requests.post(report_url, json=report_data)
        self.assertEqual(response.status_code, 401)
        
        # 如果有评论，测试举报评论
        if hasattr(self, 'test_comment_id'):
            comment_report_data = {
                "target_type": "comment",
                "target_id": self.test_comment_id,
                "reason": "测试举报评论",
                "description": "这是一条测试举报评论，用于测试举报功能"
            }
            
            response = requests.post(report_url, headers=headers, json=comment_report_data)
            self.assertEqual(response.status_code, 201)
            data = response.json()
            self.assertTrue(data.get("success"))
    
    def test_09_delete_comment(self):
        """测试删除评论"""
        if not hasattr(self, 'test_comment_id'):
            self.skipTest("没有测试评论，跳过删除测试")
            
        # 先创建一个新评论用于删除测试
        comment_url = f"{self.base_url}/api/interaction/comment"
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        comment_data = {
            "target_type": "novel",
            "target_id": self.test_novel_id,
            "content": f"这是将要被删除的测试评论 {time.time()}"
        }
        
        response = requests.post(comment_url, headers=headers, json=comment_data)
        self.assertEqual(response.status_code, 201)
        delete_comment_id = response.json()["comment"]["id"]
        
        # 删除评论
        delete_url = f"{self.base_url}/api/interaction/comment/{delete_comment_id}"
        response = requests.delete(delete_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        
        # 验证删除是否成功
        comments_url = f"{self.base_url}/api/interaction/comments"
        params = {
            "target_type": "novel",
            "target_id": self.test_novel_id
        }
        
        response = requests.get(comments_url, params=params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        comment_found = False
        for comment in data["comments"]:
            if comment.get("id") == delete_comment_id:
                comment_found = True
                break
        self.assertFalse(comment_found, "评论仍然存在，删除失败")

if __name__ == "__main__":
    unittest.main(verbosity=2) 