#!/usr/bin/env python3
"""
修复模块路径问题的脚本。
这个脚本会检查目录结构，确保app模块可以被正确导入。
"""

import os
import sys
import importlib
from pathlib import Path
import shutil

def main():
    # 获取backend目录的绝对路径
    backend_dir = Path(__file__).resolve().parent
    
    # 检查是否有嵌套的backend目录
    nested_backend = backend_dir / "backend"
    if nested_backend.exists() and nested_backend.is_dir():
        print(f"发现嵌套的backend目录: {nested_backend}")
        
        # 列出嵌套backend目录中的文件
        nested_files = list(nested_backend.glob("*"))
        print(f"嵌套目录中有 {len(nested_files)} 个文件/目录")
        
        # 询问是否需要合并目录
        answer = input("要将嵌套backend目录中的文件移动到主backend目录吗? (y/n): ")
        if answer.lower() == 'y':
            # 将文件移动到主backend目录
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
            
            # 询问是否删除嵌套目录
            answer = input("是否删除嵌套backend目录? (y/n): ")
            if answer.lower() == 'y':
                shutil.rmtree(nested_backend)
                print("已删除嵌套backend目录")
    
    # 检查app目录是否存在
    app_dir = backend_dir / "app"
    if not app_dir.exists():
        print("错误: 找不到app目录")
        return
    
    # 检查是否可以导入app模块
    sys.path.insert(0, str(backend_dir))
    try:
        import app
        print("✅ 成功导入app模块")
    except ImportError as e:
        print(f"❌ 导入app模块失败: {e}")
        return
    
    # 检查是否可以导入app.main模块
    try:
        importlib.import_module("app.main")
        print("✅ 成功导入app.main模块")
    except ImportError as e:
        print(f"❌ 导入app.main模块失败: {e}")
        return
    
    print("\n✅ 模块路径检查完成，一切正常!")
    print(f"Python路径: {sys.path}")
    
    # 创建符号链接确保模块可以被找到
    try:
        app_init = backend_dir / "app" / "__init__.py"
        if not app_init.exists() or os.path.getsize(app_init) == 0:
            with open(app_init, 'w') as f:
                f.write("# 确保app可以作为模块被导入\n")
            print("✅ 更新了app/__init__.py文件")
    except Exception as e:
        print(f"❌ 更新app/__init__.py失败: {e}")
    
    print("\n使用以下命令运行服务器:")
    print("python start_server.py")
    
if __name__ == "__main__":
    main() 