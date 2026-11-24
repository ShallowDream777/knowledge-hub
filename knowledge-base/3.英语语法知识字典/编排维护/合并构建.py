"""生成主题文档及指向页内标题的树状索引。"""
from pathlib import Path
from collections import defaultdict
from urllib.parse import quote
import hashlib
import json
import os
import re
from 条目规划 import ENTRIES, CUSTOM, RELATED, ARTICLE_NOTES
from 主题布局 import TOPICS, relative_topic, topic_name, common_prefix, display, body_normalized
from 构建知识字典 import ROOT, COURSE, sources, source_hash, extract, polish, norm, DEEP, CUSTOM_CHAPTERS

INDEX=ROOT/'00·知识树总索引.md'
BY_ID={e['编号']:e for e in ENTRIES}


def link(label,target,current,heading=None):
    relative='' if target==current and heading else os.path.relpath(target,current.parent).replace('\\','/')
    if heading:relative+='#'+quote(heading,safe='')
    return f'[{label}](<{relative}>)'


def entry_link(entry,current):
    return link(entry['标题'],ROOT/relative_topic(entry),current,entry['标题'])


def node_link(parts,entries,current):
    files={relative_topic(e) for e in entries}
    if len(files)==1:
        target=ROOT/next(iter(files))
        full=TOPICS[next(iter(files))]
        prefix=common_prefix(full)
        heading=display(parts[-1]) if len(parts)>len(prefix) else topic_name(full[0])
        return link(display(parts[-1]),target,current,heading)
    return link(display(parts[-1]),INDEX,current,parts[0])


def tree_lines(entries,current,prefix=(),indent=0):
    lines=[];groups=defaultdict(list);leaves=[]
    for e in entries:
        if len(e['路径'])==len(prefix):leaves.append(e)
        else:groups[e['路径'][len(prefix)]].append(e)
    for group,items in groups.items():
        parts=(*prefix,group)
        if len(items)==1 and display(group)==items[0]['标题']:
            lines.append('  '*indent+'- '+entry_link(items[0],current))
        else:
            lines.append('  '*indent+'- **'+node_link(parts,items,current)+'**')
            lines+=tree_lines(items,current,parts,indent+1)
    for e in leaves:lines.append('  '*indent+'- '+entry_link(e,current))
    return lines


def content(entry):
    blocks=[];origins=[];chapters=[];seen=set()
    for spec in entry['来源']:
        n,title=spec.split(':',1)
        if n=='custom':
            body=CUSTOM[title];chapters+=CUSTOM_CHAPTERS[title]
            origins.append({'类型':'同主题对照整理','标识':title,'参考章':CUSTOM_CHAPTERS[title]})
        else:
            n=int(n);body=extract(n,title,entry['编号'] in DEEP);chapters.append(n)
            origins.append({'类型':'已校订课程','章':n,'小节':title})
        paragraphs=[]
        for p in re.split(r'\n\s*\n',polish(body)):
            key=norm(p)
            if key and key not in seen:paragraphs.append(p);seen.add(key)
        if paragraphs:blocks.append('\n\n'.join(paragraphs))
    if entry['编号'] in ARTICLE_NOTES:
        blocks.append(ARTICLE_NOTES[entry['编号']].strip())
        origins.append({'类型':'查询对照与边界补充','标识':entry['编号']})
    assert blocks,entry['编号']
    return '\n\n'.join(blocks),origins,sorted(set(chapters))


def section(entry,current,level,render_heading=True):
    body,origins,chapters=content(entry)
    # 原正文中的三级标题随条目整体下移，不改写文字内容。
    body=re.sub(r'^(#{3}) (.+)$',lambda m:'#'*(level+2)+' '+m.group(2),body,flags=re.M)
    text=('#'*level+' '+entry['标题']+'\n\n') if render_heading else ''
    text+='> **速查结论：**'+entry['速查']+'\n\n'
    text+='#'*(level+1)+' 规则、例句与使用边界\n\n'+body+'\n\n'
    return text,{'实际来源':origins,'关联课程':chapters,'正文SHA256':hashlib.sha256(body_normalized(body).encode('utf-8')).hexdigest(),'正文字符':len(body)}


def topic_footer(entries,current,metadata):
    """同页词目使用目录互达；跨主题引用与课程入口在文末各保留一份。"""
    related=defaultdict(list);seen=set()
    for entry in entries:
        for code in RELATED.get(entry['编号'],[]):
            target=BY_ID[code]
            if code not in seen and ROOT/relative_topic(target)!=current:
                related[topic_name(target)].append(target);seen.add(code)
    text=''
    if related:
        text+='## 相关条目\n\n'
        for topic,items in related.items():
            text+='- '+topic+'：'+'、'.join(entry_link(e,current) for e in items)+'\n'
        text+='\n'
    chapters=sorted({n for e in entries for n in metadata[e['编号']]['关联课程']})
    text+='## 课程与练习\n\n'
    for n in chapters:
        chapter=sources[n]
        quiz=next((COURSE/'强化题目').glob(f'{n:02}·强化练习·*.md'))
        text+='- '+link(f'课程第{n:02}章：'+chapter.stem.split('·',1)[1],chapter,current)+'；'+link('强化题',quiz,current)+'\n'
    heading='本页目录' if len(entries)>1 else entries[0]['标题']
    text+='\n'+link('本页目录' if len(entries)>1 else '页首',current,current,heading)+'　'+link('总索引',INDEX,current)+'\n'
    return text


