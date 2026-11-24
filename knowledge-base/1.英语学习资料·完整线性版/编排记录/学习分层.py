"""保守的七个月首轮标记：真题出现事实与教学深度建议分开维护。"""
from pathlib import Path
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- study-priority:start -->'
END = '<!-- study-priority:end -->'

# 年份和页码均指用户提供文件的PDF页序，不是页脚页码。
EVIDENCE = {
    'E01': ('2023口语第1—3题', '2019-2023年英语真题及答案.pdf', 2, 'I have a problem with my credit card.', '基础主语、动词、名词及问答，是后续句子分析的前提。'),
    'E02': ('2023阅读一第2段', '2019-2023年英语真题及答案.pdf', 4, 'Hundreds of individuals and businesses have registered their cameras', '可数复数、数量、冠词和动词搭配出现在阅读题面；不能因此声称每条名词例外都单独设题。'),
    'E03': ('2023短文完成Text One', '2019-2023年英语真题及答案.pdf', 12, 'cause big ... / are in ... / brings together ...', '组装problems、danger、information；回填需识别主语和动词结构。'),
    'E04': ('2020阅读四及第36题', '2019-2023年英语真题及答案.pdf', 87, 'Ellen Rose had been a patient of mine for years', '双重所有格实际出现；并承载人物关系定位，不能列为完全未考。'),
    'E05': ('2023英译汉', '2019-2023年英语真题及答案.pdf', 13, 'neighbors they can rely on ... were less likely to experience ...', '定语从句、介词搭配、比较与可能性均影响翻译意义。'),
    'E06': ('2023短文完成Text One', '2019-2023年英语真题及答案.pdf', 12, "40% of the world's insects ... One third of the world's insects", '百分数、分数、部分与整体、数量一致实际用于正文。'),
    'E07': ('2025词汇第15题', '2025年同等学力申硕英语真题以及参考答案详解.pdf', 2, "Only when you've got enough credits will you be eligible to apply", 'only状语前置倒装实际在题面中；词汇设问目标是eligible，不把倒装冒称为该题独立得分点。'),
    'E08': ('2021词汇第18题', '2019-2023年英语真题及答案.pdf', 55, 'Under no circumstances should we do anything against the will of the people.', '否定范围和倒装实际出现；设问为短语替换。'),
    'E09': ('2025阅读一', '2025年同等学力申硕英语真题以及参考答案详解.pdf', 2, 'a study examining how exercising with limited gym equipment affects the human body', '非谓语修饰、间接疑问内容和动名词主语叠加，是读长句的实际需要。'),
    'E10': ('2025阅读二、三', '2025年同等学力申硕英语真题以及参考答案详解.pdf', 3, "Our people have been enjoying ... / if you've been sleeping less than optimally", '现在完成进行式在新近卷中实际出现，不因形式长就降低整个主题。'),
    'E11': ('2010阅读二', '2007-2012年英语真题及答案.pdf', 36, 'a nonprofit group that had been developing digital science and math books for about two years', '过去完成进行式有题面实例。建议识读，不声称从未考过。'),
    'E12': ('2010完形正文', '2007-2012年英语真题及答案.pdf', 41, 'By the end of the evening you will have spoken with up to twenty men or women!', '将来完成式有题面实例；首轮保留时间关系辨认，降低机械造句要求。'),
    'E13': ('2022阅读三', '2019-2023年英语真题及答案.pdf', 34, 'might have been considered a very old, fragile, and even a sick person', '情态＋完成＋被动同时出现在阅读；不能整块跳过情态完成。'),
    'E14': ('2023词汇第15题', '2019-2023年英语真题及答案.pdf', 3, 'All classes ... will have to be called off when the hurricane arrives.', '助动、情态意义和被动叠加，取消义的理解依赖结构。'),
    'E15': ('2013阅读四', '2013同等学力英语真题及答案解析.pdf', 7, 'the world would not have known about, had we not asked for help', '虚拟条件倒装、情态完成实际用于阅读，不是只在答案解析里出现。'),
    'E16': ('2017阅读三', '2017年同等学力英语真题及参考答案.pdf', 9, 'Silicon Valley would never have boomed were it not for the fact that ...', '反事实与省if形式实际出现，过去结果配一般条件说明不能机械把时间不一致判错。'),
    'E17': ('2016博客正文', '2016年同等学力英语考试真题.pdf', 11, 'I did not know Mr. Jobs, though I wish I had.', 'wish、过去愿望与省略实际出现；保留理解要求。'),
    'E18': ('2025阅读三', '2025年同等学力申硕英语真题以及参考答案详解.pdf', 3, 'I replied, heart racing.', 'heart具有自己的逻辑主体，是独立主格的实际例子；不是主句主语I直接作racing主体。'),
    'E19': ('2025博客正文', '2025年同等学力申硕英语真题以及参考答案详解.pdf', 4, 'With the cost-of-living crisis biting, more people are considering living in alternative housing', 'with复合结构在新近题面出现，仍须能读懂背景关系。'),
    'E20': ('2022口语Dialogue Two', '2019-2023年英语真题及答案.pdf', 29, "Wow, that's great.", '感叹词实际在交际材料出现，不能整类宣称未考。'),
    'E21': ('2025英译汉', '2025年同等学力申硕英语真题以及参考答案详解.pdf', 6, "whether you're at a local park or camping in the wilderness ... Anything you leave behind", '选择让步、定语省略、情态可能性和目的均承载全文意义。'),
    'E22': ('2025完形第46—55题', '2025年同等学力申硕英语真题以及参考答案详解.pdf', 5, 'as well as ... However ... Furthermore ... Therefore', '词义、搭配、词形与逻辑衔接均在真实设空任务中使用。'),
    'E23': ('2025短文完成Text One—Three', '2025年同等学力申硕英语真题以及参考答案详解.pdf', '5—6', 'slipping ... can earn as much ... as men ... watched on TV by ...', '短语组装与回填需要搭配、比较、主被动及句子位置判断。'),
    'E24': ('2025阅读与完形', '2025年同等学力申硕英语真题以及参考答案详解.pdf', '4—5', 'fMRI / AI / ABS / countless / unrepresentative', '首字母缩写和词缀在卷面出现；识别词义词性有用途，不要求穷举所有构词来源。'),
    'E25': ('2023口语与英译汉', '2019-2023年英语真题及答案.pdf', '2、13', "There is a charge ... There are real benefits ... What do you mean?", '存在句、问句、主谓一致及人称时态均为阅读与基本表达前提。'),
    'E26': ('2023英译汉', '2019-2023年英语真题及答案.pdf', 13, 'as is the case with all friendships', 'as补充类比实际出现；首轮重在识读其承接关系。'),
    'E27': ('2025写作要求', '2025年同等学力申硕英语真题以及参考答案详解.pdf', 6, 'Discuss the significance ... Include examples and reasons to support your viewpoint.', '写作需要完整句子、逻辑与基本表达，不要求展示复杂时态或倒装清单。后半是教学深度判断，不是对所有年份作文的统计结论。'),
}

