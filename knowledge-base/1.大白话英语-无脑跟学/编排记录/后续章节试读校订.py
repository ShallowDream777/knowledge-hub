"""第7—31章及考试强化的顺序试读校订；仅替换登记过的片段。"""
from pathlib import Path
import re,json,hashlib
RECORD=Path(__file__).resolve().parent
VAULT=RECORD.parents[1]
CHANGES=[]
QUIZ_CHANGES=[
    ('基础',10,'介词状语','介词短语作表语'),
    ('考试',5,'最后一句还存在时间形式错误。','The office closes yesterday把一般现在时closes与已结束的yesterday相配，时间形式也不合适。'),
    ('考试',15,'首项覆盖整个转向','正确标题覆盖整个转向'),
]

def revise_quiz(text,n,course='基础'):
    for kind,chapter,old,new in QUIZ_CHANGES:
        if kind==course and chapter==n:text=text.replace(old,new)
    return text
def add(n,old,new,reason,course='基础'):
    CHANGES.append({'资料':course,'章':n,'原文':old,'新文':new,'原因':reason})

add(7,'**核心规则**：\n1. 常见结构：动词+介词','先认识下文的名称：**及物**表示这个用法直接带宾语，例如turn on the light（打开灯），the light是对象；**不及物**表示这个用法不直接带宾语，例如get up（起床）。**可分**指某些结构能把宾语放在两个词中间：turn the light on；**不可分**如look after the child（照顾孩子），不能写look the child after。不是凭字面猜能不能拆，要随具体搭配记。\n\n**核心规则**：\n1. 常见结构：动词+介词','先解释及物、可分，再用术语分类')
add(7,'不可分结构则放后面，如 look after him，如 pick it up，不能说 pick up it。','不可分结构则放后面，如look after him；pick up属于可分结构，所以用pick it up，不写pick up it。','复盘错误串联了可分和不可分示例')
add(7,'good **at** 不能说 good in；arrive **at/in** 不能说 arrive to。','表达“擅长……”本章使用good at，如good at math；到达城市用arrive in Beijing，到达车站用arrive at the station，不写arrive to。','给具体语义和地点尺度，不让读者猜at/in')
add(8,'**基数词（cardinal numbers）表示数量，回答"How many"的问题。**','**基数词（cardinal numbers）表示数量，回答“How many（多少个）”的问题。**\n\n先用这张表认识基本写法，后面的组合都从这里取词：\n\n| 数量 | 英语 | 数量 | 英语 |\n|---|---|---|---|\n| 0 | zero | 11 | eleven |\n| 1 | one | 12 | twelve |\n| 2 | two | 13 | thirteen |\n| 3 | three | 14 | fourteen |\n| 4 | four | 15 | fifteen |\n| 5 | five | 16 | sixteen |\n| 6 | six | 17 | seventeen |\n| 7 | seven | 18 | eighteen |\n| 8 | eight | 19 | nineteen |\n| 9 | nine | 20 | twenty |\n| 10 | ten | 30 | thirty |\n\n整十还有forty（40，注意不是fourty）、fifty（50）、sixty（60）、seventy（70）、eighty（80）、ninety（90）；hundred＝百，thousand＝千，million＝百万。','要求记忆基本数字前提供实际词表')
add(8,'2. 21 以上由"几十 + 个位"组成，中间加连字符：twenty-one、thirty-five；','2. 21—99中非整十的数由“几十+个位”组成，中间加连字符：twenty-one、thirty-five；连字符是单词中间的短横线-。一百以上继续组合，如one hundred and twenty-one（121）；','修正所有21以上都只两段组合的误导')
add(8,'1. 基本基数词 one—twenty 需逐个记忆，21 以上由几十+个位组成，中间加连字符，如 twenty-one；','1. 基本基数词one—twenty见本章前面的词表；21—99中非整十的数把几十与个位用连字符相接，如twenty-one；','复盘与正文范围一致')
add(8,'| 基数词 | one、two...；21+ 加连字符 twenty-one |','| 基数词 | 21—99的非整十数连接几十和个位：twenty-one；更大的数继续组合 |','速查不把21+变成所有数的规则')
add(8,'- "一倍"用 once，"两倍"用 twice，三倍以上用 three times。','- once表示“一次”，不把它直接当作比较中“一倍”的通用写法；两次／两倍常用twice，三次／三倍用three times。表示与另一对象一样重，用as heavy as；表示三倍重，用three times as heavy as。','区别次数与倍数，防止once机械代入比较')
add(8,'| 倍数 + 比较级 + than | This room is three times bigger than that one. |','| 倍数 + 比较级 + than（理解时留意歧义） | three times bigger than有不同理解；要明确“是三倍大”，本章优先用three times as big as。 |','不让歧义表达承担最初的数学对应')
add(8,'2. 倍数 + 比较级 + than：This room is three times bigger than that one.；','2. 倍数+比较级+than的表达可能有歧义；准确表达“是三倍大”时用three times as big as；','复盘保留识读信息但明确输出选择')
add(8,'3. 序数词前一般加 the。','3. 序数词前一般加the。first／second／third常缩写为1st／2nd／3rd；其他常用序号如4th、5th、12th、20th。日期March 5th中的5th读fifth（第五）；','日期缩写在使用前有解释')
add(8,'**时刻**：','**时刻**：past在报时中表示“过了”，to表示“差……到下一整点”；a quarter是一刻钟（15分钟），half an hour是半小时（30分钟）。也可以直接依次读小时和分钟，如eight ten（8:10）。\n\n**时刻**：','先解释报时里的past/to和quarter')
add(8,'**易错误区**：\n- 分子大于 1，分母加 s：','**百分数和小数**：percent表示“百分之”，50%写fifty percent；2.05写two point zero five，小数点后的0也要逐位读出。\n\n**易错误区**：\n- 分子大于 1，分母加 s：','百分数第一次主讲处补写法，而非等归纳才出现')
add(9,'**通俗定义**：后面必须直接接宾语，意思才完整的动词。','**通俗定义**：及物用法直接带宾语，中间不靠介词连接，如read a book。分类看当前用法，同一个词可兼有不及物用法：I read every day（我每天阅读）不必把read后没有宾语一律判错。','区分词与句中用法，避免绝对必须')
add(9,'- 及物动词后面**必须**有宾语，不能说 I like.；','- 本章like表达“喜欢某人／某物”时，要交代对象，如I like music；不能因此推断所有词在所有语境都必须明写宾语；','使规则与可省略对象的用法不冲突')
add(9,'- 区分双及物和复杂及物：宾语和后面成分能加 is 构成通顺句子的是复杂及物（宾补），否则是双及物（双宾语）；','- 看后面一部分是否说明前面宾语的身份、状态或动作：make him happy中happy说明him；ask him to leave中leave是him要做的动作。give him a book则是给他一本书。能否加is只适合部分名词／形容词例子，不能作为通用判断法；','消除宾补一定能加is的错误算法')
add(9,'- 主动语态的宾补变被动语态后就成主补：He was made monitor.','- We made him monitor意为“我们选他当班长”，monitor说明宾语him。He was made monitor意为“他被选为班长”，monitor转而说明主语He，因此叫主语补足语（简称主补）。此处先看它说明谁，被动句变换在第17章学习。','主补第一次出现给含义与操作边界')
add(9,'**核心规则**：be、do、have 既可以作助动词，也可以作实义动词。','**核心规则**：按本书分类，be在I am a student中作系动词，在is reading中作助动词；do、have则既可有实义用法，也可有助动词用法。','同章分类口径一致')
add(9,'| 动词 | 作助动词 | 作实义动词 |','| 动词 | 作助动词 | 其他用法 |','表格不把系动词并入实义分类')
add(9,'| be | 构成进行时/被动 | 是：I am a student. |','| be | 构成进行时/被动 | 系动词：I am a student. 我是学生。 |','明确be例句身份')
add(9,'- 情态动词不能单独作谓语，后面必须跟实义动词原形；','- 完整情态表达后接动词原形，也可以是be：She can be a teacher（她可以当老师）。上下文明确时简答可省略后面内容：Can you swim? Yes, I can.（你会游泳吗？是的，我会。）','避免与下章简答冲突，be同样可跟情态词')
add(10,'1. 简单谓语：单个限定动词，如 He **runs**.；','1. 简单谓语：单个限定动词，如He **runs**。这里“限定”指动词形式受句子的时态、人称等约束，例如I run、he runs、he ran（他跑了）；不是说这个动词被加了定语；','首次用限定动词前就地解释')
add(10,'一句话记住：**英语句子 = 主语 + 谓语（这是所有句子的骨架）。**','先用“主语+谓语”分析普通完整陈述句；下一章的祈使句可以不明写主语，不能把这个起步框架当作所有表达的唯一形式。','不让口诀与紧随的例外冲突')
add(10,'**易错误区**：只有系动词后面才有表语，实义动词后面是宾语。','**易错误区**：系动词后的表语说明主语；实义动词后可能有宾语，也可能有状语或补足语，不能只凭“在动词后”判断。','不把runs fast里的副词判成宾语')
add(10,'- 只有系动词后面才有表语，实义动词后面是宾语。','- 系动词后的表语说明主语；实义动词后的成分要看具体工作，不能一律当宾语，如runs fast中的fast是状语。','复盘纠正同一概括')
add(10,'- 主系表（SVP）和主谓宾（SVO）最易混：系动词后是表语，实义动词后是宾语；','- 主系表的表语说明主语，主谓宾的宾语是动词所涉及的对象；对照She is a teacher（她是老师）与She likes a teacher（她喜欢一位老师）；','用意义和例句而非动词后的位置判断')
add(10,'**核心规则**：\n\n| 句型   |','字母只是成分标签：S＝主语，V＝动词，P＝表语，O＝宾语，I＝间接宾语，C＝补足语。例如SVO把主语、动词、宾语按顺序列出；SVIO里I为间接宾语，O为直接宾语。\n\n**核心规则**：\n\n| 句型   |','解释整套句型字母标签')
add(10,'- 主补只出现在被动结构中，主动结构中没有主补。','- 本章用被动句说明宾补怎样转为说明主语的成分；这不表示一切语法体系中的主语补足成分都只存在于被动句。重点看它说明主语还是宾语。','收窄课程术语口径而非绝对断言')
add(10,'- 主补只出现在被动结构中。','- 本节先观察被动句里的主补，判断它补充说明的是哪个主语；不据此把其他结构一概排除。','去掉前段重复的绝对断言')
add(10,'宾语和后面成分能加 is 构成通顺句子的是宾补（He is monitor），否则是双宾语','后面成分说明宾语的身份、状态或动作，就是宾补；如He is monitor能帮助理解make him monitor，但不能把“能加is”套到ask him to leave等所有结构','修正正文中的宾补判断法')
add(10,'宾语和后面成分能加 is 构成通顺句子的是宾补，否则是双宾语','后面成分说明宾语的身份、状态或动作的是宾补；give me a book中的book则是给予的另一个对象。不能只靠加is判断所有结构','修正归纳中的宾补判断法')
add(10,'1. 动词+间接宾语+直接宾语 = 动词+直接宾语+to/for+间接宾语；','1. 对允许这种转换的搭配：动词+间接宾语+直接宾语，可改成动词+直接宾语+to/for+介词宾语；加了介词后按本书口径叫介词宾语；','与第9章术语一致')
add(11,'对普通动作句，I like tea的否定是I do not like tea，提问是Do you like tea?；','对普通动作句，I like tea的否定是I do not like tea；保持主语I的语法变换是Do I like tea?，实际询问对方时才把I换成you：Do you like tea?（你喜欢茶吗？）；','不把问句构造误教成必须改变人称')
add(11,'**易错误区**：形容词后直接加名词用 what，形容词后没名词用 how。','**易错误区**：先分清要强调的整体：What a beautiful flower!强调名词短语；How beautiful the flower is!强调beautiful。另有How beautiful a flower it is!（多漂亮的一朵花！），其顺序是How+形容词+a/an+单数名词+主语+动词；不能只靠“后面有无名词”猜what/how。','正文补自测18的结构并撤掉错误口诀')
add(11,'- 形容词后直接加名词用 what，形容词后没名词用 how；','- What a beautiful flower!与How beautiful the flower is!结构不同；也有How beautiful a flower it is!，不要只数后面是否有名词；','归纳保持与题目一致')
add(11,'**核心规则**：前肯后否，前否后肯；前后人称时态保持一致。','**核心规则**：本章练“前肯后否、前否后肯”的常见附加问句。先找前句的be／情态动词；普通动作句借do／does／did，再选与主语对应的代词：She is tired, isn’t she?；She isn’t tired, is she?；He likes tea, doesn’t he?；He doesn’t like tea, does he?。四句分别表示确认“她累／她不累／他喜欢茶／他不喜欢茶”。','补反意问句实际构造步骤')
add(11,'**易错误区**：Let\'s 包括说话人，反义疑问用 shall we；Let us 不包括对方，用 will you。','**易错误区**：Let’s go表示“我们一起走吧”，常接shall we?；Let us go若表示向对方请求“让我们走”，常接will you?。区别在具体用意，不能把Let us在所有语境都解释成排除听话人。','按语用解释而非缩写形式决定包括谁')
add(11,'- Let\'s 包括说话人，反义疑问用 shall we；Let us 不包括对方，用 will you。','- Let’s提出共同建议时常接shall we?；Let us表示请求对方允许我们做某事时常接will you?，按用意区分。','归纳与正文一致')
add(11,'**核心规则**：有且只有一个限定动词作谓语，结构简单完整。','**核心规则**：简单句只有一个独立分句，可以有并列主语或并列谓语，如Tom reads and writes（汤姆读书和写字）。不能数到两个动词就断定它是两个句子。','纠正与前章冲突的动词计数法')
add(11,'3. 否定句：There be + not；疑问句：Be there...?','3. 以There is a book为例：否定There is not a book；疑问Is there a book?；肯定简答Yes, there is，否定简答No, there isn’t。主语位置保留there，不换成it。','直接示范存在句简答，支持C08')
add(11,'1. 时态变化：There was/were、There has been、There will be；','1. 先按整组意义识读：There was/were（过去有）、There has been（到现在为止有过）、There will be（将会有）；本章只独立练已经演示的is/are与will be；','提前列出的扩展形式配义')
add(11,'2. 情态动词：There must be、There may be、There used to be；','2. There must be（一定有）、There may be（可能有）；There used to be表示“过去曾有、现在通常没有了”，used to是特殊习惯表达；','used to不笼统归为普通情态动词')
add(11,'3. 扩展结构：There seem(s) to be、There happen(s) to be。','3. 扩展结构先认整组含义：There seems to be a problem（似乎有个问题）；There happens to be a seat（碰巧有个座位）。seems／happens随后面单数对象搭配，本章不要求自行推导全部形式。','不给裸公式让读者硬猜')
add(12,'一句话记住：**单数主语配单数谓语，复数主语配复数谓语。**','先找主语，再按人称与数量选动词形式：he is、they are；I am、you are按已学搭配。后文“单数谓语／复数谓语”是搭配的简称，不是让动词表示一个／多个动作。','口诀保留I/you例外')
add(12,'**核心规则**：适用于 There be 句型、either...or、neither...nor、not only...but also。','先读懂连接词组：either A or B＝A或B中的一个；neither A nor B＝A和B都不；not only A but also B＝不但A而且B；both A and B＝A和B两者都。\n\n**核心规则**：本章的There be及either…or、neither…nor、not only…but also连接不同数量主语时，按靠近动词的主语搭配。例：Either Amy or I am wrong（不是艾米错，就是我错），靠近动词的是I，所以用am。','规则先说明连接词含义，支撑C06')
add(12,'**就远原则 = 谓语动词的单复数由离它远的"核心主语"决定，中间插入的成分不影响。**','**“就远”是这里的教学简称，实际操作是找核心主语，不是找距离最远的名词。** Tom with his friends中，Tom是核心，with his friends（和朋友们一起）是附带说明，所以用Tom … is。a pair of shoes（一双鞋）同样看中心词pair：一双用is，两双two pairs用are。','说明核心主语并补pair验收所需步骤')
add(12,'**核心规则**：适用于 with、together with、as well as、but、except、besides 等连接的结构。','**核心规则**：这里看附带短语前的核心主语。with／together with＝和……一起，as well as在此＝以及，except／but在这些搭配中＝除……之外，besides＝除……以外还。它们的附带用法与both…and连接两个并列主语不同。','不要求先懂第19章连接表达')
add(13,'- 现在分词拼写：去末尾不发音 e 加 ing（make→making）；重读闭音节双写末字母（run→running）；','- 常见-ing拼写：直接加ing（work→working）；去末尾不发音e再加ing（make→making），但see→seeing保留ee；lie→lying把ie改成y。run→running这类词，末尾重读且以一个元音字母加一个辅音字母收尾才双写，w/x/y通常除外；如read→reading、help→helping不双写。','把拼写条件写全，不只列术语')
add(13,'**结构公式**：have/has + 过去分词（done）','**结构公式**：have/has + 过去分词（done）。I/you/we/they用have，he/she/it或单数名词用has；这里是助动词，不另译“有”。been是be的过去分词，所以have been reading可拆成have + been + reading。','完成时组合落到已学be形式，不只给公式')
add(13,'  - I have been writing a book.（还在写）','  - I have been writing a book.（强调此前一直在写；可能仍在写，也可能刚停下来）','完成进行不必然仍在继续')
add(14,'- 规则动词过去式拼写：辅音+y 变 y 为 ied（study→studied）；重读闭音节双写末字母（stop→stopped）；','- 规则过去式：work→worked直接加ed，live→lived只加d，study→studied把辅音字母后的y改成i再加ed。stop→stopped的双写条件同前章：末尾重读、一个元音字母接一个辅音字母，w/x/y通常除外；help→helped不双写；','过去式复盘不缩回误导口诀')
add(14,'**核心规则**：必须有一个过去的时间或动作作参照（"到某时之前已完成"）。','**核心规则**：以过去的时间或动作为参照，再回看更早的情况。参照点可以在本句，也可以由前文建立；例如“我到车站”是较晚的过去点，“火车开走”更早，因此写had left。','解释参照点可以来自前文')
add(15,'- will 表临时决定；be going to 表计划好或有迹象：','- 常见对比是will用于当场决定，be going to用于已有打算或眼前迹象；will也能表示预测、承诺等，不能说它只表示临时决定：','防止用单一中文标签决定所有将来表达')

