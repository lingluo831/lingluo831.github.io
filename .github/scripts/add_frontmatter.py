import os
import re
from datetime import datetime

def sanitize_title(filename):
    title = os.path.splitext(filename)[0]
    title = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', title)
    title = title.replace('-', ' ').replace('_', ' ')
    return title.title()

def get_file_creation_date(filepath):
    t = os.path.getmtime(filepath)
    return datetime.fromtimestamp(t).strftime('%Y-%m-%d')

def has_frontmatter(content):
    return content.strip().startswith('---')

def add_frontmatter_to_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    if has_frontmatter(content):
        print(f"已存在前置元数据，跳过：{filepath}")
        return
    title = sanitize_title(os.path.basename(filepath))
    date = get_file_creation_date(filepath)
    frontmatter = f"""---
layout: article
title: {title}
date: {date}
---

"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content)
    print(f"已添加前置元数据：{filepath}")

def main():
    for filename in os.listdir('.'):
        if filename.endswith('.md'):
            add_frontmatter_to_file(filename)

if __name__ == '__main__':
    main()