import json
import re

# 修复 questions_data.json
try:
    with open('data/questions_data.json', 'r', encoding='utf-8') as f:
        content = f.read()

    # 在特定行的双引号后添加逗号
    lines = content.split('\n')
    fixed_lines = []
    for i, line in enumerate(lines):
        if i == 33 or i == 87:
            if line.strip().endswith('"'):
                line = line + ','
        fixed_lines.append(line)

    fixed_content = '\n'.join(fixed_lines)

    # 使用正则表达式修复可能的错误
    fixed_content = re.sub(r'"\s*\n\s*}', '",\n  }', fixed_content)
    fixed_content = re.sub(r'"\s*\n\s*"', '",\n  "', fixed_content)

    # 尝试验证和格式化
    data = json.loads(fixed_content)
    with open('data/questions_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("questions_data.json 已成功修复")
except Exception as e:
    print(f"questions_data.json 修复失败: {e}")

# 修复 news_data.json
try:
    with open('data/news_data.json', 'r', encoding='utf-8') as f:
        content = f.read()

    # 在特定行的双引号后添加逗号
    lines = content.split('\n')
    fixed_lines = []
    for i, line in enumerate(lines):
        if i == 30:
            if not line.strip().endswith(','):
                line = line + ','
        fixed_lines.append(line)

    fixed_content = '\n'.join(fixed_lines)

    # 使用正则表达式修复可能的错误
    fixed_content = re.sub(r'"\s*\n\s*}', '",\n  }', fixed_content)
    fixed_content = re.sub(r'"\s*\n\s*"', '",\n  "', fixed_content)

    # 尝试验证和格式化
    data = json.loads(fixed_content)
    with open('data/news_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("news_data.json 已成功修复")
except Exception as e:
    print(f"news_data.json 修复失败: {e}") 