add(16,'情态动词不能单独作谓语，后面必须跟实义动词原形','完整表达中，can/must等后接动词原形，也可以是be，如He may be tired；简短回答可省略已知内容，如Yes, I can','与已学简答、系表结构兼容')
add(16,'may 表请求时，**否定回答用 mustn\'t**（表禁止）','may表请求时，拒绝许可可用can’t或may not；mustn’t明确表示禁止','不把一种回答当成唯一答案')
add(16,"may 表请求时，否定回答用 mustn't，表禁止。","may表请求时，拒绝许可可用can’t／may not；mustn’t强调禁止。",'同步复盘')
add(16,"许可否定答用 mustn't；might 更不确定","拒绝许可可用can’t/may not；mustn’t表示禁止",'同步速查')
add(16,'might 表推测时可能性低于 may。','might可使语气更试探；may和might都能表达可能，不能按固定概率高低选择。','避免伪精确概率规则')
add(16,'表推测时 might 可能性低于 may','表推测时may和might都表示可能，具体把握程度看语境','同步复盘')
add(16,'（可能性较低）','（表示一种可能）','不将词直接映射固定概率')
add(16,'肯定推测语气从强到弱：**must > will > may > might**','must表示有根据的强推断；will可表示预测，may/might表示可能，不能把四者排成适用于所有语境的固定概率表','纠正排序')
add(16,'推测语气强弱：一定（must）> 应该（will）> 可能（may）> 也许（might）。','先区分有根据的强推断（must）、预测（will）与可能性（may/might），再看上下文，不用中文近义词排固定等级。','同步归纳')
add(16,'must 只能表肯定推测，**不能表否定推测**（否定用 can\'t）','表示“不可能是”用can’t be；不要把mustn’t的禁止义与推测混淆','撤去超出本节范围的绝对判断')
add(16,"must 不能用于否定推测，只能用 can't。","本课表达“不可能是”用can’t be，与mustn’t表示禁止分开。",'统一核心教学表达')
add(16,'| could have done | 本能够做而没做 | He could have won. |','| could have done | 可表示本有机会但未实现，也可推测过去可能发生 | He could have won（具体按语境判断）。 |','补完成情态的两种意义')
add(16,'should have done 带"后悔、责备"意味，与 should do（应该做）不同。','本组should have done表示本该做却没做；也可表示预期，如The train should have arrived by now（按理说火车此时应该到了），不能只见形式就认定没有发生。','说明解释取决于语境')
add(16,"Had better + 主语 + do...?","Had + 主语 + better + 动词原形...?（如Had we better leave?＝我们是不是最好离开？）",'纠正问句排列')
add(16,"不能说 hadn't better do","本课优先用had better not do，不把较少见的hadn’t better作为首轮输出目标",'不把低频变体判为不存在')
add(16,'征求对方意见只能用 Shall I/we，不能用 Will I/we','提出建议常说Shall I/we…?（要不要我／我们……？）；Will I/we…?常询问将来的情况，用意不同','按语用解释区别')
add(17,'1. **只有及物动词**才有被动语态；','1. 被动常对应带宾语的结构；某些动词加介词的固定搭配也可变被动：They look after the child → The child is looked after（孩子受到照顾），after仍须保留。不能反过来认为所有带宾语结构都自然使用被动；','补介词短语被动，与第7章一致')
add(17,'**核心规则**：把"be"换成对应时态，后面跟过去分词。','**核心规则**：被动的基本组合是be+过去分词，再按时间组织整组动词。being是be的-ing形式，been是be的过去分词：is being repaired＝正在被修，has been repaired＝已经修好。表中的written是write的过去分词。','解释公式中being/been来源')
add(17,'原主语变成 by + 宾语（可省略）','需要说明执行者时写by+原主语对应形式；代词用宾格，如they→by them（整个by短语可省略）','具体说明人称转换')
add(17,'没有人称主语时（如 They、People、We）','原主语泛指、不需交代具体执行者时（如泛指用法的They、People、We）','纠正主语说法')
add(17,'sth be given to/for sb','sth be given to sb（give搭配to；buy sth for sb则用for，不能随意互换）','give不能任换to/for')
add(17,'使役被动中过去分词不能省略 be 或变成 doing。','have sth done中本来没有额外的be：I had my car repaired（我请人修了车），repaired说明car被修。对照I have repaired my car（我已修好车），后一句的have紧接过去分词，才是现在完成时。','修正have sth done结构并与完成时对照')
add(17,'to read这样的“to＋动词原形”叫不定式；','感官动词在这里指see（看见）、hear（听见）等；使役动词表示让某人做某事，如make（使／迫使）。to read这样的“to＋动词原形”叫不定式；','术语先配含义')
add(18,'| 动词必在句 | 英语每个句子必须有动词 |','| 完整陈述句 | 本课普通完整陈述句围绕限定谓语组织；简答、感叹等可省略已知内容 |','不与已学简答冲突')
add(18,'| 及物动词 | 必须有宾语：like music |','| 及物用法 | 动词直接带宾语，如like music；同一个词也可能有不带宾语的用法 |','按用法而非永远词类判断')
add(18,'及物动词后面必须直接接宾语，意思才完整','及物用法指直接带宾语；同一个动词也可有不带宾语的用法，如I read every day（我每天阅读）','同步第9章')
add(18,'必须和实义动词搭配使用，不能单独作谓语。','助动词帮助组成动词结构；简答可省略已知部分，如Yes, I do。不把这种省略误判为缺动词。','承接已学简答')
add(18,'助动词后接动词原形或分词，不能接名词，不能单独作谓语。','助动词按搭配接原形或分词；be、do、have还可有其他用法，先看本句工作，不靠词形统一判定。','区分形式与用途')
add(18,'情态动词不能单独作谓语，后面必须跟实义动词原形。','can/must等在完整结构中接动词原形，也可接be；简答Yes, I can可省略前文已知动作。','同步第16章')
add(19,'but、however','but','并列连词表不混入连接性副词')
add(20,'时间参照与事件持续在第13章已有例子','时间参照与事件持续在第14章已有例子','修正先修章号')
add(20,'从句（clause）','从句（subordinate clause）','clause本身包含独立分句')
add(20,'while 强调一段时间内正在进行，从句必须用延续性动词','while在本节时间背景用法中常描述一段持续活动；其他对比、让步用法按实际句意理解','与本章开头保持一致')
add(20,'Not until 位于句首时主句要部分倒装。','Not until位于句首时，把主句的助动词移到主语前，这叫部分倒装：I didn’t sleep until midnight → Not until midnight did I sleep（我直到半夜才睡）；did承担过去形式，sleep用原形。第29章再归纳这类语序。','第一次使用倒装给实际操作')
add(20,'区分地点状语从句和定语从句：where 前没有地点名词就是状语从句。','按从句的工作区分：You can sit where you like说明坐在哪里；I know where he lives中的从句是know的内容，作宾语。不能只看where前有没有地点名词。','修正位置判断法')
add(20,'so that 引导目的状语从句，so...that 引导结果状语从句，不要混淆','so that常表示目的，也可说明结果；so…that表示“如此……以至于”。先问整句是在说想达到的目标，还是已经造成的后果','不把连接词与关系一一对应')
add(20,'名词前有 many/much/few/little 时用 so 不用 such','many/much/few/little表示数量时用so，如so little water；little表示“小”时另看名词短语，如such little children（这么小的孩子）','little区分数量与大小')
add(21,'1. 由 that、whether、连接代词、连接副词引导；','先看名称对应什么工作：what he said＝他说的话，what承担said的宾语，叫连接代词；where he lives＝他住在哪里，where说明地点，叫连接副词。that he is right中的that只连接，不顶替从句里的主语或宾语。\n\n1. 由that、whether，以及上述连接代词、连接副词引导；','解释连接代词与连接副词')
add(21,'3. 常用 it 作形式主语，把从句放句末。','3. 主语太长时可后移：That he will win is certain → It is certain that he will win（他会赢，这一点是确定的）。it先占主语位置，后面的从句说明真正内容，这叫形式主语；这里it不译成“它”。','形式主语先示范再命名')
add(21,'that 引导主语从句时不能省略，引导宾语从句时可以省略。','句首that主语从句保留that；普通动词后宾语从句的that常可省，如I think (that) you are right。不把这条套成所有位置的省略规则。','收窄省略条件')
add(21,'3. 主句过去时，从句用相应的过去时态（时态呼应）。','3. 过去转述常后移时态：He says he is tired → He said he was tired（他说他累了）。若内容仍成立或为普遍事实，也可保持现在形式；第23章完整说明。','后移不是机械强制')
add(21,'该类句子的反义疑问句，疑问部分与从句保持一致。','I/we表达当前想法时，附加问句常针对从句：I don’t think he is right, is he?；She doesn’t believe he will come, does she?则确认她的看法，不能一律跟从句。','明确附加问句适用范围')
add(21,'否定转移后的反义疑问句要用肯定形式反问从句内容。','本节I don’t think…的例子用肯定形式确认从句内容；更换主语和语境后，重新判断要确认哪一层意思。','同步归纳')
add(22,'| 可否省略关系词 | 作宾语可省 | 不能省 |','| 可否省略关系词 | 作宾语时常可省；前置介词后仍须保留 | 不能省 |','补省略条件')
add(22,'介词后面不能用 that 和 who，只能用 which 和 whom。','本节介词直接接指人／指物的关系代词时，用whom／which，不用that；另有in whose house（在其家中）这类whose带名词的结构，不能误读成介词后永远只有两个词。','收窄规则而不误伤whose结构')
add(23,'不能单独使用，必须有过去的语境作参照（主句是过去时，从句表"当时看来的将来"）','需要过去视角作参照；该参照可在本句，也可由前文提供，并不一定另带一个过去时主句','解释上下文参照')
add(23,'不能单独使用，必须有过去的语境作参照。','需要过去语境作参照，但参照可以来自前文，不一定写在同一句中。','同步复盘')
add(23,'瞬间动词不能和"一段时间"（for 3 days、since）连用，要换延续性表达。','表达买到后一直拥有等持续状态时，用have等相应状态表达；这不禁止次数统计或否定句，如I haven’t bought a book for a year（一年没买书）。','不把持续状态规则推广到所有for/since')
add(23,'| 瞬间动词 | 不能接 for/since，换延续性动词或 be |','| 持续状态 | 表达买后持续拥有用have等；次数统计、否定句等另按句意判断 |','同步速查')
add(23,'瞬间动词 buy 不能接 for，换 had → 现在完成时','本题表示买后一直拥有，用has had；不是所有buy与for组合都错','同步答案')
add(23,'主句为过去时态时，从句时态需相应调整为过去时态','过去转述常使用后移的时态；事实仍然成立或为普遍事实时，可根据表达视角保留现在形式','弱化机械后移')
add(23,'| 时态呼应 | 主句过去时 → 从句时态后退 |','| 时态呼应 | 过去转述常后移；仍成立的事实可按当前视角保留现在形式 |','同步速查')
add(23,'状态动词（know、love、belong）不能用于进行时态。','know、love、belong等在本课稳定状态意义下通常不用进行时；词义、语境改变时不能机械禁止全部进行形式。','与前章一致')
add(23,'无时间状语时不使用','时间参照也可由上下文提供，不必每句重复时间状语','去掉必须有标志词的误导')
add(23,'By next summer, she **would have been studying** here for 4 years. 到明年夏天，她在这里学习就满四年了。（过去视角）','She said that by the following summer she **would have been studying** there for 4 years. 她说，到翌年夏天，她在那里学习就满四年了。（said提供过去视角）','复杂形式示例补齐过去参照')
add(24,'each of the boys 可数，every boy 直接接名词','可说each of the boys（这些男孩中的每一个），不能说every of the boys；every boy中every直接限定单数名词','消除可数这一误导说法')
add(24,'**不可数名词不能用 one 代替，用 that**：不能 a tea and a coffee... 的 one','one/ones替代可数名词；替代不可数内容时可根据句意用it、some、that等，不能一律填that。a tea／a coffee表示一份饮品时已是可数用法','修正茶咖啡反例')
add(24,'不可数名词不能用 one 代替，要用 that','one不能替代不可数用法；具体用it、some还是比较中的that，要看句意','同步复盘')
add(24,'完整规则见《三大从句》专题，这里先认识这些词。','第21章已学名词性从句、第22章已学定语从句；这里按本句的工作辨认同一个词，不必另找专题文件。','去掉旧文件路由')
add(24,'前者不能引导名词性从句','这些名称是按所在结构区分的；同一个who可分别用于the person who came和I know who came，不能把词本身永久归进一类','词形相同而工作不同')
add(24,'不定代词作主语时，谓语动词一般用单数，如 Everyone is here。','everyone等复合不定代词、each等作主语用单数；both用复数，none接复数对象时可用单数或复数，如None of the answers is/are correct。','题22所需规则在做题前有说明')
add(24,'电话里介绍自己用 This is...，问对方用 Is that...，不能说 I am...。','电话中常用This is…介绍自己，Is that…?确认对方；这是常见表达，不是禁止其他自然的自我介绍。','不把语用偏好当禁令')
add(25,'what to do、how to do（相当于名词性从句）','what to do（做什么）、how to do it（怎么做这件事）；do需要宾语时不能只写how to do','补完整搭配')
add(26,'what to do、how to do 等，相当于名词性从句','what to do（做什么）、how to do it（怎么做这件事）；do需要宾语时保留it','同步复盘')
add(26,'be worth 后面只能接 doing，不能接 to do','be worth后接动作时用doing，不换成to do；也可接名词或金额，如worth ten dollars（值十美元）','不禁止名词搭配')
add(26,'原解析中的 -ing 标注已改正','按感到兴趣和令人感兴趣区分','清除编辑历史')
add(26,'前面的名词和分词不是主谓结构，没有谓语动词','名词与分词有意思上的主谓关系，但没有限定谓语，不能当作独立完整句','独立主格的逻辑关系说明')
add(27,'不定式、动名词、从句作主语，谓语用单数','一个不定式／动名词活动或本节从句整体作主语通常用单数；并列不同活动可用复数，如Reading and swimming are useful','与25章并列活动一致')
add(27,'| 不定式/动名词/从句作主语 | 单数 |','| 不定式/动名词/从句作主语 | 本节单个整体通常用单数；并列不同活动另看结构 |','同步速查')
add(27,'一个句子一个主语，判断单复数后谓语跟着走。','逐个分句找主语，再判断其对应动词；主句和从句不一定共用同一个主语。','纠正句子与分句混淆')
add(27,'people、police、cattle 形式单数但意义复数','people、police、cattle不以-s结尾，但这些常见集合用法按复数搭配','不把无s说成单数形式')
add(28,'假设现在 → 时态退到现在过去','假设现在 → 用过去形式表达与现实的距离','消除无意义术语')
add(28,'**易错误区**：口语中 as if 后也可用真实语气（It looks as if it is going to rain），但正式表达多用虚拟。','**易错误区**：按说话者是否把内容当成真实可能来判断，不按正式／口语二分。It looks as if it is going to rain表示看来确实可能下雨；He talks as if he knew everything可暗示他其实并非全知。','虚拟选择不是文体选择')
add(28,'as if/as though 表"好像、仿佛"，其后常用虚拟语气（尤其在正式书面语中）。','as if/as though表示“好像、仿佛”；若把情况视为与现实有距离的假设，可用本节虚拟形式；真实可能按普通时态表达。','同步定义')
add(28,'与 4.3 方式状语从句的 as if 是同一知识点','与第20章方式状语从句的as if是同一知识点','清理旧编号')
add(29,'such a beautiful scenery','such beautiful scenery','scenery不可数')
add(29,'用"它 + be + 被强调部分 + that/who + 其余部分"来强调句子成分','用“It + is/was + 被强调部分 + that/who + 其余部分”突出信息；这里It是句型的一部分，不译成“它”','避免逐字误译')
add(29,'删去后 He came. 完整','去掉框架后保留yesterday并还原为He came yesterday，信息没有丢失','删去法应保留被强调部分')
add(29,'从句主语与主句主语相同时，可用 do/does/did 代替谓语','比较的动作相同时，可按时态用do/does/did承接；主语可以不同，如He runs faster than I do','规则与现成例句一致')
add(29,'1. 用于 here、there、out、in、up、down 等副词放句首时；','1. here、there、out等地点／方向表达置前，配合come、stand等合适动词时可用；并非任意句子都必须倒装；','不把触发条件说成一律')
add(29,'2. 用于地点介词短语放句首时；','2. 地点介词短语置前可用这种排列；也可正常说In Beijing, I work at a school，不能一见地点开头就倒装；','补正常语序反例')
add(29,'一句话记住：**能省就省，但省完不能让人看不懂。**','先按本节示例识别允许省略的位置，并确认上下文能补回具体内容；“读得懂”本身不足以允许随意删词。','不给随意省略指令')
add(29,'I like reading and my brother **likes** listening to music.（可省略重复谓语）','I like reading, and my brother (likes) listening to music. 我喜欢阅读，弟弟喜欢听音乐。括号内为可省部分；省后my brother仍是第二个分句的主语。','示范真正省掉哪部分')
add(30,'一句话记住：**会构词法 = 背一个词能推出好几个词，还能猜出生词意思。**','构词法能帮助识别词族、提出词义猜想；实际拼写、词性和意思仍要结合语境核对，不能按公式随意造词。','撤去过度承诺')
add(30,'**⭐ 记住"后缀→词性"，能秒判生词**（最实用）：','**常见后缀可提供词性线索，再结合句子确认：**','与正文限定一致')
add(30,'常见动词变名词的几组要记牢','常见词转为名词的几组要记牢','happy/kind不是动词')
add(30,'（更多构词例子已安排在本书构词法章）','（本章前面的词缀表可用于查阅）','不要把读者引回当前章的虚假后文')
add(30,'首字母缩写是否加 the 要看是否专有：the WHO 常有 the，但要看具体用法。','专有名称是否用the按惯用名称判断：常说the UN、the WHO，也说NASA，不能仅凭“专有名词”决定。','修正冠词判断')
add(31,'| 分号 ; | 连接两个完整句子 | 相当于"句号+和" |','| 分号 ; | 连接关系紧密的独立分句 | 标出句间边界；具体关系由内容决定，不必译成“和” |','分号不固定表示并列')
add(31,'2. 表转折：however、nevertheless、otherwise；','2. 表转折：however、nevertheless；otherwise在本节常表示“否则”，引出不满足前述条件时的结果；','补otherwise条件关系')
add(31,'book\'s 是"书的"','book’s可表示“书的”，在相应语境也可缩写book is／book has','与缩写规则一致')

