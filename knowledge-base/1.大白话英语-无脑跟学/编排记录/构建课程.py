from pathlib import Path
import re
import json
import hashlib
import shutil
from collections import Counter
from 内容校订 import revise, changes as quality_changes, dedup as quality_dedup
from 构建强化题 import build as build_exercises, attach_chapter_links
from 答案排版 import format_answers
from 先修衔接 import revise_course
from 基础规则校订 import revise_course as refine_basic_rules, CHANGES as basic_rule_changes
from 学习分层 import annotate_body, guide_note, save_evidence
from 标题优化 import legacy_source, optimize_tree
from 阅读体验优化 import apply_tree

OUT = Path(__file__).resolve().parents[1]
ROOT = OUT.parent
CHAPTERS = OUT / '章节'
CHAPTERS.mkdir(exist_ok=True)
SNAP = OUT / '编排记录' / '原文快照'
SNAP.mkdir(exist_ok=True)
files = {int(p.name[:2]): p for p in ROOT.glob('*.md') if re.match(r'^\d{2}', p.name)}
assert set(files) == set(range(19))
texts = {n: legacy_source(p.read_text(encoding='utf-8-sig'), p) for n, p in files.items()}
hashes = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files.values()}
for p in files.values():
    shutil.copy2(p, SNAP / (p.name+'.snapshot'))

# 单元切分只依据原文标题；不删除知识段、例句或题目。
units = {}
for n in range(2, 19):
    s = texts[n]
    marks = list(re.finditer(r'^ {0,2}## (.+)$', s, re.M))
    units[n] = []
    for i, m in enumerate(marks):
        if m.group(1) == '使用说明':
            continue
        end = marks[i+1].start() if i+1 < len(marks) else len(s)
        units[n].append((m.group(1), s[m.start():end].strip()))

def allof(n):
    return list(range(len(units[n])))

