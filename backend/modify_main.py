#!/usr/bin/env python
"""
直接修改app/main.py文件以添加同步API路由
"""

import os
import re

def modify_main_py():
    """直接修改main.py文件，添加同步API路由"""
    print("修改app/main.py文件...")
    
    # 获取当前脚本的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    main_py_path = os.path.join(current_dir, "app", "main.py")
    
    # 检查文件是否存在
    if not os.path.exists(main_py_path):
        print(f"错误: 找不到文件 {main_py_path}")
        return False
    
    # 读取原始文件内容
    with open(main_py_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # 检查是否已经包含同步API路由导入
    if "import fix_learning_sync" in content:
        print("文件已经包含同步API路由导入，跳过修改")
        return True
    
    # 添加同步API路由导入和注册
    import_code = "# 导入同步API路由\nimport fix_learning_sync\n"
    route_code = """
# 注册同步API路由
app.include_router(
    fix_learning_sync.router,
    prefix="/api/learning_sync",
    tags=["learning_sync"]
)
"""
    
    # 查找适合插入导入语句的位置
    import_match = re.search(r"from app\.api import api_router", content)
    if import_match:
        insert_pos = import_match.start()
        content = content[:insert_pos] + import_code + content[insert_pos:]
    else:
        print("警告: 无法找到合适的导入位置，将添加到文件开头")
        content = import_code + content
    
    # 查找适合插入路由注册的位置
    route_match = re.search(r"app\.include_router\(chat_router,", content)
    if route_match:
        insert_pos = route_match.end()
        # 找到该行的末尾
        line_end = content.find("\n", insert_pos)
        if line_end > 0:
            insert_pos = line_end + 1
        content = content[:insert_pos] + route_code + content[insert_pos:]
    else:
        print("警告: 无法找到合适的路由注册位置，将添加到文件末尾")
        content += "\n" + route_code
    
    # 创建备份
    backup_path = main_py_path + ".bak"
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"已创建备份: {backup_path}")
    
    # 写入修改后的文件
    with open(main_py_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("已成功修改app/main.py文件")
    return True

def main():
    """主函数"""
    print("===== 修改main.py文件添加同步API路由 =====")
    success = modify_main_py()
    
    if success:
        print("\n修改成功! 请运行以下命令启动服务器:")
        print("uvicorn app.main:app --reload")
        print("\n然后访问: http://localhost:8000/api/learning_sync")
    else:
        print("\n修改失败! 请手动修改app/main.py文件")

if __name__ == "__main__":
    main() 