add(2,'现在增加一层：Researchers found [that students [who explained a method to others] remembered it longer].','下面的方括号是拆句记号，不是原句标点；一对括号圈住一整组，内层括号表示这一组里面还有修饰内容。\n\n现在增加一层：Researchers found [that students [who explained a method to others] remembered it longer].','先解释课程记号','考试')
add(2,'真题拆解三：of 短语与主语核心','真题拆解三：两层定语从句与主语核心','标题与实际拆解对象一致','考试')
add(2,'如果儿童由这样的父母抚养——父母鼓励他们独立，并帮助他们理解行动与后果之间的联系——这些儿童往往会形成更成熟的内控倾向。','由这样的父母抚养的儿童往往有更成熟的内控倾向：这些父母鼓励孩子独立，并帮助他们理解行动与后果之间的联系。','保留限定对象而非新增条件句','考试')
add(2,'这里中文的“如果”用于顺畅表达对象条件；不能由此声称原文证明一种绝无例外的因果。','tended to表示观察到的倾向，不能译成所有儿童必然如此，也不能由本句断定因果已获证明。','跟随译文调整解释','考试')
add(3,'这一“通常与主句主语对应”的方法用于一般分词状语；with the work finished一类自带名词的结构另有自己的逻辑主体，不能删掉the work，硬说是主句的人被完成。','这一“通常与主句主语对应”的方法用于一般分词状语。with the work finished＝工作完成后／在工作已完成的情况下，可拆成with＋the work＋finished；finished说明work被完成，the work是这个小结构自己的主体，不是主句的人被完成。','把带with结构具体拆开','考试')
add(4,'NOT／EXCEPT题把选择任务反过来了。','题干中的NOT表示“不”，EXCEPT表示“除了……之外”。这类题要求选出不符合原文要求的一项，先读清具体排除什么，再判断选项。','考试指令先释义','考试')
add(4,'has done直接报告已发生的事情','本组肯定陈述中的has done直接报告已发生的事情；若外层另有否定或假设，还须合起来读','避免形式独断','考试')
add(6,'所以上调保护、限制接触','因此需要保护、限制接触','消除不自然中文','考试')
add(7,'颗粒合适的主题','概括范围合适的主题','改掉不必要术语','考试')
add(8,'Conversely，若文章明确介绍随机分组、控制条件等证据','反过来，若文章介绍随机分组（由随机方式分配参与者）、控制条件（尽量保持其他条件一致）等证据','去掉突兀英文并解释研究术语','考试')
add(9,'前章2023年felony题','第07章2023年felony题','回顾章号正确','考试')
add(12,'try and focus在这里连接尝试的行动','try and focus在这里是try to focus的常见表达，意为“尝试专注”；不能把它推广成所有try to都能随意改and','补不透明搭配解释','考试')
add(13,'that后的主语people [with positive social perceptions of their neighborhoods]','found后省略了连接词that；宾语从句的主语是people [with positive social perceptions of their neighborhoods]','不让读者找原句不存在的that','考试')
add(16,'练习末尾可以进入下一章。','练习末尾可返回本章安排复测。','最后一章无下一章','考试')