# title, stage, original source sections, opening bridge, closing recall
plan = [
('文字、句子和必备术语', '第一阶段：先把词与句子认清', [],
 '先认识最简单的句子，再看原先修速览。这里不要求两分钟记住全部成分，也不把高级术语当作入学测验。',
 '分清“词的类别”和“词在句子里的工作”。名词不等于主语；下一章先细学名词。'),
('名词基础：分类、单复数与不可数', '', [(2, [0,1,2,3])],
 '主语是句子谈论的人或事物；宾语常是动作涉及的对象。名词可以放在这些位置。本章先保留原文完整的分类、变化规则和不可数用法。',
 '能说明 book/books 与 water 的差别即可继续；所有格要用到“我的、你的”，所以先学代词。'),
('代词基础：人称、所属、反身与指示', '', [(3,[0,1,2,3,4,5,7])],
 '先记 I/me/my/mine 这类不同位置的形式。概览表里若见到关系代词，只需知道它是后续从句的连接工具；详细正文已经安排在从句之后。',
 '自己比较 I like her、She likes me、my book、The book is mine，不必另外寻找对照表。'),
('冠词：a、an、the 与零冠词', '', [(15,[6,7,8,9,10])],
 '你已经见过可数性和 my/mine。现在把名词前“有没有限定、用哪个限定”完整讲清，再进入所有格和名词定语。',
 '检验：an apple；a university；my book；the book I bought。末例意为“我买的那本书”，后面的词帮助确定是哪本。'),
('名词进阶、搭配与完整自测', '', [(2,[4,5,6,7,8,9,10])],
 'my book 中 my 表所属；a friend of mine 表“我的一位朋友”。复合名词指几个词合成的一个名称，如 passer-by（过路人）。本章原文的这两类例子现在都有入口。',
 '完成原名词自测再展开答案。后面的同主题复盘保留原 01 的讲解，不是新的必选阅读分支。'),
('形容词与副词：位置、比较和程度', '', [(14,allof(14))],
 '形容词说明人或物“什么样”：a red book；副词可以说明动作“怎样”：run quickly。比较结构里的 than 表“比”，as ... as 表“和……一样”。',
 '用同一组词比较 a careful student 与 The student works carefully，确认描述对象不同。'),
('介词与短语动词', '', [(16,[0,1,2,3])],
 '介词后的名词或代词和它一起构成短语：in the room、with me。它们可以说明位置、时间等。短语动词则把动词与小词作为整体学习，如 turn on。',
 '不要把中文的“在”统一翻成一个介词，也不要把短语动词的每个小词都逐字翻译。'),
('数词、倍数、时间日期与综合自测', '', [(15,[0,1,2,3,4,5,11,12,13])],
 '这一章沿用原数词的全部讲解。分数作主语时，先按例句观察：Two thirds of the water is ...；Two thirds of the students are ...。决定搭配的是后面的 water/students。',
 '本章原综合自测同时复习冠词；因为冠词已提前学过，现在不必另开文件。'),
('动词基础：动作、系动词与助动词', '第二阶段：句子骨架与动词时间', [(4,[0,1,2,3,4])],
 '本章要区分词的身份：I have a book 里的 have 表“有”；I have finished 里的 have 帮助表达完成。be 也能表示状态，或帮助构成进行、被动。先看它在整句里做什么。',
 '系动词后说明主语的内容叫表语；动作对象叫宾语；补充说明宾语的内容叫宾补。下一章直接用完整句型整理它们。'),
('句子成分与五大基本句型', '', [(5,[0,1,2])],
 '已经认识名词、代词、形容词和动词，现在把“词类”放回“句子职位”里看。例句中的 have done 暂按完成结构理解，be doing 按进行结构理解，后面逐一展开。',
 '读 She gave me a book 与 She made me happy：前者给我一本书，后者使我开心。不要只数动词后有几个词。'),
('句子种类、疑问、祈使与 There be', '', [(5,[3,4,5,6,7])],
 '进入原文详细分类前，先用下方的否定与提问对照表把操作顺序练熟。There be 用于介绍某处有什么；have 常用于某人或某物拥有。',
 '现在能按 be、普通动作动词、情态动词三类处理基本否定与疑问，再学主谓一致。'),
('主谓一致基础：先确定动词跟谁搭配', '', [(12,[0,1,2,3,4])],
 '单数主语的一般现在时动作动词常加 s：She works；复数主语用原形：They work。be 则有 am/is/are。本章先学原文基础原则，涉及从句和非谓语的易错细节已顺延至第 27 章。',
 '主语后夹着 with/as well as 短语时，先找核心主语；不要机械看离动词最近的名词。'),
('时态入口与现在时态', '', [(6,[0,1])],
 '原时态总表完整保留，用于看见整体，不要求先背熟。过去分词是动词的一种形式：规则词常与过去式同形，如 worked；不规则要分别记，如 go—went—gone、write—wrote—written。',
 '一般现在时说习惯或一般情况，进行时突出进行中的活动，完成结构关联参照时间之前的情况。不要只凭一个标志词套答案。'),
('过去时态：发生、进行与过去之前', '', [(6,[2])],
 'was/were 是 be 的过去形式。过去式表达过去事件；过去分词可参与完成和被动。比较 went 与 had gone，后者关注过去某个参照点之前。',
 '在纸上画两件事的时间先后：When I arrived, she had left. 先离开，后到达。'),
('将来时态：打算、预测与未来参照点', '', [(6,[3])],
 'will、be going to 等用于表达未来，具体选择看计划、预测、安排等语境。进行、完成组合仍按“参照时间＋观察方式”理解。',
 '你已经看过现在、过去、将来各组形式。接下来先学情态与被动；过去将来和时态呼应会在转述之后自然出现。'),
('情态动词完整专题', '', [(8,allof(8))],
 'will 后接原形，can、must、should 等也有类似的搭配。情态动词 + have done 中的 done 就是过去分词，用来谈过去的推测、遗憾或本应怎样。',
 'mustn’t 是禁止，don’t have to 是不必。过去推测和虚拟体系有联系，但本章例句可以独立理解，后面还有完整虚拟语气。'),
('语态：被动及各种特殊结构', '', [(7,allof(7))],
 '时态改变时间关系，语态改变从谁的角度组织句子。Tom wrote the book 从作者说起；The book was written by Tom 从书说起。核心公式是相应形式的 be + 过去分词，不需要先背完 16 格才能理解。',
 '检查 is cleaned、was cleaned、must be cleaned、has been cleaned：时间或情态不同，被动的意义仍在。'),
('动词进阶、谓语层次与完整自测', '', [(4,[5,6,7,8,9])],
 '时态、情态、被动都已出现，再读限定与非限定动词就不会只有术语。to read、reading、written 可以作为句子零件；完整非谓语专题在后面展开。',
 '本章原动词自测中涉及进行、完成和被动的题，现在已具备所需知识。'),
('连词、并列与连接关系', '第三阶段：从简单句走向复杂句', [(16,[4,5,6,7,8,9,10])],
 '并列连词连接同等地位的成分或分句。从属连词把一个句子单位接成另一句的时间、原因、条件等背景，这个附属单位叫从句。',
 '保留原介词与连词联合自测；介词部分已经学过，不必返回第 7 章找题。'),
('从句入口与状语从句', '', [(10,[0,3])],
 '先从最直观的关系学起：I stayed home because it rained. 我待在家，因为下雨了。because it rained 说明原因。if 条件句、when 时间句等在同一条主线上继续展开。',
 '辨认从句的任务：是在说时间、原因、条件，还是其他背景？别看到长句就逐词硬译。'),
('名词性从句：一整句作为一个成分', '', [(10,[1])],
 '比较 I know the answer 与 I know that she is here：知道的“内容”可以是名词，也可以是一整句。表语说明主语，同位语说明名词内容，这些职位现在由从句来承担。',
 'Do you know where she is? 外层是问句，内层 where she is 用陈述语序。'),
('定语从句：把名词说明得更清楚', '', [(10,[2])],
 '定语修饰名词。the book that I bought 中，book 是被修饰的先行词，that 引入说明它的从句。关系词还在从句里承担角色，能否省略要看角色。',
 '在 the girl who works here 中 who 是从句主语；在 the book that I bought 中 that 是从句宾语。'),
('转述、过去将来、时态呼应与综合自测', '', [(10,[4,5,6,7]),(6,[4,5,6,7,8])],
 '现在可以把从句和时态合在一起理解：Tom said that he would come. 汤姆说他会来。would 从过去的“说”这一参照点看之后的“来”。本章接回原文全部过去将来、特殊时态用法和综合题。',
 '完成从句与时态两套原自测。时态后移要看转述语境和事实是否仍成立，不把每个动词机械后退。'),
('代词进阶：不定、替代、it 与关系词', '', [(3,[6,8,9,10,11,12,13,14])],
 '关系代词和连接代词现在不再是提前出现的术语。形式主语 it 指先用 it 占主语位置，再把较长内容放后面：It is useful to read. 阅读是有用的。to read 暂按“阅读这件事”理解，下一章展开。',
 '做完原代词自测，留意代词指代哪个名词、是主格还是宾格、是否替代整类事物。'),
('非谓语基础：不定式、动名词与分词', '第四阶段：整合与进阶', [(9,[0,1,2,3,5])],
 'to read、reading、written 都能作句子零件，但不独自承担完整的限定谓语。先观察它在整句的位置，再看主动、被动和时间关系。原文的完整变体、复合结构和搭配比较全部保留。',
 '比较 I am reading、Reading is useful、I enjoy reading。同样是 reading，所在结构和工作不同。'),
('非谓语进阶：独立主格、时态语态与自测', '', [(9,[4,6,7,8,9,10,11])],
 '已经学过从句、被动和完成结构，现在再整合非谓语中的逻辑主语、先后与主被动。逻辑主语就是意思上由谁做这个动作。独立主格带着自己的这类主体。',
 '完整做原非谓语自测，优先解释“谁做、主动还是被动、动作先后、在句中充当什么”。'),
('主谓一致进阶与完整自测', '', [(12,[5,6,7,8])],
 '前面的基础一致规则已用于时态学习。现在从句和非谓语都学过了，再读原文第六部分的细节：Reading is useful 中整个活动作主语；the students who work here 中从句动词与 students 对应。',
 '把主谓一致视为找准主语之后的搭配判断，不只背“就近、就远”的名字。'),
('虚拟语气完整专题', '', [(13,allof(13))],
 '你已经认识过去完成时、would/could、条件从句与名词性从句。现在看真实条件与非真实假设的差别，以及愿望、建议、混合条件等完整体系。',
 '分别判断现实条件、现在假设、过去反事实。形式与时间参照有关，不是看到 if 就统一套虚拟。'),
('特殊句式：倒装、强调与省略', '', [(11,allof(11))],
 '倒装可改变通常语序，强调突出某个信息，省略避免重复。这些都以普通句为基础。先恢复普通语序或补足省略部分，再解释用途。',
 '理解之后再练输出。特殊句式不是让简单表达更复杂，而是帮助读懂不同信息安排。'),
('构词法与感叹词', '', [(17,allof(17))],
 '构词法放在熟悉多种词类之后整理：前后缀、合成、转化、缩略。词尾能提供线索，但不能保证每次都猜对词性或意思。原主文档的感叹词内容也保留在本章。',
 '把构词当成辅助判断工具；遇到词义多变、固定搭配或看似相同的词尾，要结合句子。'),
('语篇连接、标点与全程收束', '', [(18,allof(18))],
 '最后从单句走到句间关系。but 与 however 不同：前者是连词，后者通常需要句号或分号等安排，不能只用逗号把两个独立句子硬接起来。',
 '原语法资料已全部归入本路线。下一轮应增加分级文章、听音与实际表达；本版保存的是完整语法知识材料，不把语法覆盖等同于全部语言能力。'),
]