CHAPTER_EVIDENCE = {
    1:['E01'],2:['E02','E03'],3:['E01','E21'],4:['E02','E03'],5:['E04','E02'],
    6:['E05','E23'],7:['E05','E22'],8:['E06','E23'],9:['E01','E14'],10:['E09','E05'],
    11:['E25'],12:['E03','E25'],13:['E10','E25'],14:['E04','E11'],15:['E12','E27'],
    16:['E13','E08'],17:['E14','E13'],18:['E09','E14'],19:['E22'],20:['E21'],
    21:['E05','E09'],22:['E05','E09'],23:['E04','E10','E12'],24:['E21','E23'],
    25:['E09','E21'],26:['E18','E19','E09'],27:['E03','E06'],28:['E15','E16','E17'],
    29:['E07','E08','E15'],30:['E24','E20'],31:['E22','E27'],
}

# B是输出深度降低，不是“未考过”。证据未覆盖某细则时不据此标C。
B_RULES = {
    (6,'多个形容词的排序'): ('看懂修饰对象与基本先后即可；不背整条排序长口诀，不反复排列多重形容词。形副位置和比较仍必学。', ['E05','E27']),
    (14,'过去完成进行时'): ('辨认had been doing，理解持续到过去参照点；暂不反复做否定、疑问和自由造句。2010卷有实际用法。', ['E11']),
    (15,'将来进行时'): ('看懂will be doing在未来时点的活动背景；本节读完即可，暂缓多轮变换。基本will和going to仍必学。', ['E12','E27']),
    (15,'将来完成时'): ('看懂will have done及by参照点；2010完形正文实际出现，不能直接跳过理解。', ['E12']),
    (15,'将来完成进行时'): ('按will＋have been doing理解未来参照点前的持续，不要求背写全套变换。题面检索未见该完整词串，不等于历年未考。', ['E12','E10']),
    (16,'need / dare'): ('普通need to do和“不必／禁止”仍必学；dare及双身份的复杂变换先做到识别，不反复造句。', ['E13','E08']),
    (22,'优先使用 that 的常见场合'): ('看懂关系词与所指对象，知道这些是常见选择倾向；暂不穷举每一种优先场合。基础关系词与从句缺位检查仍必学。', ['E05','E09']),
    (22,'as 引导的定语从句'): ('读懂as承接前后内容的类比／补充关系；2023翻译实际出现，不要求模仿所有位置变式。', ['E26']),
    (26,'独立主格结构'): ('找到结构自己的逻辑主体，再理解时间、原因或伴随背景；2025阅读有heart racing，不能整块跳过。暂缓反复仿写。', ['E18','E19']),
    (28,"would rather 与 It's time 的虚拟"): ('能理解偏好、到该做某事时的含义及过去形式不等于过去时间；先不反复背写多种从句组合。普通would rather do仍要理解。', ['E15','E27']),
    (28,'虚拟语气的倒装与混合'): ('2013、2017题面已有实例；会恢复if关系、辨认条件与结果时间，不要求主动生成各种复杂组合。', ['E15','E16']),
    (28,'虚拟条件句的倒装'): ('见到had／were／should前置，能还原条件关系即可；保留阅读能力，不反复从普通句生成倒装。', ['E15','E16']),
    (28,'混合虚拟（错综时间）'): ('分别判断条件与结果的时间，不机械要求形式一致；2017阅读有过去结果与一般条件组合，不作“未考”处理。', ['E16']),
    (29,'完全倒装'): ('找回真正主语和动词、还原普通语序；不必首轮熟练仿写每种地点或方向前置。', ['E07','E08','E27']),
    (29,'其他特殊倒装'): ('按让步、结果、条件或时间关系读懂；not until的否定范围仍要掌握。虚拟倒装已有真题实例，不标可跳。', ['E15','E16','E08']),
    (30,'合成法'): ('看懂熟悉词如何组合成整体意思；特殊合成复数与连字符先按词识别，不反复套规则造词。普通名词复数仍必学。', ['E24','E27']),
    (30,'缩略法'): ('看懂常用截短和首字母缩写即可，不背每个缩写的完整展开。2025题面有AI、ABS和fMRI。', ['E24']),
    (31,'直接引语的标点规则'): ('读懂引号内外是谁在说话，了解标点区别；首轮不反复操练英美嵌套引号格式。独立句边界仍必学。', ['E01','E27']),
}

