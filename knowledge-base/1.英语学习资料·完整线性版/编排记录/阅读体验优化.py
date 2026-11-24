"""集中使用说明，保留语法讲解；可在生成后重复应用。"""
from pathlib import Path
import re
import json
import hashlib
from 零基础试读校订 import revise
from 后续章节试读校订 import revise as revise_later, revise_quiz

VAULT=Path(__file__).resolve().parents[2]
RECORD=Path(__file__).resolve().parent
COURSE=VAULT/'英语学习资料·完整线性版'
EXAM=VAULT/'同等学力申硕英语·考试强化'
DICTIONARY=VAULT/'英语语法知识字典'

MODIFIER='“修饰”是提供说明信息，例如a red book中red说明书是红色的，整个短语是“一本红色的书”。在这个短语中red放book前，不写a book red。本章先理解这种关系，不要求背诵全部句子成分。'
WORD_CHECK='先用一小步检查：book表示事物名称，所以是名词；happy描述状态，所以是形容词。本章不要求掌握所有词类。'
USAGE='''## 使用说明：符号与练习记法

下面是这套资料的书写约定。看懂用途即可，不需要背诵；示例中的英语会在正文中讲解。

| 符号 | 在资料中的含义 | 示例 |
|---|---|---|
| / 或 ／ | 并列列出几种写法 | am/is/are 表示分别列出 am、is、are |
| → | 从左边的写法变成右边 | book → books |
| + | 将几个部分组合起来 | I + am + happy 组合成 I am happy. |
| -s、-ing | 表示接在词尾的字母；短横线不抄进单词 | book 加 -s，写成 books |
| ___ | 练习中需要补写的位置 | I ___ happy. 的空白处填 am |

正文中的例句用于讲清当前知识点。先读讲解、尝试例题，再做章末练习；学习深度按下方标签和题库里的首轮题单执行。

'''

REPLACEMENTS={
    '> **本章要求：**先理解例句，再独立完成练习；只变换本章已经演示的am/is/are否定，不要求提前处理普通动作句的否定、提问。':'> **本章学习目标：**认识词和句子，读懂“我是……”这类简单表达，并学会把它变成否定句。',
    '> 以下保留原 01 对本主题的讲解。与专题重合的内容用于复盘，独有细节也留在这里，无须回到原文件。':'',
    '完成原名词自测再展开答案。后面的同主题复盘保留原 01 的讲解，不是新的必选阅读分支。':'能区分名词所有格、名词作定语与冠词搭配后，进入章末练习。正文自测可用于检查易错点。',
    '本章原综合自测同时复习冠词；因为冠词已提前学过，现在不必另开文件。':'本章综合自测同时复习数词与已学冠词，重点检查数量、顺序、比例和名词搭配。',
    '原语法资料已全部归入本路线。下一轮应增加分级文章、听音与实际表达；本版保存的是完整语法知识材料，不把语法覆盖等同于全部语言能力。':'完成本章后，可以结合分级阅读、听力和实际表达继续练习。需要复习某个语法概念时，用知识字典定位；进入考试准备时，按考试强化资料继续学习。',
    '这 7 类 + 几个特殊用法，就是代词的完整体系。':'下表按常见用途介绍代词，后续小节会分别说明；不同语法体系的分类方式可能有所不同。',
    '第05章的前后夹证':'第05章结合空白前后的对话判断意图',
    '基础线性版已将复杂语法的生成要求降为识读；到这里重在用它读懂材料，不增加背公式门槛。':'基础线性版中标为“识读即可”的内容，仍以读懂结构和意义为目标；其他知识按“必学”要求掌握，并用于本套练习。',
    '特指（双方都知道、上文提过、有后置定语限定）都要加 the。':'对象可以确定时常用 the；已有 my、this 等限定词时不再叠加 the，如 my book、this book。后面有修饰语也不一定用 the，如 a book about music（一本关于音乐的书）。',
}

def wording(text):
    for old,new in REPLACEMENTS.items():text=text.replace(old,new)
    return text

