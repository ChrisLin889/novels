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

class AdminModuleTest(unittest.TestCase):
    """管理模块测试类"""
    
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
    
    def test_01_dashboard_stats(self):
        """测试获取仪表盘统计数据"""
        if not self.admin_token:
            self.skipTest("管理员登录失败，跳过仪表盘测试")
            
        dashboard_url = f"{self.base_url}/api/admin/dashboard"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # 管理员获取仪表盘数据
        response = requests.get(dashboard_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("user_stats", data)
        self.assertIn("novel_stats", data)
        self.assertIn("interaction_stats", data)
        self.assertIn("recent_activities", data)
        
        # 普通用户尝试获取仪表盘数据
        user_headers = {"Authorization": f"Bearer {self.user_token}"}
        response = requests.get(dashboard_url, headers=user_headers)
        self.assertEqual(response.status_code, 403)
        
        # 未登录用户尝试获取仪表盘数据
        response = requests.get(dashboard_url)
        self.assertEqual(response.status_code, 401)
    
    def test_02_user_management(self):
        """测试用户管理功能"""
        if not self.admin_token:
            self.skipTest("管理员登录失败，跳过用户管理测试")
            
        users_url = f"{self.base_url}/api/admin/users"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # 获取用户列表
        response = requests.get(users_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("users", data)
        self.assertIsInstance(data["users"], list)
        
        # 模拟创建用户
        import random
        username = f"testuser{random.randint(1000, 9999)}"
        create_data = {
            "username": username,
            "password": "password123",
            "email": f"{username}@example.com",
            "phone": f"1399{random.randint(100000, 999999)}",
            "role": "user"
        }
        
        response = requests.post(users_url, headers=headers, json=create_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data.get("success"))
        self.assertIn("user", data)
        user_id = data["user"]["id"]
        
        # 修改用户状态
        status_url = f"{self.base_url}/api/admin/user/{user_id}/status"
        status_data = {
            "status": "disabled",
            "reason": "测试禁用账户"
        }
        
        response = requests.put(status_url, headers=headers, json=status_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        
        # 获取用户详情
        detail_url = f"{self.base_url}/api/admin/user/{user_id}"
        response = requests.get(detail_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        user = response.json()
        self.assertEqual(user["status"], "disabled")
        
        # 恢复用户状态
        status_data = {
            "status": "active",
            "reason": "测试恢复账户"
        }
        
        response = requests.put(status_url, headers=headers, json=status_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        
        # 删除测试用户
        response = requests.delete(detail_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        
        # 验证删除是否成功
        response = requests.get(detail_url, headers=headers)
        self.assertEqual(response.status_code, 404)
    
    def test_03_content_management(self):
        """测试内容管理功能"""
        if not self.admin_token:
            self.skipTest("管理员登录失败，跳过内容管理测试")
            
        novels_url = f"{self.base_url}/api/admin/novels"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # 获取小说列表
        response = requests.get(novels_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("novels", data)
        self.assertIsInstance(data["novels"], list)
        
        # 如果有小说，测试内容审核功能
        if data["novels"]:
            novel_id = data["novels"][0]["id"]
            
            # 审核小说
            review_url = f"{self.base_url}/api/admin/novel/{novel_id}/review"
            review_data = {
                "status": "approved",
                "comment": "内容审核通过"
            }
            
            response = requests.put(review_url, headers=headers, json=review_data)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data.get("success"))
            
            # 验证审核是否成功
            detail_url = f"{self.base_url}/api/admin/novel/{novel_id}"
            response = requests.get(detail_url, headers=headers)
            self.assertEqual(response.status_code, 200)
            novel = response.json()
            self.assertEqual(novel["review_status"], "approved")
    
    def test_04_report_management(self):
        """测试举报管理功能"""
        if not self.admin_token:
            self.skipTest("管理员登录失败，跳过举报管理测试")
            
        reports_url = f"{self.base_url}/api/admin/reports"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # 获取举报列表
        response = requests.get(reports_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("reports", data)
        self.assertIsInstance(data["reports"], list)
        
        # 如果有举报，测试处理举报功能
        if data["reports"]:
            report_id = data["reports"][0]["id"]
            
            # 处理举报
            process_url = f"{self.base_url}/api/admin/report/{report_id}"
            process_data = {
                "status": "processed",
                "action": "no_action",
                "comment": "测试处理举报，无需采取行动"
            }
            
            response = requests.put(process_url, headers=headers, json=process_data)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data.get("success"))
            
            # 验证处理是否成功
            response = requests.get(f"{reports_url}/{report_id}", headers=headers)
            self.assertEqual(response.status_code, 200)
            report = response.json()
            self.assertEqual(report["status"], "processed")
    
    def test_05_author_approval(self):
        """测试作者申请审批功能"""
        if not self.admin_token:
            self.skipTest("管理员登录失败，跳过作者审批测试")
            
        applications_url = f"{self.base_url}/api/admin/author-applications"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # 获取作者申请列表
        response = requests.get(applications_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("applications", data)
        self.assertIsInstance(data["applications"], list)
        
        # 如果有申请，测试审批功能
        if data["applications"]:
            application_id = data["applications"][0]["id"]
            
            # 审批作者申请
            approve_url = f"{self.base_url}/api/admin/author-application/{application_id}"
            approve_data = {
                "status": "approved",
                "comment": "测试审批作者申请"
            }
            
            response = requests.put(approve_url, headers=headers, json=approve_data)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data.get("success"))
            
            # 验证审批是否成功
            response = requests.get(f"{applications_url}/{application_id}", headers=headers)
            self.assertEqual(response.status_code, 200)
            application = response.json()
            self.assertEqual(application["status"], "approved")
    
    def test_06_system_settings(self):
        """测试系统设置功能"""
        if not self.admin_token:
            self.skipTest("管理员登录失败，跳过系统设置测试")
            
        settings_url = f"{self.base_url}/api/admin/settings"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # 获取系统设置
        response = requests.get(settings_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("settings", data)
        self.assertIsInstance(data["settings"], dict)
        
        # 更新系统设置
        update_data = {
            "site_name": "测试小说平台",
            "maintenance_mode": False,
            "registration_enabled": True,
            "max_upload_size": 5,
            "default_user_avatar": "https://example.com/default-avatar.png"
        }
        
        response = requests.put(settings_url, headers=headers, json=update_data)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success"))
        
        # 验证更新是否成功
        response = requests.get(settings_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        settings = data["settings"]
        for key, value in update_data.items():
            self.assertEqual(settings.get(key), value)
    
    def test_07_logs(self):
        """测试系统日志功能"""
        if not self.admin_token:
            self.skipTest("管理员登录失败，跳过系统日志测试")
            
        logs_url = f"{self.base_url}/api/admin/logs"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # 获取系统日志
        response = requests.get(logs_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("logs", data)
        self.assertIsInstance(data["logs"], list)
        
        # 按类型筛选日志
        params = {
            "type": "error",
            "limit": 10
        }
        response = requests.get(logs_url, headers=headers, params=params)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        for log in data["logs"]:
            self.assertEqual(log["level"], "error")
    
    def test_08_backup(self):
        """测试数据备份功能"""
        if not self.admin_token:
            self.skipTest("管理员登录失败，跳过数据备份测试")
            
        backup_url = f"{self.base_url}/api/admin/backup"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # 创建数据备份
        response = requests.post(backup_url, headers=headers)
        self.assertEqual(response.status_code, 202)
        data = response.json()
        self.assertTrue(data.get("success"))
        
        # 获取备份列表
        response = requests.get(backup_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("backups", data)
        self.assertIsInstance(data["backups"], list)
    
    def test_09_notifications(self):
        """测试系统通知功能"""
        if not self.admin_token:
            self.skipTest("管理员登录失败，跳过系统通知测试")
            
        notification_url = f"{self.base_url}/api/admin/notification"
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        
        # 创建系统通知
        notification_data = {
            "title": "测试通知",
            "content": "这是一条测试系统通知",
            "type": "announcement",
            "target_users": "all",
            "expires_at": "2099-12-31T23:59:59"
        }
        
        response = requests.post(notification_url, headers=headers, json=notification_data)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data.get("success"))
        notification_id = data.get("notification", {}).get("id")
        
        # 获取通知列表
        response = requests.get(notification_url, headers=headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("notifications", data)
        self.assertIsInstance(data["notifications"], list)
        
        # 删除测试通知
        if notification_id:
            response = requests.delete(f"{notification_url}/{notification_id}", headers=headers)
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertTrue(data.get("success"))

if __name__ == "__main__":
    unittest.main(verbosity=2)