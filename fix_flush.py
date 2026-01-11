#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""临时脚本：为 ulster_spider.py 中的 print 语句添加 flush=True"""

import re

file_path = r'd:\Project\MySpiderProject\spiders\uk\ulster_spider.py'

# 读取文件
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换所有不带 flush=True 的 print 语句
# 模式：匹配 print(....") 或 print(....') 但不包含 flush 的
patterns = [
    (r'print\(f"   📍 目标地址: \{self\.list_url\}"\)', r'print(f"   📍 目标地址: {self.list_url}", flush=True)'),
    (r'print\(f"   ⚠️ 第 \{page_num\} 页加载超时,可能已到达最后一页"\)', r'print(f"   ⚠️ 第 {page_num} 页加载超时,可能已到达最后一页", flush=True)'),
    (r'print\(f"   📄 第 \{page_num\} 页: 发现 \{new_count\} 个项目 \(累计: \{after_count\}\)"\)', r'print(f"   📄 第 {page_num} 页: 发现 {new_count} 个项目 (累计: {after_count})", flush=True)'),
    (r'print\(f"   ✅ 已到达最后一页"\)', r'print(f"   ✅ 已到达最后一页", flush=True)'),
    (r'print\("\\n⚠️ 用户中断了爬取"\)', r'print("\\n⚠️ 用户中断了爬取", flush=True)'),
    (r'print\("❌ 未找到任何项目链接"\)', r'print("❌ 未找到任何项目链接", flush=True)'),
    (r'print\(f"❌ 获取项目列表失败: \{e\}"\)', r'print(f"❌ 获取项目列表失败: {e}", flush=True)'),
    (r'print\(f"❌ 爬取过程中发生错误: \{e\}"\)', r'print(f"❌ 爬取过程中发生错误: {e}", flush=True)'),
]

for pattern, replacement in patterns:
    content = re.sub(pattern, replacement, content)

# 写回文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ 已成功更新 {file_path}")
print("所有 print 语句已添加 flush=True 参数")
