from pathlib import Path
from collections import Counter
from html.parser import HTMLParser
import hashlib
import json
import re

R=Path(__file__).resolve().parent
ROOT=R.parent
manifest=json.loads((R/'题目清单.json').read_text(encoding='utf-8'))
stats=json.loads((R/'阅读考点统计.json').read_text(encoding='utf-8'))
inventory=json.loads((R/'文件清点.json').read_text(encoding='utf-8'))
checks=[]


def require(ok,label):
    assert ok,label
    checks.append(label)


class FoldParser(HTMLParser):
    def __init__(self):super().__init__();self.text=[];self.paragraphs=0
    def handle_data(self,data):self.text.append(data)
    def handle_starttag(self,tag,attrs):
        if tag=='p':self.paragraphs+=1


files=list(ROOT.rglob('*.md'))
by_stem={}
for p in ROOT.rglob('*'):
    if p.is_file():by_stem.setdefault(p.stem,[]).append(p)
for p in files:
    s=p.read_text(encoding='utf-8')
    require(s.count('<details>')==s.count('</details>'),f'折叠闭合：{p.name}')
    headings=re.findall(r'^#{1,6} (.+)$',s,re.M)
    for target in re.findall(r'!?\[\[([^]|]+)',s):
        if target.startswith('#'):require(target[1:] in headings,f'锚点：{p.name}/{target}')
        else:
            stem=Path(target.split('#')[0]).stem
            require(stem in by_stem and len(by_stem[stem])==1,f'唯一跳转目标：{p.name}/{target}')
    for fold in re.findall(r'<details>\s*<summary>.*?</summary>([\s\S]*?)</details>',s):
        parser=FoldParser();parser.feed(fold);visible=''.join(parser.text)
        require('**' not in visible and not re.search(r'`[^`]+`',visible),f'答案无裸Markdown：{p.name}')
        require(parser.paragraphs>0,f'答案有HTML段落：{p.name}')

total=0;mc_count=0;letters=Counter();essays=[]
for row in manifest:
    n=row['章'];chapter=ROOT/row['正文'];quiz=ROOT/row['练习'];s=quiz.read_text(encoding='utf-8');cs=chapter.read_text(encoding='utf-8')
    expected=[f'Q{i:02}' for i in range(1,row['任务']+1)]
    qids=re.findall(r'^\*\*(Q\d{2})\*\*',s,re.M)
    aids=re.findall(r'<strong>(Q\d{2})　答案</strong>',s)
    require(qids==aids==expected,f'题答逐项配对：第{n}章')
    require(f'[[{quiz.stem}|' in cs and s.count(f'[[{chapter.stem}|返回本章正文]]')==2,f'正文练习往返：第{n}章')
    if n<16:
        nxt=(ROOT/manifest[n]['正文']).stem
        require(cs.count(f'[[{nxt}|')==2 and f'[[{nxt}|' in s,f'下一章保留：第{n}章')
    require(len(row['题目'])==row['任务'],f'清单题量：第{n}章')
    if 2<=n<=14:require(bool(row['独立验收']),f'独立验收存在：第{n}章')
    for item in row['题目']:
        require(bool(item['显示答案'].strip()) and bool(item['解析'].strip()),f'非空答案解析：{n}/{item["编号"]}')
        if item['类型']=='单选':
            require(len(item['选项'])==len(set(item['选项']))==4,f'四项互异：{n}/{item["编号"]}')
            require(item['选项']['ABCD'.index(item['正确字母'])]==item['正确项'],f'字母与正确项一致：{n}/{item["编号"]}')
            letters[item['正确字母']]+=1;mc_count+=1
        if item['类型']=='作文':
            words=len(re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\b\d+\b",item['答案']))
            require(words>=150,f'完整范文达150词：{n}/{item["编号"]}')
            essays.append({'章':n,'题号':item['编号'],'词数':words})
    total+=row['任务']
require(total==426 and sum(r['任务'] for r in manifest[:15])==349,'426任务与349原创项')
require(manifest[14]['任务']==manifest[15]['任务']==77,'模拟与真题各75客观＋2主观')
for i in range(55,75):
    require(f'空{i+1}' in manifest[14]['题目'][i]['题目'],f'模拟短文完成原题号一致：{i+1}')
require(manifest[11]['任务']==40,'短文完成两套各20空')
require(manifest[10]['任务']==30,'完形三篇各10空')
require(stats['总题数']==150 and sum(x['题数'] for x in stats['分类'])==150,'阅读统计总数150')
for row in inventory:
    require(hashlib.sha256(Path(row['路径']).read_bytes()).hexdigest()==row['SHA256'],f'来源未改：{row["文件"]}')
require(len(inventory)==14 and sum('重复于' not in x for x in inventory)==12,'14份去重为12份')
images=list((ROOT/'原卷页').glob('2021-*.png'))
require(len(images)==13,'2021连续原卷13页')
raw=(ROOT/manifest[15]['练习']).read_text(encoding='utf-8')
for i in range(1,14):require(raw.count(f'![[2021-{i:02}.png]]')==1,f'原卷第{i}页仅出现一次')
require('已在第14章出现' in raw,'熟悉写作题的复写边界已注明')
require('缺2024年' in (ROOT/'00·考试强化总目录.md').read_text(encoding='utf-8'),'缺年范围已注明')
answerdata=json.loads((R/'2021答案校订.json').read_text(encoding='utf-8'))
require([x['题号'] for x in answerdata]==list(range(1,76)),'2021答案1—75完整')
require(answerdata[9]['答案']=='A' and '误标C' in answerdata[9]['课程解析'],'2021第10题字母笔误校订')

report={'通过':True,'检查项':len(checks),'独立正文':16,'专用练习':16,'原创任务':349,'真题任务':77,'总任务':total,
        '四选一题':mc_count,'选择题答案分布':dict(letters),'完整范文':essays,'原卷页':13,
        '读取资料页数':sum(x.get('PDF页数',0) for x in inventory),
        '检查范围':'链接、图片、题答配对、题量口径、选项与答案一致、范文词数、样本统计与来源文件哈希；自动检查不替代具体题意与自然语言审读。'}
(R/'检查结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False))
