from pathlib import Path
from collections import Counter
import copy
import hashlib
import html
import json
import re
import sys
sys.path.append(str(Path(__file__).resolve().parents[2]/'英语学习资料·完整线性版/编排记录'))
from 标题优化 import optimize_tree
from 阅读体验优化 import apply_tree

from 课程正文 import LESSONS
import 基础练习, 阅读练习, 篇章与输出练习, 全卷模拟, 真题实战
from 题库接口 import BLOCKS
from 验收标准 import assessment

ROOT=Path(__file__).resolve().parents[1]
RECORD=ROOT/'编排记录'
CHAPTERS=ROOT/'章节'
QUIZZES=ROOT/'强化题目'
CHAPTERS.mkdir(exist_ok=True);QUIZZES.mkdir(exist_ok=True)
GUIDE='00·考试强化总目录'
NAMES={n:f'{n:02}·{title}' for n,(title,_) in enumerate(LESSONS,1)}
Q_NAMES={n:f'{n:02}·考强练习·{title}' for n,(title,_) in enumerate(LESSONS,1)}


def word_count(text):
    return len(re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\b\d+\b",text))


def inline(text):
    s=html.escape(text)
    s=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
    s=re.sub(r'`([^`]+)`',r'<code>\1</code>',s)
    return s.replace('\n','<br>\n')


def paragraphs(text):
    return '\n'.join('<p>'+inline(p)+'</p>' for p in text.split('\n\n') if p.strip())


def prepared_blocks(n):
    bs=copy.deepcopy(BLOCKS[n])
    if n in [7,8,9]:bs=[bs[0],bs[2],bs[1]]
    if n==6:
        a,b=bs
        exam={'标题':'独立验收：替换与填空混合十题','材料':'合上正文和前两组解析。前五项检查替换，后五项检查空白选择。',
              '题目':a['题目'][-5:]+b['题目'][-5:],'独立验收':True}
        a['题目']=a['题目'][:-5];b['题目']=b['题目'][:-5]
        a['标题']='语境替换：分项练习15题';b['标题']='词汇填空：分项练习5题';bs=[a,b,exam]
    elif n in [2,3,4]:
        b=bs[-1];last=copy.deepcopy(b)
        last['题目']=b['题目'][-5:];b['题目']=b['题目'][:-5]
        b['标题']=b['标题'].split('：')[0]+'：分项练习15题'
        last['标题']='独立验收：五个新任务';last['材料']='合上前组答案，独立完成。不要先读解析。';last['独立验收']=True
        bs.append(last)
    elif n in [5,7,8,9,10,11,13,14]:
        bs[-1]['独立验收']=True;bs[-1]['标题']='独立验收｜'+bs[-1]['标题']
    elif n==12:
        for b in bs[3:]:b['独立验收']=True;b['标题']='独立验收｜'+b['标题']
    elif n in [15,16]:
        for b in bs:b['独立验收']=bool(b['题目'])
    return bs


def fold_answers(items):
    s='<details>\n<summary>完成本组后展开答案、证据与解析（限时卷须完成全卷后再展开）</summary>\n'
    for item in items:
        s+=f'\n<p><strong>{item["编号"]}　答案</strong></p>\n'+paragraphs(item['显示答案'])+'\n'
        if item.get('类型')=='作文':s+=f'<p>示范词数：{word_count(item["答案"])}。先完成自己的文章，再比较组织和语言。</p>\n'
        s+=paragraphs('解析：'+item['解析'])+'\n'
    return s+'</details>\n\n'


manifest=[]
for n,(title,body) in enumerate(LESSONS,1):
    nav=[f'[[{GUIDE}|总目录]]']
    if n>1:nav.append(f'[[{NAMES[n-1]}|← 上一章]]')
    if n<16:nav.append(f'[[{NAMES[n+1]}|下一章 →]]')
    else:nav.append('已完成本套学习路线')
    nav='　'.join(nav)
    headings=re.findall(r'^## (.+)$',body,re.M)
    toc='## 本章目录\n\n'+'\n'.join(f'- [[#{h}|{h}]]' for h in headings)+'\n\n'
    priority='> **【考试必学】** 本章对应真实试卷所需的理解、解题或输出任务，按现有带讲与专项验收学习。涉及复杂语法时，沿用基础线性版的识读深度，不额外要求背写全部变式。\n\n'
    chapter=f'# 第{n:02}章　{title}\n\n{nav}\n\n'+priority+toc+body.strip()
    chapter+=f'\n\n## 本章练习与验收\n\n进入 [[{Q_NAMES[n]}|本章专用强化题与解析 →]]。先独立作答，再看解析；练习末尾可以进入下一章。\n\n---\n\n{nav}\n'
    (CHAPTERS/(NAMES[n]+'.md')).write_text(chapter,encoding='utf-8')

    blocks=prepared_blocks(n);total=sum(len(b['题目']) for b in blocks)
    next_link=f'[[{NAMES[n+1]}|验收后进入下一章 →]]' if n<16 else f'[[{GUIDE}|回总目录登记完成情况]]'
    quiz=f'# 第{n:02}章强化练习　{title}\n\n[[{NAMES[n]}|返回本章正文]]　[[{GUIDE}|总目录]]\n\n'
    if n==16:
        quiz+='本卷含2021年真题75道客观题、1段翻译和1篇作文，共77项。原页在本文件连续呈现。先在草稿按原题号作答，再用下方题号记录核对；不要逐项看答案。作文同主题范文已在第14章出现，只计复写表现。\n\n'
    elif n==15:
        quiz+='完整原创模拟：75道客观题、1段翻译和1篇作文，共77项、100分。试卷一100分钟，试卷二50分钟。场景和数据为原创设定；不冒充官方试题或经过等值校准的试卷。\n\n'
    else:
        quiz+=f'本卷共{total}项作答任务。\n\n'
        if n==1:
            quiz+='先独立作答，再按错因记录起点；本章诊断不设统一通关分数。\n\n'
        elif n==12:
            quiz+='先做第一套，再合上正文和答案完成第二套；第二套三篇全部完成后再展开本套答案。\n\n'
        else:
            quiz+='先做分项练习，再合上正文与答案，完成标有“独立验收”的新材料。\n\n'
        quiz+='文中的人物与研究数据均为原创教学设定。\n\n'
    quiz+='## 题组目录\n\n'+'\n'.join(f'- [[#{b["标题"]}|{b["标题"]}]]' for b in blocks)+'\n\n'
    counter=0;items=[];exams=[]
    for b in blocks:
        quiz+='## '+b['标题']+'\n\n'+b['材料'].strip()+'\n\n'
        rendered=[]
        for original in b['题目']:
            counter+=1;item=copy.deepcopy(original);item['编号']=f'Q{counter:02}';item['章']=n;item['独立验收']=bool(b.get('独立验收'))
            quiz+=f'**{item["编号"]}**　{item["题目"]}\n\n'
            if item['类型']=='单选':
                options=item['选项'];shift=(n+counter)%4
                options=options[shift:]+options[:shift];item['选项']=options
                index=options.index(item['正确项']);letter='ABCD'[index]
                item['显示答案']=letter+'. '+item['正确项'];item['正确字母']=letter
                for k,opt in enumerate(options):quiz+=f'- {"ABCD"[k]}. {opt}\n'
                quiz+='\n'
            else:item['显示答案']=item['答案']
            rendered.append(item);items.append(item)
            if item['独立验收']:exams.append(item['编号'])
        if rendered:quiz+=fold_answers(rendered)
    assert counter==total
    quiz+='## 验收与复测\n\n'
    quiz+=assessment(n,exams,items)
    quiz+='| 日期 | 题号 | 首次答案／得分 | 错误类型与证据 | 隔天复测 |\n|---|---|---|---|---|\n|  |  |  |  |  |\n\n'
    quiz+=f'[[{NAMES[n]}|返回本章正文]]　{next_link}\n'
    path=QUIZZES/(Q_NAMES[n]+'.md');path.write_text(quiz,encoding='utf-8')
    manifest.append({'章':n,'标题':title,'正文':str((CHAPTERS/(NAMES[n]+'.md')).relative_to(ROOT)),
                     '练习':str(path.relative_to(ROOT)),'任务':total,'独立验收':exams,'题目':items})

all_tasks=sum(x['任务'] for x in manifest)
stages=[(1,4,'先把语法用于读句子'),(5,6,'交际与词义'),(7,10,'阅读理解'),(11,12,'篇章补全'),(13,14,'翻译与写作'),(15,16,'整卷应用与复测')]
progress={}
old_guide=ROOT/(GUIDE+'.md')
if old_guide.exists():
    progress={name:mark for mark,name in re.findall(r'^- \[([ xX])\] \[\[([^]|]+)',old_guide.read_text(encoding='utf-8'),re.M)}
guide='''# 同等学力申硕英语·考试强化

从第01章开始，按顺序读正文，再进入章末练习。正文保留上一章、下一章；练习开头可返回正文，末尾可进入下一章。下次从第一个未勾选的章节继续。

本套默认已经学过零基础语法主线。重点是用已学知识读懂陌生题、找到证据并完成输出。必要术语就地提醒，不要求先到其他资料中翻找。

**七个月备考深度：** 本套各章标为“考试必学”，七部分均有真实试卷任务，不整类跳过。基础线性版已将复杂语法的生成要求降为识读；到这里重在用它读懂材料，不增加背公式门槛。第16章熟悉作文仍只计复写。

## 真题依据与范围

所附14份PDF按哈希去重后为12份，覆盖2001—2023年及2025年，缺2024年；三份2025文件内容相同，按一份处理。近年重点样本是2019、2020、2021、2022、2023、2025六套，阅读150题按主要任务归类并留有逐题记录。2013—2018年用于题型对照，2001—2012年不并入近年题型频率。

本套完整覆盖七部分，不把语法书重复一遍，也不按某个词出现次数制造“必考概率”。例证引用注明年份与题型；专项和模拟中的人物、数据及研究场景除明确引用外均为原创教学设定。

'''
guide+=f'## 内容与题量\n\n16章正文、16份章内练习，共{all_tasks}项作答任务。其中前15章{sum(x["任务"] for x in manifest[:15])}项为原创训练（包含一套完整模拟），第16章为2021真题75道客观题、翻译和作文，共77项。整段翻译、完整作文各计一项，不把评分单元重复算题。\n\n'
guide+='正文中的带讲题与章末练习分开：带讲题先呈现材料，再拆解句意、证据及选项；不并入上述练习题量。同一道真题在不同章节再次分析，也不重复计数。\n\n'
guide+='阅读章提供整篇真题及全部选项；完形章走完真实十空；短文完成章走完三篇二十空；翻译章处理三段全文；写作章从真实任务、段落改写到完整成文。学习时在当前章节内连续阅读，不需要到来源记录中寻找示范。\n\n'
guide+='章末专项验收使用尚未在本卷解析中出现的新材料；两套整卷须完成全卷后再展开答案。第16章作文主题已在写作章示范，计复写而非陌生题表现。\n\n'
for a,b,label in stages:
    guide+='## '+label+'\n\n'
    for n in range(a,b+1):guide+=f'- [{progress.get(NAMES[n]," ")}] [[{NAMES[n]}]]（练习{manifest[n-1]["任务"]}项）\n'
    guide+='\n'
guide+='''## 怎样判断可以继续

各章练习末尾按实际任务写明验收办法：第02—04章五题按要点评10分；第05章四空访谈；第06章十题混合；第07—10章五题阅读／评论；第11章十空完形；第12章组词与回填两轮分开；第13章整段翻译；第14章完整作文。具体分数、解释要求与错题修复均在当前练习中，不必另找评分表。

整卷客观题60/75、翻译8/10、作文10/15作为本套自学建议；作文还须不少于150词、任务完成至少4/5、语言准确至少2/4。达到分数后仍须修正不稳项。这些都是训练标准，不是官方能力认证或考试通过承诺。

首次独立成绩、查词后修正成绩、隔天复测成绩分开记录。按词义、结构、证据范围、输出和时间五类修复，避免把所有错题都写成粗心。

已做过旧版验收题时，即使选项更新，熟悉的文章仍应记为复测材料；保留原先成绩，不把选项重写当作全新测量。

## 来源与维护记录

统计口径、逐年来源、官方大纲、原稿疑误与编排检查见 [[真题依据与考点统计]]，仅供查证，不属于顺序学习的额外步骤。原有零基础资料与知识字典保留在原文件夹。
'''
old_guide.write_text(guide,encoding='utf-8')
(RECORD/'题目清单.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
optimize_tree(ROOT)
apply_tree(ROOT)
print(json.dumps({'章节':16,'练习文件':16,'原创任务':sum(x['任务'] for x in manifest[:15]),'真题任务':manifest[15]['任务'],'合计':all_tasks,'每章任务':{x['章']:x['任务'] for x in manifest}},ensure_ascii=False))
