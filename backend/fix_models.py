#!/usr/bin/env python
import os
import sys
import re

def fix_base_model():
    """修复BaseModel中的重复索引问题"""
    base_model_path = os.path.join('app', 'models', 'base.py')
    
    if not os.path.exists(base_model_path):
        print(f"Base model file not found: {base_model_path}")
        return False
    
    with open(base_model_path, 'r') as f:
        content = f.read()
    
    # 修改id字段定义，移除index=True
    modified_content = re.sub(
        r'id = Column\(String\(36\), primary_key=True, default=generate_uuid, index=True\)',
        'id = Column(String(36), primary_key=True, default=generate_uuid)',
        content
    )
    
    if modified_content != content:
        with open(base_model_path, 'w') as f:
            f.write(modified_content)
        print(f"Fixed index issue in {base_model_path}")
        return True
    else:
        print(f"No change needed in {base_model_path}")
        return False

def main():
    """修复模型中的重复索引问题"""
    print("开始修复模型中的重复索引问题...")
    
    # 检查当前目录是否包含app目录
    if not os.path.exists('app'):
        # 尝试查找正确的目录
        if os.path.exists(os.path.join('backend', 'app')):
            os.chdir('backend')
            print("切换到backend目录")
        else:
            print("找不到app目录，请确保在正确的目录中运行此脚本")
            sys.exit(1)
    
    fixed = fix_base_model()
    
    if fixed:
        print("已修复重复索引问题，请重新运行测试")
    else:
        print("没有发现需要修复的问题")

if __name__ == "__main__":
    main() 