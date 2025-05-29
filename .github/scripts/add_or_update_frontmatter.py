import os
import re
from datetime import datetime
import shutil

def sanitize_title(filename):
    # 从文件名中提取标题
    title = os.path.splitext(filename)[0]
    # 移除已有的日期前缀
    title = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', title)
    # 将连字符和下划线转换为空格
    title = title.replace('-', ' ').replace('_', ' ')
    return title.title()

def get_file_creation_date(filepath):
    # 获取文件修改时间
    t = os.path.getmtime(filepath)
    return datetime.fromtimestamp(t).strftime('%Y-%m-%d')

def get_folder_name(filepath):
    # 取父文件夹名 (_posts/分类/xxx.md -> 分类)
    parts = filepath.replace('\\', '/').split('/')
    if len(parts) >= 3 and parts[0] == '_posts':
        return parts[1]
    elif len(parts) >= 2:
        return parts[-2]
    else:
        return "article"

def parse_frontmatter(fm_text):
    # 简单解析 key: value 形式
    result = {}
    for line in fm_text.splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            result[k.strip()] = v.strip()
    return result

def build_frontmatter(data):
    lines = ['---']
    for k, v in data.items():
        lines.append(f'{k}: {v}')
    lines.append('---\n')
    return '\n'.join(lines)

def format_filename(title, date):
    """格式化文件名为 YYYY-MM-DD-title.md 格式"""
    # 移除特殊字符,将空格转换为短横线
    clean_title = re.sub(r'[^\w\s-]', '', title.lower())
    clean_title = re.sub(r'[-\s]+', '-', clean_title).strip('-')
    return f"{date}-{clean_title}.md"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配 front matter
    match = re.match(r'^---\n([\s\S]*?)\n---\n?', content)
    if match:
        fm_text = match.group(1)
        body = content[match.end():]
        fm = parse_frontmatter(fm_text)
    else:
        fm = {}
        body = content

    # 补全字段
    changed = False
    folder_layout = get_folder_name(filepath)
    file_date = get_file_creation_date(filepath)
    
    if 'layout' not in fm:
        fm['layout'] = folder_layout
        changed = True
    if 'title' not in fm:
        fm['title'] = sanitize_title(os.path.basename(filepath))
        changed = True
    if 'date' not in fm:
        fm['date'] = file_date
        changed = True

    # 检查并更新文件名
    dirname = os.path.dirname(filepath)
    old_filename = os.path.basename(filepath)
    new_filename = format_filename(fm['title'], file_date)
    
    if old_filename != new_filename:
        new_filepath = os.path.join(dirname, new_filename)
        # 处理文件名冲突
        counter = 1
        while os.path.exists(new_filepath) and new_filepath != filepath:
            base, ext = os.path.splitext(new_filename)
            new_filepath = os.path.join(dirname, f"{base}-{counter}{ext}")
            counter += 1
        
        # 保存文件
        if changed or not match:
            new_fm = build_frontmatter(fm)
            with open(new_filepath, 'w', encoding='utf-8') as f:
                f.write(new_fm + body.lstrip('\n'))
        else:
            shutil.copy2(filepath, new_filepath)
        
        # 如果文件名发生改变且不是同一个文件,则删除旧文件
        if os.path.normpath(filepath) != os.path.normpath(new_filepath):
            os.remove(filepath)
        print(f"已重命名文件: {old_filename} -> {new_filename}")
    else:
        # 如果文件名不需要更改,只更新内容
        if changed or not match:
            new_fm = build_frontmatter(fm)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_fm + body.lstrip('\n'))
            print(f"已补全 front matter: {filepath}")
        else:
            print(f"front matter 已完善: {filepath}")

def main():
    for root, _, files in os.walk('_posts'):
        for filename in files:
            if filename.endswith('.md'):
                process_file(os.path.join(root, filename))

if __name__ == '__main__':
    main()