def strip_labels(text):
    # 兼容旧版注释包装；新版只显示学习要求，不向正文写入维护标记。
    text = re.sub(re.escape(START)+r'[\s\S]*?'+re.escape(END)+r'\n*','',text)
    # 标题及其目录锚点同时去掉同行标签；说明内容仍按登记过的生成行识别。
    text = re.sub(r'　【(?:必学|识读即可|同主题复盘|选做·综合复盘|考试必学)】','',text)
    note_lines={re.sub(r'^> \*\*【[^】]+】\*\*\s*','> ',s) for s in GENERATED_LABEL_LINES}
    return ''.join(line for line in text.splitlines(keepends=True)
                   if line.rstrip('\r\n') not in GENERATED_LABEL_LINES|note_lines)

def managed(text):
    return text.rstrip()+'\n'

def label_b(chapter,title):
    title=re.sub(r'^[（(]\d+[）)]\s*','',title)
    direct=B_RULES.get((chapter,title))
    if direct:return direct
    if chapter==30 and title in ['感叹词','什么是感叹词']:
        return ('能理解Oh／Wow等在对话中的反应，不要求背诵或列举冷僻感叹词。2022口语确实出现Wow。',['E20'])
    return None

# 精确匹配脚本生成的行，避免为重新编排而删除读者添加的其他批注。
GENERATED_LABEL_LINES = {
    '> **【必学】**',
    '> **【同主题复盘】** 与前文同一知识点不必重学；首次出现的独有内容仍按其知识标签学习，不能整块略过。',
    '> **【选做·综合复盘】** 本组完整保留；首轮按章末分层题单验收，不需同时刷完所有原有自测。',
    '> **本节分开要求：** 时间先后、日期含义和时间介词必学；past／to等多套报时读法只需识读，暂缓反复按不同说法编写同一时刻。',
    '> **本节分开要求：** 一般过去将来would do／was going to必学；would be doing、would have done、would have been doing在过去转述中的复杂组合先识读。反事实中的would have done不能因此跳过，第28章仍要理解。',
    '> **本表用途：** 作为速查与比较，不要求首轮默写16格；每行沿用前文的必学／识读深度。',
    '> **首轮学习：** 按顺序读标为“必学”的内容；“识读即可”仍需读懂例句与关系，暂缓复杂背写。原自测可留作复盘；归纳中的独有内容仍按标签学习。章末题库已列出首轮必做题。',
    '> **【识读即可】** '+label_b(30,'感叹词')[0],
} | {'> **【识读即可】** '+goal for goal,_ in B_RULES.values()}

