"""教学内容的持久校订层：由构建课程.py调用；不改旧资料。"""
import re

changes = []
dedup = []


def replace(s, old, new, chapter, required=True):
    count = s.count(old)
    if required:
        assert count, (chapter, '校订目标不存在', old)
    if count:
        changes.append({'章': chapter, '原文': old, '修订': new, '处数': count})
        s = s.replace(old, new)
    return s


GLOBAL = [
    ('英语每个句子必须有**主语和谓语**', '常规完整陈述句通常有**主语和谓语**；祈使句可以省略主语，交际中也有省略和非完整句'),
    ('中文里"我饭了"可以说（省略动词），英语**每个句子必须有动词**', '中文与英语表达状态、动作的方式不同。常规完整英语陈述句通常需要谓语动词；祈使、感叹和日常省略表达另有形式'),
    ('比较级用于两者对比，后接 than', '比较级表达程度比较；明确说出比较对象时常接 than，也可由上下文给出对象'),
    ('简单谓语只能有一个核心动词，多动词需用连词连接', '先区分限定动词、含助动词的动词短语、并列谓语以及多个分句；不能凭整句出现多个动词就判错'),
    ('一个简单句不能同时出现两个无连词连接的限定动词', '不能把互不关联的独立谓语随意堆放；但 I know she works here 是主从结构，连接词 that 可省略，不能只靠有没有连词判断'),
    ('表示过去某个时间发生的动作或存在的状态，和现在无关。', '把动作或状态放在已经结束的过去时间中叙述；这不表示它一定没有现在的后果。'),
    ('助动词 + 分词 = 一个复合谓语', '助动词 + 分词共同构成进行时动词短语'),
    ('非谓语动词（non-finite verb）= 不做谓语的动词形式。它没有人称和时态变化', '非谓语动词（non-finite verb）= 不独自承担限定谓语的动词形式。它不独立表达主谓一致和限定时态，但可用完成式等表示相对先后'),
    ('三类结构：情态动词+动词原形；助动词+实义动词（时态/被动）；系动词+表语', '动词短语可含情态动词或助动词，如 should finish、am writing；系动词后另有表语。广义的谓语部分可以包含表语，但表语不属于动词词形本身'),
    ('| 形式 | plays、played、is playing | to do / doing / done |', '| 形式 | plays、played；is playing 中 is 为限定形式 | to do / doing / done |'),
    ('限定动词（finite verb）有人称、时态、数的变化，能独立作谓语；非限定动词（非谓语）无人称时态变化，不能单独作谓语', '限定形式参与表达时态、主谓一致等；含助动词的结构中要辨认哪个是限定形式。非限定形式不独立表达这种主谓一致和时态，但可通过完成式等表示相对先后'),
    ('结构二：动词 + 直接宾语 + to/for + 间接宾语', '对应的介词结构：动词 + 直接宾语 + to/for + 介词宾语（不把它仍叫双宾语）'),
    ('形容词最高级前面必须加 the', '最高级修饰名词时通常用 the；已有 my/his 等限定词时不用再加 the，如 my best friend；部分表语用法也可不带 the'),
    ('最高级中要"排除自身"', '用比较级表达群体中的最高程度时，若主语属于该群体，应把它从比较对象中排除；直接用最高级时，主语仍属于比较范围'),
    ('表语形容词只能放在系动词后面，不能前置', 'afraid、asleep 等通常不直接放在名词前作定语，但可作表语、宾补或后置修饰语，如 keep him awake、the people alive'),
    ('最高级用于三者及以上对比，前加 the，后常接范围', '最高级通常在一个范围内比较某个对象与其余对象，常见结构为 the + 最高级 + 名词；也有 my best friend 等不用 the 的结构'),
    ('**状态动词**（know、love、belong）不能用于进行时', '**状态动词**表达稳定状态时通常不用进行时；有些词换成暂时体验、强调过程等意思时可以用进行时，如 I am loving this trip'),
    ('有明确过去时间状语只能用一般过去时，不能用现在完成时', '明确结束的过去时间通常不与本节所教的现在完成时搭配；一般过去、过去进行等仍按句意选择，如 I was reading at eight last night'),
    ('because 不能引导表语从句说明事实，要用 that', '区别具体结构：The fact is that ... 说明事实；This is because ... 解释原因；The reason is that ... 是表达原因的常用句型。不能一概禁止 because 用在 be 后'),
    ('because 不能引导表语从句，要用 that 说明事实内容', '说明事实可用 The fact is that ...；解释原因可用 This is because ...。学习 The reason is that ... 时，不要推出 because 不能出现在 be 后'),
    ('强调句的 that 不能省略，且不充当任何成分', '本课程的正式句型练习优先保留 that/who；非正式表达中，焦点对应后面从句宾语等情况下可省略，如 It was Tom (that) I met。这里 that 用作连接标记'),
    ('强调句的 that 不能省略，且它不充当任何成分', '正式句型练习优先保留 that/who；非正式表达中可见 It was Tom (that) I met 这类省略。这里 that 用作连接标记'),
    ('否定句和疑问句不能用这种强调方式', '这里介绍肯定句中的 do/does/did 强调。疑问句中的 do 也可重读以加强语气，但通常本来就承担提问作用，不是另加一个 do'),
    ('从句主语和主句主语不一致时，不能省略', '本节先教从句主语与主句主语一致时省略“主语 + be”；另有 if (it is) necessary/possible 等固定表达，不能把此条件推广为所有省略的禁令'),
    ('非谓语动词的被动式（being done）不能省略 being', 'being done 与 done 不能机械互换：进行中的被动可用 being done，完成或状态性的修饰常直接用 done，如 the house being built 与 the house built last year'),
    ('双宾语位置可互换：动词+间接宾语+直接宾语 = 动词+直接宾语+to/for+间接宾语', '部分动词允许两种结构，如 give me a book / give a book to me；能否转换、选 to 还是 for，要看动词搭配。介词后的 me 是介词宾语，不再是双宾语结构中的间接宾语'),
    ('间接宾语（人）+ 直接宾语（物）', '间接宾语（接受者等）+ 直接宾语（给予或涉及的对象）'),
    ('分直接宾语（物）和间接宾语（人）', '双宾语结构中可分直接宾语与间接宾语；不能仅按人、物判断，如 I like her 中 her 是直接宾语'),
    ('解释"全部内容"，定语是"修饰限定"，二者不同', '解释前面名词的身份或内容，定语则修饰限定；要结合具体结构区分'),
    ('对将来虚拟可能性极低，和真实条件句要区分开', '这类假设表示说话者把情况看得较不确定或较远离现实，不对应固定概率；过去形式也能表达对现在或未来的假设'),
    ('可能性极低的将来', '较不确定或较远离现实的未来假设'),
    ('纯不可数名词永远不加 s', '名词在这里的不可数用法不加复数 s'),
    ('**本身都绝不变形**', '**在该不可数用法中不因数量词而加复数 s**'),
    ('不能说 a water（一杯水要用 a glass of water）', '普通材料义用 water；计量可说 a glass of water。点单语境中 a water 也可指一份水，不能一概判错'),
    ('由普通名词组成的专有名词（the Great Wall、the Spring Festival）必须加 the', '专有名称是否带 the 要随名称和惯用法学习，如 the Great Wall、the Spring Festival；不能仅按是否由普通词组成判断，New York、Central Park 通常不带 the'),
    ('由普通名词组成的专有名词如 the Great Wall 必须加 the', 'the Great Wall 习惯带 the；并非所有由普通词组成的名称都带 the，如 Central Park'),
    ('表整体用单数，表成员用复数', '表整体通常用单数；英国英语强调成员时常用复数，美国英语通常更偏好单数，强调个人时可明确写 family members'),
]