add(10,'区分看能否加 is：He is monitor（宾补）vs give me a book（双宾，不能说 me is a book）','区分要看关系：make him monitor中monitor说明him的身份，是宾补；give me a book中me是接受者、a book是所给物，是双宾语。加is只对部分身份／状态例子有帮助','去掉遗漏的错误口诀')
add(11,'| 句子骨架 | 主语 + 谓语，不可缺 |','| 普通完整陈述句的起步骨架 | 主语＋谓语；祈使句等可省已知主语 |','与本章祈使句一致')
add(11,'must/may/used to（情态动词）','must/may（情态动词）、used to（过去习惯表达）','分类保持一致')
add(16,'表"过去具体做到了某件事"，用 was/were able to，不用 could','普通肯定句叙述过去一次成功完成的行动，通常用was/were able to或managed to；could也可用于当时感知等，如I could see the sea（我当时看得见海），不是所有实际发生都禁止could','限定一次成功行动规则')
add(16,'过去能力用 could；真做到用 was able to','过去一般能力用could；普通肯定句叙述一次成功行动常用was able to','同步速查')
add(16,'be used to doing（现在习惯）','be used to doing（习惯于，时间由be的形式决定）','区别习惯表达与时态')
add(16,'be used to doing 表现在习惯','be used to doing表示习惯于，时间随be的形式变化','同步复盘')
add(16,'be used to doing 现在习惯','be used to doing习惯于，时间看be','同步表格')
add(16,'肯定：must>will>may>might','肯定推断must；预测will；可能may/might，不作固定概率排序','同步速查')
add(16,'肯定推测语气从强到弱：must > will > may > might','must表示有根据的强推断；will常表预测；may/might表可能，不按固定概率排序','同步复盘')
add(16,'will 表将来是助动词，表意愿是情态动词','will可表示将来预测，也可表示意愿；此处按具体意思区分，不必给同一个词硬分成互斥身份','避免分类造成额外负担')
add(16,'will 表将来时是助动词，表意愿是情态动词','will可表示将来预测或意愿，按本句意思识别；形式上都接原形','同步复盘')
add(18,'| 有无变化 | 有人称/时态/数变化 | 无 |','| 与主语和时间的关系 | 承担限定时态、语气或主谓一致；并非每个形式都变词尾 | 不随主语变人称与数，但可组成完成、被动等形式 |','非限定不是没有任何形式变化')
add(18,'| 非限定动词 | to do/doing/done，不作谓语 |','| 非限定动词 | to do/doing/done等不独立作限定谓语；也可参与is working这类组合 |','与进行结构一致')
add(18,'宾语和后面成分能加 is 构成通顺句子的是复杂及物（宾补），否则是双及物（双宾语）','后面成分说明宾语的身份、状态或动作时是宾补；如ask him to leave也有宾补，却不能靠加is判断。双宾语则有接受者等间接宾语与所给内容等直接宾语','修正动词复盘判断法')
add(24,'it 只代替单数名词，复数名词用 they','it可回指单数可数对象、不可数内容或前述情况；回指复数对象时，主语用they，宾语用them','涵盖已学指代用途')
add(24,'形容词性物主代词 always 后接名词','形容词性物主代词要与名词构成一组，中间可以有修饰语，如my new book','清除突兀英文并讲准确位置')
add(28,'主句和从句时态要对应，不能混搭错误。','先分别确定条件和结果的时间。本组示例都回看过去，所以配had done与would have done；若过去条件影响现在结果，后面的混合虚拟另有合法组合。','不提前否定后面的混合时间')
add(28,'| 时态后退 | 和现实相反就往后退一步 |','| 假设形式 | 先确定条件与结果各自的时间；建议要求等结构不套统一后退口诀 |','复盘不推翻开头')
add(31,'题目开头可返回本章，末尾可进入下一章。','题目开头可返回本章，末尾可返回学习目录安排复习。','末章无下一章')
add(11,'反义疑问','反意疑问','统一术语写法，避免同一章两种名称')
add(16,"否定是 had better not do，不是 hadn't better do。",'表达“最好不要……”时，本课使用had better not do：You had better not go（你最好不要去）。','给首轮明确可用的形式，不扩张为所有变体的禁令')
add(16,'否定要说 had better not do，本课优先用had better not do，不把较少见的hadn’t better作为首轮输出目标。','表达“最好不要……”时，本课使用had better not do：You had better not go（你最好不要去）。','去掉重复的否定说明')
add(17,'口语里也常说被动（My car was broken.）','口语里也常说被动（My bike was stolen＝我的自行车被偷了）','选用不易混成状态形容词的被动示例')
add(26,'把被动形式放进完整句：I enjoy being helped（我喜欢受到帮助），being helped整个是enjoy的宾语；这里没有说此刻正在受帮助。The child being helped now is Amy（现在正受到帮助的孩子是艾米）则由修饰关系和now确定当前过程。\n\n','','已有独立小节用房子与受邀例子讲清同一对照，撤掉重复追加的段落')

