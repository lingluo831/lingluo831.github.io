import os
import re
from datetime import datetime

def sanitize_title(filename):
    title = os.path.splitext(filename)[0]
    title = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', title)
    title = title.replace('-', ' ').replace('_', ' ')
    return title.title()

def has_frontmatter(content):
    return content.strip().startswith('---')

def get_file_creation_date(filepath):
    t = os.path.getmtime(filepath)
    return datetime.fromtimestamp(t).strftime('%Y-%m-%d')

def get_category(filepath):
    # 假设你的md文件路径为 _posts/分类/xxx.md
    parts = filepath.split(os.sep)
    if len(parts) >= 3 and parts[0] == '_posts':
        return parts[1]
    return ""

def add_frontmatter_to_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if has_frontmatter(content):
        print(f"已存在前置元数据，跳过：{filepath}")
        return
    title = sanitize_title(os.path.basename(filepath))
    date = get_file_creation_date(filepath)
    category = get_category(filepath)
    frontmatter = f"""---
layout: article
title: {title}
date: {date}
categories: {category}
---

"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)
    print(f"已添加前置元数据：{filepath}")

def main():
    for root, _, files in os.walk('_posts'):
        for filename in files:
            if filename.endswith('.md'):
                add_frontmatter_to_file(os.path.join(root, filename))

if __name__ == '__main__':
    main()