def annotate_body(chapter,body):
    body=strip_labels(body)
    out=[];entries=[]
    for line in body.splitlines(keepends=True):
        out.append(line)
        m=re.match(r'^(#{2,5}) (.+?)\s*$',line)
        if not m:continue
        title=m[2]
        if title in ['通俗定义','核心规则','本章收束','本章目录','本章强化与验收']:continue
        if title.startswith('同主题归纳'):
            note='> **【同主题复盘】** 与前文同一知识点不必重学；首次出现的独有内容仍按其知识标签学习，不能整块略过。'
            level='复盘'
        elif any(x in title for x in ['高频易错自查','附：']):
            note='> **【选做·综合复盘】** 本组完整保留；首轮按章末分层题单验收，不需同时刷完所有原有自测。'
            level='复盘'
        else:
            rule=label_b(chapter,title)
            if rule:
                goal,eids=rule
                note='> **【识读即可】** '+goal
                level='B'
            else:
                note='> **【必学】**'
                level='A'
            if chapter==8 and title=='时间与日期的表达':
                note+='\n> **本节分开要求：** 时间先后、日期含义和时间介词必学；past／to等多套报时读法只需识读，暂缓反复按不同说法编写同一时刻。'
            if chapter==23 and title=='过去将来时态（4 种）':
                note+='\n> **本节分开要求：** 一般过去将来would do／was going to必学；would be doing、would have done、would have been doing在过去转述中的复杂组合先识读。反事实中的would have done不能因此跳过，第28章仍要理解。'
            entries.append({'章':chapter,'标题':title,'深度':level,'依据':rule[1] if rule else CHAPTER_EVIDENCE[chapter],
                            '说明':rule[0] if rule else '基础理解或后续学习的先修；并不宣称标题内每条细则都曾独立设题。'})
            if chapter==8 and title=='时间与日期的表达':
                entries.append({'章':chapter,'标题':'时间表达中的多套报时读法（本节内部）','深度':'B','依据':['E01','E27'],
                                '说明':'区分读懂时刻与反复编写多种说法；时间先后和介词不降级，不声称报时从未考过。'})
            if chapter==23 and title=='过去将来时态（4 种）':
                entries.append({'章':chapter,'标题':'过去转述中的进行、完成、完成进行组合（表格内部）','深度':'B','依据':['E04','E12','E15'],
                                '说明':'只降低过去转述复杂组合的主动生成要求；一般would和反事实would have不随之降级。'})
            if chapter==23 and title=='16 种时态总表':
                note+='\n> **本表用途：** 作为速查与比较，不要求首轮默写16格；每行沿用前文的必学／识读深度。'
        out.append('\n'+managed(note)+'\n')
    header='> **首轮学习：** 按顺序读标为“必学”的内容；“识读即可”仍需读懂例句与关系，暂缓复杂背写。原自测可留作复盘；归纳中的独有内容仍按标签学习。章末题库已列出首轮必做题。'
    joined=''.join(out)
    pos=joined.index('\n')+1
    joined=joined[:pos]+'\n'+managed(header)+'\n'+joined[pos:]
    return joined,entries

B_TAGS = {
    8:{'报时'},14:{'过去完成进行'},15:{'将来进行','将来完成','将来完成进行'},
    23:{'过去将来进行','过去将来完成','过去将来完成进行'},26:{'独立主格'},
    28:{'would rather'},29:{'地点倒装','代词不倒装'},30:{'合成复数','连字符'},31:{'直接引语'},
}
# 仅输出型B任务选做；识读问答仍然保留在首轮验收里。
OPTIONAL_C = {6:{10},15:{4,5},16:{4},22:{9},28:{5},29:{9,10}}
RECOGNITION_C = {8:{8,9},15:{6,7},22:{8},28:{9,10},30:{3,4,5,10},31:{7,8}}
OPTIONAL_B = {29:{2},30:{1}}
RECOGNITION_B = {26:{4},28:{2,4}}
OPTIONAL_D = {23:{1,6,7}}

