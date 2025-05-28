# import os
# import re
# from datetime import datetime

# def sanitize_title(filename):
#     title = os.path.splitext(filename)[0]
#     title = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', title)
#     title = title.replace('-', ' ').replace('_', ' ')
#     return title.title()

# def get_file_creation_date(filepath):
#     t = os.path.getmtime(filepath)
#     return datetime.fromtimestamp(t).strftime('%Y-%m-%d')

# def get_folder_name(filepath):
#     # 取父文件夹名 (_posts/分类/xxx.md -> 分类)
#     parts = filepath.replace('\\', '/').split('/')
#     if len(parts) >= 3 and parts[0] == '_posts':
#         return parts[1]
#     elif len(parts) >= 2:
#         return parts[-2]
#     else:
#         return "article"

# def parse_frontmatter(fm_text):
#     # 简单解析 key: value 形式
#     result = {}
#     for line in fm_text.splitlines():
#         if ':' in line:
#             k, v = line.split(':', 1)
#             result[k.strip()] = v.strip()
#     return result

# def build_frontmatter(data):
#     lines = ['---']
#     for k, v in data.items():
#         lines.append(f'{k}: {v}')
#     lines.append('---\n')
#     return '\n'.join(lines)

# def process_file(filepath):
#     with open(filepath, 'r', encoding='utf-8') as f:
#         content = f.read()

#     # 匹配 front matter
#     match = re.match(r'^---\n([\s\S]*?)\n---\n?', content)
#     if match:
#         fm_text = match.group(1)
#         body = content[match.end():]
#         fm = parse_frontmatter(fm_text)
#     else:
#         fm = {}
#         body = content

#     # 补全字段
#     changed = False
#     folder_layout = get_folder_name(filepath)
#     if 'layout' not in fm:
#         fm['layout'] = folder_layout
#         changed = True
#     if 'title' not in fm:
#         fm['title'] = sanitize_title(os.path.basename(filepath))
#         changed = True
#     if 'date' not in fm:
#         fm['date'] = get_file_creation_date(filepath)
#         changed = True

#     if changed or not match:
#         new_fm = build_frontmatter(fm)
#         with open(filepath, 'w', encoding='utf-8') as f:
#             f.write(new_fm + body.lstrip('\n'))
#         print(f"已补全 front matter: {filepath}")
#     else:
#         print(f"front matter 已完善: {filepath}")

# def main():
#     for root, _, files in os.walk('_posts'):
#         for filename in files:
#             if filename.endswith('.md'):
#                 process_file(os.path.join(root, filename))

# if __name__ == '__main__':
#     main()