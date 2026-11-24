"""修正基础规则的过度概括；在先修修复后、目录和答案排版前执行。"""

CHANGES = []


def revise_course(bodies):
    def change(n, old, new):
        count = bodies[n - 1].count(old)
        assert count, (n, old)
        bodies[n - 1] = bodies[n - 1].replace(old, new)
        CHANGES.append({'章': n, '原文': old, '修订': new, '次数': count})

    def before(n, marker, addition):
        assert bodies[n - 1].count(marker) == 1, (n, marker)
        change(n, marker, addition + marker)

    # 20：先用完整的、已经学过的主谓结构讲“无论”，不提前考名词性从句。
    before(20, '##### （6）目的状语从句', '''###### whether … or …：无论哪一种情况

**whether A or B** 可以列出两种情况，说明无论哪一种，主句都成立。这里的 A、B 是替换位置的标签，不是要写进句子的单词。

1. **Whether it rains or not, we will go out.** 无论下不下雨，我们都会出去。or not 补出“不下雨”这一种情况。
2. **Whether you are at home or you are at school, you can read.** 无论你在家还是在学校，你都可以阅读。

第二句也常写成 Whether you are at home or at school, you can read：第二处相同的 you are 不再重复，意思不变。先对照完整句理解，再读简写，不必猜省去了什么。

这类状语说明“无论怎样，后面的结论都不变”，不能都译成“是否”。第21章再用例句区分询问“是否”的内容从句。

''')
    change(20, '3. unless = if...not，不能再加 not；', '3. unless 表“除非／如果不”，不要为了翻译“除非”而机械再加 not；从句本身需要否定时仍可用 not，详见条件从句例句；')
    change(20, '| 让步 | though、although、even if | Although he is young |', '| 让步 | though、although、even if、whether … or … | Although he is young；Whether it rains or not |')
    change(20, '- unless 相当于 if...not，不能再加 not。', '''- 本节表示“除非／除了……情况”时，unless 常可用 if ... not 解释；不能因此给原本肯定的条件再加一次 not。
- 但不是“unless 后禁止 not”：We will go out unless you are not ready.＝我们会出去，除非你还没准备好（ready＝准备好的）。这里 not 确实否定 ready，是有意表达另一种条件，不能删掉而保持原意。''')
    change(20, '2. He talks **as if he knew everything**. 他说起话来好像什么都知道。', '2. It looks **as if it is going to rain**. 看起来好像要下雨。这里根据眼前迹象作判断，使用已学的 be going to 表达。')

    # 21、23：是否、无论、如果各有语境；or not 的限制针对紧邻位置。
    for n in [21, 23]:
        change(n, 'if 只能引导宾语从句，whether 可引导所有名词性从句', '在本章常规名词性从句中，if 主要用于动词后表达“是否”；句首主语、表语和同位语位置按 whether 的例句学习。if 还可表示“如果”，引导第20章已学的条件状语从句')
    change(21, '动词后接 whether/if 都可，介词后、or not 前只能用 whether。', '动词后的普通“是否”内容常可用 whether 或 if；介词后用 whether。紧接 or not 时用 whether or not；若 or not 在从句末尾，if 也可用，见下方对照。')
    change(21, '介词后面、or not 前面只能用 whether，不能用 if。', '介词后用 whether；紧邻 or not 的是 whether or not。不能把这个限制误读成“从句末尾有 or not 就不能用 if”。')
    before(21, '#### 宾语从句的否定转移', '''#### whether／if：先看整段在表达什么

| 句子 | 意思与结构 |
|---|---|
| I don't know whether he is at home. | 我不知道他是否在家。whether 后的内容作 know 的宾语；这里也可用 if。 |
| I don't know whether or not he is at home. | 我不知道他究竟在不在家。or not 紧接 whether；这个位置不能换成 if or not。 |
| I don't know if he is at home or not. | 我不知道他是否在家。or not 放在从句末尾，这个 if 用法成立。 |
| Whether he is at home or not, I will call him. | 无论他在不在家，我都会给他打电话。这里是第20章的“无论”状语，主句是 I will call him。 |
| If he is at home, I will call him. | 如果他在家，我就给他打电话。这是有条件的安排，意思不同。 |

不要仅凭 whether、if 或 or not 这一个词决定译法。先问：是在说“不知道什么”，还是在说“无论哪种情况”，或者在提出一个条件？

''')
    change(23, '| 陈述语序 | 所有从句都用陈述语序 |', '| 陈述语序 | 本章普通名词性从句不照搬独立问句的倒装；其他句式按各自规则判断 |')
    change(23, '| that 用法 | 宾语从句可省，主语/表语/同位语从句不可省 |', '| that 用法 | 普通动词后宾语从句的 that 常可省；本课主语、表语、同位语从句练习保留 that，不将此简表当成所有省略的禁令 |')
    change(23, '| 只用 that | 先行词为不定代词/最高级/序数词/既人又物 |', '| that 的常见选择 | 第22章所列场合常用或优先用 that；不把简表推广成脱离语境的唯一选择 |')

    # 25：分词的名称不等于时态；不定式也不自带将来时。
    change(25, '**不定式（infinitive）= to + 动词原形，可在句中充当除谓语外的几乎所有成分。**', '**不定式（infinitive）是一类非谓语形式，常见写法是 to + 动词原形；特定搭配里不带 to，如 I saw him enter。它可作主语、宾语、表语、定语、状语、补语，不独自充当限定谓语。**')
    before(25, '#### 不定式的变体', '''#### 不定式不等于“将来要做”

1. **I want to see you tomorrow.** 我想明天见你。将来的意思来自 want 的愿望和 tomorrow，不是只由 to see 决定。
2. **I am happy to see you.** 见到你我很开心。双方此刻已经见面，to see 仍是不定式，不能硬译成“以后才要见”。
3. **To read is useful.** 阅读是有用的。to read 说的是一项活动，不是在预测某次将来事件。

先看不定式在句中做什么，再结合谓语、时间词和上下文判断时间。需要明确表示“相对更早”等关系的形式，在第26章进一步比较。

''')
    change(25, '#### 现在分词 doing（主动、进行）', '#### 现在分词 doing：主动关系与具体语境')
    change(25, '**通俗定义**：现在分词表主动、进行的含义，可作定语、状语、补语。', '**通俗定义**：现在分词可作定语、状语、补语；与所说明的对象通常有主动关系。它可以描述进行中的动作，也可以说明一般活动、原因、结果等，不能一见 doing 就译成“正在”。')
    change(25, '#### 过去分词 done（被动、完成）', '#### 过去分词 done：被动关系、状态与具体语境')
    change(25, '**通俗定义**：过去分词表被动、完成的含义，可作定语、状语、补语。', '**通俗定义**：过去分词可作定语、状语、补语；常说明被动关系或状态，部分用法表示完成。“过去分词”是形式名称，不等于一般过去时，也不保证每次都能译成“已经”。')
    for n in [25, 26]:
        change(n, '流动的水很清澈。（定语，主动进行）', '流动的水很清澈。（定语，说明水的流动状态）')
        change(n, '碎了的杯子被扔掉了。（定语，被动完成）', '碎了的杯子被扔掉了。（定语，说明杯子破碎的状态）')
        change(n, 'remember/forget/regret 后接 to do 表"未做"，接 doing 表"已做"。', 'remember／forget 常按“记住或忘记要做的事”与“记得或忘了做过的事”区分；regret to say／tell 是遗憾地告知，regret doing 是对做某事后悔，不要统套“未做／已做”。')
    change(25, '| 时间 | 正在进行 | 已经完成 |', '| 时间 | 可表示同时发生或一般情况等，不独立指定现在时 | 不独立指定过去时；是否完成、何时发生要结合语境 |')
    change(25, '| 语态 | 主动 | 被动 |', '| 常见关系 | 与所说明对象通常为主动关系 | 常为被动关系或状态；如 fallen leaves（落叶）表落下后的状态，不是“被落下” |')
    change(25, '- 及物动词的过去分词表被动，不及物动词的过去分词只表完成（a fallen leaf 落叶，无被动含义）。', '- 及物动词的过去分词常表示被动关系或状态；不及物动词分词如 a fallen leaf（落叶）可说明落下后的状态，没有“被落下”的意思。不要把所有 done 都套成“被动＋已经”。')
    change(25, '- -ing 主语多为物，-ed 主语多为人。', '- 以 interesting／interested 为例，要看“令人感兴趣”还是“感到兴趣”：an interesting teacher（有趣的老师）也可用 -ing。先判断意思，不按人或物机械选词尾。')
    before(25, '### 难点一：不定式 vs 动名词作宾语', '''#### 两组对照：形式名称不替你决定时间

1. **the people living here**＝住在这里的人；living 修饰 people，说明居住情况，不必理解成此刻正在进行某个临时动作。live＝居住。
2. **Seen from here, the school looks small.** 从这里看，学校显得小。seen 表示学校是被看的对象；这里没有说“过去已经看完了学校”。

实际判断顺序：**修饰谁 → 谁做或谁承受 → 句子在说什么时候、什么状态**。分词可以带自己的宾语、介词短语等；整组内容仍能一起修饰一个对象。

''')
    change(25, '| remember/forget/regret + to do | 记得/忘记/遗憾去做（还没做） |', '''| remember／forget + to do | 记住／忘记要做的事；是否实际完成还要看整句 |
| regret to say／tell／inform | 遗憾地说／告诉／通知，常用于告知坏消息 |''')
    change(25, '| remember/forget/regret + doing | 记得/忘记/后悔做过（已做） |', '''| remember／forget + doing | 记得／忘了做过的事 |
| regret + doing | 对做某事感到后悔 |''')
    change(25, '- 动名词作主语时谓语用单数：Swimming **is** good for you.；', '- 一个动名词短语作主语时通常用单数：Swimming **is** good for you；and 连接两个不同活动作主语时通常用复数：Reading and swimming **are** useful.＝阅读和游泳都有益。不要把“一个活动”推广成全部并列结构。')
    change(25, '- 有些动词后只能接动名词：enjoy、finish、mind、avoid、practice、keep、suggest。', '- 本章比较动词后接另一项动作时，enjoy、finish、mind、avoid、practice、keep、suggest 等常接 -ing，不能机械换成 to do；这不表示这些动词后不能有名词宾语、从句等其他搭配。')
    before(25, '### 就地练习：区分动词、分句和非谓语', '''#### remember 与 regret 不共用一条时间口诀

**I remembered to lock the door.** 我记得去锁门，而且锁了。这里 remembered 已是过去式，不能把 to lock 一概解释为“这件事还没做”。

**I regret to tell you that he is ill.** 很遗憾地告诉你，他病了。说话人正在告知这一消息；tell＝告诉，ill＝生病的。对照 **I regret telling him.**＝我后悔告诉过他。前者是遗憾地告知，后者是对告知这件事后悔。

''')

    # 17、25、26：see/make 等的常见被动，不能推广到 let/have 的所有使役结构。
    change(17, '感官/使役动词后作宾补的不定式，主动不带 to，**被动要还原 to**：', 'see／hear／make 等的这类结构，主动宾补用不带 to 的原形，常见被动改用 to 不定式（不是所有使役词都能这样转换）：')
    for n, old in [(25, '- 被动语态中，不带 to 的不定式**要还原 to**：He was seen to enter the room.；'), (26, '- 被动语态中，不带 to 的不定式要还原 to，如 He was seen to enter the room。')]:
        change(n, old, '- see／hear／make 等常见被动用 to 不定式，如 He was seen to enter the room（有人看见他进入房间）、He was made to wait（他被迫等待）。这不是所有原形宾补都能照搬的变换；表示允许的 let 通常改用 be allowed to do，have sb do 不机械变成 be had to do。allow＝允许，allowed 是它的过去分词。')

    # 26：一般式、完成式、被动形式分别解释，区分分词和动名词的 being done。
    change(26, '| to do | 未做 / 将做 |', '| to do | 不定式一般式，本身不固定表示将来；时间结合谓语和语境判断 |')
    change(26, '| to have done | 已完成 |', '| to have done | 不定式完成式，通常表示相对于主要参照时间更早，不等于独立过去时 |')
    change(26, '| to be done | 将被做（被动） |', '| to be done | 不定式一般式的被动；是否将来发生仍看语境 |')
    change(26, '| doing | 主动进行 |', '| doing | 作分词时通常为主动关系；作动名词时表达活动内容，不自动表示正在 |')
    change(26, '| being done | 被动进行 |', '| being done | -ing 的被动形式；分词修饰语中常强调正在被做，动名词中不必如此 |')
    before(26, '### 难点三：主动表被动', '''#### being done：先区分是在修饰，还是在说一项活动

**the house being built now**＝现在正在建造的房子。being built 修饰 house，now 明确给出此刻正在被建造的背景。

**She likes being invited.**＝她喜欢受到邀请（invite＝邀请，invited＝其过去分词）。being invited 整体是 likes 的宾语，表达她喜欢的一类经历，不表示说话时有人正在邀请她。

所以 being done 不应在所有位置都固定译为“正在被……”。先判断整组内容的工作，再判断被动关系和时间。

''')
    change(26, '**通俗定义**：表主动、进行的含义，可作定语、状语、补语。', '**通俗定义**：现在分词可作定语、状语、补语，通常表示主动关系；它不独立表示现在时，也不总是进行中的动作。')
    change(26, '**核心规则**：和逻辑主语之间是主动关系，动作正在进行。', '**核心规则**：先确定它说明的对象及主动关系；一般情况、同时发生、原因、结果等具体关系看整句，不能仅由 doing 推出“正在”。')
    change(26, '**通俗定义**：表被动、完成的含义，可作定语、状语、补语。', '**通俗定义**：过去分词可作定语、状语、补语，常表示被动关系或状态；部分用法有完成含义，但形式名称不等于过去时。')
    change(26, '**核心规则**：和逻辑主语之间是被动关系，动作已经完成。', '**核心规则**：常见及物动词分词先看被动关系，也要识别状态；不及物动词分词如 fallen（落下的）不表示被动，是否完成和实际时间另看语境。')
    change(26, '- 及物动词的过去分词才表被动，不及物动词的过去分词只表完成。', '- 及物动词的过去分词常表示被动关系或状态；不及物动词的过去分词如 fallen 常说明完成后的状态，不要把所有分词都硬套成“被动＋已经”。')
    change(26, '1. 不定式：to do（未做）→ to be doing（正在）→ to have done（已完成）→ to be done（被动）→ to have been done（被动完成）；', '1. 不定式有一般式 to do、进行式 to be doing、完成式 to have done；被动可用 to be done、to have been done。它们是形式对照，不是从“未做”一路变成“做完”的时间流水线；')
    change(26, '2. 动名词/现在分词：doing → being done（被动进行）→ having done（主动完成）→ having been done（被动完成）；', '2. 动名词／现在分词可有 doing、being done（被动）、having done（完成）、having been done（完成被动）等形式；being done 作动名词时不必表示正在，先看结构用途；')
    change(26, '| 不定式 to do | 主语/宾语/定语/状语/补语 | 表目的、未做、具体一次 |', '| 不定式 to do | 主语/宾语/表语/定语/状语/补语 | 常见于愿望、目的等，也可表示当下或一般活动，不自带将来时 |')
    change(26, '| 现在分词 doing | 定语/状语/补语 | 主动、进行、"令人…" |', '| 现在分词 doing | 定语/状语/补语 | 通常为主动关系；进行、一般情况等含义看语境，不机械译“正在” |')
    change(26, '| 过去分词 done | 定语/状语/补语 | 被动、完成、"感到…" |', '| 过去分词 done | 定语/状语/补语 | 常表被动或状态，部分表完成，不自动表示过去或已经 |')
    change(26, '| 感官/使役 | see/watch/make/let/have + 宾语 + 原形（被动还原 to） |', '| 感官/使役 | see／hear／make 等常见被动用 to 不定式；let／have 不能统一套用这个转换 |')
    change(26, '| 只能接 doing |', '| 本课常见 doing 搭配 |')
    change(26, '| 只能接 to do |', '| 本课常见 to do 搭配 |')
    change(26, '- 动名词作主语时谓语动词用单数。', '- 一个动名词短语作主语通常用单数；and 连接两个不同活动作主语通常用复数，如本章案例中的 Walking ... and listening ... are good habits。先判断是一项活动，还是两个并列活动。')
    change(26, '**现在分词和动名词形式都是 doing，但功能不同：动名词表名词性，现在分词表形容词性。**', '**现在分词和动名词形式都是 doing，先看它们的工作：动名词可把活动作为主语、宾语等；现在分词可修饰名词、补充说明对象或说明动作背景，不只作形容词式的修饰。**')
    change(26, '**通俗定义**：现在分词和动名词形式都是 doing，但功能不同：动名词表名词性，现在分词表形容词性。', '**通俗定义**：同样写作 doing，动名词把活动作为主语、宾语等；现在分词作修饰语、状语或补语。先看整组内容在句中的功能。')
    change(26, '- 判断方法：能替换成名词的是动名词，能替换成形容词的是现在分词。', '- 先判断整组 -ing 内容是否把活动作为主语／宾语，还是在修饰名词、交代背景、补充对象；不要仅凭“能否替换成某个词”决定类别。本章 Reading is my hobby 与 the sleeping baby 是两种清楚的对照。')
    change(26, '- 不定式：to learn、to practice、to remember', '- 不定式：to learn、to practice；remember 在 helps you remember 中是不带 to 的不定式，原句没有 to remember')
    change(26, '- 动名词：reading、listening（×2）、making、trying', '- 动名词：Reading、listening（×2）、Walking、making、trying；Walking in the morning 整体参与构成主语，不是这里的分词状语')
    change(26, '1. 表目的用不定式（to learn、to practice）；', '1. To learn English well 说明目的；to practice 是 need 后的不定式宾语，不能因为有 to 就都标成目的状语；')
    change(26, '2. 介词后接动名词（be afraid of making、enjoy listening）；', '2. be afraid of making 中 of 是介词；enjoy listening 中 enjoy 是动词，listening 作它的宾语。两种结构都用 -ing，但理由不同；')
    change(26, '17. broken（过去分词表被动完成）', '17. broken（在本句中说明杯子破碎的状态，不能仅凭过去分词就另加过去时间）')
    for old in ['3. 不定式作定语时，与被修饰名词有动宾关系需加介词：a house to live in。', '3. 不定式作定语时，与被修饰名词存在动宾关系需加介词：a house to live in；']:
        change(26, old, '3. 不定式作定语时，按动词与被修饰名词的关系保留必要介词：a house to live in 中 live 不直接接 house，需 in；a book to read 中 read 可直接接 book，不另加介词；')
    change(26, '1. remember/forget/regret + to do：记得/忘记/遗憾去做（还没做）；', '1. remember／forget + to do：记住／忘记要做的事；regret to say／tell／inform：遗憾地告知，不能合并成“都还没做”；')
    change(26, '2. remember/forget/regret + doing：记得/忘记/后悔做过（已做）；', '2. remember／forget + doing：记得／忘了做过的事；regret doing：对做某事感到后悔；')
    return bodies