add(11,'| 否定疑问句 | 表惊讶/确认 | Don\'t you like music? |','| 否定疑问句 | 表惊讶/确认 | Don\'t you like music? |\n\n附加在句尾的反意疑问句这样构造：先找前句的be／情态动词；普通动作句借do／does／did，再选对应的主语代词。She is tired, isn’t she?＝她累了，对吗？He likes tea, doesn’t he?＝他喜欢茶，对吗？前句否定时，尾部通常肯定：He doesn’t like tea, does he?。下面have you的例子用到第13章完成时，本章只识别“前面是否定，尾部用肯定来确认”。','在首次示例后给操作方法，不等章末复盘才讲')
add(18,'| 能否作谓语 | ✅ 能 | ❌ 不能 |','| 能否独立承担限定谓语 | 能，如plays | 不能单独承担，但可参与is playing等谓语组合 |','表头与下方例句一致')
add(19,'3. 短语动词 look forward to + 动名词。','3. look forward to表示“期待”，本段接名词短语the summer holiday；接动作时用doing，如look forward to seeing you。','段落中实际是名词，不能标成动名词')
add(22,'| 作用 | 不可缺少，限制范围 | 补充说明，删去不影响 |','| 作用 | 限定所说对象；删去可能改变指称范围 | 对已确定对象补充信息；删去会损失这条信息，但通常仍能确定对象 |','区分句子完整、对象确定与信息是否损失')
add(23,'3. 状语从句：表时间（When）、条件（If），都满足"主将从现"。','3. When I was young回顾过去，用过去时；If I save enough money谈将来条件，用一般现在时配主句will。不能把所有时间、条件从句都套成“主将从现”。','观察结论须与本段两个真实例句一致')
add(23,'18. When ______ you ______ to Japan? (did, go / have, gone / do, go)','18. When ______ you ______ to Japan? (did, go / have, gone / do, go)（询问已经结束的那次日本之行的时间）','给过去时选择必要的时间语境')
add(23,'26. leaves（时刻表 → 一般现在时表将来）','26. leaves（every morning说明每天的固定安排，用一般现在时；本句本身没有指定某次将来行程）','答案不把日常安排强说成将来')
add(23,'重读闭音节双写末字母，如 run→running','末尾是单个元音字母加单个辅音字母、末音节重读时，通常双写末尾辅音，如run→running；w/x/y一般不双写','复盘保留拼写条件')
add(23,'重读闭音节双写末字母，如 stop→stopped','末尾是单个元音字母加单个辅音字母、末音节重读时，通常双写末尾辅音，如stop→stopped；w/x/y一般不双写','过去式拼写复盘保持条件')
add(28,'假设将来不太可能发生的事情，可能性很低。','把将来情况作为较疏远、试探性的假设提出；形式本身不给出确定的概率，具体可能性还要看语境。','虚拟形式不对应固定低概率')
add(28,'表示对将来不太可能发生的事情的假设，可能性很低。','把将来情况作为较疏远、试探性的假设提出；形式本身不给出确定的概率，具体可能性还要看语境。','复盘沿用语境判断')
add(29,'1. 否定词放句首：never、hardly、seldom、not only；','1. 否定或限制性状语置于句首，如never、hardly、seldom；not only修饰整个分句并置前时也用。否定主语不套用，如No one knows（没人知道）；','否定主语不会触发这种倒装')
add(29,'1. 否定词放句首（never、hardly、seldom、not only）；','1. 否定或限制性状语置于句首，如never、hardly、seldom；not only修饰整个分句并置前时也用。否定主语不套用，如No one knows（没人知道）；','复盘保留触发条件')
add(29,'2. 去掉后不完整 → 主语从句；','2. 去掉后不完整时，不能仅凭这一点定类；在下面It is a pity that…中，that从句是实际主语，it先占主语位置；','不能由排除强调句推出所有句子都是主语从句')
add(29,'2. 去掉后不完整的是主语从句；','2. 去掉后不完整时，再检查it是否是形式主语；下面It is a pity that…才是这种情况，不能把所有非强调结构都归成主语从句；','同步复盘判断边界')
add(29,'部分倒装还有几类特殊情形，包括让步倒装、so...that 倒装、虚拟条件句倒装等。','这里合看几类特殊排列：让步句可把表语等提前；so...that和虚拟条件句可把助动词等提前。让步句里的Child as he is没有把is放在he前，不把它与助动词倒装混成一种操作。','区分前置表语与助动词倒装')
add(29,'如果不定式里有 be 或 have，要保留 be/have','本节的省略句通常保留be；若have用于完成式，也通常保留have。不要把这个提示推广成所有实义have都必须保留','限定省略规则适用范围')
add(4,'若原来100后来200，doubled是变成两倍','占比的变化还要分清“百分点”和“相对增长率”：20%升到30%，两占比相减是增加10个百分点；相对原来的20%则增长(30−20)÷20＝50%。英文percentage points表示百分点，不能把这两种数字互换。\n\n若原来100后来200，doubled是变成两倍','在本章练习前先解释百分点','考试')

