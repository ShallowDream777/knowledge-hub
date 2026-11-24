"""检查主题文件、标题锚点、词目覆盖及正文完整性。"""
from pathlib import Path
from collections import Counter
from urllib.parse import unquote
import hashlib
import json
import re
from 主题布局 import body_normalized

ROOT=Path(__file__).resolve().parents[1]
COURSE=ROOT.parent/'英语学习资料·完整线性版'
manifest=json.loads((ROOT/'编排维护/条目来源映射.json').read_text(encoding='utf-8'))
entries=manifest['条目']
errors=[]


def require(ok,message):
    if not ok:errors.append(message)


def links(text):
    return [(m.group(1),m.group(2)) for m in re.finditer(r'\[([^\]\n]+)\]\(<([^>\n]+)>\)',text)]


def destination(current,href):
    path,sep,fragment=href.partition('#')
    return ((current.parent/unquote(path)).resolve() if path else current.resolve(),unquote(fragment) if sep else '')


def headings(text):
    result=[];inside=False;offset=0
    for line in text.splitlines(keepends=True):
        if line.startswith('```'):inside=not inside
        if not inside:
            m=re.match(r'^(#{1,6}) (.+?)\s*$',line)
            if m:result.append((len(m[1]),m[2],offset,offset+len(line)))
        offset+=len(line)
    return result


ids=[e['编号'] for e in entries]
require(len(ids)==len(set(ids)),'条目编号重复')
targets=[((ROOT/e['文件']).resolve(),e['锚点']) for e in entries]
require(len(targets)==len(set(targets)),'条目定位重复')
topic_files={path for path,_ in targets}
require(len(topic_files)==manifest['主题文档数'],'主题文件统计错误')
index=(ROOT/'00·知识树总索引.md').resolve()
all_md=[p.resolve() for p in ROOT.rglob('*.md') if '编排维护' not in p.parts]
require(set(all_md)==topic_files|{index},'存在漏生成或未清理的旧文件')
require(len({e['路径'][0] for e in entries})==12,'一级分区数错误')
texts={p:p.read_text(encoding='utf-8') for p in all_md}
all_heads={p:headings(s) for p,s in texts.items()}
root_targets=Counter(destination(index,h) for _,h in links(texts[index]))
link_count=0;anchor_count=0;body_chars=0;hash_checked=0
for path,s in texts.items():
    require(s.count('```')%2==0,f'代码围栏未闭合：{path.name}')
    for label,href in links(s):
        link_count+=1
        target,anchor=destination(path,href)
        require(target.is_file(),f'文件不存在：{path.name} → {href}')
        if anchor and target.is_file():
            anchor_count+=1
            hs=all_heads[target] if target in all_heads else headings(target.read_text(encoding='utf-8'))
            matches=[h for h in hs if h[1]==anchor]
            require(len(matches)==1,f'锚点不存在或不唯一：{path.name} → {href}')
    hs=all_heads[path]
    for a,b in zip(hs,hs[1:]):
        if b[0]<=a[0]:require(bool(s[a[3]:b[2]].strip()),f'空标题：{path.name} / {a[1]}')
for e,(path,anchor) in zip(entries,targets):
    require(root_targets[(path,anchor)]==1,f'总树词目入口遗漏或重复：{e["编号"]}')
    found=[h for h in all_heads[path] if h[1]==anchor]
    require(len(found)==1,f'条目标题不唯一：{e["编号"]}')
    if len(found)!=1:continue
    h=found[0];level=h[0]
    end=next((n[2] for n in all_heads[path] if n[2]>h[2] and n[0]<=level),len(texts[path]))
    section=texts[path][h[3]:end]
    require('> **速查结论：**'+e['速查'] in section,f'释义缺失：{e["编号"]}')
    marker='#'*(level+1)+' 规则、例句与使用边界\n\n'
    require(marker in section,f'正文缺失：{e["编号"]}')
    if marker not in section:continue
    body=re.split(r'\n(?:#{'+str(level+1)+r'} (?:相关条目|课程与练习)|\[(?:本页目录|页首)\]\(<)',section.split(marker,1)[1],maxsplit=1)[0].strip()
    body_chars+=len(body)
    require(hashlib.sha256(body_normalized(body).encode('utf-8')).hexdigest()==e['正文SHA256'],f'正文哈希不一致：{e["编号"]}')
    hash_checked+=1
    require(len(body)>=80,f'正文过短：{e["编号"]}')
    require('<details>' not in body and '[[' not in body,f'正文混入练习或歧义链接：{e["编号"]}')
    require(not re.search(r'本路线第|本章后面|第一次读到可以只记结论',body),f'正文依赖学习顺序：{e["编号"]}')
