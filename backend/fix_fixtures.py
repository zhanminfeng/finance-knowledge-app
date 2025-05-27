#!/usr/bin/env python
import os
import sys
import re

def fix_fixture_in_file(file_path):
    """Fix the async_client fixture in a test file"""
    with open(file_path, 'r') as f:
        content = f.read()

    # 1. Add pytest_asyncio import
    if 'import pytest_asyncio' not in content:
        content = re.sub(
            r'import pytest', 
            'import pytest\nimport pytest_asyncio', 
            content
        )

    # 2. Change fixture decorator from pytest to pytest_asyncio
    content = re.sub(
        r'@pytest.fixture\(scope="function"\)',
        '@pytest_asyncio.fixture(scope="function")',
        content
    )

    # Write the fixed content back to the file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Fixed fixtures in {file_path}")

def main():
    """Fix fixtures in all test files"""
    tests_dir = os.path.join('tests')
    
    if not os.path.exists(tests_dir):
        print(f"Tests directory not found: {tests_dir}")
        sys.exit(1)
    
    test_files = [f for f in os.listdir(tests_dir) if f.startswith('test_') and f.endswith('.py')]
    
    for test_file in test_files:
        fix_fixture_in_file(os.path.join(tests_dir, test_file))
    
    print(f"Fixed fixtures in {len(test_files)} test files")

if __name__ == "__main__":
    main() 