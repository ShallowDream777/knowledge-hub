from pathlib import Path
from collections import defaultdict
import os
import re
import json
import hashlib
import sys
sys.path.append(str(Path(__file__).resolve().parents[2]/'英语学习资料·完整线性版/编排记录'))
from 标题优化 import rename_title, rename_text
from 阅读体验优化 import wording
from 条目规划 import ENTRIES, CUSTOM, RELATED, ARTICLE_NOTES

ROOT=Path(__file__).resolve().parents[1]
COURSE=ROOT.parent/'英语学习资料·完整线性版'
sources={int(p.name[:2]):p for p in (COURSE/'章节').glob('*.md')}
assert set(sources)==set(range(1,32))
source_text={n:p.read_text(encoding='utf-8') for n,p in sources.items()}
source_hash={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sources.values()}
CUSTOM_CHAPTERS={'for_since':[13],'past_present_perfect':[13,14],'aspect_compare':[13,14,15],'relative_omission':[22]}
DEEP={'P07','W03','V05'}

# 先前基础课程修订曾移动或改名这些小节；保留旧来源记录的可追溯定位。
SOURCE_REDIRECTS={
    (1,'八大句子成分 · 一眼看懂表'):(10,'八大句子成分对照表'),
    (1,'一句话的本质'):(1,'主语与谓语：句子谈谁、说明什么'),
    (1,'零基础最常见的两个混淆，先帮你拆开'):(1,'字母、单词、短语与句子'),
    (13,'16 种时态总表'):(23,'16 种时态总表'),
    (25,'现在分词 doing（主动、进行）'):(25,'现在分词 doing：主动关系与具体语境'),
    (25,'过去分词 done（被动、完成）'):(25,'过去分词 done：被动关系、状态与具体语境'),
}


def norm(text):
    text=re.sub(r'^[（(]\d+[）)]\s*','',text)
    text=re.sub(r'^\d+(?:\.\d+)*\s+','',text)
    text=rename_title(text)
    return re.sub(r'[\s*`]+','',text).casefold()


def extract(chapter,title,deep=False):
    chapter,title=SOURCE_REDIRECTS.get((chapter,title),(chapter,title))
    s=source_text[chapter]
    # 不把原自测、答案和新增强化入口带入查询条目。
    s=re.sub(r'<details>[\s\S]*?</details>','',s)
    heads=list(re.finditer(r'^(#{1,6}) (.+)$',s,re.M))
    exact=[(i,m) for i,m in enumerate(heads) if m.group(2).strip()==title]
    matched=exact or [(i,m) for i,m in enumerate(heads) if norm(m.group(2))==norm(title)]
    assert matched,(chapter,title,'未找到知识标题')
    i,m=matched[0]
    end=len(s)
    for nxt in heads[i+1:]:
        h=nxt.group(2).strip()
        if len(nxt.group(1))<=len(m.group(1)):
            end=nxt.start();break
        if not deep and h not in ['通俗定义','核心规则','中英对照案例','中英对照例句','易错误区']:
            end=nxt.start();break
    body=s[m.end():end].strip()
    assert body,(chapter,title,'知识段为空')
    return body


