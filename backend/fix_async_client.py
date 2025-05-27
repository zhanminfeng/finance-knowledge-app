#!/usr/bin/env python
import os
import sys
import re

def fix_async_client_in_file(file_path):
    """Fix the AsyncClient usage in a test file"""
    with open(file_path, 'r') as f:
        content = f.read()

    # Change AsyncClient(app=app, base_url="http://test") to
    # AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    if 'from httpx import AsyncClient' in content and 'ASGITransport' not in content:
        # Add import for ASGITransport
        content = re.sub(
            r'from httpx import AsyncClient',
            'from httpx import AsyncClient\nfrom httpx import ASGITransport',
            content
        )
        
        # Fix AsyncClient usage
        content = re.sub(
            r'AsyncClient\(app=app,\s*base_url="http://test"\)',
            'AsyncClient(transport=ASGITransport(app=app), base_url="http://test")',
            content
        )

    # Write the fixed content back to the file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"Fixed AsyncClient in {file_path}")

def main():
    """Fix AsyncClient in all test files"""
    tests_dir = os.path.join('tests')
    
    if not os.path.exists(tests_dir):
        print(f"Tests directory not found: {tests_dir}")
        sys.exit(1)
    
    test_files = [f for f in os.listdir(tests_dir) if f.startswith('test_') and f.endswith('.py')]
    
    for test_file in test_files:
        fix_async_client_in_file(os.path.join(tests_dir, test_file))
    
    print(f"Fixed AsyncClient in {len(test_files)} test files")

if __name__ == "__main__":
    main() 