for path in topic_files:
    subset=[e for e in entries if (ROOT/e['文件']).resolve()==path]
    require(len(re.findall(r'^#{1,6} 相关条目$',texts[path],re.M))<=1,f'相关条目重复：{path.name}')
    require(len(re.findall(r'^#{1,6} 课程与练习$',texts[path],re.M))==1,f'课程与练习重复或缺失：{path.name}')
    topic_links=links(texts[path])
    require(sum(label=='总索引' and destination(path,href)==(index,'') for label,href in topic_links)==2,f'总索引入口应仅在页首和文末：{path.name}')
    nav_label='本页目录' if len(subset)>1 else '页首'
    expected_catalog='本页目录' if len(subset)>1 else subset[0]['标题']
    require(sum(label==nav_label and destination(path,href)==(path,expected_catalog) for label,href in topic_links)==1,f'页内返回入口应仅在文末：{path.name}')
    first_entry=min(h[2] for h in all_heads[path] if h[1] in {e['标题'] for e in subset})
    appendix_start=min(h[2] for h in all_heads[path] if h[1] in {'相关条目','课程与练习'})
    body_links=links(texts[path][first_entry:appendix_start])
    # 单词目文件的条目标题就是页首；排除其页首面包屑后检查知识正文。
    if len(subset)==1:
        section_heading=next(h for h in all_heads[path] if h[1]=='规则、例句与使用边界')
        body_links=links(texts[path][section_heading[3]:appendix_start])
    require(not any(label in {'总索引','本页目录','页首'} for label,_ in body_links),f'知识正文中残留导航：{path.name}')
    for chapter in {n for e in subset for n in e['关联课程']}:
        require(sum(label.startswith(f'课程第{chapter:02}章') for label,_ in topic_links)==1,f'课程回查重复或缺失：{path.name} / {chapter}')
    related_heading=next((h for h in all_heads[path] if h[1]=='相关条目'),None)
    if related_heading:
        end=next((h[2] for h in all_heads[path] if h[2]>related_heading[2] and h[0]<=related_heading[0]),len(texts[path]))
        related_targets=[destination(path,href) for _,href in links(texts[path][related_heading[3]:end])]
        require(len(related_targets)==len(set(related_targets)),f'文末相关条目重复：{path.name}')
        require(all(target!=path for target,_ in related_targets),f'文末重复列出同页条目：{path.name}')
    if len(subset)>1:
        heading=next(h for h in all_heads[path] if h[1]=='本页目录')
        end=next((h[2] for h in all_heads[path] if h[2]>heading[2] and h[0]<=heading[0]),len(texts[path]))
        toc_targets=Counter(destination(path,href) for _,href in links(texts[path][heading[3]:end]))
        for e in subset:require(toc_targets[(path,e['锚点'])]==1,f'页内目录遗漏或重复：{e["编号"]}')
for name,expected in manifest['课程文件SHA256'].items():
    p=COURSE/'章节'/name
    require(hashlib.sha256(p.read_bytes()).hexdigest()==expected,f'线性课程变动：{name}')
originals=json.loads((COURSE/'编排记录/来源映射.json').read_text(encoding='utf-8'))['原文件SHA256']
for name,expected in originals.items():
    require(hashlib.sha256((ROOT.parent/name).read_bytes()).hexdigest()==expected,f'旧版资料变动：{name}')

report={'通过':not errors,'知识条目':len(entries),'一级分区':12,'主题文档':len(topic_files),'读者Markdown文件':len(all_md),
        '检查链接':link_count,'检查标题锚点':anchor_count,'正文哈希核对':hash_checked,'正文字符':body_chars,
        '课程章节哈希核对':len(manifest['课程文件SHA256']),'旧版原文哈希核对':len(originals),'错误':errors,
        '检查范围':'检查文件和标题目标、总树与页内目录覆盖、正文哈希、课程与旧版资料完整性。'}
(ROOT/'编排维护/检查结果.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(0 if not errors else 1)