# 原 01 的所有教学正文按主题归入章节，保留独有内容，也保留同主题复盘。
main = texts[1]
start = main.index('## 一、词法')
end = main.index('## ✅ 读完全书后')
main = main[start:end]
pat = r'^#### 1\.1\.\d+ .+$|^### (?!1\.1 ).+$'
marks = list(re.finditer(pat, main, re.M))
dest = {'1.1.1':5,'1.1.2':24,'1.1.3':18,'1.1.4':6,'1.1.5':6,'1.1.6':7,'1.1.7':19,
 '1.1.8':4,'1.1.9':8,'1.1.10':30,'1.2':30,'2.1':10,'2.2':10,'2.3':11,'2.4':11,
 '3.1':23,'3.2':17,'3.3':16,'3.4':26,'4.1':21,'4.2':22,'4.3':20,'4.4':23,
 '5.1':29,'5.2':29,'5.3':29,'6.1':27,'6.2':28,'7.1':31,'7.2':31}
supp = {}
main_audit = []
for i,m in enumerate(marks):
    title = re.sub(r'^#+ ', '',m.group())
    key = title.split(' ')[0]
    block = main[m.start():marks[i+1].start() if i+1<len(marks) else len(main)]
    # 去掉仅用于包裹后续主题的二级标题，不动教学正文。
    block = re.sub(r'^## .+\n', '',block,flags=re.M).strip()
    assert key in dest, key
    supp.setdefault(dest[key],[]).append(block)
    main_audit.append((title,dest[key]))

