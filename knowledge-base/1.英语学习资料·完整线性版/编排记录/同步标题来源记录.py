"""核对已登记的标题和阅读体验校订，更新字典正文与课程来源校验值。"""
from pathlib import Path
import hashlib
import json
import re
from 标题优化 import VAULT, rename_text
from 阅读体验优化 import wording

RECORD=Path(__file__).resolve().parent
ROOT=VAULT/'英语语法知识字典'
manifest_path=ROOT/'编排维护/条目来源映射.json'
data=json.loads(manifest_path.read_text(encoding='utf-8'))

def body(text,entry):
    heads=list(re.finditer(r'^(#{1,6}) (.+)$',text,re.M))
    h=next(m for m in heads if m[2]==entry['锚点'])
    level=len(h[1])
    end=next((m.start() for m in heads if m.start()>h.start() and len(m[1])<=level),len(text))
    section=text[h.end():end]
    marker='#'*(level+1)+' 规则、例句与使用边界\n\n'
    return re.split(r'\n(?:#{'+str(level+1)+r'} (?:相关条目|课程与练习)|\[(?:本页目录|页首)\]\(<)',section.split(marker,1)[1],maxsplit=1)[0].strip()

def digest_body(text):
    return hashlib.sha256(re.sub(r'^#{1,6} ', '# ',text.strip(),flags=re.M).encode('utf-8')).hexdigest()

changed=0
for entry in data['条目']:
    path=ROOT/entry['文件']
    snapshot=RECORD/'标题优化前快照'/(str(path.relative_to(VAULT))+'.snapshot')
    if not snapshot.exists():snapshot=RECORD/'阅读体验优化前快照'/(str(path.relative_to(VAULT))+'.snapshot')
    old_text=snapshot.read_text(encoding='utf-8') if snapshot.exists() else path.read_text(encoding='utf-8')
    old=body(old_text,entry)
    new=body(path.read_text(encoding='utf-8'),entry)
    assert entry['正文SHA256'] in {digest_body(old),digest_body(new)},('正文记录不一致',entry['编号'])
    assert wording(rename_text(old,path))==new,('未登记的正文变化',entry['编号'])
    if old!=new:changed+=1
    entry['正文SHA256']=digest_body(new)
    if entry['编号']=='M01':entry['路径'][1]='01 情态动词基础'
data['课程文件SHA256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (VAULT/'英语学习资料·完整线性版/章节').glob('*.md')}
manifest_path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'字典 {len(data["条目"])} 个条目正文核对通过；其中 {changed} 个条目含已登记的标题或文字调整。')
