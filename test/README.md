# 测试目录说明

## 测试脚本结构

- `run_api_tests.py`: 主测试入口脚本，用于运行所有API测试并生成报告
- `test_user_api.py`: 用户模块API测试脚本，包括用户注册、登录、个人信息管理及注销功能测试
- `test_novel_api.py`: 小说模块API测试脚本，包括小说创建、查询、更新、章节管理、标签管理等功能测试

## 如何运行测试

### 运行所有测试

```bash
cd test
python run_api_tests.py
```

### 运行单个测试模块

```bash
cd test
python test_user_api.py
python test_novel_api.py
```

## 测试报告

所有测试报告都会保存在 `../doc/test_report` 目录中，包括：

- 单独测试模块的报告: `{module_name}_test_report_{timestamp}.md`
- 汇总测试报告: `summary_report_{timestamp}.md`

## 注意事项

1. 确保测试前API服务器已经启动，默认地址为 `http://localhost:5000`
2. 测试脚本会自动创建并清理测试数据，无需手动干预
3. 如需修改测试配置，请编辑对应测试脚本中的配置部分 