edits = []
fixes = [
 ('- 助动词：is（is explaining 进行时）、do（do my homework 实义"做"）', '- 助动词：is（is explaining 进行时）；do my homework 中的 do 表“做”，是实义动词。'),
 ('be 动词在虚拟语气中对所有人称都用 were，不用 was。','非真实假设中，正式表达通常用 were；非正式用法也可见 was。优先掌握 If I were you。'),
 ('be 动词一律用 were','非真实假设中的 be 正式表达通常用 were'),
 ('**be 动词一律用 were**','**非真实假设中的 be 正式表达通常用 were**'),
 ('虚拟语气里一律用 were','非真实假设中正式表达通常用 were，非正式用法也可见 was'),
 ('不能说 the room\'s door，规范表达是 the door of the room','通常说 the door of the room；不应把无生命名词的所有格一概判为不合语法'),
 ('**英语句子有五种最基本的结构，所有句子都由它们扩展而来。**','**本节用五种常见基本句型帮助分析英语句子；这是教学分析框架，不代表所有句子都只能机械归入这五类。**'),
 ('- 一个句子的谓语只能有一个"核心动词"（详见非谓语专题）。','- 一个分句需要围绕谓语组织；谓语可以由助动词和实义动词等组合，也可以有并列结构，不能简单用“整句只允许一个动词”判断。'),
 ('（详见 6.1 意义一致）','（整体与成员的区别会在主谓一致部分继续说明）'),
 ('（复合介词）','（单词介词）'),
 ('跳进，复合介词','跳进，单词介词'),
 ('详见主线 01 的 6.1 主谓一致 或 主谓一致专题','本路线第 12 章将完整说明基础主谓一致'),
 ('完整规则要到第三章《时态》《情态动词》才系统学','完整规则在本路线第 13—16 章系统学'),
 ('——第三章学完可回来再看','。后续时态、情态章节会再次提供对应结构，无需返回这里寻找'),
 ('（见下章）','（按实际意义判断，不只看词尾）'),
 ('（见 4 章）','（本章后面的推测部分将继续说明）'),
 ('完整的虚拟规则见 第六章 6.2 虚拟语气 · as if / as though','完整的虚拟规则安排在本路线第 28 章'),
 ('到 3.4 非谓语动词 和 第四章 三大从句 再系统学','从句部分已经学过；非谓语动词在紧接着的第 25—26 章系统展开'),
 ('引导词不能省略的场合见 4.2 定语从句','关系词作主语时不能省略；作宾语时在符合条件的限制性定语从句中常可省略'),
]

