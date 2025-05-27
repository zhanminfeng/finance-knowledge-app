# 雪球API测试指南

本指南解释如何测试雪球（Snow Ball）财经新闻API集成。

## 准备工作

### 1. 修复路径问题

在开始测试前，请先运行自动修复脚本，确保模块路径正确：

```bash
# 在backend目录下运行
python auto_fix_paths.py
```

如果需要交互式修复（例如有特殊路径问题需要处理），可以运行：

```bash
python fix_module_path.py
```

### 2. 安装依赖

确保已安装所有依赖：

```bash
# 在backend目录下运行
chmod +x install_xueqiu_deps.sh
./install_xueqiu_deps.sh
```

## 测试选项

### 选项1：模拟测试（无需服务器）

这些测试使用猴子补丁模拟API响应，无需实际连接到雪球API：

```bash
# 在backend目录下运行
python run_mock_tests.py
```

### 选项2：完整API测试（需要服务器）

1. 首先，启动已启用雪球API并应用了猴子补丁的服务器：

```bash
# 在backend目录下运行
python start_server.py
```

2. 然后，在另一个终端中运行API端点测试：

```bash
# 在backend目录下运行
python run_api_tests.py
```

## 测试内容

1. **模拟测试** (`run_mock_tests.py`)：
   - 测试雪球客户端初始化
   - 测试从不同分类获取热门新闻
   - 测试新闻服务功能

2. **API端点测试** (`run_api_tests.py`)：
   - 测试API状态
   - 测试获取雪球分类
   - 测试获取雪球新闻
   - 测试启动/停止新闻任务
   - 测试从API获取新闻

## 故障排除

如果遇到任何问题：

1. 确保环境变量设置正确（可以运行`auto_fix_paths.py`自动设置）
2. 检查所有依赖是否已安装
3. 确保测试API端点时服务器正在运行
4. 检查日志输出是否有特定的错误消息
5. 查看Python导入路径是否正确（`sys.path`）
6. 如果遇到导入错误，请确保运行自动修复脚本 