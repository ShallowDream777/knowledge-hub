"""核对改名范围、重复运行、原标题残留及全部阅读文件的本地链接。"""
from pathlib import Path
from urllib.parse import unquote
from collections import Counter, defaultdict
import hashlib
import json
import re
from 标题优化 import VAULT, reader_files, rename_text
from 阅读体验优化 import improve
from 标题同行标签 import SUFFIX

RECORD=Path(__file__).resolve().parent
BACKUP=RECORD/'标题优化前快照'
record_path=RECORD/'标题调整明细.json'
record=json.loads(record_path.read_text(encoding='utf-8'))
files=reader_files()
texts={p:p.read_bytes().decode('utf-8') for p in files}
before=dict(texts)
for row in record['修改文件']:
    path=VAULT/row['文件']
    raw=(BACKUP/(row['文件']+'.snapshot')).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==row['修改前SHA256'],row['文件']
    before[path]=raw.decode('utf-8')
    expected=improve(rename_text(before[path],path).replace('\r\n','\n'),path)
    assert expected==texts[path].replace('\r\n','\n'),('修改超出已登记的标题与阅读体验调整',row['文件'])
    row['修改后SHA256']=hashlib.sha256(path.read_bytes()).hexdigest()
    old=Counter(re.findall(r'^#{1,6} ([^\r\n]+)',before[path],re.M))
    new=Counter(re.findall(r'^#{1,6} ([^\r\n]+)',texts[path],re.M))
    expected_headings=Counter(re.findall(r'^#{1,6} ([^\r\n]+)',expected,re.M))
    assert expected_headings==new,('标题数量与迁移计划不同',row['文件'])
    assert not any(count>max(1,old.get(SUFFIX.sub('',h),0)) for h,count in new.items()),('新增重名标题',row['文件'])
for path,text in texts.items():
    assert rename_text(text,path)==text,('残留待改标题',str(path))
    assert '<!-- study-priority:' not in text,path

by_stem=defaultdict(list)
for p in files:
    by_stem[p.stem].append(p)
resources=defaultdict(list)
for p in VAULT.rglob('*'):
    if p.is_file() and p.suffix in {'.md','.png','.jpg','.pdf'}:
        resources[p.name].append(p)
        resources[p.stem].append(p)

def broken_links(corpus):
    heads={p:set(re.findall(r'^#{1,6} ([^\r\n]+)',s,re.M)) for p,s in corpus.items()}
    broken=set()
    checked=0
    for path,s in corpus.items():
        for target in re.findall(r'\[\[([^]|\r\n]+)',s):
            name,sep,heading=target.partition('#')
            if not name:
                destination=path
            else:
                candidate=path.parent/name
                if candidate.suffix!='.md':candidate=Path(str(candidate)+'.md')
                candidates=by_stem.get(Path(name).stem if name.endswith('.md') else name,[])
                available=resources.get(name,[])
                destination=candidate if candidate.is_file() else (candidates[0] if len(candidates)==1 else (available[0] if len(available)==1 else None))
            checked+=1
            if destination is None or (sep and heading not in heads.get(destination,set())):
                broken.add((str(path.relative_to(VAULT)),target))
        for href in re.findall(r'\]\(<([^>\r\n]+)>\)',s):
            if re.match(r'\w+://',href):continue
            name,sep,heading=href.partition('#')
            destination=(path.parent/unquote(name)).resolve() if name else path
            checked+=1
            if not destination.is_file() or (sep and unquote(heading) not in heads.get(destination,set())):
                broken.add((str(path.relative_to(VAULT)),href))
    return broken,checked

old_bad,_=broken_links(before)
new_bad,link_count=broken_links(texts)
introduced=new_bad-old_bad
assert not introduced,('改名新增无效链接',sorted(introduced))
record_path.write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
result={'通过':True,'检查文件':len(files),'修改文件':len(record['修改文件']),'修改标题':record['修改标题数'],
        '检查链接':link_count,'新增无效链接':0,'已有无效链接':sorted(new_bad),
        '正文保留核对':'逐字节快照经已登记的标题、链接与阅读体验调整后，与当前文件一致；具体内容调整另见阅读体验调整明细。'}
(RECORD/'标题优化检查结果.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