def clean(s, label):
    lines=[]
    for line in s.splitlines():
        # 已经替代的导航，不再让读者跳回旧目录；只去提示行，不去知识行。
        if line.startswith('>') and any(x in line for x in ['📖','🔗','💡 若','💡 本节依赖','🎯','🧭']):
            continue
        lines.append(line)
    s='\n'.join(lines)
    s=re.sub(r'\[\[([^]|]+)\|([^]]+)\]\]',r'\2',s)
    s=re.sub(r'\[\[([^]]+)\]\]',r'\1',s)
    s=s.replace('（想扩充去 构词法专题）','（更多构词例子已安排在本书构词法章）')
    for old,new in fixes:
        if old in s:
            edits.append({'位置':label,'原文':old,'新文':new,'次数':s.count(old)})
            s=s.replace(old,new)
    # 统一小节标题层次并移除旧编号，避免重排后读者误以为跳章。
    def heading(m):
        level=min(len(m.group(1))+1,6)
        title=m.group(2).strip()
        title=re.sub(r'^(?:[一二三四五六七八九十]+、|\d+(?:\.\d+)*\s+)', '',title)
        return '#'*level+' '+title
    s=re.sub(r'^ {0,2}(#{2,6}) (.+)$',heading,s,flags=re.M)
    # 原有“答案在章末”改为当前自测后直接折叠。
    s=s.replace('答案在本章末尾','答案紧随本组练习，先答再展开')
    pattern=r'(?m)^\*\*答案(?:与解析)?[：:]\*\*'
    m=re.search(pattern,s)
    if m:
        s=s[:m.start()]+'<details>\n<summary>完成本组练习后，展开答案与解析</summary>\n\n'+s[m.start():].rstrip()+'\n\n</details>'
    return s.strip()