# 在首次用到的地方补操作示范；用独有锚句，不另造阅读分支。
INSERTIONS={
 (11,'基础'):('**核心规则**：\n1. 肯定祈使句','祈使句用来请求、命令、劝告对方做事：Open the door（请开门）。通常不明写you，开头用动词原形；不做某事用Don’t+原形，如Don’t run（不要跑）。'),
 (13,'基础'):('### 本章小结','完成时的否定和提问也从助动词下手：She has finished → She has not finished（她还没完成）→ Has she finished?（她完成了吗？）；回答Yes, she has／No, she hasn’t。has not可缩写hasn’t，have not可缩写haven’t，后面的过去分词不变。'),
 (15,'基础'):('#### 将来进行时','先把最常用的将来句变一遍：She will come → She will not come（她不会来）→ Will she come?（她会来吗？）；will not缩写won’t，简答Yes, she will／No, she won’t。She is going to study则否定is：She isn’t going to study；提问Is she going to study?。后面的study始终用原形。'),
 (19,'基础'):('### 本章小结','but与however都能表达“然而”，接句方式不同：I tried, but I failed（我尝试了，但失败了）；I tried. However, I failed。however是连接性副词，不能像but一样只靠逗号连接两个独立分句；第31章会系统练句间标点。'),
 (20,'基础'):('#### 九种状语从句对照','“让步”是先承认一个事实，再说结果仍与通常预期不同：Although he is young, he knows a lot＝虽然年轻，却懂得很多。“目的”说想达到什么，“结果”说实际造成什么；下面按这几种具体关系读例句。'),
 (21,'基础'):('### 本章小结','whether在介词后的例子：It depends on whether she agrees（这取决于她是否同意）。先认depend on（取决于），再把whether she agrees整个看作on后的内容；这里不用if替换whether。'),
 (22,'基础'):('### 本章小结','对照同一个名词：the factory where she works＝她工作的工厂，she works不缺工作对象，where补“在哪里”；the factory that she visited＝她参观的工厂，visit需要“参观什么”，that顶替这个对象。day也一样：the day when we met说明见面时间；the day that we spent together中，spent需要“度过什么”。先还原从句里的位置，再选关系词，不能看到地点就填where、时间就填when。'),
 (23,'基础'):('### 本章小结','转述时按实际指向决定人称、地点和时间。Tom对我说“I am tired”，我转告别人可说Tom said he was tired；若转述我自己说的话，I said I was tired中的I仍保留。仍在同一地点说“这里”可保留here；隔天回报昨天的tomorrow，既可从昨天视角说the next day，也可从今天视角说today。表格给常见换法，不能脱离转述场景逐词替换。'),
 (24,'基础'):('#### 不定代词的固定搭配','补两点供本章自测使用：all也可指不可数整体，如all the water（所有的水），不只是“三个以上”；none接复数对象时可搭配单数或复数：None of the answers is/are correct（这些答案没有一个正确）。'),
 (25,'基础'):('#### 不定式的变体','常见动作搭配一起读：want／hope／decide／plan + to do，分别表示想要／希望／决定／计划做某事，如She hopes to come（她希望来）。宾补也看固定搭配：She kept me waiting＝她让我一直等；waiting说明me的动作。I saw her enter强调看见整个进入过程，I saw her entering突出看见正在进入的片段。'),
}