def polish(text):
    text=re.sub(r'^---\s*$','',text,flags=re.M)
    text=re.sub(r'^> 💡 \*\*第一次读到可以只记结论\*\*[^\n]*\n?', '',text,flags=re.M)
    text=text.replace('，本路线第 12 章将完整说明基础主谓一致。这里先记住：**is 配单数、are 配复数**即可。','。family的具体一致方式还受英美用法与整体、成员视角影响。')
    text=text.replace('（本章后面的推测部分将继续说明）','（相关条目可查推测用法）')
    text=text.replace('——完整的虚拟规则安排在本路线第 28 章。这里先记住"as if 后面常不按常规时态来"即可。','；若说话者认为情况真实或合理可能，也可以用正常的陈述形式，如It looks as if it is going to rain。')
    text=text.replace('后续词法内容会用','语法分析中会用')
    text=text.replace('在本课程采用的常见用法中','在本字典采用的常见用法中')
    text=text.replace('后续词法内容讲名词复数、动词变化时会反复说','名词复数、动词变化的规则中常见')
    text=text.replace('这里先把 26 个字母分成两组，你就不会看不懂了','26个英文字母按字母类别分成两组')
    text=text.replace('这 7 类 + 几个特殊用法，就是代词的完整体系','这些是本字典采用的常见教学分类；词类划分在不同语法体系中可能略有差异')
    text=re.sub(r'^\*\*先认识就够\*\*[^\n]*$', '**字母与声音分开判断**：复数拼写规则看字母条件；a/an则看后面实际读音，如a university、an hour。',text,flags=re.M)
    text=text.replace('上面的表是最常用的七种；下面这几个在日常英语（尤其写作）里也超高频，但最容易被中文习惯带偏：','下面列出撇号、连字符、破折号与括号的常见用途：')
    # 旧标题内的练习语气不适用于查阅；正文事实和例句保留。
    text=text.replace('背下来','查阅表').replace('必须逐个记','不规则形式')
    text=re.sub(r'^#{3,6} 通俗定义\s*$', '',text,flags=re.M)
    text=re.sub(r'^#{2,6} (.+)$',r'### \1',text,flags=re.M)
    replacements=[
      ('最高级前面必须加 the','最高级修饰名词时通常带the；已有my等限定词或特定表语结构时另看'),
      ('双重所有格表"其中之一、部分"，不表唯一所属','双重所有格表达所属关系中的一个；不据此精确断言拥有者的总数量'),
      ('双重所有格表部分概念，不表唯一所属','双重所有格常表达所属关系中的一个，不用它精确证明朋友或物品的总数'),
      ('（不是唯一的）','（表达所属关系中的一位）'),
      ('a friend of my father（我爸爸的朋友，可能唯一）和 a friend of my father\'s（我爸爸朋友中的一个）语气不同，教学上常用后者','a friend of my father与a friend of my father\'s都可按语境表达所属；不靠这一区别精确判断朋友总数'),
      ('限定性定语从句','限制性定语从句'),
      ('主句意思不完整','识别对象所需的信息可能改变'),
      ('是句子不可缺少的部分','用于限制名词的识别范围；去掉后句子仍可能合语法，但指代不同'),
      ('while 引导的从句必须用延续性动词','本条while表示时间同时关系时通常描述持续背景；while还可用于对比和让步，不能一概要求所有用法都带延续动作'),
      ('while 强调一段时间内正在进行，从句必须用延续性动词','while在这里强调一段时间内的背景活动；其对比、让步等用法另按实际意义判断'),
      ('不能用瞬间动词','不把本条时间背景的偏好推广成while所有用法的禁令'),
      ('介词后面、or not 前面只能用 whether，不能用 if','介词后或or not紧随连接词时，本条用whether；if ... or not可在另一些宾语结构中使用'),
      ('介词后、or not 前只能用 whether','介词后或or not紧随连接词时，本条用whether'),
      ('瞬间动词不能和"一段时间"（for 3 days、since）连用，要换延续性表达','表示一个状态持续多久时，不能把单次发生事件直接当持续状态；如买后拥有多久用have had。次数统计、否定和其他语境不能机械套此限制'),
      ('瞬间动词（buy、join、leave）不能和 for/since 连用，要转化为延续性动词','表达持续拥有、处于组织中等状态时，应使用相应延续表达；不可推广成这些词在任何语境都不能与for/since同现'),
      ('主语必须是名词，代词主语不倒装','本条here/there等常见地点结构中，名词主语可倒装，代词主语通常不倒装'),
      ('代词主语不倒装','本条here/there等地点倒装的代词主语通常保持普通语序'),
      ('核心是系动词，后面接表语，没有动作','核心是系动词加表语，说明主语；become等还可表达变化，不能概括成所有系表结构都没有动作或变化'),
      ('只有系动词后面才有表语，实义动词后面是宾语','本字典把系动词后的主语补足成分称为表语；其他动词后还可能有宾语、宾补或状语，不能一律叫宾语'),
      ('间接宾语是人，直接宾语是物，可转换位置加介词 to/for','间接宾语常表示接受者、受益者，直接宾语表示所给或所传达的内容。部分动词可改成宾语加to/for短语，须按具体搭配核对，不是所有双宾结构都可机械转换'),
      ('主语 + 及物动词 + 宾语，动作有明确的承受对象','主语 + 及物动词 + 宾语，宾语是该动词用法所涉及的对象，不必是被动作改变的承受者'),
      ('谓语是及物动词，后面必须接宾语意思才完整','本句型中动词按带宾语的及物用法使用；某些词也能用于不带宾语的其他句型，如She reads every evening'),
      ('不定式、动名词、从句作主语，谓语用单数','一个不定式、动名词结构或单个内容从句作主语时，谓语通常用单数；两个结构用and并列时须另看是否为同一整体'),
      ('从句必须用陈述语序，不能说 I don\'t know where is he，要说 I don\'t know where he is.','普通间接疑问从句用陈述语序：I don\'t know where he is，而不是where is he。不要把这条推广成所有从句都排除倒装；条件倒装、比较等另有结构。'),
      ('I like reading and my brother **likes** listening to music.（可省略重复谓语）','I like tea and my brother (likes) coffee. 我喜欢茶，我兄弟喜欢咖啡。（可写成I like tea and my brother coffee；后一个likes承前省略）'),
      ('英语句子 = 主语 + 谓语（这是所有句子的骨架）','常规完整陈述句通常有主语与谓语；祈使句、省略句等另按各自结构判断'),
      ('情态动词不能单独作谓语，后面必须跟实义动词原形','can、must等核心情态通常与动词原形组成完整动词短语，也可接be、have构成的结构；上下文明确的简答中可省略后续内容，如Yes, I can'),
      ('can、may、must 等都无人称变化，只有 have to 有人称变化（has to）','can、may、must等核心情态无人称数变化；have to属于相关的半情态表达，有has to、had to等变化，不能把核心情态的形式规则机械推广到所有相关表达'),
      ('**不可数名词不能用 one 代替，用 that**：不能 a tea and a coffee... 的 one','**one作同类名词替代时通常要求可数意义**。不可数比较可用that，如the water in this bottle与that in the glass；a tea表示一杯茶等可数用法，须与材料义区分'),
      ('By next summer, she **would have been studying** here for 4 years. 到明年夏天，她在这里学习就满四年了。（过去视角）','In 2020, she said that by the following summer she **would have been studying** there for four years. 她在2020年说，到随后那个夏天，她在那里学习就满四年了。（过去的转述视角）'),
      ('不能单独使用，必须有过去的语境作参照','需要过去参照点，但不一定写在从句里；过去参照也可由前文叙事提供。would另有假设、习惯等用法，须看语境'),
      ('| 以 s/x/ch/sh/o 结尾 |','| 以s/x/ch/sh或部分o结尾 |'),
      ('多数变 ves','部分变ves，其他常直接加s'),
    ]
    for a,b in replacements:text=text.replace(a,b)
    text=re.sub(r'\n{3,}','\n\n',text)
    return wording(rename_text(text.strip()))



if __name__=='__main__':
    from 合并构建 import build
    build()