primer='''### 先从三句话进入

I am a student. 我是一名学生。You are happy. 你很开心。She likes books. 她喜欢书。

I/you/she 分别是我、你、她，在这里作主语。am/are 是 be 的形式；like 是“喜欢”，主语为 she 时在这个现在时句子里写 likes。student、book 是名词，happy 是形容词。英语不能照中文省掉 I am happy 中的 am，也不能给 I like books 随意加 am。

先记最常用的搭配：I am；you/we/they are；he/she/it is。否定时，be 后加 not；普通现在时的 like 需要 do/does 帮忙：I don't like ...；She doesn't like ...。does 后 like 恢复原形。后文会完整解释，不要求此刻记住全部变化。

字母分大小写；句首大写，“我”I 总大写。字母名与单词中的发音不是一回事，例如字母 A 的名称与 cat（猫）中 a 的读音不同。本版没有配音频，字母常识不等于完整发音训练。

### 接着读原先修内容
'''
question_bridge='''### 就地铺垫：三类否定与疑问

| 原句 | 否定 | 一般疑问 |
|---|---|---|
| She is tired. 她累了。 | She isn't tired. | Is she tired? |
| She likes tea. 她喜欢茶。 | She doesn't like tea. | Does she like tea? |
| She can swim. 她会游泳。 | She can't swim. | Can she swim? |

be 或情态动词可以直接加 not、放到主语前；普通一般现在时的动作动词通常需要 do/does。过去时普通动作句改用 did/didn't，后面仍接原形。这些会在时态中展开。

先试：把 She likes tea 改成否定，把 You are tired 改成疑问。

<details><summary>展开这两题的答案</summary>

She doesn't like tea.；Are you tired?

</details>
'''

used=Counter()
audit=[]
bodies=[]
names=[f'{i:02}·{p[0]}' for i,p in enumerate(plan,1)]
for i,(title,stage,sources,bridge,recall) in enumerate(plan,1):
    body=f'# 第 {i:02} 章　{title}\n\n'
    body+=f'> **本章入口：**{bridge}\n\n'
    if i==1:
        s=texts[0]
        s=s[s.index('## 一句话的本质'):]
        s=s.split('> 🧭')[0]
        s=re.sub(r'想系统学 →.*', '后续各章将按顺序详细展开这些内容，不需要另外打开旧文件。',s)
        s=s.replace('如 cry 里 y 发 i 的音','如 cry 里的 y 表示 /aɪ/').replace('字母 **y** 单独出现时，当元音','字母 **y** 在某些单词中表示元音')
        s=s.replace('也都是辅音字母一类，原理相同','是拼写规则中的词尾条件；其中 o 是元音字母，ch/sh 是字母组合，不能统称辅音字母')
        s=s.replace('第一章','后续词法内容').replace('这段几十秒','这段文字')
        s=s.replace('第四章·三大从句','第 20—23 章：从句').replace('第三章·3.4 非谓语动词','第 25—26 章：非谓语动词')
        s=s.replace('第三章·3.4 非谓语动词','第 25—26 章：非谓语动词')
        body+=primer+'\n'+clean(s,'原00先修正文')+'\n\n'
    if i==11:
        body+=question_bridge+'\n\n'
    for n, indices in sources:
        for j in indices:
            used[(n,j)]+=1
            h,s=units[n][j]
            audit.append({'来源':files[n].name,'原小节':h,'新章':i,'新标题':title})
            body+=clean(s,f'{i:02}章/{files[n].name}/{h}')+'\n\n'
    if supp.get(i):
        body+='## 同主题归纳与补充（保留原主文档内容）\n\n> 以下保留原 01 对本主题的讲解。与专题重合的内容用于复盘，独有细节也留在这里，无须回到原文件。\n\n'
        for s in supp[i]:
            body+=clean(s,f'{i:02}章/原01归纳')+'\n\n'
    body+=f'## 本章收束\n\n{recall}\n'
    body=revise(i,body)
    bodies.append(body)

bodies=revise_course(bodies)
bodies=refine_basic_rules(bodies)
priority_entries=[]
for n,body in enumerate(bodies,1):
    bodies[n-1],entries=annotate_body(n,body)
    priority_entries.extend(entries)

expected={(n,j) for n in range(2,19) for j in range(len(units[n]))}
assert set(used)==expected, ('缺失',expected-set(used),'多余',set(used)-expected)
assert all(v==1 for v in used.values()),'原专题小节重复编入'