def foundation_chapter(text):
    text=wording(text)
    text=re.sub(r'^> \*\*首轮学习：\*\* 按顺序读标为“必学”的内容；[^\n]*\n\n?', '',text,flags=re.M)
    text=text.replace('> **本章要求：**先理解例句，再独立完成练习；按本章已经演示的步骤完成对应练习；用于说明当前知识点的例句，不额外验收尚未教过的其他规则。\n\n','')
    text=text.replace('> **本章入口：**从单词、句子和具体搭配开始。所有需要用来做题的名称，都在使用前解释。\n\n','')
    match=re.search(r'^### 资料中常用符号的含义\n[\s\S]*?(?=^### |\Z)',text,re.M)
    if match:
        assert MODIFIER in match[0] and WORD_CHECK in text,'符号说明或修饰段落结构已改变，需人工核对'
        text=text[:match.start()]+text[match.end():]
        text=text.replace(WORD_CHECK,WORD_CHECK+'\n\n'+MODIFIER,1)
    text=re.sub(r'^- \[\[#资料中常用符号的含义\|资料中常用符号的含义\]\]\n','',text,flags=re.M)
    return revise_later(revise(re.sub(r'\n{4,}','\n\n\n',text)))

def improve_content(text,path):
    path=Path(path).resolve()
    if path.parent==COURSE/'章节':return foundation_chapter(text)
    if path.parent in [COURSE/'强化题目',EXAM/'强化题目']:
        return revise_quiz(text,int(path.name[:2]),'基础' if path.parent==COURSE/'强化题目' else '考试')
    if path==COURSE/'00·从这里开始.md':
        if '## 使用说明：符号与练习记法' not in text:
            text=text.replace('## 七个月备考标记\n',USAGE+'## 七个月备考标记\n',1)
        text=text.replace('**从第一章开始，按顺序读独立的章节 MD。每章顶部、底部都有“下一章”和“学习目录”。**',
                          '首次学习先读下方使用说明，再从第01章顺序学习。\n\n[[01·文字、句子和必备术语|开始第01章 →]]　[[#阅读进度|继续上次进度 →]]')
        return text
    if path.parent==EXAM/'章节':
        text=re.sub(r'^> \*\*【考试必学】\*\* 本章对应真实试卷[^\n]*', '> **【考试必学】**',text,flags=re.M)
        return revise_later(wording(text),'考试')
    if path==EXAM/'00·考试强化总目录.md':return wording(text)
    if path.is_relative_to(DICTIONARY):return wording(text)
    return text

def improve(text,path):
    from 标题同行标签 import format_reader
    from 外部资料吸收 import revise as absorb_external
    from 祈使句带学 import revise as teach_imperatives
    return format_reader(teach_imperatives(absorb_external(improve_content(text,path),path),path),path)

def apply_tree(root,backup=False):
    changed=[]
    for path in sorted(Path(root).rglob('*.md')):
        if any(x in path.parts for x in ['编排记录','编排维护']):continue
        raw=path.read_bytes();text=raw.decode('utf-8')
        newline='\r\n' if '\r\n' in text else '\n'
        after=improve(text.replace('\r\n','\n'),path).replace('\n',newline).encode('utf-8')
        if after==raw:continue
        if backup:
            snap=RECORD/'阅读体验优化前快照'/(str(path.relative_to(VAULT))+'.snapshot')
            snap.parent.mkdir(parents=True,exist_ok=True)
            if not snap.exists():snap.write_bytes(raw)
        path.write_bytes(after)
        changed.append({'文件':path.relative_to(VAULT).as_posix(),'修改前SHA256':hashlib.sha256(raw).hexdigest(),'修改后SHA256':hashlib.sha256(after).hexdigest()})
    return changed

if __name__=='__main__':
    rows=[]
    for root in [COURSE,EXAM,DICTIONARY]:rows+=apply_tree(root,backup=True)
    if rows:
        record_path=RECORD/'阅读体验调整明细.json'
        existing=json.loads(record_path.read_text(encoding='utf-8')) if record_path.exists() else []
        merged={row['文件']:row for row in existing}
        for row in rows:
            if row['文件'] in merged:row['修改前SHA256']=merged[row['文件']]['修改前SHA256']
            merged[row['文件']]=row
        record_path.write_text(json.dumps(list(merged.values()),ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'阅读体验调整：{len(rows)} 份文件。')
