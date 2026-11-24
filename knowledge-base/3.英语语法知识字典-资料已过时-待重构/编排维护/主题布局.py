"""文件按主题合并；知识分类与词目不依赖文件数量。"""
from pathlib import Path
from collections import defaultdict
import re
import sys
sys.path.append(str(Path(__file__).resolve().parents[2]/'英语学习资料·完整线性版/编排记录'))
from 标题优化 import rename_text
from 条目规划 import ENTRIES


def topic_name(entry):
    code=entry['编号']
    n=int(code[1:])
    kind=code[0]
    if kind=='N':return '名词'
    if kind=='A':return '冠词与限定词'
    if kind=='P':return '代词'
    if kind=='J':return '形容词与副词'
    if kind=='Q':return '数词'
    if kind=='R':return '介词'
    if kind=='W':return '构词法' if n<=6 else ('感叹词' if n==7 else '字母与音素')
    if kind=='S':
        if n<=10:return '句法概念与句子成分'
        if n<=15:return '基本句型'
        if n<=22:return '句子类型'
        return '句子结构与存在句'
    if kind=='V':return '动词'
    if kind=='T':return '时态与体'
    if kind=='G':return '主谓一致'
    if kind=='B':return '语态'
    if kind=='M':return '情态动词'
    if kind=='F':return '非谓语动词'
    if kind=='C':
        if n<=5:return '连词与从句概念'
        if n<=11:return '名词性从句'
        if n<=19:return '定语从句'
        if n<=29:return '状语从句'
        return '直接引语与间接引语'
    if kind=='H':return '虚拟语气'
    if kind=='X':return '倒装' if n<=3 else ('强调' if n<=6 else '省略')
    if kind=='D':return '语篇与标点'
    raise ValueError(code)


def relative_topic(entry):
    return Path(entry['路径'][0])/(topic_name(entry)+'.md')


TOPICS=defaultdict(list)
for entry in ENTRIES:TOPICS[relative_topic(entry)].append(entry)


def common_prefix(entries):
    result=[]
    for values in zip(*(entry['路径'] for entry in entries)):
        if len(set(values))!=1:break
        result.append(values[0])
    return tuple(result)


def display(name):
    return re.sub(r'^\d+\s+','',name)


def body_normalized(text):
    """合并时仅允许改变标题层级；正文文字、表格和例句须逐条保持。"""
    return re.sub(r'^#{1,6} ', '# ',rename_text(text.strip()),flags=re.M)
