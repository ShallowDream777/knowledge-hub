"""验证已识别的先修断层、验收范围与关键知识保留；不声称机器证明全部教学效果。"""
from pathlib import Path
import json
import re
import hashlib
from 答案排版 import markdown_answers_for_check
from 强化题库 import SEEDS,CHECKS

ROOT=Path(__file__).resolve().parents[1]
chapters={int(p.name[:2]):p for p in (ROOT/'章节').glob('*.md')}
text={n:markdown_answers_for_check(p.read_text(encoding='utf-8')) for n,p in chapters.items()}
tests=[]


def require(condition,label):
    assert condition,label
    tests.append(label)


def before(n,a,b):
    require(a in text[n] and b in text[n] and text[n].index(a)<text[n].index(b),f'第{n:02}章先解释：{a[:22]}')


before(1,'叫**动词原形**','**be是一个动词的原形')
before(1,'be是一个动词的原形','| I（我） | am |')
before(1,'**主语**是句子正在谈论','这个位置叫**宾语**')
require('am/are 是 be 的形式' not in text[1],'旧起步句已替换')
for term in ["don't", "doesn't",'do/does','She likes','SVOC','动名词','同位语','宾补']:
    require(term not in text[1],f'第一章不提前要求：{term}')
first_exam='\n'.join(q for _,q,_ in CHECKS[1])
for term in ['宾补','同位语','非谓语','do/does','to read','一般疑问句']:
    require(term not in first_exam,f'第一章验收不含：{term}')
require(SEEDS[1][5][0]=='名词短语' and SEEDS[1][6][0]=='动作句','第一章动作否定与三单情境已替换')
before(3,'for me＝给我','2. **宾格作宾语**')
require('改为否定和一般疑问句' not in text[3],'第3章不提前操作问句')
before(4,'**音素**是区别单词读音','a 用在辅音音素开头')
before(4,'**音标**','useful 以 j 音开头')
before(6,'**音节**可以理解为','| 单音节 |')
before(6,'**重音**是读一个词','| 重读闭音节 |')
before(7,'叫**动名词**','介词后必须接**名词、代词宾格或动名词**')
before(9,'sb是somebody的缩写','explain sth to me')
before(9,'简称宾补','对应主谓宾补（SVOC）句型')
before(10,'不定式to read','可由名词、代词、动名词、不定式')
before(11,'do not常缩写don\'t','| She likes tea.')
before(12,'不能把“单数主语”一概等同于“动词加s”','### 什么是主谓一致')
before(13,'**规则变化**' if '**规则变化**' in text[13] else '“规则变化”指','| 原形 | 过去式 | 过去分词 |')
before(13,'### 持续状态、单次事件与for／since','#### 现在完成时')
require('#### 16 种时态总表' not in text[13] and '#### 16 种时态总表' in text[23],'16格总表在完整组合学习后保留')
before(17,'叫不定式','see／hear／make 等的这类结构')
require('be used to do与习惯表达的区别' in text[17],'习惯与用途被动知识保留在第17章')
require('八大句子成分 · 一眼看懂表' in text[10],'原成分总表保留在第10章')
require('术语串联：词类、句子职位与逻辑关系' in text[25],'原高级术语知识在第25章归纳')
q23=re.search(r'### 三大从句高频易错自查[\s\S]*?</details>',text[23]).group()
require('13. While I' in q23 and '(was reading / will read / am reading)' in q23,'第23章超前虚拟自测已改为过去背景')
require('knew / knows / will know' not in q23,'第23章不验收第28章的形式选择')
for n,total in [(5,30),(6,25),(8,25)]:
    block=re.search(r'### [^\n]*高频易错自查[\s\S]*?<details>',text[n]).group()
    require(block.count('（句意：')==total,f'第{n:02}章原自测附足{total}题中文句意')
q6=re.search(r'### 形容词与副词高频易错自查[\s\S]*?<details>',text[6]).group()
require('18. He ______ late.' in q6,'第6章不提前用自测验收动词三单')
q8=re.search(r'### 数词与冠词高频易错自查[\s\S]*?<details>',text[8]).group()
require('number of students' not in q8,'第8章不提前考第27章number of的区别')
require('wish 与 if only 的虚拟' in text[28] and 'as if / as though 的虚拟' in text[28],'虚拟知识在第28章完整保留')
active=[ROOT/'00·从这里开始.md',*chapters.values(),*list((ROOT/'强化题目').glob('*.md'))]
for p in active:
    matches=list(ROOT.rglob(p.name))
    require(len(matches)==1,f'现行笔记唯一：{p.name}')
baseline=json.loads((ROOT/'编排记录/先修修复前快照/文件哈希.json').read_text(encoding='utf-8'))
for name,sha in baseline.items():
    p=ROOT/'编排记录/先修修复前快照'/name
    if p.suffix=='.md':p=p.with_suffix('.md.snapshot')
    require(hashlib.sha256(p.read_bytes()).hexdigest()==sha,f'修复前备份完整：{name}')
report={'通过':True,'核对项':len(tests),'检查项目':tests,'独立章节':len(chapters),
        '限度':'核对已识别的具体先修风险、验收题、知识移位与备份。先修判断包含人工审读，自动检查不等于全部教学效果或所有新词发音均已验证。'}
(ROOT/'编排记录/先修衔接检查结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k!='检查项目'},ensure_ascii=False))
