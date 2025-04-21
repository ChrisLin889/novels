# 测试用户账户信息

本目录包含用于作者模块功能测试的测试用户账户。

## 普通用户

| 用户名 | 密码 | 邮箱 | 手机号 | ID |
|-------|------|------|-------|-----|
| testuser1 | password123 | testuser1@example.com | - | 24 |
| testuser2 | password123 | testuser2@example.com | - | 25 |
| testuser3 | password123 | - | 13800138000 | 26 |

## 潜在作者用户

> **注意**: 以下账号目前仅为普通用户账号，尚未成为作者。需要通过作者模块的相关API（如申请成为作者）将其转换为作者账号。

| 用户名 | 密码 | 邮箱 | 手机号 | ID |
|-------|------|------|-------|-----|
| testauthor1 | password123 | testauthor1@example.com | - | 27 |
| testauthor2 | password123 | testauthor2@example.com | 13900139000 | 28 |

## 使用说明

1. 这些用户可用于测试作者模块的各项功能
2. 用户信息以JSON格式保存在相应的文件中
3. 用户登录可使用用户名、邮箱或手机号，配合密码进行登录
4. 登录API示例：`/api/user/login`
5. 请参考用户模块API文档获取更多信息 