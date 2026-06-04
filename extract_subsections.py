#!/usr/bin/env python3
"""Extract subsection data from Chapter 7 TeX for AI summarization."""
import json, re

lines = open('manufactver3tex.tex', encoding='utf-8').readlines()
data = []
cur_sec, cur_sub, cur_text = '', '', []

for i in range(2960, 4042):
    raw = lines[i].strip()
    if not raw or raw.startswith('%'):
        continue
    m = re.match(r'\\(?:section|section\*)\{([^}]*)\}', raw)
    if m:
        if cur_text and cur_sub:
            data.append({'section': cur_sec, 'title': cur_sub, 'text': ''.join(cur_text), 'idx': len(data)})
        cur_sec = m.group(1)
        cur_sub = ''
        cur_text = []
        continue
    m = re.match(r'\\(?:subsection|subsubsection)\{([^}]*)\}', raw)
    if m:
        if cur_text and cur_sub:
            data.append({'section': cur_sec, 'title': cur_sub, 'text': ''.join(cur_text), 'idx': len(data)})
        cur_sub = m.group(1)
        cur_text = []
        continue
    if re.match(r'\\begin\{figure\}', raw) or re.match(r'\\end\{figure\}', raw):
        continue
    if re.match(r'\\label\{', raw):
        continue
    SKIP = ['第一版','第二版','本书为','本书集','本书可满','此次修订','本次修订',
            '国家精品','一流本科','普通高等教育','国家级规划','编委会','责任编辑',
            '封面设计','ISBN','定价','版权所有','侵权必究']
    if any(k in raw for k in SKIP):
        continue
    clean = re.sub(r'\\(?:item|begin\{itemize\}|end\{itemize\}|begin\{enumerate\}|end\{enumerate\})\s*', '', raw)
    clean = clean.strip()
    if clean and len(clean) > 5:
        if re.match(r'^[\d\s\.,%、，。；：\'\"\-=→←◎\{\}【】《》<>\\]+$', clean):
            continue
        cur_text.append(clean)

if cur_text and cur_sub:
    data.append({'section': cur_sec, 'title': cur_sub, 'text': ''.join(cur_text), 'idx': len(data)})

# Output as structured markdown for easy reading
for item in data:
    print(f'## [{item["idx"]}] {item["title"]}')
    print(f'*Section: {item["section"]}*')
    print()
    print(item['text'][:200])
    print('...')
    print()
    print(f'--- 全文 {len(item["text"])} 字 ---')
    print()
