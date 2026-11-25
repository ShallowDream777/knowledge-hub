from pathlib import Path
import json
import re
from 强化题库 import SEEDS, CHECKS, EXTRA
from 答案排版 import format_answers
from 学习分层 import mark_questions, first_round_panel
from 标题优化 import rename_text

ROOT = Path(__file__).resolve().parents[1]
EXERCISES = ROOT / '强化题目'
EXERCISES.mkdir(exist_ok=True)

BOUNDARIES = {
1:'只验收本章起步搭配、字母分类和已给例句的职位识别；不要求掌握完整时态、复数规则或复杂从句。',
2:'只要求名词分类、数与计量；不额外考尚未系统学习的冠词选择和时态构造。',
3:'只要求本章人称、所属、反身、指示、疑问及相互代词；不考第24章的形式it与复杂替代。',
4:'重点是冠词、可数性和已有的所属限定词；不要求自行构造尚未学的从句。',
5:'重点是名词所有格、名词定语、计量和基础一致；不考后续从句与非谓语构造。',
6:'重点是形副的位置、程度、比较与本章例句中的常用结构；不要求复杂时态或从句。',
7:'只考介词意义、常见搭配与可分/不可分结构；不考未展开的复杂连词和从句。',
8:'只考本章数词、时间日期、倍数、冠词复习和本章明确说明的数量一致。',
9:'按本章示例识别动词角色与基本搭配；不要求独立掌握全部完成、被动和非谓语变化。',
10:'重点是已给句子的成分与基本句型；复杂动词形式如出现仅作已给结构识别。',
11:'只考本章句子用途、否定提问、祈使感叹、存在句与本章已有反意问句；不考后续复杂从句规则。',
12:'只考基础一致、意义一致及本章的就近与核心主语判断；不提前考第27章的复杂从句一致。',
13:'只要求现在时组及本章所给动词形式表；不提前考过去、将来整组句型。',
14:'可串联前章现在形式作比较，新增要求仅限本章过去时组；不考未学的将来组合。',
15:'只新增将来时组与计划预测；不考第23章的过去将来和转述变换。',
16:'只考本章情态、半情态、过去推测和遗憾；不额外要求第28章完整wish/混合虚拟体系。',
17:'只考被动、主动对应及本章特殊结构；使用的时态、情态均来自前章。',
18:'重点是动词角色、限定形式、动词短语和已学时态语态；不要求独立主格等未学分析。',
19:'只新增连词与关系概览；不提前要求完整宾语从句、关系从句或复杂省略。',
20:'只新增状语从句及本章时间条件方式比较等关系；不考尚未展开的名词性、定语从句构造。',
21:'只新增主语、宾语、表语、同位语从句及相关语序；不考第22章的关系词省略规则。',
22:'只新增关系从句和本章相关比较；不提前考第23章间接引语的完整时态后移。',
23:'可串联此前全部时态、语态、情态及三类从句；不加入独立主格和复杂非谓语缩写。',
24:'重点是代词、替代、数量、关系词和本章形式it；含to结构只辨本章已给的功能，不展开第26章难点。',
25:'只考本章不定式、动名词、分词的基本角色与搭配；不提前要求独立主格和复杂非谓语完成被动。',
26:'新增要求限本章非谓语逻辑主语、相对时间、主被动与独立主格；不提前考完整虚拟和强调倒装。',
27:'只强化一致，串联已经学过的从句、非谓语和数量结构；不混入后续虚拟考点。',
28:'只新增本章假设、wish、建议要求、混合条件及虚拟倒装；不提前考第29章其他倒装与强调细则。',
29:'可串联虚拟、从句、非谓语；新要求限本章倒装、强调、省略。',
30:'只新增构词与感叹词识别；不要求猜出没给含义的冷僻词，也不把词尾线索当绝对规则。',
31:'重点是语篇关系、标点和已学结构的综合表达；不加入课程之外的语言学术语或考试专项。',
}