def replace(text,old,new):
    if new and old in new and new in text:return text
    if old.startswith('|') and '\n' not in old:
        key=lambda s:'|'.join(c.strip() for c in s.strip().split('|'))
        return '\n'.join(new if l.lstrip().startswith('|') and key(l)==key(old) else l for l in text.split('\n'))
    return text.replace(old,new)

def revise(text,course='基础'):
    m=re.search(r'^# 第\s*(\d{1,2})\s*章',text,re.M)
    if not m:return text
    n=int(m[1])
    for c in CHANGES:
        if c['资料']==course and c['章']==n:text=replace(text,c['原文'],c['新文'])
    extra=INSERTIONS.get((n,course))
    if (n,course)==(11,'基础'):
        text=text.replace(extra[1]+'\n\n#### 祈使句','#### 祈使句')
        # 祈使句已由完整带学替换时，不再插入旧的一句话引言。
        if '##### 什么时候需要用祈使句\n' in text or '#### 祈使句\n\n**学习目的：**' in text:extra=None
    if extra and extra[1] not in text:
        anchor=extra[0]
        # 小结在现有文件中用二级标题；兼容历史源标题。
        if anchor not in text and anchor=='### 本章小结':anchor='## 本章小结'
        assert anchor in text,(n,anchor)
        text=text.replace(anchor,extra[1]+'\n\n'+anchor,1)
    if course=='基础' and n==17:
        heading='### 感官、使役动词变被动时的不定式 to'
        start=text.find(heading+'\n');target=text.find('### 什么是语态\n')
        if 0<=start<target:
            block=text[start:target]
            text=text[:start]+text[target:]
            text=text.replace('### 特殊被动结构\n',block+'### 特殊被动结构\n',1)
            entry='- [[#感官、使役动词变被动时的不定式 to|感官、使役动词变被动时的不定式 to]]\n'
            text=text.replace(entry,'',1).replace('- [[#特殊被动结构|特殊被动结构]]',entry+'- [[#特殊被动结构|特殊被动结构]]',1)
    if course=='基础' and n==26:
        old='- 分词：faced（过去分词，表被动：当你面对……）'
        text=text.replace(old,'- 分词：faced来自be faced with（面对）；When faced with…省略了与祈使句默认主语you对应的you are，完整理解为When you are faced with…（当你面对……时）。第29章再归纳省略。')
    if course=='基础':
        from 学习分层 import label_b
        def inherit(m):
            rule=label_b(n,m[2])
            return m[1]+'> **【识读即可】** '+rule[0] if rule else m[0]
        text=re.sub(r'(^#{2,6} ([（(]\d+[）)][^\n]+)\n\n)> \*\*【必学】\*\*',inherit,text,flags=re.M)
    return text

