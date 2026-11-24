"""题干主任务人工编码。交叉题只计一个主类，不等于官方题型划分。"""
from pathlib import Path
from collections import Counter
import csv
import json
import re

ROOT = Path(__file__).resolve().parent
annual = json.loads((ROOT/'分年试题.json').read_text(encoding='utf-8'))
scanned_stems = '''What is special about Rubio?
Why is treadmill a poor exercise choice in the spacecraft?
What does an enhanced spaceflight diet refer to?
Why did Rubio grow vegetables in the space station?
What is the main topic of this passage?
What do we learn about native Australians in Paragraph 1?
Where do Australian honeypot ants store their honey?
What is Ulrich's job as mentioned in Paragraph 3?
What do we know about ant honey from the Carter Lab's study?
What would be the next step for the Carter Lab team?
The miracle in the first paragraph refers to what?
Caffeine brings the following benefits EXCEPT which one?
The phrase hit the reset button means what?
What is the effect of drinking coffee regularly according to Japanese research?
What does the author indicate in the last paragraph?
What can be learned about the study by Simon and Walker?
What did the MRI result indicate about the mind network?
What did the scientists find after tracking people online and measuring their sleep?
What does Simon emphasize in the last paragraph?
Which of the following can be the best title for this passage?
What makes more people think about living in vans and houseboats?
What might be the biggest expense if you choose to live in a van?
The word enticing most probably means what?
Which comment agrees that vans and houseboats do not offer enough space?
Which comment indicates the conveniences of living in vans?'''.splitlines()
annual['2025'] = {'来源':'2025年同等学力申硕英语真题以及参考答案详解.pdf', '起页':1, '止页':6,
                  '阅读题干':[{'题号':n,'题干':q,'记录方式':'扫描原页人工核读后的题干简录'} for n,q in enumerate(scanned_stems,21)]}
# 一题只分配一个主类；例如按照已指明评论查事实，归细节；选择哪条评论才归评论匹配。
codes = {
 2019:{'词义与指代':[23,28,32,36],'主旨与标题':[25,40],'推断与结论':[37,43],'态度与语气':[31,35,39],'例证与篇章作用':[33],'评论匹配':[44,45]},
 2020:{'词义与指代':[21,22,27,32,40],'主旨与标题':[26,41],'推断与结论':[35,38],'态度与语气':[29,43],'例证与篇章作用':[25,34],'评论匹配':[44,45]},
 2021:{'词义与指代':[21,33,37],'主旨与标题':[41],'推断与结论':[24,25,34,35,43],'态度与语气':[30,42],'例证与篇章作用':[22],'评论匹配':[44]},
 2022:{'词义与指代':[43],'主旨与标题':[31,40],'推断与结论':[39],'态度与语气':[30,41],'例证与篇章作用':[34,36],'评论匹配':[44,45]},
 2023:{'词义与指代':[23,33],'主旨与标题':[22],'推断与结论':[28,35,37],'态度与语气':[24,25],'例证与篇章作用':[30],'评论匹配':[44,45]},
 2025:{'词义与指代':[23,31,33,43],'主旨与标题':[25,39,40],'推断与结论':[30,35,36],'态度与语气':[],'例证与篇章作用':[],'评论匹配':[44,45]},
}
rows = []
for year,mapping in codes.items():
    lookup = {n:category for category,ns in mapping.items() for n in ns}
    assert len(lookup) == sum(map(len,mapping.values())), year
    qs = annual[str(year)]['阅读题干']
    assert [q['题号'] for q in qs] == list(range(21,46)), year
    for q in qs:
        n = q['题号'];page = None
        if year == 2025:
            page = 2 if n<=25 else 3 if n<=35 else 4 if n<=40 else 5
        else:
            for p in annual[str(year)]['页']:
                if re.search(rf'(?m)^\s*{n}\s*[.．]',p['文本']):page = p['PDF页'];break
        assert page, (year,n)
        rows.append({'年份':year,'题号':n,'主考点':lookup.get(n,'细节与因果定位'),'题干':q['题干'],
                     '来源文件':annual[str(year)]['来源'],'PDF页':page})
with (ROOT/'近年阅读150题分类.csv').open('w',encoding='utf-8-sig',newline='') as f:
    writer = csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
counts = Counter(x['主考点'] for x in rows)
summary = [{'主考点':k,'题数':v,'出现年份':[y for y in codes if any(x['年份']==y and x['主考点']==k for x in rows)]}
           for k,v in counts.most_common()]
(ROOT/'阅读考点统计.json').write_text(json.dumps({'年份':list(codes),'总题数':len(rows),'口径':'按题干主任务人工编码，交叉题仅归一类；类别边界有解释空间，不是官方统计；只据6套样本描述，不预测下一次考试概率。','分类':summary},ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'分年试题.json').write_text(json.dumps(annual,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'总题数':len(rows),'分类':summary},ensure_ascii=False))
