"""核对本次修复的边界、已知误导语句、原题保留及新增练习落盘。"""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / '编排记录/基础规则修复前快照'
baseline = json.loads((SNAP / '快照清单.json').read_text(encoding='utf-8'))
chapters = {int(p.name[:2]): p for p in (ROOT / '章节').glob('*.md')}
texts = {n: p.read_text(encoding='utf-8') for n, p in chapters.items()}
results = []


def require(ok, label):
    assert ok, label
    results.append(label)


changed = []
for rel, digest in baseline['课程'].items():
    p = ROOT / rel
    # 正文范围按实际文字比较，不将Windows换行格式变化算作知识内容改动。
    if p.read_text(encoding='utf-8') != (SNAP / (rel + '.snapshot')).read_text(encoding='utf-8'):
        changed.append(rel)
changed_chapters = [int(Path(p).name[:2]) for p in changed if Path(p).parent.name == '章节']
require(sorted(changed_chapters) == [17, 20, 21, 23, 25, 26], '正文修改限定在6章')
for key in ['原资料', '知识字典']:
    for rel, digest in baseline[key].items():
        p = ROOT.parent / rel
        require(hashlib.sha256(p.read_bytes()).hexdigest() == digest, f'{key}保持原样：{rel}')

for n, needles in {
    20: ['whether … or …：无论哪一种情况', 'or you are at school', '不是“unless 后禁止 not”'],
    21: ["I don't know if he is at home or not.", '不能把这个限制误读成', 'If he is at home, I will call him.'],
    25: ['不定式不等于“将来要做”', 'I am happy to see you.', 'the people living here', 'Seen from here', 'I remembered to lock', 'regret to tell', 'an interesting teacher', 'Reading and swimming **are** useful.'],
    26: ['She likes being invited.', '原句没有 to remember', 'enjoy 是动词', 'a book to read', '不是从“未做”一路变成“做完”的时间流水线', '先判断是一项活动，还是两个并列活动'],
}.items():
    for needle in needles:
        require(needle in texts[n], f'第{n}章保留修正与解释：{needle}')
for n, forbidden in {
    20: ['unless = if...not，不能再加 not', 'He talks **as if he knew'],
    21: ['or not 前只能用 whether', 'or not 前面只能用 whether', 'if 只能引导宾语从句'],
    23: ['所有从句都用陈述语序', 'if 只能引导宾语从句'],
    25: ['| 时间 | 正在进行 | 已经完成 |', 'remember/forget/regret 后接 to do', '不带 to 的不定式**要还原 to**'],
    26: ['| to do | 未做 / 将做 |', '动作正在进行。', '动作已经完成。', 'be afraid of making、enjoy listening', '不定式：to learn、to practice、to remember', '被动还原 to）', '能替换成名词的是动名词'],
}.items():
    for needle in forbidden:
        require(needle not in texts[n], f'第{n}章消除误导概括：{needle}')

preserved = 0
added = 0


def canonical_question(line):
    # 表达题本来就把提示词打乱；比较任务与词语集合，不把The/the的顺序视为换题。
    marker = '可用词语（次序打乱，不要求全部唯一用法）：'
    if marker not in line:
        return line
    prefix, words = line.split(marker, 1)
    return prefix + marker + ' / '.join(sorted(words.rstrip('。').split(' / ')))


for p in sorted((ROOT / '强化题目').glob('[0-9][0-9]·强化练习*.md')):
    old = (SNAP / '强化题目' / (p.name + '.snapshot')).read_text(encoding='utf-8')
    new = p.read_text(encoding='utf-8')
    pattern = r'^\*\*([ABCD]\d{2})｜[^\n]+'
    old_questions = {m.group(1): m.group() for m in re.finditer(pattern, old, re.M)}
    new_questions = {m.group(1): m.group() for m in re.finditer(pattern, new, re.M)}
    require(all(k in new_questions and canonical_question(new_questions[k]) == canonical_question(v) for k, v in old_questions.items()), f'原题逐题保留：{p.name}')
    preserved += len(old_questions)
    added += len(new_questions) - len(old_questions)
    n = int(p.name[:2])
    if n in [20, 21, 25, 26]:
        count = 4 if n == 21 else 6
        require(all(f'**D{i:02}｜' in new and f'<strong>D{i:02}</strong>' in new for i in range(1, count + 1)), f'第{n}章补练题答配对')
        require('完成D中的基础规则补练' in new and '隔一天合上解析重做D组错题' in new, f'第{n}章补练进入学习顺序和复测')
require(preserved == 1256 and added == 22, '原1256题完整保留，新增22题')
guide = (ROOT / '00·从这里开始.md').read_text(encoding='utf-8')
require('共46道' in guide and '共44道' in guide, '学习目录题量与实际一致')
report = {'检查项': len(results), '修改正文章': sorted(changed_chapters), '保留强化任务': preserved, '新增基础补练': added,
          '原资料': '19份未改', '知识字典': '30份未改', '范围': '已知错误回归、原题逐题保留、文档与习题边界；不代表整套自然语言内容已经无误'}
(ROOT / '编排记录/基础规则检查结果.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