def fix_questions(s, chapter, group, items):
    """按原自测分组与题号修订，题目/解析保持成对。"""
    pattern = r'(?m)^### [^\n]*(?:自查|自测)[^\n]*\n[\s\S]*?</details>'
    matches = list(re.finditer(pattern, s))
    assert group < len(matches), (chapter, group)
    m = matches[group]
    text = m.group()
    split = text.index('<details>')
    qs, ans = text[:split], text[split:]
    for number, (question, answer) in items.items():
        if question is not None:
            old = re.search(rf'(?m)^{number}\. .+$', qs)
            assert old, (chapter, number)
            changes.append({'章': chapter, '题组': group+1, '题号': number, '原题': old.group(), '新题': f'{number}. {question}'})
            qs = qs[:old.start()] + f'{number}. {question}' + qs[old.end():]
        if answer is not None:
            old = re.search(rf'(?m)^{number}\. .+$', ans)
            assert old, (chapter, number)
            changes.append({'章': chapter, '题组': group+1, '题号': number, '原解析': old.group(), '新解析': f'{number}. {answer}'})
            ans = ans[:old.start()] + f'{number}. {answer}' + ans[old.end():]
    return s[:m.start()] + qs + ans + s[m.end():]


QUESTIONS = {
    5: {0: {
        5: (None, '❌ pants 是复数形式；题目要表达“两条裤子”，应为 I bought two pairs of pants. 一条则是 a pair of pants。'),
        28: ('She has long hairs.（想表达“她留着长发”，不是几根单独的长毛发）', '❌ 泛指整头头发时用不可数的 hair → She has long hair. 若特指几根毛发，hairs 可用。'),
    }},
    6: {0: {
        15: ('The ______ boy is my brother. (sleeping / asleep / sleep)（正在睡觉）', None),
    }},
    8: {0: {
        8: (None, 'ten（ten to eight = 7:50，差十分八点；8:50 是 ten to nine）'),
        9: ('I have ______ dictionary. (a / an / the)（第一次介绍一本，双方尚未确定是哪本）', None),
        10: ('There is ______ orange on the table. (a / an / the)（第一次引入一个橙子）', None),
        11: ('He is ______ honest boy. (a / an / the)（一般身份描述，不特指已知的那个男孩）', None),
        12: ('This is ______ useful book. (a / an / the)（介绍一本有用的书，不特指已知的某本）', None),
        13: ('______ book on the desk is mine. (A / An / The)（桌上只有一本，双方都知道指哪本）', None),
        20: ('______ cup of coffee, please. (A / An / The)（点一杯咖啡，不指已点好的某杯）', None),
    }},
    11: {0: {
        1: ('______ is in the room? (Who / Whom / Where)（问里面的人是谁）', None),
        7: ('______ fast he runs! (How / What / What a)', 'How（How + 副词 fast + 主语 he + 动词 runs；runs 是动词）'),
        12: ('We made him ______. (monitor / happy / to monitor)（表达“我们选他当班长”，按职务补语的常见用法）', 'monitor（这里表示选任的职务，不加冠词；不能概括成 make 的所有名词宾补都不带冠词，如 make him a star）'),
        14: ('There ______ a meeting tomorrow. (will be / will / are)（用 will 表将来）', 'will be（There will be 表将来存在；There is a meeting tomorrow 也可表示已安排的会议，本题按要求练 will 结构）'),
    }},
    16: {0: {
        2: ('______ I open the window? (May / Must / Need)（请求许可：“我可以开窗吗？”）', None),
        3: ("You ______ be tired after the long trip. (must / can't / need)（说话者根据长途旅行作有把握的肯定推测：“你一定累了”）", None),
        4: ('He ______ go now. He has to. (must / may / can)（表达义务，不是允许或能力）', None),
        6: ("You ______ finish the work today. (needn't / needn't to / mustn't)（今天不必完成，明天交即可）", "needn't（不必）；mustn't 语法形式可用，但表示禁止，不符合题目语境。"),
        8: ('I ______ have called you, but I was busy. (should / could / must)（表达“本来有可能打电话，却没打”，不表达“本应该”）', 'could（未实现的可能）；should have called 表“本应该打”，也能组成正确句子，但不符合本题指定意思。'),
        9: ("He ______ be at home. The lights are on. (must / can't / needn't)（把灯亮着作为依据，表达有把握的肯定推测；现实中这不是逻辑保证）", None),
        14: ("She ______ have passed the exam, but she didn't study. (could / must / need)（设想本有机会通过，不是断定实际已通过）", None),
        15: ('You ______ told me the truth earlier. (should have / should / must have)（责备“本应该早点告诉我”，实际没有）', None),
        17: ('He ______ used to living in the city now. (is / was / does)（说现在已经习惯）', 'is（现在的习惯状态）；若谈过去某时的状态，则 was 也能成立。'),
        18: ("We ______ have waited so long. (needn't / mustn't / couldn't)（我们确实等了，但后来得知不必等）", None),
        19: ('______ we go for a walk? (Shall / Will / Would)（主动提出建议：“我们去散步好吗？”）', None),
        20: ('It ______ rain this evening. Take an umbrella. (might / must / need)（表达可能下雨，不作“必定下雨”的断言）', None),
    }},
    17: {0: {
        16: ('Rice ______ in the south. (grows / is grown / growing)（要求用被动结构，表达“人们在那里种水稻”）', 'is grown（本题指定被动）；Rice grows in the south 也正确，意思是水稻在南方生长。'),
    }},
    18: {0: {
        2: (None, '❌ 普通城市名 Beijing 前常用 in → She arrived in Beijing yesterday. at 常搭配某个具体地点，如 arrive at the station。'),
        12: ('My mother is cook.（想表达“我妈妈是一名厨师”，cook 是普通身份名词）', '❌ 普通身份名词在这里需要限定词 → My mother is a cook. 若表达“我妈妈做饭”，另说 My mother cooks. 问题不在于 is 后不能接名词。'),
    }},
    19: {0: {
        4: ('The cat is ______ the table. (under / at / by time)（表达“猫在桌子下面”）', None),
        6: ('She is good ______ math. (at / in / on)（按本章常见固定搭配，表达数学学得好）', None),
        10: ('I tried my best, ______ I failed. (but / and / so)（明确表达转折：“尽力了，却失败了”）', None),
        11: ('______ it was late, I went home. (Because / So / Although)（表达原因：“因为晚了，所以回家”）', 'Because（题目指定原因）；Although 也能构成句子，但会变成让步关系，与题意不同。'),
        16: ('He was late ______ he missed the bus. (because / because of / so)（错过公交是迟到的原因）', None),
        17: ('The cat jumped ______ the box. (into / in front of / at)（从外面跳到盒子里面）', None),
        20: ('He is smart ______ hard-working. (and / but / or)（中性并列：“聪明而且勤奋”，不表示选择或反预期）', None),
    }},
    23: {
      0: {
        2: ('______ he will come is unknown. (If / Whether / What)（不知道他是否会来）', None),
        7: ('He was late ______ he missed the bus. (because / so / but)（错过公交是迟到的原因）', None),
        8: ('Although he is young, ______ he knows a lot. (but / so / ×)（按本章常见让步句式，不加另一个连词）', '×（本题练 Although 从句 + 主句）；不把本题推出成 yet 在所有让步表达中都不能出现。'),
        12: ('He was so tired ______ he fell asleep. (that / so / as)', 'that（so ... that 引出结果；这里把两部分统一放在过去叙述中）'),
        15: ('Everything ______ he said is true. (that / what / who)', 'that（本题物的关系从句中用 that；这里不设置 which 作干扰项，避免把偏好误当普遍禁令）'),
        17: ('This is the best movie ______ I have ever seen. (that / what / who)', 'that（最高级后常用 that；实际英语中也可见 which，不能把这一偏好写成绝对禁止）'),
        22: ('He studies hard ______ he can pass the exam. (so that / because / although)（表达学习的目的：“为了通过考试”）', None),
        23: ('She said she ______ come the next day. (would / will / can)（按过去视角转述当时的将来计划，练时态后移）', 'would（按本题指定的过去视角转述）；在事实仍有效且说话者保留当前视角等语境中，不后移也可能成立。'),
      },
      1: {
        6: ('When I arrived, she ______ dinner. (cooks / cooked / was cooking)（我到时她正在做饭，尚未做完）', None),
        7: ('The train ______ before I got to the station. (left / has left / had left)（要求用过去完成时突出“到站之前已离开”）', 'had left（按本题要求突出过去之前）；有 before 等明确先后线索时，其他合适语境中也可用一般过去时叙事。'),
        10: ('She said she ______ help me. (will / would / can)（按过去视角，把当时的 will 后移）', None),
        14: ('I ______ TV when the phone rang. (watch / watched / was watching)（电话响时我正在看）', None),
        16: ('She ______ her keys. Can you help her find them? (lost / has lost / loses)（按本章英式用法，要求用现在完成时强调当前找不到）', 'has lost（本题指定现在完成时）；lost 在另一些叙述或美式口语语境中也可成立，不能只因现在有后果就一概排除过去时。'),
        21: ('By the time I got home, she ______. (leaves / left / had left)（突出我到家前她已离开，要求过去完成时）', None),
        23: ('I ______ a letter when you called. (wrote / was writing / write)（你打来时我正在写）', None),
        27: ('I ______ you at the station tomorrow. (am meeting / meet / met)（用现在进行时表达已安排的会面）', None),
        28: ('He said he ______ already ______ the book. (has, read / had, read / reads)（按过去视角时态后移，阅读发生在说之前）', None),
        30: ("I ______ this book for a week. I'll finish it tomorrow. (have read / have been reading / am reading)（要求突出到现在一直进行的阅读活动）", 'have been reading（按题意强调持续过程；避免原题重复列 read，并以指定表达目标区分完成与完成进行）。'),
      },
    },
    26: {0: {
        6: ('I saw him ______ the room. (enter / to enter / entering)（强调看到进入房间的整个过程，而非截取正在进入的片段）', 'enter（感官动词后原形突出事件整体；entering 可突出进行中的片段，不按动作“瞬间/延续”机械划分）。'),
        13: ('He stopped ______. (to talk / talking / talk)（停止说话，安静下来）', 'talking（停止正在说话）；stopped to talk 表停下原来的活动去说话，意义不同。'),
        14: ('______ his work, he went home. (Finishing / Having finished / Finished)（要求用完成式突出做完工作后才回家）', 'Having finished（本题要求主动完成式）；普通叙述中的 Finishing 可有其他语境，不能只凭先后就断言必须用完成式。'),
        16: (None, 'interested, interesting（interested 描述人感到感兴趣；interesting 描述电影令人感兴趣，原解析中的 -ing 标注已改正）'),
    }},
    27: {0: {
        3: ('My family ______ watching TV. (is / are / am)（按英式用法，特意强调各位成员）', 'are（本题指定英式成员视角）；美国英语或整体视角中 is watching TV 也常见。'),
        21: ('A knife and fork ______ on the table. (is / are / am)（把一套刀叉作为一个整体来表达）', 'is（本题指定成套整体）；若分别说刀与叉这两件东西，are 也可成立。'),
    }},
    28: {0: {
        1: ('If I ______ you, I would study harder. (were / am / was)（按本课程正式假设表达作答）', 'were（本题指定正式假设形式）；非正式语境也可见 was，不能笼统判为所有英语中都错。'),
        5: ('If it ______ tomorrow, we would stay at home. (should rain / rains / rained)（本题可多选：选出可表达假设未来的形式）', 'should rain 或 rained。两者都能表达相应的未来假设；前者可突出偶然发生的条件，后者是常见过去形式假设。'),
        9: ('I wish I ______ a bird. (am / were / was)（按正式假设形式作答）', 'were（本题指定正式形式）；非正式用法也可见 was。'),
        10: ('He wishes he ______ harder when he was at school. (studied / had studied / studies)（明确对已经结束的求学阶段表示后悔）', 'had studied（本题对过去遗憾）；若表达对现在学习状态的不满，可说 He wishes he studied harder。'),
        16: ('He talks as if he ______ everything. (knew / knows / know)（说话者认为他事实上并非无所不知，表达非真实假设）', None),
        17: ('She looked as if she ______. (cried / had cried / cries)（要求用过去完成形式，突出哭泣在当时“看起来”之前已发生）', 'had cried（按题目要求，用过去完成形式表示相对过去的先发生）。'),
        19: ('If I ______ to do it, I would do it differently. (were / am / was)（按正式 were to 假设结构作答）', None),
        24: ('It is important that you ______ careful. (be / are / was)（要求用本章介绍的原形虚拟结构）', 'be（本题指定原形虚拟结构；也可用 should be）；其他语体中存在陈述式表达，不能把所有 are 都判为不合语法。'),
    }},
    29: {0: {
        8: ('______ he is young, he knows a lot. (Although / Because / So)（表达让步：“虽然年轻，却懂得很多”）', None),
        10: ('So loudly ______ he speak that everyone heard him. (did / was / does)（叙述过去发生的事情）', 'did（过去时由 did 承担，后面的主要动词用原形 speak；完整句 So loudly did he speak that everyone heard him.）。'),
    }},
    31: {0: {
        10: ('连接性副词在任何位置出现，紧前面都必须是句号或分号。', '❌ 只有用它衔接两个独立分句时，需要处理两句之间的句号、分号或连词；句中可说 He was, however, tired.，不能要求每个 however 紧前都是句号或分号。'),
        13: ('直接引语内还有引语时，英美英语对内外层单双引号只有一种共同规则。', '❌ 美式出版物常外双内单，英式出版物常外单内双，也受具体风格指南影响。本书示例使用外双内单，不把另一套系统判错。'),
    }},
}