# B组每题实际串联的已学章节；等于当前章时是本章应用，不伪称前章。
CUMULATIVE_SOURCES = {
1:[1,1,1,1],2:[1,1,2,2],3:[2,1,1,3],4:[2,3,4,2],
5:[3,2,2,1],6:[3,4,2,6],7:[3,2,6,1],8:[2,4,7,2],
9:[6,3,7,1],10:[2,6,9,9],11:[10,3,9,4],12:[2,11,7,11],
13:[12,11,13,13],14:[13,11,2,13],15:[14,11,11,8],16:[14,11,13,11],
17:[14,3,16,4],18:[14,17,16,9],19:[12,7,7,14],20:[14,6,16,19],
21:[20,11,12,21],22:[12,21,7,12],23:[20,22,14,23],24:[23,6,7,21],
25:[13,21,22,17],26:[20,17,13,26],27:[12,3,2,25],28:[20,14,16,28],
29:[14,28,3,21],30:[2,6,12,30],31:[20,5,22,19],
}


def names_for(chapter):
    source = next((ROOT/'章节').glob(f'{chapter:02}·*.md'))
    title = source.stem.split('·',1)[1]
    return source, f'{chapter:02}·强化练习·{title}'


def hint(text):
    words = re.findall(r"[A-Za-z]+(?:[-'][A-Za-z]+)*",text)
    return ' / '.join(sorted(set(words),key=lambda word:(word.lower(),word)))


def render_group(title, items, prefix):
    s=f'## {title}\n\n'
    for k,item in enumerate(items,1):
        s+=f'**{prefix}{k:02}｜【{item.get("首轮要求","必做")}】{item["知识点"]}**　{item["题目"]}\n\n'
    s+='<details>\n<summary>完成本组后再展开答案与解析</summary>\n\n'
    for k,item in enumerate(items,1):
        s+=f'**{prefix}{k:02}**　{item["答案"]}\n\n'
    return s+'</details>\n\n'


