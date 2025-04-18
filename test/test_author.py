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

class AuthorModuleTest(unittest.TestCase):
    """作者模块测试类"""
    
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
    
    def get_token(self, user_data):
        """获取用户登录token"""
        login_url = f"{self.base_url}/api/user/login"
        response = requests.post(login_url, json=user_data)
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    
    def test_01_get_author_profile(self):
        """测试获取作者信息"""
        # 获取指定作者信息
        author_url = f"{self.base_url}/api/author/profile/testauthor"
        response = requests.get(author_url)
        self.assertEqual(response.status_code, 200)
        author = response.json()
        self.assertEqual(author["username"], "testauthor")
        self.assertEqual(author["pen_name"], "testauthor")
        self.assertIn("author_stats", author)
        
        # 获取不存在的作者
        response = requests.get(f"{self.base_url}/api/author/profile/nonexistent")
        self.assertEqual(response.status_code, 404)
    
    def test_02_get_author_novels(self):
        """测试获取作者的小说列表"""
        novels_url = f"{self.base_url}/api/author/novels/testauthor"
        
        # 获取作者的小说列表
        response = requests.get(novels_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("novels", data)
        self.assertIsInstance(data["novels"], list)
        for novel in data["novels"]:
            self.assertEqual(novel["author"]["username"], "testauthor")
    
    def test_03_apply_author(self):
        """测试申请成为作者"""
        apply_url = f"{self.base_url}/api/author/apply"
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        # 普通用户申请成为作者
        application_data = {
            "pen_name": "新作者笔名",
            "bio": "这是一个新作者的简介",
            "contact_email": "newauthor@example.com"
        }
        
        response = requests.post(apply_url, headers=headers, json=application_data)
        
        # 这里需要注意，如果该用户已经申请过，会返回400
        if response.status_code == 400 and "已经是作者" in response.json().get("error", ""):
            print("用户已经是作者或已申请成为作者")
        else:
            self.assertIn(response.status_code, [201, 202])
            data = response.json()
            self.assertTrue(data.get("success"))
            if response.status_code == 201:
                self.assertIn("author", data)
                self.assertEqual(data["author"]["pen_name"], application_data["pen_name"])
            else:  # 202表示申请已提交，需要审核
                self.assertIn("message", data)
                self.assertIn("申请已提交", data["message"])
    
    def test_04_update_author_profile(self):
        """测试更新作者信息"""
        update_url = f"{self.base_url}/api/author/profile"
        headers = {"Authorization": f"Bearer {self.author_token}"}
        
        # 作者更新自己的信息
        update_data = {
            "bio": "这是更新后的作者简介",
            "contact_email": "updated@example.com"
        }
        
        response = requests.put(update_url, headers=headers, json=update_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data["author"]["bio"], update_data["bio"])
        self.assertEqual(data["author"]["contact_email"], update_data["contact_email"])
        
        # 验证更新是否成功
        author_url = f"{self.base_url}/api/author/profile/testauthor"
        response = requests.get(author_url)
        self.assertEqual(response.status_code, 200)
        author = response.json()
        self.assertEqual(author["bio"], update_data["bio"])
        
        # 普通用户尝试更新作者信息
        user_headers = {"Authorization": f"Bearer {self.user_token}"}
        response = requests.put(update_url, headers=user_headers, json=update_data)
        self.assertEqual(response.status_code, 403)
    
    def test_05_get_author_stats(self):
        """测试获取作者统计信息"""
        stats_url = f"{self.base_url}/api/author/stats/testauthor"
        
        # 获取作者统计信息
        response = requests.get(stats_url)
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        self.assertIn("novel_count", stats)
        self.assertIn("total_words", stats)
        self.assertIn("total_views", stats)
        self.assertIn("total_followers", stats)
        
        # 获取不存在的作者统计
        response = requests.get(f"{self.base_url}/api/author/stats/nonexistent")
        self.assertEqual(response.status_code, 404)
    
    def test_06_follow_author(self):
        """测试关注作者"""
        follow_url = f"{self.base_url}/api/author/follow/testauthor"
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        # 用户关注作者
        response = requests.post(follow_url, headers=headers)
        
        # 可能已经关注过，所以需要处理两种情况
        if response.status_code == 400 and "已经关注" in response.json().get("error", ""):
            print("用户已经关注过该作者")
            
            # 取消关注
            unfollow_url = f"{self.base_url}/api/author/unfollow/testauthor"
            response = requests.post(unfollow_url, headers=headers)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data.get("success"))
            
            # 再次关注
            response = requests.post(follow_url, headers=headers)
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 201)
            data = response.json()
            self.assertTrue(data.get("success"))
        
        # 未登录用户尝试关注
        response = requests.post(follow_url)
        self.assertEqual(response.status_code, 401)
    
    def test_07_get_followers(self):
        """测试获取作者的粉丝列表"""
        followers_url = f"{self.base_url}/api/author/followers/testauthor"
        headers = {"Authorization": f"Bearer {self.author_token}"}
        
        # 作者获取自己的粉丝列表
        response = requests.get(followers_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("followers", data)
        self.assertIsInstance(data["followers"], list)
        
        # 检查刚才关注的用户是否在粉丝列表中
        follower_found = False
        for follower in data["followers"]:
            if follower.get("username") == "testuser":
                follower_found = True
                break
        self.assertTrue(follower_found, "未找到之前关注的用户")
        
        # 普通用户尝试获取粉丝列表
        user_headers = {"Authorization": f"Bearer {self.user_token}"}
        response = requests.get(followers_url, headers=user_headers)
        self.assertEqual(response.status_code, 403)
    
    def test_08_withdraw_author(self):
        """测试注销作者身份"""
        # 这是一个危险测试，不在实际测试中执行，避免影响测试账号
        # 仅做示范，实际执行请谨慎
        
        # withdraw_url = f"{self.base_url}/api/author/withdraw"
        # headers = {"Authorization": f"Bearer {self.author_token}"}
        # 
        # # 作者注销自己的作者身份
        # response = requests.post(withdraw_url, headers=headers, json={
        #     "confirm": True,
        #     "password": self.test_author["password"]
        # })
        # self.assertEqual(response.status_code, 200)
        # data = response.json()
        # self.assertTrue(data.get("success"))
        
        # 为了不影响后续测试，这里不实际执行注销操作
        print("跳过作者身份注销测试，避免影响测试账户")

if __name__ == "__main__":
    unittest.main(verbosity=2) 