def mark_questions(chapter,groups):
    counts={};required={}
    for prefix,items in groups.items():
        required[prefix]=[]
        for i,item in enumerate(items,1):
            status='必做';reason='本章基础理解与应用。'
            if prefix=='A':
                if item['知识点'] in B_TAGS.get(chapter,set()):
                    status='选做';reason='对应识读知识的形式输出；先读懂正文例句，再按需加练。'
                elif 9<=i<=16:
                    status='选做';reason='与同情境补全、表达重复；前两项有错或不稳时再做本项改错。'
            elif prefix=='C':
                if i in OPTIONAL_C.get(chapter,set()):status='选做';reason='复杂形式的输出或细则回忆，不作首轮门槛。'
                elif i in RECOGNITION_C.get(chapter,set()):status='识读必做';reason='检查能否读懂结构／语境，不要求额外仿写变式。'
            elif prefix=='B':
                if i in OPTIONAL_B.get(chapter,set()):status='选做';reason='从普通句主动生成复杂倒装，首轮只要求读懂其反向还原。'
                elif i in RECOGNITION_B.get(chapter,set()):status='识读必做';reason='有真题使用证据，保留关系识别，不要求穷举生成。'
            elif prefix=='D' and i in OPTIONAL_D.get(chapter,set()):
                status='选做';reason='复杂时态的输出训练，首轮保留理解，不作背写门槛。'
            item['首轮要求']=status;item['分层理由']=reason
            if status!='选做':required[prefix].append(f'{prefix}{i:02}')
        counts[prefix]={'必做':len(required[prefix]),'选做':len(items)-len(required[prefix])}
    return {'题单':required,'数量':counts,'验收满分':2*len(required['C']),
            '验收建议':math.ceil(0.8*2*len(required['C']))}

def first_round_panel(plan):
    def ids(prefix):return '、'.join(plan['题单'][prefix]) or '无'
    return ('## 七个月首轮题单\n\n'
            '题目标记中的“选做”只表示本轮训练安排，不表示知识点从未考过。“识读必做”仍需理解并作答。\n\n'
            + ''.join(f'- **{label}：**{ids(prefix)}。\n' for prefix,label in [('A','分项必做'),('B','串联必做'),('D','补练必做'),('C','验收必做')])
            + f'\n先做以上题目。首轮C按实际必做题计算，满分{plan["验收满分"]}分，建议至少{plan["验收建议"]}分；'
              '得分后仍要修正错题与不稳项。A、B、D中的必做题能独立完成并说明题干要求的理由即可，不再要求把选做题刷完才能继续。\n\n'
              '若A的某个情境不稳，再做同情境标为选做的改错题；只针对卡点加练。原有全卷与完整复习标准保留在文末，供第二轮使用。\n\n')

def guide_note():
    return managed('''## 七个月备考标记

- **【必学】**：基础理解和必要运用；也包括后续阅读的前提，不表示每条细则都单独考过。
- **【识读即可】**：仍读讲解与例句，能还原结构、说清意思；暂缓复杂背写和多轮造句。
- **【选做·复盘】**：重复归纳或完整自测的安排，首轮以章末题单为准，不表示该知识冷门。

未另标的段落沿用最近的上级要求；同一知识点在归纳表再次出现，沿用前面的深度，不因重复出现就升级。本轮没有把任何完整知识点标成“证据充分、可放心跳过”：提供的材料缺2024年，文字检索未见也不能证明从未考过。独立主格、虚拟倒装、双重所有格都已找到真实题面实例。

每章练习开头有首轮必做题号，题目旁也有标记，文末按首轮实际题数计算验收。标为选做的题不阻挡进入下一章；所有知识与题目完整保留。真题定位与分层理由留在编排记录中，日常学习不用额外查表。''')

def save_evidence(entries,plans=None):
    data={'口径':'真题出现事实、学习先修和首轮输出深度分开；不从正则未命中推出未考。',
          '题面范围':'用户提供2001—2023及2025年；2024缺失。文字层检索剔除参考解析；2025题面PDF1—6页人工核读。',
          '知识标记':entries,'真题定位':EVIDENCE,'放心跳过的完整知识点':[],
          '首轮题单':plans or []}
    (ROOT/'编排记录/学习分层明细.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