for i,body in enumerate(bodies):
    nav=['[[00·从这里开始|学习目录]]']
    if i>0: nav.append(f'[[{names[i-1]}|← 上一章]]')
    if i<len(bodies)-1: nav.append(f'[[{names[i+1]}|下一章：{plan[i+1][0]} →]]')
    else: nav.append('已完成本版全部章节。')
    titles=[]
    for heading in re.findall(r'^#{2,3} (.+)$',body,re.M):
        if heading not in titles:
            titles.append(heading)
    local_toc='## 本章目录\n\n'+''.join(f'- [[#{h}|{h}]]\n' for h in titles)+'\n---\n\n'
    first,rest=body.split('\n',1)
    content=first+'\n\n'+'　'.join(nav)+'\n\n'+local_toc+rest.lstrip()
    (CHAPTERS/(names[i]+'.md')).write_text(format_answers(content+'\n---\n\n'+'　'.join(nav)+'\n'),encoding='utf-8')

full='# 英语学习资料 · 完整线性正文\n\n> 本文与章节文件内容相同。一直向下读即可；答案就在对应练习后折叠展示。章节长短按原知识内容决定，不规定一天读完一章。\n\n'
for i,body in enumerate(bodies):
    stage=plan[i][1]
    if stage:full+='\n---\n\n# '+stage+'\n\n'
    # 正文中的二级以下标题再降一级，章标题为二级。
    body=re.sub(r'^(#{1,5}) ',r'#\1 ',body,flags=re.M)
    full+=body+'\n\n---\n\n'
# full 仅用于完整性统计；学习入口只提供独立章节，不再输出长文。

guide='''# 英语学习目录

**从第一章开始，按顺序读独立的章节 MD。每章顶部、底部都有“下一章”和“学习目录”。**

读完一章，进入章末的“专用强化题与验收”链接，按首轮题单完成必做强化与独立验收后，再在下面勾选它。选做题不作为七个月首轮的继续条件。题目开头可返回本章，末尾可进入下一章；原章节的下一章链接也保留。下次打开这个目录，点击第一个未勾选的章节即可继续，不需要在全书中滚动定位。章节中途暂停时，可以在 Obsidian 给当前章节加书签；各章也有本章目录，可直接定位小节。

每章包含详细讲解、例句和易错点；原专题自测放在对应主题学完的位置，答案就地折叠。部分章节较长，可以分几次读，不要求一天读完一章。

题目另放在“强化题目”文件夹。各章基础安排为40道任务；第20、25、26章各有6道基础规则补练，共46道，第21章有4道补练，共44道，第23章因包含完整时态复习为56道。每章独立验收12题，附评分、错题修复与延迟复测办法。

## 阅读进度

'''
oldguide=(OUT/'00·从这里开始.md').read_text(encoding='utf-8') if (OUT/'00·从这里开始.md').exists() else ''
checked={name for mark,name in re.findall(r'^- \[([ xX])\] \[\[([^]|]+)\]\]',oldguide,re.M) if mark.lower()=='x'}
for i,p in enumerate(plan):
    if p[1]:guide+='\n### '+p[1]+'\n\n'
    mark='x' if names[i] in checked else ' '
    guide+=f'- [{mark}] [[{names[i]}]]\n'
guide+='''
## 关于这一版

本版复用原 02—18 的 160 个知识、练习和速查小节，并将原 01 的 30 个教学主题按内容归入对应章节。原资料与上一次简版保持不变。

“线性”指学习顺序唯一、前后衔接明确，日常阅读采用目录与独立章节。来源映射、原文快照和调整说明放在“编排记录”中，不属于学习路线。早先生成的连续长文已移到编排记录中存档。

本版已按内容审查修正规则、例句和自测，补充基础变换与输出练习。部分原单选已补语境或改成允许多解；答案说明不同形式的意义。已合并可确认同文的重复段落，独有例句和细则保留。详细记录见“编排记录/内容整改说明.md”。发音、听力与分级阅读尚未另行补充。
'''
(OUT/'00·从这里开始.md').write_text(guide,encoding='utf-8')
guide_path=OUT/'00·从这里开始.md'
guide_text=guide_path.read_text(encoding='utf-8')
guide_text=guide_text.replace('## 阅读进度\n',guide_note()+'\n\n## 阅读进度\n',1)
guide_path.write_text(guide_text,encoding='utf-8')