def render_entries(entries,current,prefix,level,metadata):
    text='';groups=defaultdict(list);leaves=[]
    for e in entries:
        if len(e['路径'])==len(prefix):leaves.append(e)
        else:groups[e['路径'][len(prefix)]].append(e)
    for group,items in groups.items():
        parts=(*prefix,group)
        if len(items)==1 and display(group)==items[0]['标题']:
            section_text,data=section(items[0],current,level)
            text+=section_text;metadata[items[0]['编号']]=data
        else:
            text+='#'*level+' '+display(group)+'\n\n'
            text+=render_entries(items,current,parts,level+1,metadata)
    for e in leaves:
        section_text,data=section(e,current,level)
        text+=section_text;metadata[e['编号']]=data
    return text


def old_body(entry,path):
    s=path.read_text(encoding='utf-8')
    # 合并后的再次构建直接沿用清单中的正文哈希。
    if '锚点' in entry:return entry['正文SHA256']
    body=s.split('## 规则、例句与使用边界\n\n',1)[1]
    body=re.split(r'\n## (?:相关条目|课程与练习)',body,maxsplit=1)[0]
    return hashlib.sha256(body_normalized(body).encode('utf-8')).hexdigest()


def build():
    old_file=ROOT/'编排维护/条目来源映射.json'
    old=json.loads(old_file.read_text(encoding='utf-8')) if old_file.exists() else {'条目':[]}
    old_entries=old['条目'];previous={};obsolete=set()
    for e in old_entries:
        path=(ROOT/e['文件']).resolve()
        assert path.is_relative_to(ROOT) and path.is_file(),path
        previous[e['编号']]=old_body(e,path)
        obsolete.add(path)
        if '锚点' not in e:
            for i in range(1,len(e['路径'])+1):obsolete.add(ROOT.joinpath(*e['路径'][:i],'00·分区索引.md').resolve())
    # 所有文档在内存中生成并核对正文，再写入并移除旧的生成文件。
    outputs={};metadata={}
    for relative,entries in TOPICS.items():
        target=ROOT/relative;title=topic_name(entries[0]);prefix=common_prefix(entries)
        text='# '+title+'\n\n'+link('总索引',INDEX,target)+' › '+link(display(entries[0]['路径'][0]),INDEX,target,entries[0]['路径'][0])+'\n\n'
        if len(entries)==1 and entries[0]['标题']==title:
            section_text,data=section(entries[0],target,1,render_heading=False)
            text+=section_text;metadata[entries[0]['编号']]=data
        else:
            if len(entries)>1:
                text+='## 本页目录\n\n'+'\n'.join(tree_lines(entries,target,prefix))+'\n\n---\n\n'
            text+=render_entries(entries,target,prefix,2,metadata)
        text+=topic_footer(entries,target,metadata)
        outputs[target]=text
    assert set(metadata)==set(BY_ID)
    changes=[code for code,sha in previous.items() if metadata[code]['正文SHA256']!=sha]
    assert not changes,('合并不能改变正文',changes)
    prefixes={tuple(e['路径'][:i]) for e in ENTRIES for i in range(1,len(e['路径'])+1)}
    master='# 英语语法索引\n\n'+f'{len(ENTRIES)} 条目 · {len(TOPICS)} 主题文档 · 12 分区 · '+link('课程目录',COURSE/'00·从这里开始.md',INDEX)+'\n\n'
    for group in dict.fromkeys(e['路径'][0] for e in ENTRIES):
        master+='## '+group+'\n\n'+'\n'.join(tree_lines([e for e in ENTRIES if e['路径'][0]==group],INDEX,(group,)))+'\n\n'
    outputs[INDEX]=master
    for path,text in outputs.items():
        assert path.resolve().is_relative_to(ROOT)
        if path.exists() and path.resolve() not in obsolete and path!=INDEX:
            raise FileExistsError('目标未登记，停止以防覆盖：'+str(path))
    for path,text in outputs.items():
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')
    manifest=[{**e,'文件':str(relative_topic(e)),'锚点':e['标题'],'主题':topic_name(e),**metadata[e['编号']]} for e in ENTRIES]
    new_paths={path.resolve() for path in outputs}
    removed=[]
    for stale in sorted(obsolete-new_paths):
        assert stale.is_relative_to(ROOT)
        if stale.exists():stale.unlink();removed.append(str(stale.relative_to(ROOT)))
    for directory in sorted((p for p in ROOT.rglob('*') if p.is_dir()),key=lambda p:len(p.parts),reverse=True):
        assert directory.resolve().is_relative_to(ROOT)
        if not any(directory.iterdir()):directory.rmdir()
    result={'课程文件SHA256':source_hash,'条目':manifest,'分区数':len(prefixes),'条目数':len(ENTRIES),'主题文档数':len(TOPICS),'布局':'主题文档＋标题锚点'}
    old_file.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    report={'合并前读者文件':len(obsolete)+1,'合并后读者文件':len(outputs),'知识条目':len(ENTRIES),'主题文档':len(TOPICS),'正文保持一致':len(previous),'正文变化':changes,'移除旧生成文件':removed}
    audit=ROOT/'编排维护/主题合并记录.json'
    if removed or not audit.exists():audit.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='移除旧生成文件'},ensure_ascii=False))
