#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""临时脚本：为 progress.py 中的简单 print 语句添加 flush=True"""

import re

file_path = r'd:\Project\MySpiderProject\utils\progress.py'

# 读取文件
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换简单文本模式中的print语句(不含flush的)
# 只替换在简单模式(_run_with_simple_progress)中的print
patterns = [
    (r'print\(f"\\n🔥 \[\{phase_name\}\] 启动 \{self\.max_workers\} 个并发窗口进行后台抓取\.\.\."\)', 
     r'print(f"\\n🔥 [{phase_name}] 启动 {self.max_workers} 个并发窗口进行后台抓取...", flush=True)'),
    
    (r'print\(f"按 Ctrl\+C 可随时中断"\)',
     r'print(f"按 Ctrl+C 可随时中断", flush=True)'),
    
    (r'print\(f"⏳ 任务队列已建立，正在全力运行中\.\.\."\)',
     r'print(f"⏳ 任务队列已建立，正在全力运行中...", flush=True)'),
    
    (r'print\(f"\[\{self\.completed_count\}/\{total\}\] \{percent:.1f\}% ✅ \{name_preview\} \| ⏱️ \{duration:.2f\}s \| 预计剩余: \{remaining:.0f\}s"\)',
     r'print(f"[{self.completed_count}/{total}] {percent:.1f}% ✅ {name_preview} | ⏱️ {duration:.2f}s | 预计剩余: {remaining:.0f}s", flush=True)'),
    
    (r'print\(f"❌ 任务异常: \{item\.get\(\'name\', \'\'\)\[:20\]\} - \{exc\}"\)',
     r'print(f"❌ 任务异常: {item.get(\'name\', \'\')[:20]} - {exc}", flush=True)'),
    
    (r'print\("\\n⚠️ 检测到中断信号，正在优雅停止\.\.\."\)',
     r'print("\\n⚠️ 检测到中断信号，正在优雅停止...", flush=True)'),
    
    # 简单统计信息中的各种print
    (r'print\("\\n" \+ "=" \* 50\)',
     r'print("\\n" + "=" * 50, flush=True)'),
    
    (r'print\(f"📊 抓取统计 - \{status\}"\)',
     r'print(f"📊 抓取统计 - {status}", flush=True)'),
    
    (r'print\("=" \* 50\)',
     r'print("=" * 50, flush=True)'),
    
    # print_phase_start 函数中的print
    (r'print\(f"\\n🚀 \[\{phase_name\}\] \{description\}"\)',
     r'print(f"\\n🚀 [{phase_name}] {description}", flush=True)'),
    
    (r'print\(f"   并发线程数: \{workers\}"\)',
     r'print(f"   并发线程数: {workers}", flush=True)'),
    
    (r'print\(f"   总任务数: \{total\}"\)',
     r'print(f"   总任务数: {total}", flush=True)'),
    
    # print_phase_complete 函数中的print
    (r'print\(f"✅ \[\{phase_name\}\] 完成！共锁定 \{count\} 个项目"\)',
     r'print(f"✅ [{phase_name}] 完成！共锁定 {count} 个项目", flush=True)'),
]

# 不在循环中的简单字符串打印（特殊处理）
simple_patterns = [
    (r'(\n\s+)(print\(f"  总任务:)', r'\1\2'),
    (r'(\n\s+)(print\(f"  成功:)', r'\1\2'),
    (r'(\n\s+)(print\(f"  成功率:)', r'\1\2'),
    (r'(\n\s+)(print\(f"  平均耗时:)', r'\1\2'),
    (r'(\n\s+)(print\(f"\\n⚠️ 共有)', r'\1\2'),
]

for pattern, replacement in patterns:
    content = re.sub(pattern, replacement, content)

# 为简单统计信息中的print调用添加flush(需要更智能的匹配)
# 我们将直接替换_print_summary_simple函数中未处理的print
content = re.sub(
    r'(def _print_summary_simple.*?)(print\(f"  总任务: \{total\})',
    r'\1print(f"  总任务: {total}", flush=True',
    content,
    flags=re.DOTALL
)

# 单独处理剩余的简单print语句
content = re.sub(r'print\(f"  总任务: \{total\} \| 已完成: \{self.completed_count\}"\)',
                 r'print(f"  总任务: {total} | 已完成: {self.completed_count}", flush=True)', content)
content = re.sub(r'print\(f"  成功: \{self.success_count\} \| 失败: \{self.fail_count\}"\)',
                 r'print(f"  成功: {self.success_count} | 失败: {self.fail_count}", flush=True)', content)
content = re.sub(r'print\(f"  成功率: \{\(self.success_count/self.completed_count\)\*100:.1f\}%"\)',
                 r'print(f"  成功率: {(self.success_count/self.completed_count)*100:.1f}%", flush=True)', content)
content = re.sub(r'print\(f"  平均耗时: \{avg:.2f\}s \| 最快: \{min\(self.durations\):.2f\}s \| 最慢: \{max\(self.durations\):.2f\}s"\)',
                 r'print(f"  平均耗时: {avg:.2f}s | 最快: {min(self.durations):.2f}s | 最慢: {max(self.durations):.2f}s", flush=True)', content)
content = re.sub(r'print\(f"\\n⚠️ 共有 \{self.fail_count\} 个项目抓取失败"\)',
                 r'print(f"\\n⚠️ 共有 {self.fail_count} 个项目抓取失败", flush=True)', content)

# 写回文件
with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ 已成功更新 {file_path}")
print("progress.py 中的所有 print 语句已添加 flush=True 参数")
