"""学习要求附在标题后；下级继承相同要求，并同步章节锚点。"""
from pathlib import Path
from urllib.parse import quote, unquote
import re, json, hashlib

RECORD=Path(__file__).resolve().parent
VAULT=RECORD.parents[1]
RECORD_FILE=RECORD/'标题同行标签明细.json'
LABELS='必学|识读即可|同主题复盘|选做·综合复盘|考试必学'
SUFFIX=re.compile(r'\s*【('+LABELS+r')】$')
LINE=re.compile(r'^> \*\*【('+LABELS+r')】\*\*(.*)$')

def arrange(text):
    lines=text.split('\n');heads=[];last=None;remove=set();notes={}
    for i,line in enumerate(lines):
        m=re.match(r'^(#{1,6}) (.+)$',line)
        if m:
            label=SUFFIX.search(m[2])
            last={'line':i,'level':len(m[1]),'title':SUFFIX.sub('',m[2]),
                  'old':m[2],'label':label[1] if label else None}
            heads.append(last)
        tag=LINE.match(line)
        if tag:
            assert last is not None,('标签没有标题',line)
            assert not last['label'] or last['label']==tag[1],('同一标题要求冲突',last)
            last['label']=tag[1]
            if tag[2].strip():notes[i]='> '+tag[2].strip()
            else:remove.add(i)
    stack=[];mapping={};placed=0;suppressed=0
    for h in heads:
        while stack and stack[-1][0]>=h['level']:stack.pop()
        inherited=stack[-1][1] if stack else None
        own=h['label'];effective=own or inherited
        show=own and own!=inherited
        title=h['title']+('　【'+own+'】' if show else '')
        lines[h['line']]='#'*h['level']+' '+title
        if title!=h['old']:mapping[h['old']]=title
        if show:placed+=1
        elif own:suppressed+=1
        stack.append((h['level'],effective))
    result='\n'.join(notes.get(i,l) for i,l in enumerate(lines) if i not in remove)
    result=re.sub(r'\n{4,}','\n\n\n',result)
    return result,mapping,{'保留同行标签':placed,'省去同要求子标签':suppressed}

def mapping_data():
    return json.loads(RECORD_FILE.read_text(encoding='utf-8')) if RECORD_FILE.exists() else {'锚点映射':{}}

def rewrite_links(text,path,maps):
    path=Path(path).resolve()
    by_stem={}
    for rel in maps:by_stem.setdefault(Path(rel).stem,[]).append(rel)
    def new_anchor(target,anchor):
        try:rel=target.resolve().relative_to(VAULT).as_posix()
        except ValueError:return anchor
        return maps.get(rel,{}).get(anchor,anchor)
    def wiki(m):
        name,sep,anchor=m[1].partition('#')
        if not sep:return m[0]
        if name:
            dest=path.parent/(name if name.endswith('.md') else name+'.md')
            if not dest.exists():
                choices=by_stem.get(Path(name).stem,[])
                if len(choices)!=1:return m[0]
                dest=VAULT/choices[0]
        else:dest=path
        new=new_anchor(dest,anchor)
        if new==anchor:return m[0]
        display=m[2] if m[2] is not None else (anchor if not name else m[1])
        return '[['+name+'#'+new+'|'+display+']]'
    text=re.sub(r'\[\[([^\]|\n]+)(?:\|([^\]\n]*))?\]\]',wiki,text)
    def markdown(m):
        href=m[1];name,sep,anchor=href.partition('#')
        if not sep or re.match(r'\w+://',name):return m[0]
        dest=(path.parent/unquote(name)) if name else path
        decoded=unquote(anchor);new=new_anchor(dest,decoded)
        if new==decoded:return m[0]
        return '](<'+name+'#'+quote(new,safe='')+'>)'
    return re.sub(r'\]\(<([^>\n]+)>\)',markdown,text)

def format_reader(text,path):
    text,_,_=arrange(text)
    text=rewrite_links(text,path,mapping_data()['锚点映射'])
    if Path(path).name=='00·从这里开始.md':
        old='未另标的段落沿用最近的上级要求；同一知识点在归纳表再次出现，沿用前面的深度，不因重复出现就升级。'
        new='学习标签放在标题旁；子标题与上级要求相同时不重复标注，未标段落沿用最近的上级要求。同一知识点在归纳表再次出现，沿用前面的深度，不因重复出现就升级。'
        text=text.replace(old,new)
    return text

def apply():
    from 标题优化 import reader_files
    files=reader_files();maps={};stats={};rows=[]
    for p in files:
        _,mapping,count=arrange(p.read_text(encoding='utf-8'))
        if mapping:maps[p.relative_to(VAULT).as_posix()]=mapping
        if count['保留同行标签'] or count['省去同要求子标签']:stats[p.relative_to(VAULT).as_posix()]=count
    assert not RECORD_FILE.exists(),'迁移已执行；后续使用阅读体验优化.apply_tree保持格式'
    data={'锚点映射':maps,'标签统计':stats,'修改文件':[]}
    RECORD_FILE.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    for p in files:
        raw=p.read_bytes();before=raw.decode('utf-8').replace('\r\n','\n')
        after=format_reader(before,p)
        assert format_reader(after,p)==after,('重复执行不稳定',p)
        if after==before:continue
        snapshot=RECORD/'标题同行标签前快照'/(str(p.relative_to(VAULT))+'.snapshot')
        snapshot.parent.mkdir(parents=True,exist_ok=True);snapshot.write_bytes(raw)
        p.write_bytes(after.replace('\n','\r\n' if b'\r\n' in raw else '\n').encode('utf-8'))
        rows.append({'文件':p.relative_to(VAULT).as_posix(),'修改前SHA256':hashlib.sha256(raw).hexdigest(),'修改后SHA256':hashlib.sha256(p.read_bytes()).hexdigest()})
    data['修改文件']=rows
    RECORD_FILE.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'修改文件':len(rows),'同行标签':sum(x['保留同行标签'] for x in stats.values()),'去除重复子标签':sum(x['省去同要求子标签'] for x in stats.values())},ensure_ascii=False))

if __name__=='__main__':apply()