def edit_chapter(chapter, s):
    if chapter == 7:
        for old,new in [
            ('整体充当一个及物动词', '依具体搭配决定是否带宾语，不能把所有这类结构都归为及物'),
            ('宾语是代词时，须放在动词和副词之间', '可分的及物短语动词带代词宾语时，代词放中间，如 turn it on；不可分结构则放后面，如 look after him'),
            ('宾语是代词 it/them 时必须放中间', '对于 turn on、pick up 这类可分结构，代词 it/them 要放中间；look after、look for 则不能拆开'),
        ]:
            s=replace(s,old,new,chapter)
        block='\n### 三种搭配就地对照\n\n| 类型 | 名词宾语 | 代词宾语 |\n|---|---|---|\n| 可分及物：turn on | turn on the light / turn the light on | turn it on |\n| 不可分：look after | look after the child | look after him/her |\n| 不及物：get up | 不直接带动作对象 | I get up at seven. |\n\n不要写 look him after；也不要把 get up 后的 at seven 当直接宾语。\n\n'
        pos=s.index('## 本章收束')
        s=s[:pos]+block+s[pos:]
    if chapter == 9:
        s=replace(s,'动词按功能分两大类、五个类别。','本课程按句中用法区分实义动词、系动词、助动词与情态动词；这些不是彼此绝对排斥的词表，同一个 be/have/do 可有不同身份。',chapter)
        a=s.index('```'); b=s.index('```',a+3)+3
        tree='''| 分析角度 | 先问什么 | 例子 |
|---|---|---|
| 实义用法 | 是否表达动作、事件或状态本身 | work、know；have a book 中的 have |
| 系动词用法 | 是否连接主语与说明主语的表语 | be、become、seem |
| 助动词用法 | 是否帮助组成时态、被动、否定或疑问 | is reading；has finished；do you like |
| 情态用法 | 是否表达能力、许可、义务或推测等 | can、must、should |

系动词并非全部“没有词义”：become 表变化，seem 表看起来。实义动词还可按所带宾语和补足成分分析为不同句型。'''
        changes.append({'章':chapter,'修订':'替换原混合分类树，改为按用法区分的对照表'})
        s=s[:a]+tree+s[b:]
    if chapter in (10,18):
        pairs=[
            ('系表结构整体作谓语，表语是谓语的一部分，不是独立的宾语', '本书区分狭义的“谓语动词”和广义的“谓语部分”：He is happy 中 is 是系动词，happy 是表语；is happy 整体是对主语的陈述部分。表语不是宾语'),
            ('复合谓语：情态+原形、助动词+实义动词、系动词+表语', '动词短语可包含情态动词、助动词与主要动词，如 should finish、am writing；系动词后另分析表语。广义谓语部分可包含这些补足成分'),
            ('复合谓语：两个及以上词共同作谓语，三类结构', '这里把谓语动词短语与广义谓语部分分开观察'),
            ('系动词 + 表语：The flowers **smell sweet**.', '系动词后接表语：The flowers **smell sweet**.（smell 是系动词，sweet 是表语）'),
            ('（复合：系表）','（系动词 + 表语）'),
            ('**一个简单句只能有一个限定动词作谓语核心**，多动词需用连词或非谓语', '先找每个分句的限定谓语，再看并列和非谓语结构；She sings and dances 有并列的谓语成分，I know she works 有主从两个分句'),
            ('一个简单句有且只能有一个限定动词作谓语核心，多动词需用连词或非谓语形式', '句子可包含主从或并列结构；不能只数动词单词。每个分句围绕自己的限定谓语组织，其余动作可以通过并列、从句或非谓语表达'),
            ('简单句只有一个限定动词作谓语核心', '按分句和并列关系识别谓语，不机械数动词'),
            ('explain、suggest 只能说 explain sth to me', 'explain 常用 explain sth to me；suggest 可用 suggest sth to me、suggest doing 或 suggest that 从句'),
            ('双宾语后置+介词','直接宾语 + for 介词短语'),
        ]
        for old,new in pairs:s=replace(s,old,new,chapter,False)
    if chapter == 19:
        s=replace(s,'look after、give up；代词宾语放中间','look after 不可分：look after him；give up/turn on 等可分结构的代词宾语放中间',chapter)
    if chapter == 22:
        s=replace(s,'只能用 that 的场合','优先使用 that 的常见场合',chapter)
        s=replace(s,'先行词或结构满足特定条件时，关系代词只能用 that，不能用 which/who。','限制性定语从句中，不定代词、最高级等后面常优先使用 that；这是常见选择倾向，不代表所有 which/who 都不合语法。',chapter)
        s=replace(s,'先行词既有人又有物时，只能用 that 引导','先行词并列包含人和物时，限制性定语从句中通常优先用 that',chapter)
    if chapter == 24:
        s=replace(s,'14. ✅ me 作间接宾语','14. ✅ me 是 to 的介词宾语；Give me the book 中 me 才在双宾语结构中作间接宾语',chapter)
    if chapter == 25:
        for old,new in [
            ('一个句子里只能有一个"真谓语"，其他动词都要变成非谓语','先识别分句与并列关系，再看动词是否是限定形式。额外动作可用并列、从句或非谓语表达，不能仅按整句有几个动词判断'),
            ('一个简单句**只能有一个限定动词作谓语**，多出的动词用非谓语或连词','同一结构中不能随意把独立谓语堆在一起；并列谓语、多个分句和含助动词的动词短语要分别分析'),
            ('一个句子只能有一个谓语，但动作可能不止一个，剩下的动作怎么办？变成非谓语。','当一个动作需要作为主语、宾语、修饰语等零件时，可使用非谓语形式；另一个动作也可以通过并列或从句表达。'),
            ('He playing games.（两个动词，错）','He playing games.（He 是代词；playing 不能在这里独自构成完整的限定谓语，缺少 is 等合适形式）'),
            ('"助动词 + 分词"（is playing）是复合谓语，不算两个动词','is 与 playing 是两个动词形式，共同组成进行时动词短语；不要把单词数量与谓语结构数量混为一谈'),
        ]:s=replace(s,old,new,chapter)
    if chapter == 28:
        for old,new in [
            ('说"假如/要是/希望"这些不真实的话，就用虚拟语气，时态要往后退一步','先区分真实条件、远离现实的假设、遗憾以及建议要求；这些结构不都靠机械“时态后退”来构造'),
            ('wish 后的时态都要后退一层，不能用现在时','本节 wish + 从句表达非真实愿望时，通常用过去式表示现在，用过去完成表示过去；不要把这条推广到所有 wish 用法，如 I wish you well、I wish to leave'),
        ]:s=replace(s,old,new,chapter,False)
    if chapter == 31:
        for old,new in [
            ('连接性副词**不能像连词那样直接连接两个句子**，前面要用分号或句号','连接性副词本身不能代替并列连词连接两个独立分句；两句之间可用句号或分号等。副词也可在句中出现，如 He was, however, tired，不要求它紧前总有句号或分号'),
            ('连接性副词不能像连词那样直接连接两个句子，前面要用分号或句号','连接性副词不独自承担并列连词的连接作用；两个独立句之间常用句号或分号，但副词本身也可位于句中'),
            ('前面用句号或分号，不能直接逗号连','连接两个独立分句时处理句间标点；也可在句中作插入成分'),
            ('引语在前：句号/问号放引号内', '引语在前且后接 she said 等引述语时，普通陈述引语常以逗号衔接；问句或感叹句可保留问号或感叹号'),
            ('引语内还有引语时，外层用双引号、内层用单引号：He said, "She told me \'I am busy\'."', '本书示例采用美式常见的外双内单：He said, "She told me, \'I am busy.\'" 英式出版物也常用外单内双，应遵循所选风格而非判另一套错误'),
            ('标点在引号内；内层引语用单引号', '引语自身的标点按所选风格处理；本书采用外双内单，另有外单内双系统'),
        ]:s=replace(s,old,new,chapter,False)
    return s


