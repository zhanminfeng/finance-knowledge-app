#!/usr/bin/env python3
"""
自动修复模块路径问题的脚本。
此脚本会自动检查并修复目录结构，确保app模块可以被正确导入。
"""

import os
import sys
import importlib
from pathlib import Path
import shutil

def main():
    print("开始自动修复模块路径问题...")
    
    # 获取backend目录的绝对路径
    backend_dir = Path(__file__).resolve().parent
    
    # 检查是否有嵌套的backend目录
    nested_backend = backend_dir / "backend"
    if nested_backend.exists() and nested_backend.is_dir():
        print(f"发现嵌套的backend目录: {nested_backend}")
        
        # 列出嵌套backend目录中的文件
        nested_files = list(nested_backend.glob("*"))
        print(f"嵌套目录中有 {len(nested_files)} 个文件/目录")
        
        # 自动将嵌套目录中的文件复制到主目录
        for item in nested_files:
            dest = backend_dir / item.name
            if not dest.exists():
                if item.is_dir():
                    shutil.copytree(item, dest)
                    print(f"复制目录: {item.name}")
                else:
                    shutil.copy2(item, dest)
                    print(f"复制文件: {item.name}")
            else:
                print(f"已存在，跳过: {item.name}")
        
        # 不删除嵌套目录，以防万一
        print("注意: 嵌套的backend目录未被删除，如果确认不再需要，可以手动删除")
    
    # 确保app目录中有__init__.py文件
    app_dir = backend_dir / "app"
    if not app_dir.exists():
        print(f"错误: 找不到app目录: {app_dir}")
        return False
    
    # 确保app/__init__.py存在且非空
    app_init = app_dir / "__init__.py"
    if not app_init.exists() or os.path.getsize(app_init) == 0:
        with open(app_init, 'w') as f:
            f.write("# 确保app可以作为模块被导入\n")
        print("✅ 更新了app/__init__.py文件")
    
    # 将backend目录添加到Python路径
    sys.path.insert(0, str(backend_dir))
    
    # 检查能否导入app模块
    try:
        import app
        print("✅ 成功导入app模块")
    except ImportError as e:
        print(f"❌ 导入app模块失败: {e}")
        return False
    
    # 创建.env文件确保环境变量设置正确
    env_file = backend_dir / ".env"
    env_content = """
# 雪球API设置
XUEQIU_API_ENABLED=True
XUEQIU_COOKIE=mock_cookie_for_testing

# 应用设置
LOG_LEVEL=DEBUG
"""
    
    if not env_file.exists():
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ 创建了.env文件")
    
    print("\n✅ 自动修复完成!")
    print(f"Python路径: {sys.path}")
    print("\n您现在可以运行以下命令启动服务器:")
    print("python start_server.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 