report='# 来源与编排记录\n\n本文件用于核对，不属于学习必读内容。\n\n'
report+='## 原详细专题去向\n\n| 来源 | 原知识小节 | 新章节 |\n|---|---|---|\n'
for row in audit:report+=f'| {row["来源"]} | {row["原小节"]} | 第{row["新章"]:02}章：{row["新标题"]} |\n'
report+='\n## 原主文档教学正文去向\n\n| 原主题 | 新章节 |\n|---|---|\n'
for title,d in main_audit:report+=f'| {title} | 第{d:02}章 |\n'
report+='\n## 导航处理与正文修正\n\n去掉各专题旧“使用说明”、旧外链导读和旧章节跳转提示；原01的学习顺序与练题地图由新导航替代。旧章节编号在小标题中去掉，不改变其中知识段落。答案移入本组练习后的折叠块。原00的跳转结尾去掉，修正 y/元音字母表述。\n\n'
report+='以下只记录本次实际修正，不能据此认定其他原文都已经校对无误。\n\n'
for e in edits:report+=f'- **{e["位置"]}**：`{e["原文"]}` → `{e["新文"]}`\n'
report+='\n## 完整性检查\n\n'
report+=f'- 原 02—18 共 {len(expected)} 个知识／练习／速查小节，全部各编入一次。\n'
report+=f'- 原 01 共 {len(main_audit)} 个主题块全部编入；原 00 的基础内容用于第01章，成分总表移至第10章，术语关系在第25章归纳。原文快照保留。\n'
report+=f'- 共 {len(plan)} 章，教学正文合计约 {len(full):,} 字符（统计不含各章导航）（含英文、标点、表格和格式字符）。字符数仅用于规模核对，不等于教学效果。\n'
report+='- 原始文件逐字节快照保存在本目录的“原文快照”，便于检查改编差异；读者无需打开。\n'
(OUT/'编排记录'/'来源与调整记录.md').write_text(report,encoding='utf-8')
(OUT/'编排记录'/'内容整改明细.json').write_text(json.dumps({'具体修订':quality_changes,'重复段落合并':quality_dedup},ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'编排记录'/'基础规则校订明细.json').write_text(json.dumps(basic_rule_changes,ensure_ascii=False,indent=2),encoding='utf-8')
(OUT/'编排记录'/'来源映射.json').write_text(json.dumps({'原文件SHA256':hashes,'专题小节':audit,'主文档主题':main_audit,'正文修正':edits},ensure_ascii=False,indent=2),encoding='utf-8')

for p in files.values():assert hashlib.sha256(p.read_bytes()).hexdigest()==hashes[p.name],p.name
assert '[[' not in full,'正文残留跨文件链接'
assert full.count('<details>')==full.count('</details>')
priority_quizzes=build_exercises()
attach_chapter_links()
save_evidence(priority_entries,[{'章':r['章'],**r['首轮分层']} for r in priority_quizzes])
optimize_tree(OUT)
apply_tree(OUT)
all_names={p.stem for p in OUT.rglob('*.md')}
for p in [OUT/'00·从这里开始.md',*CHAPTERS.glob('*.md')]:
    for target in re.findall(r'\[\[([^]|]+)',p.read_text(encoding='utf-8')):
        if target.startswith('#'):
            headings=re.findall(r'^#+ (.+)$',p.read_text(encoding='utf-8'),re.M)
            assert target[1:] in headings,(p.name,target)
        else:
            assert target in all_names,(p.name,target)
print(json.dumps({'章节':len(plan),'专题小节':len(expected),'主文档主题':len(main_audit),'教学正文字符':len(full),'折叠答案组':full.count('<details>'),'原文未改':True},ensure_ascii=False))
