# 用户注册与注销测试文档

## 测试环境

- MySQL 版本：系统默认MySQL
- 后端API运行在端口：5000
- 数据库连接：MySQL (root:ok123456)

## 测试流程

### 1. 初始环境准备

测试开始时我们发现数据库模式与代码模型之间存在不匹配，User 模型中定义了 `banned_until` 字段，但该字段在数据库中不存在。执行以下SQL语句添加了该字段：

```sql
ALTER TABLE novel_db.user ADD COLUMN banned_until DATETIME DEFAULT NULL;
```

### 2. 用户注册测试

#### API 请求:

```bash
curl -X POST http://localhost:5000/api/user/register -H "Content-Type: application/json" -d '{"username": "testuser2", "password": "password123", "email": "test2@example.com"}'
```

#### 响应结果:

```json
{
  "message": "User registered successfully",
  "success": true,
  "user": {
    "created_at": "2025-04-19T12:31:21",
    "email": "test2@example.com",
    "id": 7,
    "phone": null,
    "username": "testuser2"
  }
}
```

#### 数据库验证:

```sql
SELECT id, username, email, created_at FROM novel_db.user WHERE username='testuser2';
```

结果显示用户已成功添加到数据库中：

```
+----+-----------+-------------------+---------------------+
| id | username  | email             | created_at          |
+----+-----------+-------------------+---------------------+
|  7 | testuser2 | test2@example.com | 2025-04-19 12:31:21 |
+----+-----------+-------------------+---------------------+
```

### 3. 用户登录测试

#### API 请求:

```bash
curl -X POST http://localhost:5000/api/user/login -H "Content-Type: application/json" -d '{"username": "testuser2", "password": "password123"}'
```

#### 响应结果:

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "success": true,
  "user": {
    "avatar": "default.jpg",
    "created_at": "2025-04-19T12:31:21",
    "email": "test2@example.com",
    "id": 7,
    "phone": null,
    "role": "user",
    "status": "active",
    "updated_at": "2025-04-19T20:31:40",
    "username": "testuser2"
  }
}
```

### 4. 用户注销测试

在使用API注销用户时，我们遇到了一个错误：User对象没有'role'属性，但deactivate_account函数尝试检查user.role是否等于'admin'。这表明代码中存在不一致的地方。

错误信息:
```
AttributeError: 'User' object has no attribute 'role'
```

为了完成测试，我们直接使用SQL从数据库中删除了用户：

```sql
DELETE FROM novel_db.user WHERE username='testuser2';
```

查询验证用户已被成功删除：

```sql
SELECT id, username, email FROM novel_db.user WHERE username='testuser2';
```

没有返回任何结果，表明用户已被成功删除。

## 测试结论

1. **用户注册功能正常工作**：
   - API能够成功接收请求并创建新用户
   - 数据库中正确存储了用户信息

2. **用户登录功能正常工作**：
   - 成功验证凭据并返回JWT令牌
   - 返回适当的用户信息

3. **用户注销功能存在问题**：
   - 发现代码与数据库模型之间存在不一致
   - User对象没有直接的'role'属性，但代码尝试访问它
   - 建议修改UserService.deactivate_account方法，使用PermissionService.get_user_role(user.id)来正确获取用户角色

## 改进建议

1. 修复deactivate_account方法中的role检查，可以改为：
```python
# 使用PermissionService获取角色而不是直接访问user.role
from app.services.permission_service import PermissionService
user_role = PermissionService.get_user_role(user.id)
if user_role == 'admin':
    # ...
```

2. 确保所有数据库更改都通过适当的迁移脚本进行管理，避免模型和数据库架构不匹配的问题。

3. 在部署前运行全面的集成测试，确保所有API端点按预期工作。 