"""检查整个资料目录中的 Markdown，不改动正文或读者排版。"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
hits = []
count = 0
for path in ROOT.rglob('*.md'):
    if '.git' in path.parts:
        continue
    count += 1
    for number, line in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        if re.search(r'<!--\s*study-priority:(?:start|end)\s*-->', line):
            hits.append(f'{path.relative_to(ROOT)}:{number}')
assert not hits, '\n'.join(hits)
print(f'通过：扫描 {count} 份 Markdown，未发现学习分层维护注释。')
