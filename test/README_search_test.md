# 搜索模块 API 测试指南

本文档提供搜索模块API测试脚本的使用指南。

## 测试内容

`test_search_api.py` 脚本测试了以下搜索模块API功能:

1. 小说搜索 (`/api/search/novels`)
2. 标签搜索 (`/api/search/novels/tag/{tag}`)
3. 相似小说推荐 (`/api/search/similar/{novel_id}`)
4. 获取热门标签 (`/api/search/tags/hot`)

## 运行环境要求

- Python 3.6+
- requests 库

## 运行方法

### 准备工作

1. 确保API服务器已经启动
2. 默认连接到 `http://localhost:5000`，如需修改，请编辑脚本中的 `BASE_URL` 变量

### 执行测试

从项目根目录执行以下命令：

```bash
python test/test_search_api.py
```

或在test目录中运行：

```bash
cd test
python test_search_api.py
```

### 测试流程说明

1. 脚本会尝试登录测试账户以获取认证令牌（如果需要）
2. 获取测试数据（小说ID和标签）
3. 执行搜索模块的各API测试
4. 生成测试报告（保存在 `doc/test_report` 目录）

## 测试报告

测试完成后，会自动生成Markdown格式的测试报告文件，包含：

- 测试执行时间
- 测试结果摘要
- 测试覆盖详情
- 失败测试的错误信息
- 建议与改进

报告文件命名格式为 `搜索模块_api_test_report_时间戳.md`

## 故障排查

### 常见问题

1. 连接错误：确保API服务器已启动，`BASE_URL` 配置正确

   ```
   ConnectionError: HTTPConnectionPool(host='localhost', port=5000)
   ```

2. 认证失败：检查测试账户信息是否正确

   ```
   用户登录失败: {"message": "Invalid credentials"}
   ```

3. 接口变更：如果API接口有变更，需要相应地更新测试脚本

## 维护与扩展

增加新的测试用例的步骤：

1. 在 `TestSearchAPI` 类中添加新的测试方法，方法名应以 `test_` 开头
2. 遵循现有的测试模式，确保测试方法包含充分的断言
3. 更新测试报告模板，加入新增测试的描述 