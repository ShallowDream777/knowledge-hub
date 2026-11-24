"""只移除旧版维护注释行，保留学习要求与正文的原始字节。"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BACKUP = ROOT / '编排记录' / '分层标记清理前快照'
PATTERN = re.compile(rb'(?m)^[ \t]*<!-- study-priority:(?:start|end) -->[ \t]*(?:\r?\n|$)')

if __name__ == '__main__':
    changed = 0
    for path in ROOT.rglob('*.md'):
        relative = path.relative_to(ROOT)
        if '编排记录' in relative.parts:
            continue
        before = path.read_bytes()
        after = PATTERN.sub(b'', before)
        if before == after:
            continue
        snapshot = BACKUP / (str(relative) + '.snapshot')
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        if not snapshot.exists():
            snapshot.write_bytes(before)
        path.write_bytes(after)
        changed += 1
    print(f'已清理 {changed} 个阅读文件；正文及可见学习标签原样保留。')