PRACTICE = {
  3: ('人称与 be 的搭配', '''先遮住答案，补全：① I ___ a student. ② She ___ happy. ③ We ___ friends. ④ Tom and I ___ students. 再把 She is happy 改为否定和一般疑问句。''',
      '① am ② is ③ are ④ are。She is not happy.／She isn’t happy.；Is she happy? 主语 Tom and I 对应 we。'),
  7: ('代词宾语的位置', '把名词对象改为代词：① turn on the light ② look after the boy ③ look for the keys。light 灯；keys 钥匙。',
      '① turn it on ② look after him ③ look for them。只有第一项是这里所教的可分结构。'),
  11: ('三类句子自己变', '把下列句子各改成否定和一般疑问，再给一个肯定简答：① She is tired. ② He likes tea. ③ They can swim.',
      '① She isn’t tired. Is she tired? Yes, she is. ② He doesn’t like tea. Does he like tea? Yes, he does. ③ They can’t swim. Can they swim? Yes, they can. 简答跟随问句的 be、do 或情态动词。'),
  13: ('习惯与正在进行的对照', '① 把 She works here 改成否定、疑问、肯定简答。② 把 She is working now 同样变换。③ 用 I 写一句日常习惯，再写一句此刻正在做的事。',
      '① She doesn’t work here. Does she work here? Yes, she does. ② She isn’t working now. Is she working now? Yes, she is. ③ 示例：I read every day. I am writing now. 允许其他符合实际、搭配正确的句子。'),
  14: ('过去动作与过去状态', '① 把 I worked yesterday 改为否定句，再用 you 作主语向对方问“你昨天工作了吗”。② She was tired 改否定和问句。③ 回答 Did you work yesterday?，分别给肯定、否定简答。④ 用英语描述昨天八点你正在做的事。',
      '① I didn’t work yesterday. Did you work yesterday? ② She wasn’t tired. Was she tired? ③ Yes, I did.／No, I didn’t. ④ 示例：I was reading at eight last night. 过去状态句用 was/were；普通动作句否定、疑问用 did 后接原形。'),
  15: ('未来表达与累计复习', '① She will come tomorrow 改否定、疑问。② She is going to study 改否定、疑问。③ 把 I work here 改成“昨天在这里工作”。④ 写一句明天的计划。',
      '① She won’t come tomorrow. Will she come tomorrow? ② She isn’t going to study. Is she going to study? ③ I worked here yesterday. ④ 示例：I am going to read tomorrow. 计划、预测等表达有重叠，按本题指定结构练习。'),
  17: ('主动与被动的对应', '把 Tom cleaned the room yesterday 改成以 The room 开头的句子；再把该被动句改为否定和一般疑问。clean 打扫。',
      'The room was cleaned by Tom yesterday. The room wasn’t cleaned by Tom yesterday. Was the room cleaned by Tom yesterday? 时间变化体现在 was，cleaned 保持过去分词形式。'),
  21: ('从句语序与自己的表达', '① 把 Where is she? 放入 I know ... 中。② 合并 I think ... 与 She is right。③ 写一句“我不知道他在哪里工作”。',
      '① I know where she is. ② I think (that) she is right. ③ I don’t know where he works. 从句内部用陈述语序，不复制独立问句的倒装。'),
  25: ('区分动词、分句和非谓语', '① 分析 I know she works here：有几个限定分句？② She sings and dances 是否必须把 dances 改成 dancing？③ 改正 He playing games。④ 用 want to do 和 enjoy doing 各写一句。',
      '① 两个：I know ... 与 she works here，各有自己的限定谓语。② 不必，sings 与 dances 是并列的谓语成分。③ He is playing games. ④ 示例：I want to read. I enjoy reading. 检查主语、动词形式和搭配，不只数动词个数。'),
  28: ('用语境区分假设', '① 用给定词写句：if / I / have more time / would read more，表达与现在不同的假设。② 对照解释 I wish I studied harder 与 I wish I had studied harder。③ 写一句现在或将来的真实条件。',
      '① If I had more time, I would read more. ② 前者通常希望现在更用功；后者遗憾过去没更用功。③ 示例：If it rains tomorrow, I will stay at home. 不是所有 if 句都用同一假设结构。'),
  31: ('综合输出', '用 5—7 句写一段自己的学习经历：至少包含一个现在习惯、一个过去事件、一个计划，以及 because/but/if 中的一种连接。写完检查主语、谓语形式、名词单复数、指代和标点。',
      '示例：I study English at home. I read every day. Yesterday I learned a new word. It was difficult, but my friend helped me. Tomorrow I am going to write a short story. If I need help, I will ask her. 开放题不只有一个答案；重点检查时间一致、搭配和句间关系。'),
}

