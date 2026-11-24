"""题面候选定位，可复核；检索次数不等于语法考频，未命中不等于未考。"""
from pathlib import Path
import json
import re

R = Path(__file__).resolve().parent
pages=[]
for year,data in json.loads((R/'分年试题.json').read_text(encoding='utf-8')).items():
    for page in data.get('页',[]):
        pages.append({'year':int(year),'file':data['来源'],'page':page['PDF页'],'text':page['文本']})

OLD = {
    '2001-2006年英语真题及答案.json': [(2001,1,10),(2002,11,20),(2003,21,30),(2004,31,40),(2005,41,51),(2006,52,63)],
    '2007-2012年英语真题及答案.json': [(2007,1,10),(2008,11,21),(2009,22,30),(2010,31,42),(2011,43,54),(2012,55,66)],
}
for filename,bounds in OLD.items():
    data=json.loads((R/'原卷提取'/filename).read_text(encoding='utf-8'))
    for year,start,end in bounds:
        for page in data:
            if start<=page['PDF页']<=end:
                pages.append({'year':year,'file':filename.replace('.json','.pdf'),'page':page['PDF页'],'text':page['文本']})

PATTERNS = {
    '将来完成进行完整词串': r"(?:\b(?:will|shall)(?:\s+not)?|\b\w+'ll|\bwon't)\s+have\s+been\s+[a-z]+ing\b",
    '将来完成进行疑问词串': r'\b(?:will|shall)\s+(?:i|you|he|she|it|we|they)\s+have\s+been\s+[a-z]+ing\b',
    'would完成进行词串_不自动区分转述和反事实': r"\b(?:would(?:n't)?\s+have|would've)\s+been\s+[a-z]+ing\b",
    '完成进行被动词串': r'\b(?:have|has|had)(?:\s+not)?\s+been\s+being\b',
    '现在完成进行候选': r'\b(?:have|has)\s+been\s+[a-z]+ing\b',
    '过去完成进行候选': r'\bhad\s+been\s+[a-z]+ing\b',
    '将来完成候选_未穷举所有不规则词尾': r'\bwill\s+have\s+[a-z]+(?:ed|en)\b',
    '双重所有格候选_限制明确代词': r'\bof\s+(?:mine|yours|ours|theirs)\b',
    '虚拟倒装候选': r'\b(?:had\s+(?:we|i|it|they|he|she)\s+(?:not\s+)?(?:known|been|[a-z]+ed)|were\s+it\s+not)\b',
    '独立主格固定词串候选_不覆盖全部独立主格': r'\b(?:weather\s+permitting|all\s+things\s+considered|all\s+things\s+being\s+equal|time\s+permitting|there\s+being)\b',
    '感叹词候选': r'\b(?:alas|hurrah|hurray|oops|ouch|ugh|wow)\b',
}

result={'范围':'2001—2023题面文字层，排除参考解析；2025题面无文字层，另核读扫描PDF1—6页。',
        '缺年':[2024],'纳入题面PDF页数_不含2025':len(pages),'年份':sorted(set(p['year'] for p in pages)),
        '限制':'匹配只定位片段，包含选项和设空；误命中、缺词、OCR及缩写变体均需人工核对。候选数不作语法考频。',
        '2025人工反例':['PDF3阅读三：I replied, heart racing.','PDF4博客：With the cost-of-living crisis biting, ...'],
        '检索未见不等于未考':True,'模式':{}}
for label,pattern in PATTERNS.items():
    hits=[]
    for page in pages:
        text=re.sub(r'\s+',' ',page['text']).replace('’',"'").replace('‘',"'")
        for match in re.finditer(pattern,text,re.I):
            hits.append({'年':page['year'],'来源':page['file'],'PDF页':page['page'],
                         '片段':text[max(0,match.start()-90):match.end()+140],'命中':match.group()})
    result['模式'][label]={'候选数':len(hits),'定位':hits}
(R/'优先级题面检索.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
(R/'优先级题面语料.json').write_text(json.dumps(pages,ensure_ascii=False),encoding='utf-8')
print(json.dumps({'题面文字页':len(pages),'模式数':len(PATTERNS),'扫描页另核读':6,'结果不是考频统计':True},ensure_ascii=False))
