#!/usr/bin/env python

import pytest
import os
import sys

"""
财知道后端API测试脚本
运行方式: python run_tests.py
"""

if __name__ == "__main__":
    print("=== 开始运行财知道后端API测试 ===")
    # Add the current directory to the path so pytest can find the test modules
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    # Run all tests
    result = pytest.main(["-v", "tests/"])
    
    if result == 0:
        print("=== 所有测试通过! ✅ ===")
    else:
        print("=== 测试失败! ❌ ===")
        sys.exit(1) 