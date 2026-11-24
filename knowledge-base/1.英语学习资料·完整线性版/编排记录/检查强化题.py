from 答案排版 import markdown_answers_for_check
from pathlib import Path
import json
import re
import hashlib
from 强化题库 import SEEDS, CHECKS, EXTRA

ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'编排记录/强化题目清单.json').read_text(encoding='utf-8'))
assert len(manifest)==31
questions=0
for row in manifest:
    n=row['章']
    chapter=ROOT/row['章节文件']
    quiz=ROOT/row['练习文件']
    c=chapter.read_text(encoding='utf-8')
    s=markdown_answers_for_check(quiz.read_text(encoding='utf-8'))
    assert c.count('## 本章强化与验收')==1,chapter
    assert f'[[{quiz.stem}|' in c,chapter
    assert s.count(f'[[{chapter.stem}|返回第{n:02}章：')==2,quiz
    assert s.splitlines()[2].startswith(f'[[{chapter.stem}|'),quiz
    chapters=sorted((ROOT/'章节').glob('*.md'))
    if n<31:
        next_name=chapters[n].stem
        assert c.count(f'[[{next_name}|')==2,chapter
        assert f'[[{next_name}|' in s,quiz
    assert s.count('<details>')==s.count('</details>')==(4 if EXTRA.get(n) else 3),quiz
    before_answers=[]
    after_answers=[]
    parts=re.split(r'(<details>[\s\S]*?</details>)',s)
    for part in parts:
        ids=re.findall(r'^\*\*([ABCD]\d{2})(?:｜[^*]+)?\*\*',part,re.M)
        if part.startswith('<details>'):after_answers+=ids
        else:before_answers+=ids
    assert len(before_answers)==len(set(before_answers)),(quiz,'重复题号')
    assert set(before_answers)==set(after_answers),(quiz,'题答不配对')
    assert len(before_answers)==row['题量'],quiz
    assert set(re.findall(r'^\*\*(C\d{2})｜',s,re.M))=={f'C{k:02}' for k in range(1,13)}
    all_items=row['分项强化']+row['串联']+row['验收']+row['专项']
    assert all(x['来源章']==n for x in all_items)
    assert all(all(p<n for p in x.get('可用前章',[])) for x in all_items)
    # 形式和显式范围记录的检查，不把它冒充机器证明“不超纲”。
    assert len(SEEDS[n])==8 and len(CHECKS[n])==16
    assert len({q for _,q,_ in CHECKS[n]})==16
    for tag,cloze,correct,wrong,chinese,reason in SEEDS[n]:
        assert all([tag,cloze,correct,wrong,chinese,reason])
        assert correct!=wrong,(n,correct)
        assert '___' in cloze,(n,cloze)
        assert '___' not in correct and '___' not in reason,(n,correct)
    for target in re.findall(r'\[\[([^]|]+)',s):
        if target.startswith('#'):
            assert target[1:] in re.findall(r'^#+ (.+)$',s,re.M),(quiz,target)
        else:
            assert any(p.stem==target for p in [ROOT/'00·从这里开始.md',*chapters,*list((ROOT/'强化题目').glob('*.md'))]),(quiz,target)
    questions+=len(before_answers)
assert questions==1278
assert questions==sum(40+len(EXTRA.get(n,[])) for n in range(1,32))
# 本章不得要求明确属于后章的结构操作；人工编排之外再检查几个关键前置风险。
early='\n'.join((ROOT/r['练习文件']).read_text(encoding='utf-8') for r in manifest[:12])
for forbidden in ['If I were','would have been','Had I known','Having finished','the house being built']:
    assert forbidden not in early,forbidden
original=json.loads((ROOT/'编排记录/来源映射.json').read_text(encoding='utf-8'))
for name,digest in original['原文件SHA256'].items():
    assert hashlib.sha256((ROOT.parent/name).read_bytes()).hexdigest()==digest
report={
 '章节':31,'专用练习MD':31,'基础每章任务':40,'第23章任务':56,
 '基础规则补练':{str(n):len(EXTRA[n]) for n in [20,21,25,26]},
 '总任务':questions,'强化核心情境':248,'独立验收题':372,'串联应用题':124,
 '检查':'31组往返与下一章链接、题号唯一、题答配对、折叠完整、来源章与前章范围记录、关键早期超纲风险通过；19份来源资料与当前登记哈希一致',
 '范围限度':'逐章按已讲主题人工编排并记录边界；结构检查不等于对所有自然语言含义的形式化证明',
}
(ROOT/'编排记录/强化题目检查结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