def build():
    BOUNDARIES[1]='只验收本章已解释的词类、简单主语宾语、原形与形式、am/is/are搭配和not位置；不要求正文尚未演示的句子变换。'
    manifest=[]
    assert set(SEEDS)==set(CHECKS)==set(range(1,32))
    for chapter in range(1,32):
        source,name=names_for(chapter)
        body=source.read_text(encoding='utf-8')
        for heading in ['## 本章目录','## 本章收束']:
            assert heading in body
        seeds=SEEDS[chapter]
        practice=[]
        for tag,cloze,correct,wrong,chinese,reason in seeds:
            practice.append({'知识点':tag,'题目':'按提示补全或完成（写完整句子或短语）：'+cloze,'答案':f'{correct}；{reason}','类型':'补全','来源章':chapter})
        for tag,cloze,correct,wrong,chinese,reason in seeds:
            practice.append({'知识点':tag,'题目':f'目标意思：{chinese} 请修正不合形式或不合题意的表达：`{wrong}`。','答案':f'{correct}；{reason} 这项修正以题意为准，不把所有其他语境也一概判错。','类型':'修正','来源章':chapter})
        for tag,cloze,correct,wrong,chinese,reason in seeds:
            practice.append({'知识点':tag,'题目':f'独立表达：{chinese} 可用词语（次序打乱，不要求全部唯一用法）：{hint(correct)}。','答案':f'参考：{correct}；{reason} 意思、指定结构相同的其他正确表达也可。','类型':'表达','来源章':chapter})
        cumulative=[]
        for j,(tag,q,a) in enumerate(CHECKS[chapter][:4]):
            link_chapter=CUMULATIVE_SOURCES[chapter][j]
            assert link_chapter<=chapter
            label='本章应用' if link_chapter==chapter else f'串联第{link_chapter:02}章'
            q+=f'（{label}；需要回看时可点 [[{names_for(link_chapter)[0].stem}|对应已学章节]]）'
            cumulative.append({'知识点':tag,'题目':q,'答案':a,'类型':'串联','来源章':chapter,'关联章':link_chapter,'可用前章':[link_chapter] if link_chapter<chapter else []})
        exam=[{'知识点':tag,'题目':q,'答案':a,'类型':'验收','来源章':chapter} for tag,q,a in CHECKS[chapter][4:]]
        extra=[{'知识点':tag,'题目':q,'答案':a,'类型':'专项加练','来源章':chapter} for tag,q,a in EXTRA.get(chapter,[])]
        first_plan=mark_questions(chapter,{'A':practice,'B':cumulative,'C':exam,'D':extra})
        src_link=f'[[{source.stem}|返回第{chapter:02}章：{source.stem.split("·",1)[1]}]]'
        next_link=f'[[{names_for(chapter+1)[0].stem}|准备好后进入下一章 →]]' if chapter<31 else '本课程已到最后一章，可从学习目录选择下一轮复习。'
        total=len(practice)+len(cumulative)+len(exam)+len(extra)
        text=f'# 第 {chapter:02} 章专用强化与验收\n\n{src_link}　[[00·从这里开始|学习目录]]\n\n'
        text+=f'> 本卷共 **{total} 道任务**：24道分项强化、4道串联、12道独立验收'+(f'、{len(extra)}道专项加练' if extra else '')+'。分项强化刻意围绕8个核心情境做三种操作；它们不是24个互不相干的新情境。独立验收使用另一组题。\n\n'
        text+=f'**范围边界：**{BOUNDARIES[chapter]}\n\n'
        if chapter==1:
            text+='本章是课程起点，B组只做本章应用；从第2章开始，B组才串联此前已经学过的内容。\n\n'
        d_order='完成D中的基础规则补练' if chapter in [20,21,25,26] else '需要专项补练时完成D'
        text+='**首轮顺序：**按下方题单完成A、B及存在的D中必做题，最后合上正文完成C中必做题。选做题用于补卡点或第二轮，不阻挡进入下一章。每组答案折叠在题后；表达题给可用词，不把生词量当本卷目标。\n\n'
        text+='[[#A 分项强化|A 分项强化]]　[[#B 前章串联与本章应用|B 串联应用]]　'+('[[#D 专项补练|D 专项补练]]　' if extra else '')+'[[#C 独立验收|C 独立验收]]　[[#验收标准与错题修复|验收标准]]\n\n'
        text+=first_round_panel(first_plan)
        text+='## 本章覆盖与学习卡点\n\n| 核心情境 | 主要检查 | 关联题号 |\n|---|---|---|\n'
        for k,(tag,_,_,_,_,reason) in enumerate(seeds,1):
            text+=f'| {tag} | {reason} | A{k:02}、A{k+8:02}、A{k+16:02} |\n'
        text+='\nA是从补全到修正再到表达的强化；C则检查在没有原情境提示时能否辨认和解释。覆盖表列出核心情境，其他本章细节还会出现在B、C和原章节自测中。\n\n'
        text+=render_group('A 分项强化',practice,'A')
        text+=render_group('B 前章串联与本章应用',cumulative,'B')
        if extra:text+=render_group('D 专项补练',extra,'D')
        text+=f'## C 独立验收\n\n先关闭本章、A/B答案，独立作答。完整12题每题2分，共24分；七个月首轮只计算上方必做题，满分{first_plan["验收满分"]}分、建议至少{first_plan["验收建议"]}分。选做题不进入首轮分母。这是自学建议，不是标准化等级考试。\n\n'
        for k,item in enumerate(exam,1):text+=f'**C{k:02}｜【{item["首轮要求"]}】{item["知识点"]}**　{item["题目"]}\n\n'
        text+='<details>\n<summary>独立验收完成后展开：参考答案与给分办法</summary>\n\n'
        text+='**给分：**正确并能解释关键理由2分；结构方向正确但漏一项必要条件、拼写或解释1分；核心规则错误、无法独立完成或先看答案0分。开放题按题目要求、结构和意义给分，不要求逐字复制参考。若题目有多个合理形式，按解析允许它们。\n\n'
        for k,item in enumerate(exam,1):text+=f'**C{k:02}**　{item["答案"]}\n\n'
        text+='</details>\n\n## 验收标准与错题修复\n\n'
        text+=f'**七个月首轮：**C必做题至少{first_plan["验收建议"]}/{first_plan["验收满分"]}；A、B、D中的必做项能够独立完成，错题和不稳项能说明题干要求的理由。标为选做的题不作为继续条件。\n\n**第二轮完整复习：**下面保留原全量训练标准；它不覆盖或撤销上面的首轮题单。\n\n'
        if chapter in [20,21,25,26]:
            text+='- **基础规则补练：**D组每题先独立作答，再展开解析。错题须能解释与旧口诀的区别，并用题中结构复述；隔一天合上解析重做D组错题，不能只看懂参考答案就算掌握。\n'
        text+='- **可以继续：**C达到20/24分，A的24题至少20题能独立完成，B至少3题会做；C中的表达题能说明自己写法的核心理由。不能用“刚看答案后抄对”计入独立完成。\n'
        text+='- **需要巩固：**C为16—19分，或某个核心情境的三种任务中连续错两题。按上表标签回到正文对应小节，解释错因后重做同标签的A题，再用自己的词写一个同结构例子。\n'
        text+='- **先修复再继续：**C低于16分，或只能认选项、无法完成基本表达。先回本章，处理错得最多的两个标签；不要求盲目刷完整卷第二遍。\n'
        text+='- **延迟复测：**隔一天先不看答案，重做错过的C题，再重做A中相应的表达题。复测沿用已有题，不另算新增题量；能够解释并改对再进入下一章。\n\n'
        text+='| 日期 | 题号/知识点 | 我原来的判断 | 正确理由 | 下次复测结果 |\n|---|---|---|---|---|\n|  |  |  |  |  |\n\n'
        text+='达到自己的验收要求后，再在学习目录勾选这一章。若有合理答案与参考不同，先核对题意和结构，不把措辞不同直接判错。\n\n---\n\n'+src_link+'　'+next_link+'\n'
        (EXERCISES/(name+'.md')).write_text(rename_text(format_answers(text)),encoding='utf-8')
        manifest.append({'章':chapter,'章节文件':str(source.relative_to(ROOT)),'练习文件':str((EXERCISES/(name+'.md')).relative_to(ROOT)),'边界':BOUNDARIES[chapter],'题量':total,'核心情境':len(seeds),'分项强化':practice,'串联':cumulative,'验收':exam,'专项':extra,'首轮分层':first_plan})
    (ROOT/'编排记录/强化题目清单.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    index='# 强化题目目录\n\n每章学完后，从章末链接进入对应题目即可；本目录用于定位。完成练习与验收后，题目底部可回章节或去下一章。\n\n'
    index+='题量按具体任务计数；同一个核心情境会练补全、修正和表达。验收题独立编排，延迟复测不重复计入新增题量。\n\n'
    for r in manifest:
        p=Path(r['练习文件'])
        index+=f'- [[{p.stem}]]（{r["题量"]}题）\n'
    (EXERCISES/'00·强化题目目录.md').write_text(index,encoding='utf-8')
    print(f'已构建31份练习，共{sum(x["题量"] for x in manifest)}道任务。')
    return manifest


def attach_chapter_links():
    for chapter in range(1,32):
        source,name=names_for(chapter)
        s=source.read_text(encoding='utf-8')
        block=(f'\n## 本章强化与验收\n\n'
               f'读完本章后，进入 [[{name}|第{chapter:02}章专用强化题与验收 →]]。题目开头可返回本章，末尾可进入下一章。\n\n'
               f'七个月首轮按练习开头的必做题单和首轮标准继续；识读知识先理解例句，不必刷完选做输出题。\n')
        # 只替换本工具管理的入口，重复运行不叠加；不修改正文和阅读进度。
        s=re.sub(r'\n## 本章强化与验收\n[\s\S]*?(?=\n---\n\n\[\[00·从这里开始)', '',s)
        pos=s.rfind('\n---\n\n[[00·从这里开始')
        assert pos!=-1,source
        s=s[:pos]+block+s[pos:]
        source.write_text(s,encoding='utf-8')


if __name__=='__main__':
    build()
    attach_chapter_links()