def apply():
    from 阅读体验优化 import improve
    rows=[]
    for dirname,kind in [('英语学习资料·完整线性版','基础'),('同等学力申硕英语·考试强化','考试')]:
        for path in sorted([*(VAULT/dirname/'章节').glob('*.md'),*(VAULT/dirname/'强化题目').glob('*.md')]):
            raw=path.read_bytes();before=raw.decode('utf-8').replace('\r\n','\n')
            after=improve(before,path)
            assert improve(after,path)==after,('重复执行不稳定',path)
            snap=RECORD/'后续试读前快照'/(str(path.relative_to(VAULT))+'.snapshot')
            if after!=before:
                snap.parent.mkdir(parents=True,exist_ok=True)
                if not snap.exists():snap.write_bytes(raw)
                path.write_bytes(after.replace('\n','\r\n' if b'\r\n' in raw else '\n').encode('utf-8'))
            if snap.exists():rows.append({'文件':path.relative_to(VAULT).as_posix(),'修改前SHA256':hashlib.sha256(snap.read_bytes()).hexdigest(),'修改后SHA256':hashlib.sha256(path.read_bytes()).hexdigest()})
    sources=[(RECORD/'强化题库.py','基础',10),
             (VAULT/'同等学力申硕英语·考试强化/编排记录/基础练习.py','考试',5),
             (VAULT/'同等学力申硕英语·考试强化/编排记录/全卷模拟.py','考试',15)]
    for path,kind,n in sources:
        raw=path.read_bytes();old=raw.decode('utf-8');new=revise_quiz(old,n,kind)
        if new!=old:
            snap=RECORD/'后续试读前快照'/(str(path.relative_to(VAULT))+'.snapshot')
            snap.parent.mkdir(parents=True,exist_ok=True)
            if not snap.exists():snap.write_bytes(raw)
            path.write_bytes(new.encode('utf-8'))
    for path,kind in [(RECORD/'强化题目清单.json','基础'),(VAULT/'同等学力申硕英语·考试强化/编排记录/题目清单.json','考试')]:
        data=json.loads(path.read_text(encoding='utf-8'))
        for row in data:
            def walk(value):
                if isinstance(value,str):return revise_quiz(value,row['章'],kind)
                if isinstance(value,list):return [walk(v) for v in value]
                if isinstance(value,dict):return {k:walk(v) for k,v in value.items()}
                return value
            updated=walk(row);row.clear();row.update(updated)
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    from 学习分层 import label_b
    p=RECORD/'学习分层明细.json';data=json.loads(p.read_text(encoding='utf-8'));inherited=[]
    for entry in data['知识标记']:
        if re.match(r'^[（(]\d+[）)]',entry['标题']):
            rule=label_b(entry['章'],entry['标题'])
            if rule:
                entry.update(深度='B',依据=rule[1],说明=rule[0]);inherited.append({'章':entry['章'],'标题':entry['标题']})
    p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    (RECORD/'后续试读校订明细.json').write_text(json.dumps({'修改文件':rows,'定点校订':CHANGES,'题库校订':QUIZ_CHANGES,'复盘标签继承':inherited,'补充示范':[{'章':n,'资料':k,'插入位置':a,'内容':b} for (n,k),(a,b) in INSERTIONS.items()]},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'已登记 {len(rows)} 份修改文件，{len(CHANGES)} 条校订规则。')

if __name__=='__main__':apply()