VERB_TABLE = '''### 常用动词形式：先覆盖本书实际用到的词

规则动词过去式、过去分词常同形；不规则动词要分别记。下面是起步表，后续遇到新词再补。

| 原形 | 过去式 | 过去分词 | 常见意思 |
|---|---|---|---|
| be | was/were | been | 是、处于 |
| do | did | done | 做；也可作助动词 |
| have | had | had | 有；也可作助动词 |
| go | went | gone | 去 |
| come | came | come | 来 |
| see | saw | seen | 看见 |
| take | took | taken | 拿、带走 |
| give | gave | given | 给 |
| write | wrote | written | 写 |
| read | read | read | 读；原形常读 /riːd/，后两种读 /red/ |
| buy | bought | bought | 买 |
| make | made | made | 制作、使 |
| know | knew | known | 知道、认识 |
| eat | ate | eaten | 吃 |
| leave | left | left | 离开 |
| lose | lost | lost | 丢失 |
| speak | spoke | spoken | 说 |
| learn | learned/learnt | learned/learnt | 学习 |
| work | worked | worked | 工作 |
| study | studied | studied | 学习 |

常见规则拼写：work—worked；live—lived（末尾已有 e 只加 d）；study—studied（辅音字母 + y）；play—played（元音字母 + y 不变）；stop—stopped。双写不是所有辅音结尾都适用；先掌握这些高频词，再按遇到的词逐步扩展。

这张表不要求一口气背完。先把 go、do、have、be、see、write 用进句子，分清过去式与过去分词：She went home.／She has gone home.，不能写 has went。
'''


