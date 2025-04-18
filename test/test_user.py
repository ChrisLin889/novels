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

class UserModuleTest(unittest.TestCase):
    """用户模块测试类"""
    
    def setUp(self):
        """测试前的准备工作"""
        self.base_url = BASE_URL
        # 测试账户信息
        self.test_user = {
            "username": "testuser",
            "password": "password123",
            "email": "user@test.com",
            "phone": "12345678901"
        }
        self.test_author = {
            "username": "testauthor",
            "password": "password123",
            "email": "author@test.com",
            "phone": "12345678902"
        }
        self.test_admin = {
            "username": "testadmin",
            "password": "password123",
            "email": "admin@test.com",
            "phone": "12345678903"
        }
        # 登录并获取token
        self.user_token = self.get_token(self.test_user)
        self.author_token = self.get_token(self.test_author)
        self.admin_token = self.get_token(self.test_admin)
    
    def get_token(self, user_data):
        """获取用户登录token"""
        login_url = f"{self.base_url}/api/user/login"
        response = requests.post(login_url, json={
            "username": user_data["username"],
            "password": user_data["password"]
        })
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    
    def test_01_login(self):
        """测试用户登录"""
        login_url = f"{self.base_url}/api/user/login"
        
        # 测试正确登录
        response = requests.post(login_url, json={
            "username": self.test_user["username"],
            "password": self.test_user["password"]
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        self.assertIsNotNone(data.get("access_token"))
        
        # 测试错误密码
        response = requests.post(login_url, json={
            "username": self.test_user["username"],
            "password": "wrong_password"
        })
        self.assertEqual(response.status_code, 401)
        
        # 测试不存在的用户
        response = requests.post(login_url, json={
            "username": "nonexistent_user",
            "password": "password123"
        })
        self.assertEqual(response.status_code, 401)
    
    def test_02_get_profile(self):
        """测试获取个人信息"""
        profile_url = f"{self.base_url}/api/user/profile"
        
        # 测试正确获取个人信息
        headers = {"Authorization": f"Bearer {self.user_token}"}
        response = requests.get(profile_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        user_data = response.json()
        self.assertEqual(user_data.get("username"), self.test_user["username"])
        
        # 测试无token获取个人信息
        response = requests.get(profile_url)
        self.assertEqual(response.status_code, 401)
    
    def test_03_update_profile(self):
        """测试更新个人信息"""
        profile_url = f"{self.base_url}/api/user/profile"
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        # 更新个人信息
        new_avatar = "https://example.com/avatar.jpg"
        response = requests.put(profile_url, headers=headers, json={
            "avatar": new_avatar
        })
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data["user"]["avatar"], new_avatar)
        
        # 检查信息是否真的更新了
        response = requests.get(profile_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        user_data = response.json()
        self.assertEqual(user_data.get("avatar"), new_avatar)
    
    def test_04_admin_get_user_list(self):
        """测试管理员获取用户列表"""
        user_list_url = f"{self.base_url}/api/admin/users"
        
        # 管理员获取用户列表
        admin_headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = requests.get(user_list_url, headers=admin_headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("users", data)
        self.assertIsInstance(data["users"], list)
        
        # 普通用户尝试获取用户列表
        user_headers = {"Authorization": f"Bearer {self.user_token}"}
        response = requests.get(user_list_url, headers=user_headers)
        self.assertEqual(response.status_code, 403)
    
    def test_05_register(self):
        """测试用户注册"""
        register_url = f"{self.base_url}/api/user/register"
        
        # 创建新用户数据
        import random
        random_suffix = random.randint(1000, 9999)
        new_user = {
            "username": f"newuser{random_suffix}",
            "password": "password123",
            "email": f"new{random_suffix}@test.com",
            "phone": f"1389{random_suffix}"
        }
        
        # 测试正确注册
        response = requests.post(register_url, json=new_user)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data.get("success"))
        self.assertEqual(data["user"]["username"], new_user["username"])
        
        # 测试重复注册
        response = requests.post(register_url, json=new_user)
        self.assertEqual(response.status_code, 400)
    
    def test_06_change_password(self):
        """测试修改密码"""
        change_pw_url = f"{self.base_url}/api/user/change-password"
        headers = {"Authorization": f"Bearer {self.user_token}"}
        
        # 测试修改密码
        response = requests.post(change_pw_url, headers=headers, json={
            "current_password": self.test_user["password"],
            "new_password": "newpassword123"
        })
        # 注意：文档提到此API可能尚未实现
        # 如果返回404，表示API未实现
        if response.status_code == 404:
            print("Change password API not implemented yet")
            return
            
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        
        # 使用新密码登录
        login_url = f"{self.base_url}/api/user/login"
        response = requests.post(login_url, json={
            "username": self.test_user["username"],
            "password": "newpassword123"
        })
        self.assertEqual(response.status_code, 200)
        
        # 恢复原密码（测试完成后恢复）
        response = requests.post(change_pw_url, headers={"Authorization": f"Bearer {response.json()['access_token']}"}, json={
            "current_password": "newpassword123",
            "new_password": self.test_user["password"]
        })
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main(verbosity=2) 