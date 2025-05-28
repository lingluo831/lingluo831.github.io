import os
import re
from datetime import datetime
import yaml

def sanitize_title(filename):
    title = os.path.splitext(filename)[0]
    title = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', title)
    title = title.replace('-', ' ').replace('_', ' ')
    return title.title()

def get_file_creation_date(filepath):
    t = os.path.getmtime(filepath)
    return datetime.fromtimestamp(t).strftime('%Y-%m-%d')

def get_folder_name(filepath):
    # 获取父文件夹名 (_posts/分类/xxx.md -> 分类)
    parts = filepath.replace('\\', '/').split('/')
    if len(parts) >= 3 and parts[0] == '_posts':
        return parts[1]
    elif len(parts) >= 2:
        return parts[-2]
    else:
        return "article"

def split_frontmatter(content):
    # 拆分 front matter 和正文
    match = re.match(r'^---\n([\s\S]*?)\n---\n?', content)
    if match:
        fm = match.group(1)
        body = content[match.end():]
        return fm, body
    else:
        return None, content

def merge_frontmatter(old_fm, new_fields):
    # old_fm: str or None; new_fields: dict
    if old_fm:
        try:
            data = yaml.safe_load(old_fm)
            if data is None:
                data = {}
        except Exception:
            data = {}
    else:
        data = {}
    # 只补充缺失的字段，不覆盖原有字段
    for k, v in new_fields.items():
        if k not in data or not data[k]:
            data[k] = v
    # 防止 yaml.dump 输出 'null'
    data = {k: ("" if v is None else v) for k, v in data.items()}
    return "---\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False).strip() + "\n---\n"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    old_fm, body = split_frontmatter(content)
    title = sanitize_title(os.path.basename(filepath))
    date = get_file_creation_date(filepath)
    layout = get_folder_name(filepath)
    new_fields = {
        "layout": layout,
        "title": title,
        "date": date
    }
    new_fm = merge_frontmatter(old_fm, new_fields)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_fm + body.lstrip('\n'))
    print(f"已合并/补全 front matter：{filepath}")

def main():
    for root, _, files in os.walk('_posts'):
        for filename in files:
            if filename.endswith('.md'):
                process_file(os.path.join(root, filename))

if __name__ == '__main__':
    main()