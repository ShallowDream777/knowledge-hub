"""验证标签不删知识、选做不进首轮分母、原题与答案不被分层改写。"""
from pathlib import Path
from collections import Counter
import hashlib
import json
import math
import re
from 学习分层 import strip_labels,B_RULES,annotate_body,managed,guide_note
from 标题优化 import rename_text
from 阅读体验优化 import foundation_chapter
from 后续章节试读校订 import revise_quiz

ROOT=Path(__file__).resolve().parents[1]
R=ROOT/'编排记录';SNAP=R/'学习分层前快照'
data=json.loads((R/'学习分层明细.json').read_text(encoding='utf-8'))
current=json.loads((R/'强化题目清单.json').read_text(encoding='utf-8'))
old=json.loads((SNAP/'编排记录/强化题目清单.json.snapshot').read_text(encoding='utf-8'))
checks=[]
def need(ok,label):
    assert ok,label
    checks.append(label)

def knowledge_only(text):
    text=strip_labels(text)
    text=rename_text(text)
    text=foundation_chapter(text)
    text=re.sub(r'\n## 本章强化与验收\n[\s\S]*?(?=\n---\n\n\[\[00·从这里开始)', '',text)
    # 编辑器对齐表格时会补空格和横线；逐格比较内容，忽略这些排版差异。
    lines=[]
    for line in text.splitlines():
        if line.strip().startswith('|') and line.strip().endswith('|'):
            cells=[cell.strip() for cell in line.strip()[1:-1].split('|')]
            if all(re.fullmatch(r':?-{3,}:?',cell) for cell in cells):
                cells=[re.sub(r'-+', '---',cell) for cell in cells]
            line='|'+'|'.join(cells)+'|'
        lines.append(line)
    text='\n'.join(lines)
    return re.sub(r'\s+',' ',text).strip()

need('study-priority' not in managed('> **【必学】**')+guide_note(),'生成器不再输出维护标记')
need('study-priority' not in (ROOT/'00·从这里开始.md').read_text(encoding='utf-8'),'入口页无维护标记')
sample='# 验证章节\n\n## 将来完成时\n\n正文与读者批注。\n> 自己记录的复习提醒。\n'
once,_=annotate_body(15,sample)
twice,_=annotate_body(15,once)
need(knowledge_only(once)==knowledge_only(sample),'纯文本标签可移除且保留读者批注')
need(twice.count('【识读即可】')==once.count('【识读即可】')==1,'重复标记不会累积学习标签')

for p in sorted((ROOT/'章节').glob('*.md')):
    before=(SNAP/'章节'/(p.name+'.snapshot')).read_text(encoding='utf-8')
    now=p.read_text(encoding='utf-8')
    need(knowledge_only(before)==knowledge_only(now),f'知识正文无删改：{p.name}')
    need('【必学】' in now,f'读者就地可见要求：{p.name}')
    need('<!-- study-priority:' not in now,f'阅读正文无维护标记：{p.name}')
    for anchor in re.findall(r'\[\[#([^]|]+)',now):
        need(anchor in re.findall(r'^#+ (.+)$',now,re.M),f'原目录锚点可用：{p.name}/{anchor}')

required=0;optional=0
for prev,row in zip(old,current):
    n=row['章'];plan=row['首轮分层'];quiz=(ROOT/row['练习文件']).read_text(encoding='utf-8')
    need(n==prev['章'] and row['题量']==prev['题量'],f'原章与题量保留：{n}')
    for key,prefix in [('分项强化','A'),('串联','B'),('验收','C'),('专项','D')]:
        need(len(prev[key])==len(row[key]),f'原组题量保留：{n}/{key}')
        ids=[]
        for i,(a,b) in enumerate(zip(prev[key],row[key]),1):
            for field in ['题目','答案','知识点','类型','来源章']:
                expected=revise_quiz(a[field],n) if isinstance(a[field],str) else a[field]
                need(expected==b[field],f'原题属性保留或经登记纠正：{n}/{prefix}{i:02}/{field}')
            need(b['首轮要求'] in ['必做','识读必做','选做'],f'题目有明确首轮要求：{n}/{prefix}{i:02}')
            need(f'【{b["首轮要求"]}】{b["知识点"]}' in quiz,f'标记实际落盘：{n}/{prefix}{i:02}')
            if b['首轮要求']!='选做':ids.append(f'{prefix}{i:02}');required+=1
            else:optional+=1
        need(ids==plan['题单'][prefix],f'首轮题号恰与必做对应：{n}/{prefix}')
    maximum=2*len(plan['题单']['C']);threshold=math.ceil(maximum*0.8)
    need(plan['验收满分']==maximum and plan['验收建议']==threshold,f'验收分母排除选做：{n}')
    need(f'至少{threshold}/{maximum}' in quiz,f'首轮分数落盘：{n}')
    need('第二轮完整复习' in quiz and '七个月首轮题单' in quiz,f'两轮标准区分：{n}')

need(required+optional==1278,'题库1278项完整保留')
need(not data['放心跳过的完整知识点'],'未凭未命中新增放心跳过标签')
matched={(x['章'],x['标题']) for x in data['知识标记'] if x['深度']=='B'}
need(set(B_RULES)<=matched,'所有识读规则匹配实际小节')
for key in ['E04','E15','E16','E18','E19']:
    need(key in data['真题定位'],f'关键反例保留：{key}')
for name,digest in json.loads((R/'来源映射.json').read_text(encoding='utf-8'))['原文件SHA256'].items():
    need(hashlib.sha256((ROOT.parent/name).read_bytes()).hexdigest()==digest,f'来源文件与登记哈希一致：{name}')

result={'通过':True,'核查项':len(checks),'基础章节':31,'原题保留':required+optional,'首轮必做':required,'选做':optional,
        '标记位置数':dict(Counter(x['深度'] for x in data['知识标记'])),
        '放心跳过的完整知识点':0,'范围':'内容保留、题答保留、标记和题单一致、首轮计分、原资料哈希；不把自动检查作为语法考频证明。'}
(R/'学习分层检查结果.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
