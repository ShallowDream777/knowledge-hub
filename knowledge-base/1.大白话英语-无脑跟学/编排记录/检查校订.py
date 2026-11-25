from 答案排版 import markdown_answers_for_check
"""检查内容修订后的文件、题号、导航和已知错误回归。"""
from pathlib import Path
import hashlib
import json
import re

root = Path(__file__).resolve().parents[1]
chapters = sorted((root / '章节').glob('*.md'))
assert len(chapters) == 31
guide = (root / '00·从这里开始.md').read_text(encoding='utf-8')
assert len(re.findall(r'^- \[[ xX]\] \[\[',guide,re.M)) == 31
manifest = json.loads((root/'编排记录/来源映射.json').read_text(encoding='utf-8'))
assert len(manifest['专题小节']) == 160
assert len(manifest['主文档主题']) == 30
for name, sha in manifest['原文件SHA256'].items():
    assert hashlib.sha256((root.parent/name).read_bytes()).hexdigest() == sha

all_text = ''
test_groups = 0
question_count = 0
practice_groups = 0
all_names = {p.stem for p in root.rglob('*.md')}
for i,p in enumerate(chapters):
    s=markdown_answers_for_check(p.read_text(encoding='utf-8'))
    all_text += s
    assert f'# 第 {i+1:02} 章' in s
    assert s.count('[[00·从这里开始|学习目录]]') == 2
    if i<30:
        assert s.count(f'[[{chapters[i+1].stem}|') == 2
    assert s.count('<details>') == s.count('</details>')
    heads = re.findall(r'^#+ (.+)$',s,re.M)
    for target in re.findall(r'\[\[([^]|]+)',s):
        if target.startswith('#'):
            assert target[1:] in heads,(p.name,target)
        else:
            assert target in all_names,(p.name,target)
    for m in re.finditer(r'(?m)^### [^\n]*(?:自查|自测)[^\n]*\n[\s\S]*?</details>',s):
        block=m.group()
        title=block.splitlines()[0]
        total=int(re.search(r'（(\d+) 道',title).group(1))
        questions, answers=block.split('<details>',1)
        q=[int(n) for n in re.findall(r'(?m)^(\d+)\. ',questions)]
        a=[int(n) for n in re.findall(r'(?m)^(\d+)\. ',answers)]
        assert q==a==list(range(1,total+1)), (p.name,q,a)
        question_count += total
        test_groups += 1
    practice_groups += s.count('### 就地练习：')
assert test_groups == 17 and question_count == 395
assert practice_groups == 11
for bad in ['ten to eight = 8:50','How + 副词 runs','did he spoke',
            '（两个动词，错）','最高级前面必须加 the','because 不能引导表语从句',
            '和现在无关。','有明确过去时间状语只能用一般过去时',
            '一个句子里只能有一个"真谓语"','一个简单句只能有一个限定动词作谓语核心']:
    assert bad not in all_text,bad
for good in ['ten to eight = 7:50','look after him','my best friend',
             'So loudly did he speak','should rain 或 rained','studied harder',
             'This is because','常用动词形式：','I didn’t work yesterday']:
    assert good in all_text,good

data=json.loads((root/'编排记录/内容整改明细.json').read_text(encoding='utf-8'))
dedup_count=sum(r['合并段数'] for r in data['重复段落合并'])
result={
 '独立章节':31,'原专题小节':160,'原总论主题':30,
 '原自测组':test_groups,'原自测题':question_count,
 '新增就地练习组':practice_groups,
 '具体修订记录':len(data['具体修订']),
 '合并同文重复段落':dedup_count,
 '原文件SHA256':'19份全部一致',
 '检查范围':'导航、题号及答案配对、已知错误回归；自动检查不替代所有句子的语法审读',
}
(root/'编排记录/校订检查结果.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