def merge_exact_repeats(s, chapter):
    """只合并可证明同文的重复定义/规则；保留所有独有文字、例句和题目。"""
    marker='## 同主题归纳与补充（保留原主文档内容）'
    if marker not in s:
        return s
    pre,post=s.split(marker,1)
    normalize=lambda t: re.sub(r'[\s*`]+','',t)
    known=normalize(pre)
    kept=[]
    removed=[]
    for paragraph in re.split(r'\n\s*\n',post):
        p=paragraph.strip()
        # 不删例句、表格、答案、小标题，只处理重复的定义和规则段。
        eligible=(p.startswith(('**通俗定义**','**核心规则**','**易错误区**'))
                  and not re.search(r'(?m)^\d+\. |\|',p)
                  and len(normalize(p))>=18)
        if eligible and normalize(p) in known:
            removed.append(p)
        else:
            kept.append(paragraph)
        known+=normalize(p)
    # 原文标题只承担主题标记，不在无内容的情况下留下空标题。
    out='\n\n'.join(kept)
    out=re.sub(r'(?m)^(#{4,6} .+)\n\s*(?=#{1,6} |---\s*$)', '',out)
    if removed:
        dedup.append({'章':chapter,'合并段数':len(removed),'合并原文':removed})
    return pre+marker+out