def repair_bank(seeds, checks, extra):
    """保留原1256项任务，另加22项本章内的基础规则辨析。"""
    extra[20] = [
        ('无论', '翻译：Whether it is hot or cold, I will go out.（hot＝热的；cold＝冷的）', '无论天气热还是冷，我都会出去。两种情况都不改变主句结论。'),
        ('两种情况', '按“无论下不下雨”补全：Whether it rains ___, we will go out.', 'or not；补出不下雨这一种情况，不是说要先确定是否下雨。'),
        ('重复内容', 'Whether you are at home or at school中的or后没有再写you are，完整说法是什么？', 'Whether you are at home or you are at school；相同内容没有重复，不改变“无论”的意思。'),
        ('unless否定', 'Unless you hurry, you will be late中，若无故把hurry改成do not hurry，意思还一样吗？', '不一样。原句是“除非赶快，否则迟到”；加not会把例外条件变成“不赶快”，不能重复添加否定。'),
        ('not的真实含义', 'We will go out unless you are not ready.中的not是否必须删掉？（ready＝准备好的；原意为除非你还没准备好）', '不必删；not ready正是原意所需的否定条件。unless后并非在所有语境都禁止not。'),
        ('独立表达', '用whether ... or not写“无论天气冷不冷，我都会读书”，提供it／is／cold／I／will／read。', 'Whether it is cold or not, I will read.；两种天气情况下都会读书。'),
    ]
    extra[21] = [
        ('位置辨析', "I don't know if he is at home or not.中的if一定错误吗？", '不错误；or not位于从句末尾，普通是否宾语从句可用if，也可用whether。'),
        ('紧邻or not', "修正：I don't know if or not he is at home.（保留or not的紧邻位置）", "I don't know whether or not he is at home.；这个位置用whether or not。"),
        ('功能辨析', "I don't know whether he is at home与Whether he is at home or not, I will call him中的whether意思相同吗？", '前句询问是否在家，内容作know的宾语；后句表示无论在不在家都打电话，是状语。'),
        ('是否与条件', '翻译并区分：I wonder if he is at home.／If he is at home, I will call him.（wonder＝想知道）', '我想知道他是否在家。／如果他在家，我就给他打电话。前句表达是否内容，后句提出条件。'),
    ]
    extra[25] = [
        ('不定式时间', '双方此刻已经见面：I am happy to see you.中的to see是否必定表示将来才见？', '不是；这句是“见到你很开心”，时间来自当前情境，不由to see自动指定。'),
        ('分词时间', 'the people living here必须译成“此刻正在临时住这里的人”吗？（live＝居住）', '不必；可译“住在这里的人”，living说明居住情况，不能仅凭-ing就认定临时或正在。'),
        ('过去分词', 'Seen from here, the school looks small.能否仅凭seen断定说的是过去已看完？', '不能；seen表示学校是被看的对象，整句是“从这里看，学校显得小”，并未另给过去时间。'),
        ('人和词尾', 'an interesting teacher能否因为teacher是人就判错？（interesting＝有趣的）', '不能；这是“有趣的老师”，描述令人感兴趣的特点。interested则描述感到兴趣，不能按人或物机械选词尾。'),
        ('remember时间', 'I remembered to lock the door.是否一定表示门还没锁？', '不是；通常表示当时记得去锁门，而且锁了。to lock不能脱离remembered的过去语境硬解释成仍未做。'),
        ('regret含义', '翻译并区分：I regret to tell you that he is ill.／I regret telling him.（ill＝生病的）', '很遗憾地告诉你，他病了。／我后悔告诉过他。前句在遗憾地告知消息，后句对告知这件事后悔。'),
    ]
    extra[26] = [
        ('被动动名词', 'She likes being invited.是否表示说话时她正在被邀请？（invite＝邀请）', '不一定；being invited整体作likes的宾语，说她喜欢受到邀请这类经历，不自带正在的含义。'),
        ('形式与时间', 'to do、to be doing、to have done是否是每个动作依次必须经历的三步？', '不是；这是形式对照，分别表达一般、进行、完成等观察方式；须按句中用途和相对时间选用。'),
        ('介词必要性', 'a book to read与a house to live in为什么只有后者有in？', 'read可直接以book作对象；live不直接接house，居住与房子的地点关系需in表达，不能见不定式定语就一律加介词。'),
        ('标注纠错', 'Reading aloud helps you remember words.中是否实际出现了to remember？（aloud＝大声地）', '没有；remember是不带to的不定式，help sb do是本章已给搭配；不能在原句标注中凭空补出to。'),
        ('搭配分类', 'enjoy listening与be afraid of making中，enjoy和of都是介词吗？', '不是；enjoy是动词，listening作其宾语；of是介词，making位于介词后，两者用-ing的结构理由不同。'),
        ('被动转换边界', 'see／make的常见被动会带to，是否所有let／have＋宾语＋原形都能机械变成be let／be had＋to do？', '不能统一套用；表示允许的let通常换成be allowed to do；have sb do不机械变成be had to do。'),
    ]