def revise(chapter, s):
    for old,new in GLOBAL:
        s=replace(s,old,new,chapter,False)
    s=edit_chapter(chapter,s)
    for group,items in QUESTIONS.get(chapter,{}).items():
        s=fix_questions(s,chapter,group,items)
    s=merge_exact_repeats(s,chapter)
    if chapter == 13:
        pos=s.index('### 现在时态')
        s=s[:pos]+VERB_TABLE+'\n\n'+s[pos:]
    if chapter in PRACTICE:
        title,prompt,answer=PRACTICE[chapter]
        block=f'### 就地练习：{title}\n\n{prompt}\n\n<details>\n<summary>先作答，再展开参考答案</summary>\n\n{answer}\n\n</details>\n\n'
        pos=s.index('## 本章收束')
        s=s[:pos]+block+s[pos:]
    # 核心能力与进阶识别分层，但不要求读者在不同路径中选择。
    goal=('**本章要求：**能解释典型例句，辨认结构；第一次不要求熟练使用全部进阶细则。'
          if chapter in (26,28,29,30) else
          '**本章要求：**先理解例句，再独立完成练习；基础句型要能自己变换和写出，不能只在看答案时认识。')
    first,rest=s.split('\n',1)
    return first+'\n\n> '+goal+'\n'+rest
