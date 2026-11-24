"""每章8个强化情境×3种任务，4道串联题，12道独立验收题。"""
SEEDS = {}
CHECKS = {}


def add(n, seeds, checks):
    # 分隔符不是英语标点，便于逐条验证题目字段。
    SEEDS[n] = [tuple(x.strip() for x in line.split('¦')) for line in seeds.strip().splitlines() if line.strip()]
    CHECKS[n] = [tuple(x.strip() for x in line.split('¦')) for line in checks.strip().splitlines() if line.strip()]
    assert len(SEEDS[n]) == 8 and all(len(x)==6 for x in SEEDS[n]), n
    assert len(CHECKS[n]) == 16 and all(len(x)==3 for x in CHECKS[n]), n


add(1, '''
大小写¦把“我开心”写完整：___ am happy.¦I am happy.¦i am happy.¦我很开心。¦表示“我”的I大写。
be搭配¦补全：She ___ happy.¦She is happy.¦She are happy.¦她很开心。¦she搭配is；本章已给出基础对应。
be搭配¦补全：We ___ students.¦We are students.¦We is students.¦我们是学生。¦we搭配are。
句子骨架¦补全：I ___ a student.¦I am a student.¦I a student.¦我是一名学生。¦这里不能省略am。
be否定¦补全否定：He is ___ happy.¦He is not happy.¦He not is happy.¦他不开心。¦not放在is后。
动作否定¦补全“不喜欢”：I ___ like books.¦I don't like books.¦I am like books.¦我不喜欢书。¦本章起步已给出don't，不能随意加am。
三单起步¦补全：She ___ books.（like）¦She likes books.¦She like books.¦她喜欢书。¦本章先识别she likes这组搭配。
be搭配¦补全：You ___ happy.¦You are happy.¦You am happy.¦你很开心。¦you搭配are。
''','''
字母¦a、e、i、o、u属于哪类字母？¦元音字母；这是字母分类，不等于全部语音。
句子职位¦I like books中，谁是主语，什么是宾语？¦I为主语；books为宾语。
修饰职位¦a red book中的red做什么工作？¦定语，说明book是什么样的；red意为红色的。
所属术语¦“名词”和“主语”是同一概念吗？¦不是；名词是词类，主语是句中职位。
起步搭配¦分别写出be与I、she、they的本章基础搭配。¦I am、she is、they are。
字母¦city和boy中，y前分别是什么字母，属于哪类？¦t是辅音字母；o是元音字母；本题只判断，不考完整复数规则。
主语¦Tom runs（汤姆跑）谈论的是谁？¦Tom，主语。
谓语¦Tom runs中表示动作的词是什么？¦runs，是动词，在这里构成谓语。
表语¦She is a teacher中a teacher说明谁的身份？¦说明she，是表语；不是动作对象。
状语¦He runs fast中fast（快地）说明什么？¦说明跑的方式或程度，是状语。
宾补¦We made him happy中happy说明谁的状态？¦him的状态，是宾补；无需自行构造新句型。
同位语¦Tom, our teacher, is here中our teacher解释谁？¦解释Tom，作同位语；整句意为“汤姆，我们的老师，在这里”。
字音¦A的字母名是否一定等于cat中a的读音？¦不是；字母名和单词中的声音不同。
元辅音¦o是辅音字母吗？ch是一个字母吗？¦o是元音字母；ch是两个字母的组合。
起步搭配¦改正：He am happy.¦He is happy.；he搭配is。
范围¦本章提到to read，是否要求现在掌握全部非谓语规则？¦不要求；只识别它是后续要学的结构，验收不考其复杂变化。
''')

add(2, '''
规则复数¦two ___（desk，书桌）¦two desks¦two desk¦两张书桌。¦规则复数加s。
es复数¦three ___（box，盒子）¦three boxes¦three boxs¦三个盒子。¦box复数加es。
辅音加y¦four ___（city，城市）¦four cities¦four citys¦四座城市。¦辅音字母+y变ies。
元音加y¦two ___（toy，玩具）¦two toys¦two toies¦两个玩具。¦元音字母+y直接加s。
不规则¦three ___（child，孩子）¦three children¦three childs¦三个孩子。¦child复数children。
同形复数¦five ___（sheep，绵羊）¦five sheep¦five sheeps¦五只绵羊。¦sheep单复数同形。
不可数¦some ___（advice，建议）¦some advice¦some advices¦一些建议。¦advice的本章用法不可数。
计量¦two ___ of water（glass，杯）¦two glasses of water¦two glass of waters¦两杯水。¦杯数让glass变复数，water不变。
''','''
句中职位¦The books are here（书在这里）中books是词类还是职位？同时给出两者。¦词类为名词；职位为主语。
元辅音¦把family（家庭）变复数，并说明y前的字母。¦families；y前l是辅音字母。
可数性¦a student与some milk（一些牛奶）哪个可数？¦student在这里可数，milk在这里不可数。
词义变化¦a coffee在点单中能指一杯咖啡吗？¦可以；按份可数化，不能因此说所有不可数名词都随意加a。
规则复数¦写出watch（手表）的复数。¦watches；ch结尾加es。
特殊复数¦写出woman（女人）的复数。¦women；不规则变化。
f词尾¦把knife（刀）变复数。¦knives；该词变fe为ves。
例外¦roof（屋顶）复数是rooves吗？¦不是，roofs；不能把所有f结尾一律变ves。
不可数¦改正：three informations。¦three pieces of information；计量词pieces承担复数。
分类¦London（伦敦）与city（城市）哪个是专有名词？¦London是专有名词；city是普通名词。
抽象名词¦love（爱）、desk（书桌）哪个通常表示抽象概念？¦love。
集合¦family与member（成员）表达的是同一种数量层次吗？¦不是，family可表示一个集合，member表示个体成员。
计量¦“两条裤子”用给定词pair、trousers写成短语。¦two pairs of trousers；不写two trousers。
不可数¦改正“许多家具”：many furnitures。¦much furniture或a lot of furniture；furniture通常不可数。
同形复数¦按本章普通计数用法写“两条鱼”：two ___（fish）。¦two fish；此题不讨论种类义等扩展用法。
边界¦water按份点单可说a water，是否与材料义water不可数矛盾？¦不矛盾；意义或计量视角变了。
''')

add(3, '''
主格宾格¦___ likes me.（她）¦She likes me.¦Her likes me.¦她喜欢我。¦作主语用she。
宾格¦Tom helps ___.（我）¦Tom helps me.¦Tom helps I.¦汤姆帮助我。¦动作对象用me。
所属限定¦This is ___ book.（我的）¦This is my book.¦This is mine book.¦这是我的书。¦名词前用my。
名词性所属¦This book is ___.（她的）¦This book is hers.¦This book is her.¦这本书是她的。¦不再接名词，用hers。
反身¦She helps ___.（她自己）¦She helps herself.¦She helps himself.¦她帮助她自己。¦反身与she对应。
指示复数¦___ are books.（这些）¦These are books.¦This are books.¦这些是书。¦books复数搭配these。
远指¦___ is my book.（那个）¦That is my book.¦Those is my book.¦那是我的书。¦单数远指that。
相互¦They help ___.（彼此）¦They help each other.¦They help each other's.¦他们互相帮助。¦这里需要相互代词，不需所有格。
''','''
前章名词¦把“这一个孩子”改成“这些孩子”：this child。¦these children；代词和名词同时变复数。
be¦补全：They ___ my friends.¦are；they搭配are，friends是复数。
职位¦I help her中I、her各是什么职位？¦I为主语；her为宾语。
所属¦改正：It is it's name.（表达“这是它的名字”）¦It is its name.；it's是it is，its才表所属。
宾格¦补全：We help ___.（他们）¦them；宾格。
主格¦补全：___ help us.（他们）¦They；主格。
物主¦把your pen改成不再重复pen的所属形式。¦yours；如This pen is yours。
物主¦补全：The house is ___.（我们的）¦ours；后面不再接house。
反身¦“我独自”写成by ...短语。¦by myself。
反身¦改正：Myself am happy.¦I am happy.；正常主语用I，myself可作强调等，不在这里代替I。
指示¦those books对应近指复数是什么？¦these books。
疑问¦指着一个人问“她是谁”，用已给词who/is/she写问句。¦Who is she?；who问身份。
相互¦“两人互相帮助”能用each other吗？¦能；They help each other。
宾格¦改正：She likes we.¦She likes us.；宾格us。
反身¦Tom makes the toy himself中himself表达什么意思？¦汤姆亲自动手做；是强调，不是另一个人。
限定与替代¦my、mine能互换填入同一位置吗？举出一组。¦不能；my book与The book is mine位置不同。
''')

add(4, '''
初次引入¦I have ___ pen.（首次说一支笔）¦I have a pen.¦I have pen.¦我有一支笔。¦单数可数名词需合适限定。
元音音素¦___ apple（一个苹果）¦an apple¦a apple¦一个苹果。¦apple开头元音音素。
辅音音素¦___ useful book（一本有用的书）¦a useful book¦an useful book¦一本有用的书。¦useful开头辅音/j/。
不发音h¦___ hour（一小时）¦an hour¦a hour¦一小时。¦hour的h不发音。
所属限定¦___ my book（不重复添加冠词）¦my book¦the my book¦我的书。¦my已限定，不再叠加the。
再次提及¦I have a cat. ___ cat is small.¦I have a cat. The cat is small.¦I have a cat. A cat is small.¦我有一只猫。那只猫很小。¦题意为同一只猫，再次提及用the。
泛指复数¦___ dogs are animals.（泛指狗）¦Dogs are animals.¦The dogs are animals.¦狗是动物。¦题目指定泛指整类，不是特定的一群狗。
不可数泛指¦___ water is important.（泛指水）¦Water is important.¦A water is important.¦水很重要。¦材料义不可数泛指通常零冠词。
''','''
名词¦“一条建议”选择an advice还是a piece of advice？¦a piece of advice；advice在这里不可数。
代词¦改正：This is a her bag.¦This is her bag.；her已限定。
读音¦university前为何用a？¦开头是辅音/j/，看声音而非只看字母u。
词类¦the会把不可数名词变可数吗？¦不会；the water仍可为不可数，只是特指水。
读音¦“一位诚实的人”：___ honest person。¦an honest person；h不发音。
读音¦“一本书”：___ book。¦a book；辅音音素开头。
泛指¦改正：I like a music.（泛指音乐）¦I like music.；music通常不可数。
明确对象¦双方都知道指哪扇门：“Please open ___ door.”¦the；可确定对象，不要求前文一定出现过。
乐器¦按本章常见用法补全：play ___ piano。¦the；这里练常见乐器表达。
球类¦按运动项目用法补全：play ___ tennis。¦零冠词；tennis作运动项目。
三餐¦普通日常表达：have ___ breakfast。¦零冠词；不指特别的一顿早餐。
所属¦补全：“他的最好的朋友”：___ best friend。¦his best friend；不在his后再加the。
种类¦a dog可泛指一个典型成员吗？¦可以；泛指类别不只有复数一种方式。
语境¦I saw a dog中的a能在任何语境都不能换成the吗？¦不是；the可用于双方能确定的狗，意义条件不同。
限定¦“这些书”与“那些书”分别如何写？¦these books；those books，不再叠加the。
开放¦用a引入一个物品，第二句用the继续说它（给词book/new）。¦示例：I have a book. The book is new. 检查是否为同一对象。
''')

add(5, '''
单数所有格¦___ book（Tom的书）¦Tom's book¦Toms book¦汤姆的书。¦单数名称后加's。
规则复数所有格¦the ___ room（teachers的房间）¦the teachers' room¦the teachers's room¦老师们的房间。¦规则复数已有s只加撇号。
不规则复数所有格¦the ___ toys（children的玩具）¦the children's toys¦the childrens' toys¦孩子们的玩具。¦children不以s结尾，再加's。
双重所有格¦a friend of ___（我的一位朋友）¦a friend of mine¦a friend of my¦我的一位朋友。¦of后用名词性所属形式。
时间所有格¦___ news（今天的消息）¦today's news¦todays news¦今天的消息。¦时间名词也可用's。
名词定语¦a ___ shop（鞋店，shoe）¦a shoe shop¦a shoes shop¦一家鞋店。¦shoe在此作名词定语用常见单数形式。
数量一致¦The news ___ good.¦The news is good.¦The news are good.¦消息很好。¦news虽以s结尾，此处搭配is。
限定¦I have ___ book.（我的）¦I have my book.¦I have a my book.¦我有我的书。¦my不与a叠加。
''','''
名词代词¦把my mother's friend改成“我妈妈的一位朋友”的of结构。¦a friend of my mother's；双重所有格。
名词计量¦改正：two pair of scissors。¦two pairs of scissors；计量词pair变复数。
可数性¦“她留着长发”用hair还是hairs？¦hair；整头头发通常作不可数，单根可数语境另说。
词类职位¦a school bus中school还是名词吗？作什么职位？¦仍是名词，在这里作定语。
共同拥有¦Tom和Amy共用一个房间，用所有格写“他们的房间”。¦Tom and Amy's room；只在最后一个名字后加's。
分别拥有¦Tom和Amy各有一间房，写“他们各自的房间”。¦Tom's and Amy's rooms；分别加's，rooms复数。
无生命¦the door of the house正确吗？能否推断's只用于有生命对象？¦正确；不能推断，无生命名词也可依语境用's。
双重所属¦改正：a friend of me（本题要用双重所有格）。¦a friend of mine。
时间¦“一周的假期”用week、holiday写所有格短语。¦a week's holiday。
复数所有格¦“两周的假期”用weeks、holiday写短语。¦two weeks' holiday；复数s后加撇号。
词性变位¦Tom's可在Tom's book后省略book吗？¦前文明确时可以，如This book is Tom's。
例外¦sports shoes中的sports说明名词定语全都单数吗？¦不能；存在固定复数形式，要随搭配学习。
专有名称¦能因Central Park含普通词就强行加the吗？¦不能；专有名称按习惯命名用法，不靠词源机械判断。
冠词¦my father's book还需要在最前加a吗？¦不需要；所有格已起限定作用。
所属词形¦a friend of my mother's中的mother's后面需要再加一个friend吗？¦不需要；mother's在这个双重所有格中已表达我妈妈的所属关系。
开放¦用孩子们的、书和新的写一句话。¦示例：The children's books are new. 检查children's和books的复数搭配。
''')

add(6, '''
形副区别¦She is a ___ worker.（careful，细心的）¦She is a careful worker.¦She is a carefully worker.¦她是细心的工作者。¦名词前用形容词。
副词修饰¦He works ___.（careful变副词）¦He works carefully.¦He works careful.¦他工作很细心。¦修饰work用carefully。
系动词¦The soup tastes ___.（good）¦The soup tastes good.¦The soup tastes well.¦汤尝起来很好。¦tastes作系动词，接描述汤的形容词。
比较级¦This bag is ___ than mine.（big）¦This bag is bigger than mine.¦This bag is more bigger than mine.¦这个包比我的大。¦bigger已是比较级。
程度¦Tom is ___ taller than me.（much）¦Tom is much taller than me.¦Tom is very taller than me.¦汤姆比我高得多。¦比较级用much等加强程度。
enough¦She is ___ to drive.（old enough）¦She is old enough to drive.¦She is enough old to drive.¦她年龄够大，可以开车。¦enough修饰形容词放后面。
不定代词修饰¦I have something ___.（important）¦I have something important.¦I have important something.¦我有重要的事。¦形容词修饰something放后。
所属最高级¦He is ___ best friend.（我的）¦He is my best friend.¦He is my the best friend.¦他是我最好的朋友。¦my后不再加the。
''','''
代词比较¦“我的书比她的更有趣”：用book、interesting、hers写句。¦My book is more interesting than hers.；比较对象同为书。
冠词比较¦给出“班里最高的学生”：tall、student、in the class。¦the tallest student in the class；范围包含该学生。
名词修饰¦“两本新书”怎么写？¦two new books；new不因名词复数加s。
副词位置¦改正：I like very much tea.¦I like tea very much.；不要把very much随意插在动宾之间。
比较¦good的比较级、最高级是什么？¦better、best。
比较¦把“越来越冷”写成含cold的短语。¦colder and colder。
比较¦“越来越有趣”：用interesting写短语。¦more and more interesting。
同级¦补全：Amy is ___ tall ___ Tom.（一样高）¦as；as，as tall as。
程度¦hard与hardly都表示“努力地”吗？¦不是；hard可指努力地，hardly指几乎不。
副词¦“他英语说得好”：用speak English、well写句。¦He speaks English well.；well修饰speaks。
对象一致¦改正：The weather here is colder than Beijing.¦The weather here is colder than that in Beijing.；比较天气与天气。
最高范围¦“最高级必须排除主语本人”正确吗？¦不正确；Tom is the tallest in his class把Tom包括在范围内。
表语形容词¦表达“睡着的孩子”，用sleeping child还是asleep child？¦a sleeping child是这里的常见表达；asleep通常不直接放名词前。
顺序¦把small、red、box排成常见顺序，表达一个小红盒。¦a small red box；大小通常在颜色前。
频率¦按中性常见语序改正：She goes always there.¦She always goes there.；频度副词通常放普通动作动词前。
开放¦用more ... than比较两本书，再解释比较对象。¦示例：This book is more useful than that one. 对象均为书，比较级不是most。
''')

add(7, '''
时间介词¦___ Monday（在周一）¦on Monday¦in Monday¦在星期一。¦具体某一天用on。
时间介词¦___ six o'clock¦at six o'clock¦on six o'clock¦在六点。¦时刻用at。
时间介词¦___ October¦in October¦at October¦在十月。¦月份用in。
宾格¦with ___（她）¦with her¦with she¦和她一起。¦介词后用宾格。
固定搭配¦She is interested ___ music.¦She is interested in music.¦She is interested on music.¦她对音乐感兴趣。¦interested in是这里的搭配。
可分结构¦Turn ___ on.（灯，用it）¦Turn it on.¦Turn on it.¦打开它，指灯。¦可分结构的代词放中间。
不可分结构¦Look after ___.（他）¦Look after him.¦Look him after.¦照顾他。¦look after不可拆开。
不及物结构¦I get up ___ seven.¦I get up at seven.¦I get up seven.¦我七点起床。¦at seven是时间短语，不是get up的动作宾语。
''','''
代词¦改正：This letter is for I.¦This letter is for me.；介词后宾格。
名词计量¦表达“杯子里的水”：用water、in、cup。¦the water in the cup；in the cup修饰限定water。
形容词搭配¦good at math是否意味着每个“擅长”语境可随意换介词？¦不是；本章先学good at +学科/活动的常见搭配。
位置¦把on the desk放入“我的书在桌上”。¦My book is on the desk.；不要省be。
空间¦“从外面跳进盒子”：jump ___ the box。¦into；强调移动到里面。
空间¦“坐在盒子里面”：sit ___ the box。¦in；说明所处位置。
交通¦按常见方式表达“乘公交”：___ bus。¦by bus。
搭配¦“同意你”：agree ___ you。¦with。
可分名词¦turn off the light能改为turn the light off吗？¦能；turn off在这里可分，light意为灯。
可分代词¦用代词替代pick up the books中的the books。¦pick them up；不能pick up them。
不可分代词¦用代词替代look for the key中的the key。¦look for it；不能look it for，key为钥匙。
双小词¦“期待它”：look forward to ___（it）。¦look forward to it；不能把it插入中间。
不及物¦get up是否一定要有一个宾语？¦不需要；I get up at six可完整表达。
搭配¦“到达北京”：arrive ___ Beijing。¦in；城市名通常搭配arrive in。
搭配¦“到达车站”：arrive ___ the station。¦at；这里是具体地点。
开放¦各用一个可分和不可分结构造句，宾语必须是代词。¦示例：Turn it off. Please look after her. 检查代词位置不同。
''')

add(8, '''
基数拼写¦___ students（21名学生）¦twenty-one students¦twenty one students¦二十一名学生。¦规范拼写中几十与个位间加连字符。
序数¦my ___ day（第一天）¦my first day¦my one day¦我的第一天。¦顺序用first，my后不加the。
分数¦___ of the students（学生的三分之二）¦two thirds of the students¦two third of the students¦学生的三分之二。¦分子大于一，分母用复数。
分数一致¦Half of the water ___ clean.¦Half of the water is clean.¦Half of the water are clean.¦一半的水干净。¦water是不可数，搭配is。
倍数¦three times ___ heavy as that box¦three times as heavy as that box¦three times more heavy as that box¦重量为那个盒子的三倍。¦本题指定times as ... as结构。
报时¦ten to ___（7:50）¦ten to eight¦ten to seven¦七点五十分。¦距离八点差十分。
时间介词¦___ 2020¦in 2020¦on 2020¦在2020年。¦年份用in。
冠词复习¦___ honest student¦an honest student¦a honest student¦一位诚实的学生。¦honest开头h不发音。
''','''
名词数量¦“三百本书”用three hundred还是three hundreds？¦three hundred books；明确数字后hundred不加s。
冠词序数¦改正：my the second book。¦my second book；my已限定。
介词日期¦“在星期五”与“在五月”各用什么介词？¦on Friday；in May。
可数一致¦Two thirds of the books ___ new.¦are；of后的books复数。
基数¦写出数字35的英语。¦thirty-five。
序数¦写出third对应的数字和意思。¦3，第三；不同于three三个。
序数¦写出数字12的序数形式。¦twelfth。
数量¦hundreds of books中的hundreds需要s吗？¦需要；hundreds of表达数百本，区别于three hundred books。
分数¦“四分之一”用英语写。¦one quarter或one fourth。
百分数¦20 percent of the students ___ here.¦are；students为复数。
百分数¦20 percent of the milk ___ here.¦is；milk为不可数。
报时¦quarter past nine是几点？¦9:15；quarter表示十五分钟，past表示过了。
报时¦ten to six是几点？¦5:50；不是6:50。
倍数¦A is twice as long as B，A长10米，B多长？¦5米；A是B长度的两倍。
小数¦按数字读出3.5。¦three point five。
开放¦用日期或时间介词、一个数量短语写句子（给词books、desk、at six）。¦示例：Two books are on the desk at six. 检查books复数与are、时间at搭配。
''')

add(9, '''
动作动词¦She ___ a book.（read按she搭配）¦She reads a book.¦She is reads a book.¦她读一本书。¦reads已经承担动作谓语，不另加is。
系动词¦The food tastes ___.（good）¦The food tastes good.¦The food tastes well.¦食物尝起来好。¦描述食物的特点用形容词good。
状态系词¦He ___ happy.（be）¦He is happy.¦He happy.¦他很开心。¦状态句需要系动词is。
实义have¦I ___ a pen.（有）¦I have a pen.¦I has a pen.¦我有一支笔。¦have在这里表拥有，主语I用have。
助动词¦___ she like tea?¦Does she like tea?¦Does she likes tea?¦她喜欢茶吗？¦does帮助提问，like恢复原形。
双宾语¦She gives ___ a book.（我）¦She gives me a book.¦She gives I a book.¦她给我一本书。¦接受者在此作宾语，用me。
宾补¦The story makes him ___.（happy）¦The story makes him happy.¦The story makes him happily.¦这个故事让他开心。¦happy说明him的状态。
情态起步¦He can ___.（swim，游泳）¦He can swim.¦He can swims.¦他会游泳。¦can后用原形，不加第三人称s。
''','''
形副串联¦The flowers smell sweet中的sweet是描述花还是描述闻的方式？¦描述花的气味，作表语；smell在这里是系动词。
宾格串联¦改正：She gives we a pen.¦She gives us a pen.；间接宾语用宾格us。
介词串联¦用explain、the rule、to me写“她给我解释规则”，she后按常见搭配变化。¦She explains the rule to me.；不写explains me the rule。
be与动作¦I am like music哪里有问题？¦应为I like music.；like本身是这里的主要动作/状态动词，不加am。
实义动词¦I do my homework中的do是实义还是助动词？¦实义，表示做；homework意为家庭作业。
助动词¦Do you do homework中的两个do各有什么作用？¦第一个帮助提问；第二个表示做。
词的身份¦I have a book与I have finished中的have身份相同吗？¦不同；前者表有，后者帮助构成完成结构；本题只辨身份。
系动词¦become、seem是否都没有意义？¦不是；become表示变成，seem表示似乎，系动词也可带意义。
宾语¦She sleeps中的sleep需要动作对象才完整吗？¦这里不需要；sleep是不及物用法。
宾语¦She likes books中的books为什么叫宾语？¦它是喜欢的对象，跟在及物用法的like后。
结构¦She gave me a pen与She made me happy的后两项一样吗？¦不同；前者为接受者与给予物，后者happy补充说明me。
转换¦用to重写give me a book短语。¦give a book to me；to后的me是介词宾语。
搭配¦suggest与give都能无条件接“人+物”吗？¦不能；要分别学搭配，不能照中文机械套用。
主语一致¦把I work here的主语换成Tom。¦Tom works here.；当前一般现在时单数主语用works。
助动词省略¦回答Do you like tea?时Yes, I do中的do能独自出现吗？¦能；它在简答中承接已知内容，不能把“助动词必须总带后续动词”当绝对规则。
开放¦各写一个动作句和状态句，标出主要动词。¦示例：I read books.／I am happy.；read表达动作，am连接状态。
''')

add(10, '''
主语¦___ reads books.（Tom）¦Tom reads books.¦Reads Tom books.¦汤姆读书。¦普通陈述句先给主语，再组织谓语。
宾语¦I like ___.（她）¦I like her.¦I like she.¦我喜欢她。¦her是宾语，用宾格。
表语¦He is a ___.（teacher）¦He is a teacher.¦He is teacher.¦他是老师。¦teacher在此作表语，单数普通身份需要a。
定语¦a ___ book（新的，new）¦a new book¦a newly book¦一本新书。¦new作定语描述book。
状语¦He runs ___.（quickly）¦He runs quickly.¦He runs quickness.¦他跑得快。¦quickly在此说明动作方式。
双宾语¦She gives ___ a pen.（他）¦She gives him a pen.¦She gives he a pen.¦她给他一支笔。¦him为接受者，a pen为给予物。
宾补¦We make her ___.（happy）¦We make her happy.¦We make her happily.¦我们让她开心。¦happy是说明her的宾补。
介词短语作表语¦The book is ___ the desk.（在上面）¦The book is on the desk.¦The book on the desk.¦书在桌上。¦on the desk可作表语；本句仍需要is。
''','''
名词职位¦The teacher reads a book中两个名词短语分别作什么？¦The teacher为主语；a book为宾语。
形副职位¦a careful worker与works carefully中的修饰对象各是什么？¦careful修饰worker；carefully修饰works。
宾格¦分析She gives us books中的us和books。¦us为间接宾语，books为直接宾语。
对比¦The soup tastes good与She tastes the soup中的soup职位相同吗？¦不同；前句The soup是主语，后句the soup为宾语；taste用法不同。
五句型¦I sleep属于哪种基本句型？¦主谓；本句不要求宾语。
五句型¦She reads English属于哪种基本句型？¦主谓宾；English是宾语。
五句型¦She is kind属于哪种基本句型？¦主系表；kind意为友善的，是表语。
五句型¦He gives Amy a gift属于哪种基本句型？¦主谓双宾；gift为礼物。
五句型¦The news makes Tom happy属于哪种基本句型？¦主谓宾补；happy说明Tom。
同位语¦Tom, my friend, is here中的my friend作什么？¦同位语，解释Tom的身份。
独立成分¦Tom, come here中的Tom与Tom comes here中的Tom工作相同吗？¦不同；前者是呼语，后者是主语。
补语区别¦He is happy与We make him happy中happy各说明谁？¦前者说明He，是表语；后者说明him，是宾补。
词性职位¦red在a red bag中是词性还是职位？给出两种描述。¦词性为形容词；职位为定语。
动词短语¦She is working中is与working可以因两个单词就判成两个互相冲突的谓语吗？¦不能；共同组成进行时动词短语，本题只识别已给结构。
宾语对象¦“直接宾语必须是物”成立吗？用I like her反驳或支持。¦不成立；her指人，在这里是直接宾语。
开放¦各写一个主系表句和主谓宾句，标出表语/宾语。¦示例：I am tired. tired为表语；I like books. books为宾语。
''')

add(11, '''
be疑问¦___ she tired?¦Is she tired?¦Does she tired?¦她累吗？¦有be时把be提前，不用does代替。
动作疑问¦___ he like tea?¦Does he like tea?¦Is he like tea?¦他喜欢茶吗？¦普通一般现在时动作句用does提问。
动作否定¦He ___ like tea.¦He doesn't like tea.¦He doesn't likes tea.¦他不喜欢茶。¦doesn't后用原形。
祈使¦___ the door, please.（open）¦Open the door, please.¦Opens the door, please.¦请开门。¦祈使句用原形。
否定祈使¦___ run here.（不要）¦Don't run here.¦Not run here.¦不要在这里跑。¦用Don't加原形。
存在句单数¦There ___ a book here.¦There is a book here.¦There are a book here.¦这里有一本书。¦单数对象搭配is。
存在句复数¦There ___ two books here.¦There are two books here.¦There is two books here.¦这里有两本书。¦复数对象搭配are。
感叹句¦___ fast he runs!¦How fast he runs!¦What fast he runs!¦他跑得多快啊！¦how加副词fast，runs是动词。
''','''
前章主语¦Who works here?中的Who作什么，为什么不用does？¦Who是主语，问主语时这里不用do辅助倒装。
代词简答¦肯定回答Are you a student?。¦Yes, I am.；you提问，回答者以I自称。
否定简答¦否定回答Does she work here?。¦No, she doesn't.；不回答No, she isn't。
冠词感叹¦写“多漂亮的一朵花”：what、beautiful、flower。¦What a beautiful flower!；单数flower前有a。
特殊疑问¦用where问“你的书在哪里”：your book、is。¦Where is your book?
选择疑问¦Tea or coffee?通常要求怎样回答？¦选择一种，如Tea, please，不把它只当普通yes/no题。
反意疑问¦补全：She isn't tired, ___?¦is she；本题前否后肯。
反意疑问¦补全：He likes tea, ___?¦doesn't he；普通现在时肯定陈述对应否定附加问句。
反意疑问¦Let's go, ___?¦shall we；本章常见搭配。
存在句疑问¦把There is a pen here改为一般疑问。¦Is there a pen here?
存在句否定¦把There are books here改成“不存在任何书”。¦There aren't any books here.；也可There are no books here。
简答¦肯定回答Is there a book here?。¦Yes, there is.
存在与拥有¦“我有一本书”与“桌上有一本书”各用have或there be表达。¦I have a book.／There is a book on the desk.；角度不同。
感叹¦改正：How a beautiful day!。¦What a beautiful day!；或How beautiful the day is!
句子类别¦Please sit down是什么用途的句子？通常省掉谁？¦祈使句，通常省略you。
开放¦写一个be问句和一个普通动作问句，并各给简答。¦示例：Are you tired? No, I'm not.／Do you read? Yes, I do.
''')

add(12, '''
基本一致¦The boy ___ here.（work）¦The boy works here.¦The boy work here.¦这个男孩在这里工作。¦一般现在时单数主语配works。
复数一致¦The boys ___ here.（work）¦The boys work here.¦The boys works here.¦这些男孩在这里工作。¦复数主语用原形。
夹入短语¦Amy, with her friends, ___ here.（be）¦Amy, with her friends, is here.¦Amy, with her friends, are here.¦埃米和朋友们在这里。¦with短语不改变核心主语Amy。
as well as¦Tom, as well as his parents, ___ tea.（like）¦Tom, as well as his parents, likes tea.¦Tom, as well as his parents, like tea.¦汤姆以及他的父母喜欢茶。¦核心主语Tom决定likes。
就近¦Either the boys or Amy ___ here.¦Either the boys or Amy is here.¦Either the boys or Amy are here.¦男孩们或埃米在这里。¦按本章就近规则配Amy。
就近¦Neither Amy nor the boys ___ late.¦Neither Amy nor the boys are late.¦Neither Amy nor the boys is late.¦埃米和男孩们都没迟到。¦最近的是boys。
金额整体¦Ten dollars ___ enough.¦Ten dollars is enough.¦Ten dollars are enough.¦十美元够了。¦金额作为整体看待。
集合整体¦My family ___ a small one.¦My family is a small one.¦My family are a small one.¦我家是个小家庭。¦本句明确说一个整体。
''','''
名词计量¦A pair of shoes ___ here.¦is；中心词pair是单数，不由shoes决定。
否定¦改正：She doesn't likes tea.¦She doesn't like tea.；does承担三单，后用原形。
介词插入¦The teacher with two students ___ happy.¦is；核心主语teacher。
存在句¦There ___ a pen and two books here.（按本章就近用法）¦is；先出现a pen。
集合语体¦My family are watching TV必须判错吗？¦不必；英式成员视角可用are，整体或美式用法更常用is。
意义一致¦The news ___ good.¦is；news在这里为单数概念。
意义一致¦The police ___ here.¦are；police通常搭配复数。
连词¦Both Tom and Amy ___ ready.¦are；both ... and连接两者，不按就近变单数。
语法一致¦把The student has a pen改为复数主语句。¦The students have pens.；若指定每人一支，可另说The students each have a pen。
就近¦Either Amy or I ___ wrong.¦am；按就近与I搭配。
就近¦Not only the teachers but also Tom ___ late.¦is；Tom是最近的主语。
夹入短语¦Tom, together with his parents, ___ here.¦is；together with不构成并列主语。
时间整体¦Two hours ___ enough.（两小时时长整体）¦is；整体时间量。
区分原则¦为何“就远”不等于永远找最远的名词？¦它是在相关结构中找真正的核心主语，不能用物理距离代替句法分析。
纠错¦改正：My friends is happy.¦My friends are happy.；friends复数。
开放¦写一组单数/复数主语的一般现在时句，体现动词变化。¦示例：The girl likes tea.／The girls like tea. 检查主谓同时变化。
''')

add(13, '''
现在习惯¦She ___ here every day.（work）¦She works here every day.¦She is work here every day.¦她每天在这里工作。¦稳定日常习惯用一般现在时。
现在进行¦She ___ now.（work，正在）¦She is working now.¦She working now.¦她现在正在工作。¦进行结构需要is加working。
现在否定¦He ___ like tea.¦He doesn't like tea.¦He don't like tea.¦他不喜欢茶。¦he搭配doesn't，like原形。
进行疑问¦___ they reading now?¦Are they reading now?¦Do they reading now?¦他们现在正在读书吗？¦用are提前提问。
现在完成¦She has ___ the book.（read的分词）¦She has read the book.¦She has reads the book.¦她已经读过这本书。¦has后用过去分词read。
for时长¦I have lived here ___ two years.¦I have lived here for two years.¦I have lived here since two years.¦我在这里已经住了两年。¦时长用for。
since起点¦I have lived here ___ 2022.¦I have lived here since 2022.¦I have lived here for 2022.¦我从2022年起住在这里。¦起始点用since。
完成进行¦I have been ___ for an hour.（read）¦I have been reading for an hour.¦I have been read for an hour.¦我已经持续读了一个小时。¦have been加ing强调持续活动。
''','''
主谓¦把I read every day改成she作主语。¦She reads every day.；reads有三单s。
否定¦She is reading now改否定。¦She isn't reading now.；否定加在is后。
简答¦肯定回答Has she finished?。¦Yes, she has.；finish表示完成。
原形分词¦写出go的原形、过去式、过去分词。¦go—went—gone；不能写has went。
习惯对比¦选正确目标：I ___ here every Monday.（习惯，work/is working）¦work；I work here every Monday。
进行拼写¦write的ing形式是什么？¦writing；末尾不发音e去掉。
进行拼写¦run的ing形式是什么？¦running；该词双写n。
状态动词¦普通“我知道答案”应说I know还是I am knowing the answer？¦I know the answer；稳定状态通常不进行化。
完成否定¦把I have seen the film改为否定。¦I haven't seen the film.；seen是see的分词，film电影。
完成疑问¦把She has finished改为一般疑问。¦Has she finished?
持续意义¦He has lived here for ten years一定表示他已搬走吗？¦不是；这个用法通常关联持续到现在的居住。
进行意义¦I have been reading一定表示已经读完整本书吗？¦不一定；突出持续活动，不保证全书完成。
时间选择¦I have seen him yesterday中的yesterday符合本章所讲的现在完成常见搭配吗？¦不符合；明确结束的过去时间通常不用本节现在完成，下一章再系统学习对应的过去句型。
词形¦补全：She has ___ home.（go）¦gone；过去分词，不是went。
结构¦She is reading中的is、reading分别是什么形式？¦is为限定的be形式，reading为现在分词，共同构成进行时。
开放¦用一个习惯句和一个正在进行句介绍自己，标出时间线索。¦示例：I read every day. I am writing now. 检查am与ing及一般现在时结构。
''')

add(14, '''
过去规则¦She ___ yesterday.（work）¦She worked yesterday.¦She works yesterday.¦她昨天工作了。¦明确过去事件用worked。
过去不规则¦He ___ home yesterday.（go）¦He went home yesterday.¦He goed home yesterday.¦他昨天回家了。¦go过去式went。
过去否定¦I ___ work yesterday.¦I didn't work yesterday.¦I didn't worked yesterday.¦我昨天没有工作。¦didn't后原形。
过去疑问¦___ she come yesterday?¦Did she come yesterday?¦Did she came yesterday?¦她昨天来了吗？¦did承担过去，come原形。
过去be¦They ___ tired last night.¦They were tired last night.¦They was tired last night.¦他们昨晚很累。¦they过去be用were。
过去进行¦I ___ reading at eight last night.¦I was reading at eight last night.¦I were reading at eight last night.¦我昨晚八点正在读书。¦I搭配was，加reading。
过去完成¦She had ___ before I arrived.（leave）¦She had left before I arrived.¦She had leave before I arrived.¦我到达前她已离开。¦had加过去分词left，强调先发生。
过去完成进行¦He had been ___ for an hour.（work）¦He had been working for an hour.¦He had been worked for an hour.¦到当时为止他已持续工作一小时。¦had been后用ing表示持续活动。
''','''
词形¦study、play的过去式分别是什么？¦studied、played；y前辅音与元音不同。
be与动作¦She was tired为何否定不写didn't tired？¦tired在这里为状态形容词，否定在was后加not。
名词串联¦把The child was happy改为多个孩子。¦The children were happy.；child—children，was—were。
现在过去¦I work here与I worked here的主要区别是什么？¦前者说现在的一般情况，后者叙述过去情况。
过去拼写¦stop的过去式是什么？¦stopped；该词双写p。
过去拼写¦live的过去式是什么？¦lived；已有e只加d。
简答¦否定回答Did you read yesterday?。¦No, I didn't.
过去be¦把He was at home改成疑问。¦Was he at home?
过去进行¦把They were working改为否定。¦They weren't working.
过去进行¦把She was sleeping改成疑问。¦Was she sleeping?
先后¦When I arrived, Tom had left中谁先发生？¦Tom离开先发生，我到达后发生。
先后¦单纯“我昨天读了一本书”是否必须用过去完成时？¦不必；I read a book yesterday即可，read过去读音/red/。
影响¦“一般过去时表示和现在绝无联系”对吗？¦不对；过去事件可造成当前后果，如昨天丢钥匙今天仍找不到。
时间状语¦at eight last night是否只能搭配一般过去时？¦不是；I was reading at eight last night可表达当时正在进行。
改错¦改正：She had went home.¦She had gone home.；had后分词gone。
开放¦写一句过去动作句和一句过去状态句，并各改否定。¦示例：I worked.→I didn't work.／I was tired.→I wasn't tired. 检查原形与be两类。
''')

add(15, '''
will原形¦She will ___ tomorrow.（come）¦She will come tomorrow.¦She will comes tomorrow.¦她明天会来。¦will后动词原形。
will否定¦She ___ come tomorrow.（不会）¦She won't come tomorrow.¦She doesn't will come tomorrow.¦她明天不会来。¦will not缩写won't。
will疑问¦___ you help me?（will）¦Will you help me?¦Do will you help me?¦你会帮助我吗？¦will提前，不另加do。
打算¦I am going to ___ tomorrow.（study）¦I am going to study tomorrow.¦I am going to studying tomorrow.¦我打算明天学习。¦be going to后原形。
打算疑问¦___ she going to work?¦Is she going to work?¦Does she going to work?¦她打算工作吗？¦把is提前。
将来进行¦I will be ___ at six tomorrow.（work）¦I will be working at six tomorrow.¦I will be worked at six tomorrow.¦我明天六点会正在工作。¦will be加ing。
将来完成¦I will have ___ by Friday.（finish）¦I will have finished by Friday.¦I will have finish by Friday.¦到周五我将已完成。¦will have加过去分词。
将来完成进行¦By six, I will have been ___ for two hours.（work）¦By six, I will have been working for two hours.¦By six, I will have been work for two hours.¦到六点我将已持续工作两小时。¦will have been加ing。
''','''
过去现在串联¦把I worked yesterday改成用will说“明天工作”。¦I will work tomorrow.；去掉过去式ed，换未来时间。
be串联¦否定They are going to read。¦They aren't going to read.
简答¦肯定回答Will she come?。¦Yes, she will.
数量时间¦用in two days（两天后）和will come写句。¦示例：She will come in two days.；数字与复数days搭配。
计划¦用be going to写“我们打算读书”。¦We are going to read.；we搭配are。
预测¦有当前迹象的预测只能用will、绝不能用going to吗？¦不是；going to也常用于根据当前迹象预测。
临时决定¦当场答应“我会帮助你”，用will表达。¦I will help you.／I'll help you.
否定¦把He will be working改成否定。¦He won't be working.
完成疑问¦把She will have finished改一般疑问。¦Will she have finished?
时间关系¦will have finished by six强调六点正在做还是六点前完成？¦六点前或到六点为止完成，不是单纯正在做。
进行关系¦will be reading at eight重点是什么？¦未来八点时的阅读活动正在进行。
主谓¦She will works如何改？为什么？¦She will work.；will后用原形，不加三单s。
结构¦We going to study哪里缺少形式？¦缺are；We are going to study。
时态¦用所给read/write，把“我昨天读书，明天写作”写成两句。¦I read yesterday. I will write tomorrow.；前句read为过去式。
范围¦过去、现在、将来各四格是否必须第一次就同等熟练？¦不必；先掌握常用结构，低频组合先能辨认时间关系。
开放¦各用will与be going to写一个有明确情境的句子。¦示例：I'll help you.（当场答应）I'm going to read tonight.（已有打算）；不把用法硬性互斥。
''')

add(16, '''
能力¦He can ___.（swim）¦He can swim.¦He can to swim.¦他会游泳。¦can后原形不加to。
建议¦You should ___.（rest）¦You should rest.¦You should rests.¦你应该休息。¦should后原形。
禁止¦You ___ go.（禁止）¦You mustn't go.¦You don't have to go.¦你不准去。¦禁止不同于不必，按指定意思改。
不必¦You ___ work today.（不必，用needn't）¦You needn't work today.¦You needn't to work today.¦你今天不必工作。¦情态needn't后直接原形。
最好不¦You had better ___ go.（最好不要）¦You had better not go.¦You had not better go.¦你最好不要去。¦否定放在better后。
过去习惯¦I ___ live here.（过去住、现在不住）¦I used to live here.¦I am used to live here.¦我过去住这里。¦used to加原形表示过去习惯/状态。
现在习惯¦I am used to ___ here.（live）¦I am used to living here.¦I am used to live here.¦我习惯住在这里。¦这里to为介词，后接living。
过去遗憾¦You should have ___ me.（tell，分词told）¦You should have told me.¦You should have tell me.¦你本应该告诉我。¦should have加分词，指定本应却未做。
''','''
时态串联¦can表示过去一般能力常用哪个词？用swim写“我小时候会游泳”。¦I could swim when I was a child.；could表示当时能力。
否定简答¦Must I leave now?按“不必”作否定回答。¦No, you needn't.／No, you don't have to.；不答No, you mustn't来表示不必。
过去完成串联¦must have left中的have left表达对现在还是对过去离开的推测？¦对过去离开的推测；不是强迫过去发生。
提问¦委婉请求“你能帮助我吗”，用Could开头。¦Could you help me?；不一定表示过去。
许可¦用May问“我可以进来吗”（come in）。¦May I come in?
建议¦Shall we go?中shall主要提出什么？¦提出一起去的建议或征询意见。
普通need¦按实义动词用法补全：She ___ to rest.（need）¦needs；实义need有三单变化。
普通dare¦按实义动词用法写“他敢发言”：he/dare to/speak。¦He dares to speak.；普通动词dare可变化并接to。
推测¦用must表达有把握的“她一定累了”。¦She must be tired.；这是推测，不是义务。
否定推测¦用can't表达“他不可能在这里”。¦He can't be here.；不是简单能力否定。
过去可能¦could have called可表示哪种未实现情况？¦本来可能或有机会打电话，却没有打；语境决定具体解释。
过去不必¦needn't have waited通常暗示实际等了吗？¦等了，后来认为没必要；与单纯不必去做的表达区别。
would¦用would like表达“我想喝茶”。¦I would like some tea.／I'd like some tea.；would like常表示委婉愿望。
情态原形¦改正：She must goes now.¦She must go now.；must后原形。
多义¦You must work与You must be tired的must完全同义吗？¦不完全；前者义务，后者推测，需结合句意。
开放¦写“禁止”和“不必”各一句，解释差别。¦示例：You mustn't run here.／You don't have to run.；分别是不得做、没有必要。
''')

add(17, '''
一般现在被动¦English ___ here.（speak用被动，分词spoken）¦English is spoken here.¦English speaks here.¦这里有人说英语，要求被动。¦主语English是动作涉及的语言，用is spoken。
一般过去被动¦The room ___ yesterday.（clean用被动）¦The room was cleaned yesterday.¦The room is cleaned yesterday.¦房间昨天打扫过了。¦明确过去事件用was cleaned。
情态被动¦The work must ___ finished.¦The work must be finished.¦The work must finished.¦工作必须完成。¦情态被动为must be加分词。
进行被动¦The room is ___ cleaned now.¦The room is being cleaned now.¦The room is been cleaned now.¦房间正在被打扫。¦进行被动用is being加分词。
完成被动¦The work has ___ finished.¦The work has been finished.¦The work has be finished.¦工作已经完成，要求被动。¦has been加过去分词。
将来被动¦The house will ___ built.¦The house will be built.¦The house will built.¦房子将被建造。¦will be加分词built。
感官被动¦He was seen ___ leave.¦He was seen to leave.¦He was seen leave.¦有人看见他离开，要求原形宾补对应的被动。¦此类被动常恢复to。
无被动¦The accident ___ yesterday.（happen）¦The accident happened yesterday.¦The accident was happened yesterday.¦事故昨天发生了。¦happen在这里不及物，不造被动。
''','''
时态串联¦把Tom cleaned the window改成窗户作主语的句子。¦The window was cleaned by Tom.；cleaned既是过去式词形也是分词，结构不同。
宾格串联¦把They invited her改被动（invite邀请）。¦She was invited by them.；主语用She，by后them。
情态串联¦“这本书可以被阅读”用can/read写被动句。¦This book can be read.；can后be，read为过去分词。
冠词串联¦“一座新桥将被建造”用bridge、new、will、build写。¦A new bridge will be built.；单数bridge需限定，build分词built。
被动辨认¦The book was written by Amy中write的分词是什么？¦written；was表现过去，written标记主要动词分词形式。
执行者¦被动句是否每次都必须带by加执行者？¦不必；未知、不重要或显而易见时可省略。
双宾语¦把They gave me a book改成I作主语的被动。¦I was given a book.；接受者也可作为被动主语。
双宾语¦把They gave Amy a pen改成A pen作主语。¦A pen was given to Amy.；给予物作主语时保留to短语。
使役¦用have ... done、hair/cut/yesterday表达“我昨天理了发”。¦I had my hair cut yesterday.；cut是此处的分词，表示请人理发。
状态¦My keys are lost可以一律当成一次清晰的被动动作吗？¦不能；are lost常描述丢失状态，要结合上下文。
主动被动¦Rice grows here与Rice is grown here都可能正确吗？¦都可以；分别说生长和人们种植，本题不把主动一概判错。
动词限制¦改正：This book is belonged to me.¦This book belongs to me.；belong to通常不用于被动。
进行否定¦把The door is being painted改否定（paint粉刷）。¦The door isn't being painted.
完成疑问¦把The letters have been sent改一般疑问（send分词sent）。¦Have the letters been sent?
受伤¦got hurt可以表达受伤吗？¦可以；get被动常用于此类变化或遭遇。
开放¦同一事件分别用主动和被动表达，指出信息焦点。¦示例：Amy wrote the book.／The book was written by Amy.；焦点从Amy换到书。
''')

add(18, '''
限定形式¦She ___ reading now.¦She is reading now.¦She reading now.¦她现在正在读书。¦is为限定形式，与reading组成动词短语。
复合结构¦He has ___ the work.（finish）¦He has finished the work.¦He has finish the work.¦他已经完成工作。¦has为限定形式，finished为分词。
情态结构¦She can ___ here.（work）¦She can work here.¦She can works here.¦她可以在这里工作。¦can后原形。
状态与动作¦He ___ a teacher.¦He is a teacher.¦He does a teacher.¦他是一名老师。¦is连接身份表语。
普通have¦She ___ a book.（表示拥有）¦She has a book.¦She is have a book.¦她有一本书。¦has为拥有用法的实义动词。
普通do¦I ___ my homework every day.¦I do my homework every day.¦I am do my homework every day.¦我每天做家庭作业。¦do在此表做，不另加am。
系词表语¦The flowers smell ___.（sweet）¦The flowers smell sweet.¦The flowers smell sweetly.¦花闻起来香。¦sweet描述花，作表语。
动词搭配¦She explained the rule ___ me.¦She explained the rule to me.¦She explained me the rule.¦她给我解释了规则。¦explain常用物加to加人。
''','''
过去时态¦改正：Did he went home?¦Did he go home?；did承担过去，go原形。
被动串联¦指出The book was written中的限定形式及主要动词分词。¦was为限定形式；written是write的过去分词。
情态串联¦Do you do homework中的两个do与must do中的do作用相同吗？¦前句第一个do为助动词，第二个为主要动词；must do的do是原形主要动词。
状态变化¦She became tired中的became和tired各是什么？¦became是become过去形式，作系动词；tired是表语。
分析层次¦is playing是一个单词吗？是两个互相冲突的谓语吗？¦不是单词；是两个动词形式组成的一个进行时动词短语，不互相冲突。
非限定识别¦I want to read中to read是否独自表达了时态？¦没有；want是本句的限定谓语，to read是不定式结构。
并列¦He sings and dances是否必须删去一个动词？¦不必；sings、dances是并列的谓语成分。
状态词¦I know the answer一般是否改成I am knowing？¦不改；普通知道的稳定状态通常用know。
分类¦系动词是否等于“完全没有意义的助动词”？¦不是；become、seem等带意义；be/have/do要看具体用法。
主谓¦非谓语形式会因he/she自动加第三人称s吗？¦不会；它不独立承担这种主谓一致。
主谓结构¦给出She is happy中狭义系动词、表语和广义谓语部分。¦is；happy；is happy。分析时要声明层次。
词义¦have在She has lunch中表示拥有吗？¦不完全；have lunch是吃午餐的实义搭配，不因have出现就认作完成助动词。
双宾与介词¦Give her a book与Give a book to her中的her句法职位相同吗？¦前者是间接宾语；后者是to的介词宾语。
不及物¦She sleeps为何不需要补一个宾语？¦sleep在这里不及物；主谓结构已可成立。
复合形式¦has been working中哪个形式直接与单数主语对应？¦has；been和working为非限定形式，共同组成完成进行动词短语。
开放¦写一句实义have和一句助动词have的句子，解释意义。¦示例：I have a book.／I have read the book.；前者有，后者帮助组成完成结构。
''')

add(19, '''
并列¦Tom ___ Amy are here.（和）¦Tom and Amy are here.¦Tom but Amy are here.¦汤姆和埃米都在这里。¦and连接并列对象，按中性并列题意。
转折¦I am tired, ___ I am happy.（但）¦I am tired, but I am happy.¦I am tired, so I am happy.¦我累，但我开心。¦指定转折，不是结果。
结果¦I am tired, ___ I will rest.（所以）¦I am tired, so I will rest.¦I am tired, because I will rest.¦我累了，所以我会休息。¦前因为后果，so引出结果。
原因¦___ it rained, I stayed home.（因为）¦Because it rained, I stayed home.¦Because it rained, so I stayed home.¦因为下雨，我待在家。¦此常见结构不重复because和so。
让步¦___ I am tired, I will help.（虽然）¦Although I am tired, I will help.¦Although I am tired, but I will help.¦虽然我累，我仍会帮助。¦本题用Although从句加主句。
选择¦You can stay ___ go.（或者）¦You can stay or go.¦You can stay and go.¦你可以留下或者走。¦按指定选择意义用or。
关联结构¦Either Tom ___ Amy is here.¦Either Tom or Amy is here.¦Either Tom and Amy is here.¦汤姆或埃米在这里。¦either与or配对。
原因介词¦We stayed home because ___ the rain.¦We stayed home because of the rain.¦We stayed home because the rain.¦因为下雨，我们待在家。¦名词短语前用because of。
''','''
一致串联¦Not only Amy but also her friends ___ here.¦are；按本章关联主语就近规则。
介词串联¦补全：She is interested ___ music.¦in；这仍是前章搭配复习，不由中文的“对”换介词。
代词位置¦look after it能改成look it after吗？¦不能；不可分，避免把所有短语动词都当可分。
时态串联¦I worked yesterday, and I ___ work tomorrow.（用will）¦will；两分句可按各自时间表达。
逻辑¦“因为太晚而回家”用Because还是Although开头？¦Because；若换Although就变成“虽然晚了”，逻辑不同。
连接对象¦and只能连接两个完整句子吗？¦不是；可连接词、短语或分句，如Tom and Amy。
从句概念¦Because I am tired, I will rest中哪部分依附另一部分说明原因？¦Because I am tired是原因从句，I will rest是主句。
关联¦补全：Both Tom ___ Amy like tea.¦and；both ... and。
主谓¦Both Tom and Amy ___ tea.（like）¦like；两人并列用复数一致形式。
逻辑纠错¦改正中性句式：Because I was tired, so I rested.¦Because I was tired, I rested.或I was tired, so I rested。
让步纠错¦改正中性句式：Although he is young, but he knows a lot.¦Although he is young, he knows a lot.或He is young, but he knows a lot。
结构¦because接The rain与because of接It rained能直接互换吗？¦不能；本章常见用法because接从句，because of接名词短语。
选择¦表达“不仅聪明而且勤奋”：not only smart ___ hard-working。¦but also；not only ... but also。
判断¦“___ it was late, I went home”若无语境，Because与Although都能成句吗？¦都能；语义关系不同，不能无条件判一个错。
题意¦“She is clever ___ kind”表达中性并列而非反预期，选and/but/or。¦and；题意已指定并列。
开放¦写原因与结果两种句式表达同一件事。¦示例：Because I was tired, I rested.／I was tired, so I rested.；不要重复双连词。
''')

add(20, '''
未来条件¦If it ___ tomorrow, I will stay home.（rain）¦If it rains tomorrow, I will stay home.¦If it will rain tomorrow, I will stay home.¦如果明天下雨，我就待在家。¦本题普通未来条件从句用现在形式。
未来时间¦When she ___, we will eat.（come）¦When she comes, we will eat.¦When she will come, we will eat.¦她来时我们会吃饭。¦本题时间从句用现在形式表未来。
一就¦I will call as soon as I ___.（arrive）¦I will call as soon as I arrive.¦I will call as soon as I will arrive.¦我一到就打电话。¦普通未来时间从句不机械用will。
除非¦___ you hurry, you will be late.（除非）¦Unless you hurry, you will be late.¦Unless you don't hurry, you will be late.¦除非你赶快，否则会迟到。¦unless本身含if not的关系，不无故再加not。
原因¦I stayed home ___ I was tired.（因为）¦I stayed home because I was tired.¦I stayed home because of I was tired.¦我因为累而待在家。¦because引出完整从句。
让步¦___ it rained, we went out.（虽然）¦Although it rained, we went out.¦Although it rained, but we went out.¦虽然下雨，我们仍出去了。¦本题常见结构不重复but。
目的¦I study ___ I can read English.（为了）¦I study so that I can read English.¦I study so I that can read English.¦我学习以便能读英语。¦so that引出目的从句。
结果¦He was so tired ___ he slept.¦He was so tired that he slept.¦He was so tired because he slept.¦他太累了，所以睡了。¦指定结果结构so ... that。
''','''
时态串联¦While I was reading, the phone rang中背景和事件各是什么？¦was reading是进行背景，rang是电话响的事件；while从句表时间。
形容词串联¦补全：It is ___ a useful book that I read it twice.（such/so）¦such；本题名词短语a useful book前用such。
情态串联¦If you need help, you ___ ask me.（表示可以，can）¦can；主句不只有will一种选择。
连词串联¦把Because it rained, so I stayed home按中性标准结构改正。¦去so或改为It rained, so I stayed home。
时间¦before和after表达的时间顺序相同吗？¦不同；before表示在……之前，after表示在……之后。
条件¦unless在本章常见语境中可用哪个if结构解释？¦if ... not；如Unless you hurry可对应If you don't hurry。
让步¦Even though I was tired, I helped her中哪个意思是“即使/尽管”？¦even though，引出让步。
地点¦Where there is water, there is life中where从句表达什么？¦地点/范围背景，意为有水的地方。
方式¦Do as I do中的as从句说明什么？¦方式，意为照我做的方式做。
比较¦He runs faster than I do中than后部分与什么结构相关？¦比较结构；do代替前面已知的run，避免重复。
目的结果¦so that与so ... that在这里的用途有什么区别？¦前者可引出目的，后者典型引出程度导致的结果，须看具体句意。
完成关系¦“到他到达时，我已完成”用by the time与had finished造句。¦By the time he arrived, I had finished.；先完成，后到达。
句子边界¦Because I was tired作为独立书面解释是否通常还需主句？¦本课完整复合句训练通常需主句；对话里可作省略回答，不能把所有片段都当同类任务。
语序¦条件从句可以放主句后吗？用下雨例句说明。¦可以：I will stay home if it rains tomorrow.；意义仍成立。
范围¦从句里的will在全部英语用法中都禁止吗？¦不是；本章“主将从现”针对普通未来条件/时间等用法，不应推广为全体从句禁令。
开放¦写一个未来条件句，并标主从句。¦示例：If I have time, I will read.；if部分为条件从句，后半为主句。
''')

add(21, '''
宾语that¦I know ___ she is here.（that）¦I know that she is here.¦I know that is she here.¦我知道她在这里。¦从句用陈述语序。
宾语where¦I know where she ___.（work）¦I know where she works.¦I know where does she work.¦我知道她在哪里工作。¦嵌入从句不复制独立问句倒装。
是否主语¦___ he will come is unknown.（是否，whether）¦Whether he will come is unknown.¦If he will come is unknown.¦他是否会来还不知道。¦本题句首主语从句用whether。
what内容¦I know ___ she said.（她说的话）¦I know what she said.¦I know that she said.¦我知道她说的话。¦what兼任said的内容成分。
表语¦The fact is ___ she is tired.¦The fact is that she is tired.¦The fact is what she is tired.¦事实是她累了。¦that引出事实内容，不在从句里补对象。
because表语¦This is ___ I was tired.（因为）¦This is because I was tired.¦This is because of I was tired.¦这是因为我累了。¦because后接完整从句；be后可以有这种解释结构。
同位内容¦The news ___ she won is good.¦The news that she won is good.¦The news what she won is good.¦她赢了的消息是好消息。¦that从句说明news的内容。
否定转移¦I ___ think he is right.（我认为他不对）¦I don't think he is right.¦I don't thinks he is right.¦我认为他不对。¦think本句配I用原形；常见否定转移结构。
''','''
前章条件¦If he comes, I will rest与I don't know if he will come中的if功能一样吗？¦不同；前者条件，后者是否的宾语内容，后者可正常用will。
问句串联¦把Where is Amy?嵌入Do you know ...?。¦Do you know where Amy is?；外层提问，内层陈述语序。
代词主谓¦I know that they ___ ready中填be。¦are；从句有自己的主语they。
表语连接¦The reason is ___ I was ill.（本章常见句型）¦that；不能据此禁止This is because ...。
主语¦What she said is true中主语是什么？¦What she said整体；不是单独she。
宾语¦I believe that he is right中that在从句里作主语吗？¦不作；he是从句主语，that起连接作用。
what与that¦I know ___ he wants.（他想要的东西）¦what；从句wants缺内容对象。
whether¦It depends on ___ she agrees.（是否，用whether/if）¦whether；介词on后的本题用whether。
是否连接¦按本章常见用法补全：I don't know ___ or not she agrees.（whether/if，or not紧随连接词）¦whether；本题or not紧随连接词，用whether。
同位语¦that I passed inThe news that I passed made me happy说明哪个词的内容？¦news；内容是我通过了。
内容与修饰¦“消息是她会来”里的that是否代替news充当come的主语？¦不是；从句she才是主语，that连接内容。
省略¦I think (that) she is right中的that在本题常见宾语结构中能省吗？¦通常可以；句首that主语从句等另有条件，不能普遍省略。
否定¦I don't know where he works改成“我知道他在哪里工作”。¦I know where he works.；从句语序不变。
疑问¦改正：Can you tell me where is the book?¦Can you tell me where the book is?
形式主语¦It is true that she is here中it的作用是什么？¦形式主语，后面的that从句提供真正内容。
开放¦写一句“我不知道是否……”的宾语从句。¦示例：I don't know whether she is here.；检查是否意义和陈述语序。
''')

add(22, '''
人物主语关系¦The girl ___ works here is Amy.¦The girl who works here is Amy.¦The girl which works here is Amy.¦在这里工作的女孩是埃米，关系词指人。¦who在从句中作主语；that在适当限制性结构中也可。
物的关系¦This is the book ___ I bought.（用that）¦This is the book that I bought.¦This is the book what I bought.¦这是我买的那本书。¦that引出修饰book的从句。
不重复宾语¦This is the book that I ___.（bought）¦This is the book that I bought.¦This is the book that I bought it.¦这是我买的那本书，不重复它。¦that已对应bought的对象，不加it。
地点状语¦This is the house ___ I live.（where）¦This is the house where I live.¦This is the house which I live.¦这是我居住的房子。¦live here缺地点关系，可用where或in which。
时间状语¦I remember the day ___ we met.¦I remember the day when we met.¦I remember the day where we met.¦我记得我们见面的那天。¦day后的该从句缺时间状语。
所属关系¦The boy ___ bag is red is Tom.¦The boy whose bag is red is Tom.¦The boy who bag is red is Tom.¦书包是红色的男孩是汤姆。¦whose修饰bag，表示所属。
非限制性¦Amy, ___ works here, is kind.¦Amy, who works here, is kind.¦Amy, that works here, is kind.¦埃米很友善，补充她在这里工作。¦非限制性从句不使用that。
介词前置¦The person to ___ I spoke is Amy.¦The person to whom I spoke is Amy.¦The person to that I spoke is Amy.¦我和她说话的那个人是埃米。¦介词前置后本题指人用whom。
''','''
名词串联¦the teacher who likes books中likes为何加s？¦who对应单数先行词teacher，按一般现在时单数一致。
从句区别¦I know that she works与the girl that works中的that作用一样吗？¦不一样；前者连接宾语内容，不作从句成分；后者在关系从句中作主语。
介词串联¦把the house where I live换成介词+which形式。¦the house in which I live。
主谓串联¦the students who ___ here中的work怎样填？¦work；先行词students为复数。
省略¦the book that I read中that能省略吗？¦限制性结构中作宾语，通常可省：the book I read。
不可省¦the girl who lives here中who能因知道是女孩就删吗？¦不能；who承担从句主语。
非限制性¦This book, which I read yesterday, is useful中的which能随意省吗？¦不能；此非限制性关系词通常不省。
范围¦Everything that he said中that常用，是否意味所有类似which都绝对不合语法？¦不能如此推广；本课教常见选择倾向而非普遍禁令。
主宾选择¦The city ___ I visited（访问）用that/where哪个符合缺宾语？¦that；visited缺对象，不是单纯地点状语。
主宾选择¦The day ___ I spent here（度过）用that/when哪个？¦that；spent缺对象，不能仅看到day就选when。
整句指代¦He won, which made Amy happy中的which可指什么？¦前面获胜这件事，不一定只指某一个名词。
as¦As is known to all可放句首吗？通常表达什么？¦可以；表示众所周知，引出补充性说明。
人和物¦先行词包含人和物时，限制性从句通常优先选哪个关系词？¦that；本课先掌握这一常见选择。
比较¦限定与补充的区别只在句子删去后是否合语法吗？¦不是；限制性关乎识别范围，删除后也可能仍是合语法句，但信息识别改变。
纠错¦改正：Amy, who she works here, is my friend.¦Amy, who works here, is my friend.；不重复从句主语she。
开放¦用book、read、useful写一句带限制性定语从句的句子。¦示例：The book that I read is useful.；关系词作宾语也可省。
''')

add(23, '''
转述人称¦Tom said that ___ was tired.（原话I am tired）¦Tom said that he was tired.¦Tom said that I was tired.¦汤姆说他自己累了，转述者不是汤姆。¦I按说话者身份转成he，题意指定后移。
过去将来¦She said she ___ come.（把will按过去视角后移）¦She said she would come.¦She said she will come.¦她说她会来，要求按过去视角后移。¦本题练will到would，不宣称所有转述都必须后移。
转述疑问¦He asked where I ___.（lived）¦He asked where I lived.¦He asked where did I live.¦他问我住在哪里。¦间接问句内部陈述语序。
是否转述¦She asked ___ I liked tea.（whether）¦She asked whether I liked tea.¦She asked that I liked tea.¦她问我是否喜欢茶。¦whether/if表达是否，that不能代替这一意思。
过去将来进行¦He said he would be ___.（work）¦He said he would be working.¦He said he would be worked.¦他说他到时会正在工作。¦would be加ing。
过去将来完成¦She said she would have ___ by then.（finish）¦She said she would have finished by then.¦She said she would have finish by then.¦她说到那时将已完成。¦would have后用过去分词。
过去将来完成进行¦He said he would have been ___ for two hours.（work）¦He said he would have been working for two hours.¦He said he would have been work for two hours.¦他说到那时会已持续工作两小时。¦完整结构would have been加ing。
延续转换¦He has ___ the car for two years.（have的分词）¦He has had the car for two years.¦He has bought the car for two years.¦他已拥有这车两年，表达持续拥有。¦不是购买事件持续两年，需用had。
''','''
条件与宾语¦I don't know if she will come是否违反普通条件“主将从现”？¦不违反；if在这里表示是否，引出宾语从句。
关系从句¦合并：I bought a book. The book is useful.¦The book that I bought is useful.；也可用which或省宾语关系词。
过去先后¦转述原话I have finished，要求said过去视角后移。¦He/She said that he/she had finished.；人称随原说话者，完成转过去完成。
时间表达¦隔天转述昨天说的I will come tomorrow，按过去视角写。¦He/She said that he/she would come the next day.；tomorrow依转述时间改。
客观事实¦转述The earth goes around the sun是否必须把goes改went？¦不必；仍成立的客观事实可保留现在形式。
时间表¦The train ___ at six every morning.（leave）¦leaves；一般现在时可表达时间表。
安排¦按现在进行时表达已安排的明天见面：I/meet/Amy/tomorrow。¦I am meeting Amy tomorrow.
即将¦be about to通常适合与一个很远的将来日期机械搭配吗？¦不适合；它通常表示即将发生，不与任意遥远计划时间等同。
三大从句¦I know where she works中的从句是宾语还是地点状语？¦宾语从句；整体是知道的内容，不因where就一定是地点状语从句。
从句语序¦改正：Do you know where does Amy work?¦Do you know where Amy works?
现在完成¦I have lived here since 2020中的since表示起点还是时长？¦起点；这里从2020年持续到现在。
瞬间延续¦I have bought this car for two years想表达持续拥有两年，本章建议如何改？¦I have had this car for two years.；区分购买事件与持续拥有状态。
过去完成¦The train had left when I arrived，arrived是哪个参照点？¦过去到达的时点；离开在它之前。
进行完成¦has been reading与has read the whole book重心相同吗？¦不同；前者突出持续阅读活动，后者可突出读完整本书的结果。
转述祈使¦把Amy said to me, Please wait改为tell类间接表达。¦Amy told me to wait.；转述请求/指令采用对应结构。
开放¦用said、would、the next day写一句过去计划的转述，并解释先后。¦示例：Tom said he would study the next day.；说发生在过去，学习相对说的时点在之后。
''')

add(24, '''
不定代词一致¦Everyone ___ here.¦Everyone is here.¦Everyone are here.¦每个人都在这里。¦everyone按本章单数一致。
可数数量¦I have ___ books.（一些，用a few）¦I have a few books.¦I have a little books.¦我有几本书。¦a few修饰可数复数。
不可数数量¦There is ___ milk.（一点，用a little）¦There is a little milk.¦There is a few milk.¦有一点牛奶。¦a little修饰不可数milk。
替代词¦This pen is broken. I need a new ___.¦This pen is broken. I need a new one.¦This pen is broken. I need a new it.¦这支笔坏了，我需要另一支新的。¦one替代同类单数物，不指原支坏笔。
比较替代¦My books are newer than ___.（她的）¦My books are newer than hers.¦My books are newer than her.¦我的书比她的更新。¦hers替代她的书，保持比较对象一致。
否定代词¦She likes ___ of them.（两者都不，用neither）¦She likes neither of them.¦She doesn't like neither of them.¦两者她都不喜欢，按本章标准否定结构。¦neither本身带否定，不另叠doesn't。
形式主语¦___ is useful to read.¦It is useful to read.¦Is useful to read.¦阅读是有用的。¦这里it占形式主语位置，to read提供内容。
关系词¦The girl ___ works here is Amy.（who）¦The girl who works here is Amy.¦The girl who she works here is Amy.¦在这里工作的女孩是埃米。¦who已作从句主语，不再加she。
''','''
前章指代¦Tom said that he was tired中的he应按什么判断？¦按原说话者及语境判断，不机械把所有I都改成同一个人。
前章比较¦The weather here is warmer than that in Beijing中的that替代什么？¦weather；避免把天气和地点比较。
介词宾语¦改正：The letter is for you and I.¦The letter is for you and me.；for后用宾格。
从句串联¦I don't know ___ she is.（她在哪里）¦where；宾语从句中she is陈述语序。
all与both¦两个对象“都喜欢”用both还是all最直接？¦both；all通常用于三个及以上或整体范围。
either¦either of the two表示两者都还是二者中任一？¦二者中任一，不等于both。
none¦None of the students are here一定要改is吗？¦不一定；none与复数对象对应时，现代英语可用单数或复数，按语境和风格。
数量语气¦few books与a few books侧重点相同吗？¦不同；few强调很少、近乎没有，a few强调还有一些。
数量语气¦little water与a little water哪个通常表达“还有一点水”？¦a little water。
it同一物¦I bought a pen. It is blue中的it能换成one且意思完全相同吗？¦不完全；it指同一支笔，one常用于同类替代。
ones¦I like red pens, not blue ones中的ones替代什么？¦pens，可数复数同类替代。
指代数¦改正：Where are my keys? I can't find it.¦Where are my keys? I can't find them.；keys复数。
形式宾语¦I find it useful to read中it为什么不等于某本书？¦这里是形式宾语，后面的to read提供被评价内容，本题只辨已给结构。
相互所属¦each other's books有错误吗？¦没有；这里需要彼此的所有格，不能因help each other不加's就全面禁止。
电话指示¦电话里自报身份常用This is Amy还是That is Amy？¦This is Amy；that常用于询问对方身份。
开放¦各写一个a few与a little短语，并说明名词可数性。¦示例：a few books、a little water；books可数复数，water此处不可数。
''')

add(25, '''
want搭配¦I want ___ read.¦I want to read.¦I want reading.¦我想阅读。¦want在本章常见结构后接to不定式。
enjoy搭配¦I enjoy ___.（read）¦I enjoy reading.¦I enjoy to read.¦我喜欢阅读。¦enjoy后用ing形式作宾语。
动名词主语¦___ is useful.（read变成阅读这件事）¦Reading is useful.¦Read is useful.¦阅读是有用的。¦本题动名词短语作主语。
不定式目的¦I came here ___ study.¦I came here to study.¦I came here for study English.¦我来这里学习，按不定式目的表达。¦to study说明来的目的。
告诉某人做¦She told me ___ wait.¦She told me to wait.¦She told me wait.¦她叫我等待。¦tell sb to do。
不定式否定¦She told me ___ to go.（不要）¦She told me not to go.¦She told me to not to go.¦她叫我不要去。¦本题常见否定为not to go。
主动分词¦the boy ___ here（正在工作的男孩，work）¦the boy working here¦the boy worked here¦在这里工作的男孩，要求用主动分词修饰。¦working与boy为主动关系。
被动分词¦the book ___ by Amy（write分词written）¦the book written by Amy¦the book writing by Amy¦埃米写的书，要求用分词修饰。¦书是被写，使用written。
''','''
时态串联¦She is reading与Reading is useful中reading作用一样吗？¦不一样；前者参与进行时，后者作主语。
分句串联¦I know she works here能因know与works同时出现就判错吗？¦不能；两个分句各有自己的限定谓语。
关系串联¦把the girl who is reading改为分词修饰短语。¦the girl reading；reading修饰girl。
被动串联¦把the letter that was written by Tom改成分词修饰短语。¦the letter written by Tom；保留被动关系。
搭配¦补全：She hopes ___ come.¦to；hope to do。
搭配¦补全：He finished ___ the book.（read）¦reading；finish doing。
记忆¦remember to lock与remember locking差别是什么？¦前者记得去锁，后者记得曾锁过；lock为锁。
停止¦stop talking与stop to talk差别是什么？¦前者停止说，后者停下原活动去说。
尝试¦按“试试另一种方法”填：Try ___ it another way.（do）¦doing；本题试用一种方法。
意图¦按“打算帮助”填：He means ___ help.¦to；mean to do表示打算。
感官¦强调看见整个进入过程：I saw her ___ the room.（enter）¦enter；saw sb do突出事件整体，entering可表示进行片段。
否定¦用to不定式写“不要迟到”的宾补：tell him ...。¦tell him not to be late；not放在to前的常见形式。
分词语义¦interesting book与interested student通常分别描述什么？¦前者令人感兴趣，后者感到有兴趣；不能机械认定所有人都用ed所有物都用ing。
补语¦She kept me waiting中的waiting说明谁在等？¦me，是动作等待的逻辑主体，waiting作宾补。
谓语¦改正：They playing outside.¦They are playing outside.；缺合适限定形式，不是因为They是第二个动词。
开放¦用want to与enjoy doing各写一句，两句须有不同主要动作。¦示例：I want to sleep. I enjoy reading.；检查搭配与主语形式。
''')

add(26, '''
完成主动¦___ the work, she went home.（要求完成式，finish）¦Having finished the work, she went home.¦Having finish the work, she went home.¦完成工作后她回家，强调先完成。¦having加分词finished。
完成被动¦___ warned, he stayed home.（要求having been）¦Having been warned, he stayed home.¦Having be warned, he stayed home.¦被警告后他待在家，warn警告。¦完成被动为having been加分词。
独立主格¦Weather ___, we will go out.（permit允许，主动ing）¦Weather permitting, we will go out.¦Weather permitted, we will go out.¦天气允许的话，我们会出去。¦weather是permitting自己的逻辑主语。
分词被动¦___ from the hill, the city is beautiful.（see）¦Seen from the hill, the city is beautiful.¦Seeing from the hill, the city is beautiful.¦从山上看，这座城市很美。¦city是被看的对象，用seen。
不定式介词¦a room to live ___¦a room to live in¦a room to live¦一间可居住的房间。¦本结构live与房间的关系需要in。
主动表被动¦The flowers need ___.（water，用ing）¦The flowers need watering.¦The flowers need to watering.¦花需要被浇水，要求ing表达。¦need doing在此表示需要被做。
worth搭配¦The book is worth ___.（read）¦The book is worth reading.¦The book is worth to read.¦这本书值得读。¦worth doing是这里的结构。
进行被动修饰¦the house ___ built（正在建的房子）¦the house being built¦the house been built¦正在被建造的房子。¦being built强调进行中的被动。
''','''
从句串联¦把Because she had finished, she went home按同主语主动完成分词改写。¦Having finished, she went home.；finished的主体与she一致。
被动串联¦the house built last year与the house being built now差别是什么？¦前者去年建的房子，后者现在正在建；不能机械删加being而保持同义。
时态串联¦to have finished的完成式表达独立的过去时吗？¦不是；通常表示相对主要参照动作更早，实际时间由上下文确定。
逻辑主语¦Weather permitting, we will go out中weather与we是同一个逻辑主语吗？¦不是；独立主格带自己的主体weather。
悬垂修饰¦Seeing the dog, I stopped中的seeing主体是谁？¦I；普通此类分词状语的主体应能从主句合理对应。
悬垂纠错¦想说“我走着，看见一辆公交”：Walking home, a bus was seen by me应如何清楚改写？¦Walking home, I saw a bus.；让走路的人I作主句主语。
主动被动¦having done与having been done可以无条件互换吗？¦不能；前者主动，后者被动。
不定式被动¦写出to do的被动形式。¦to be done。
不定式完成¦写出to do的完成式。¦to have done。
动名词被动¦用being helped表达“我喜欢被帮助”：I enjoy ...。¦I enjoy being helped.；动名词被动结构作宾语。
主动表被动¦The room needs cleaning能换成needs to be cleaned吗？¦通常可以；本题两者表达需要打扫房间。
介词遗留¦a chair to sit on为何保留on？¦sit与chair的地点关系在该结构中由on表达，不能按中文把介词随意删掉。
动名分词¦Reading is useful与a reading child中的reading作用相同吗？¦不同；前者活动作主语，后者修饰child。
比较¦to read与having read区别只是有没有to吗？¦不是；结构类别与相对时间都不同，需按句中任务和先后分析。
完成逻辑¦Having finished her work, Amy left中的两个动作谁先？¦先完成工作，后离开。
开放¦把“看见老师后，我停下”写成主动分词状语句，提供see/saw/seen、stop/stopped。¦Seeing the teacher, I stopped.；普通先后语境不强制having seen，主体均为I。
''')

add(27, '''
数量集合¦A number of students ___ here.¦A number of students are here.¦A number of students is here.¦许多学生在这里。¦a number of在这里表示许多，配复数。
数量数目¦The number of students ___ large.¦The number of students is large.¦The number of students are large.¦学生的人数很大。¦核心是number表示数目。
分数一致¦Two thirds of the water ___ clean.¦Two thirds of the water is clean.¦Two thirds of the water are clean.¦三分之二的水干净。¦与water的不可数用法相配。
分数一致¦Half of the students ___ here.¦Half of the students are here.¦Half of the students is here.¦一半学生在这里。¦students复数。
一类人¦The rich ___ not always happy.¦The rich are not always happy.¦The rich is not always happy.¦富人并非总快乐。¦the rich指一类人，配复数。
动名词主语¦Reading books ___ useful.¦Reading books is useful.¦Reading books are useful.¦读书是有用的。¦整个活动作主语，不由books决定。
从句主语¦What she said ___ true.¦What she said is true.¦What she said are true.¦她说的话是真的。¦本句一个内容整体作主语，用is。
关系从句一致¦He is one of the boys who ___ here.（work）¦He is one of the boys who work here.¦He is one of the boys who works here.¦他是那些在这里工作的男孩之一。¦本题关系从句修饰boys，用work。
''','''
基础回顾¦Tom, as well as his friends, ___ here.¦is；核心主语Tom，as well as不改变其数。
代词回顾¦Each of them ___ a pen.（have）¦has；each按单数一致。
计量回顾¦Two pairs of shoes ___ here.¦are；pairs复数，而非只看shoes。
非谓语回顾¦To read every day ___ useful.¦is；本句一个不定式活动整体作主语。
each并列¦Each boy and each girl ___ a book.（have）¦has；本章each ... and each ...通常用单数。
普通并列¦Tom and Amy ___ ready.¦are；普通两人并列主语。
整体餐具¦A knife and fork ___ on the table.（明确说一套餐具整体）¦is；若分别列举两件物品则are也可，题意指定整体。
only one¦He is the only one of the boys who ___ here.（按从句限定the only one，work）¦works；题目明确修饰唯一的one。
one of¦She is one of the teachers who ___ English.（teach）¦teach；关系从句在本题中修饰teachers。
集合语体¦My family is watching TV必因“看电视是成员行为”而错吗？¦不必；美式或整体视角可用is，英式强调成员也可are。
无形式s¦The police ___ looking for him.¦are；police配复数。
不可数¦The equipment ___ new.¦is；equipment通常不可数，不按现实中设备件数变are。
百分数¦Sixty percent of the students ___ ready.¦are；students复数。
时间金额¦Fifty dollars ___ enough.（一笔金额整体）¦is；整体金额。
假主语¦It ___ useful to read.¦is；形式主语结构，不按read等词的个数决定。
开放¦用a number of和the number of各造一句，说明一致区别。¦示例：A number of students are here. The number of students is ten.；分别指许多人和人数。
''')

add(28, '''
现在假设¦If I ___ you, I would rest.（正式假设形式）¦If I were you, I would rest.¦If I am you, I would rest.¦如果我是你，我会休息，要求正式假设。¦本题用were，不表示实际过去。
现在假设¦If I ___ time, I would read.（have，假设现在没时间）¦If I had time, I would read.¦If I have time, I would read.¦假如现在有时间，我会读书。¦过去形式had表达与当前现实的距离。
过去假设¦If I had known, I ___ have helped.¦If I had known, I would have helped.¦If I had known, I will have helped.¦如果当时知道，我就会帮忙。¦对过去反事实，主句would have加分词。
过去条件¦If she had ___, she would have passed.（study）¦If she had studied, she would have passed.¦If she has studied, she would have passed.¦要是当时学了，她就通过了。¦本题过去条件用had studied。
现在愿望¦I wish I ___ more time now.（have）¦I wish I had more time now.¦I wish I have more time now.¦我真希望现在有更多时间。¦对现在非真实愿望用过去形式。
过去愿望¦I wish I ___ studied yesterday.¦I wish I had studied yesterday.¦I wish I would study yesterday.¦我真希望昨天学过。¦过去遗憾用had加分词。
建议要求¦She suggested that he ___ more.（read，原形虚拟）¦She suggested that he read more.¦She suggested that he reads more.¦她建议他多读，要求原形虚拟结构。¦read可前加should，不随he加s。
would rather¦I'd rather you ___ tomorrow.（come，偏好你明天来）¦I'd rather you came tomorrow.¦I'd rather you will come tomorrow.¦我宁愿你明天来。¦would rather接该从句常用过去形式表达现在/未来偏好。
''','''
真实条件回顾¦If it rains tomorrow, I will stay home与If it rained tomorrow, I would stay home都可表达未来吗？¦都可以；说话者对条件的现实距离不同，并非rained必指过去。
时态回顾¦If I had studied, I would be ready now是主从时间不一致就必错吗？¦不是；可以是混合条件，过去学习影响现在状态。
情态回顾¦could have helped在假设里可表达什么？¦在相应条件下本可帮助；与would have的确定结果、能力侧重点可不同。
倒装预备¦Had I known可对应哪种if开头形式？¦If I had known；省if并提前had。
未来假设¦If it ___ tomorrow, we would stay home，should rain/rained哪些可用？¦两者都可；表达对应的未来假设，不把本题设置成无条件单选。
愿望语体¦I wish I was taller在非正式英语中一定错吗？¦不一定；was与were可受语体影响，正式形式通常优先were。
过去愿望¦He wishes he studied harder与had studied harder区别是什么？¦前者通常愿现在更用功，后者通常遗憾过去没更用功。
if only¦If only I had known!表达对现在还是过去的遗憾？¦过去；had known表示早先不知道。
时间句¦It's time we ___ home.（go，本章过去式结构）¦went；表示现在该走了，不表示实际过去走过。
含蓄条件¦Without your help, I couldn't have finished中的without表达什么？¦暗示如果没有帮助的反事实条件，主句谈过去未能完成的假设。
suggest多义¦His smile suggested that he was happy中的suggest必须让从句变原形吗？¦不必；这里表示表明，不是提出建议。
insist多义¦insist表示坚持要求时，本章介绍哪类从句形式？¦(should)加动词原形，如insisted that he (should) leave；坚持事实时另看语义。
as if¦He talks as if he knew everything是否意味着他说的是一个实际过去事件？¦不是；knew可表达与当前现实不同的假设。
省if¦If had I known为何不符合本章倒装方式？¦省if才把had提前；应Had I known或If I had known。
条件概率¦使用过去形式假设能对应一个固定的低于1%的概率吗？¦不能；反映说话者态度与现实距离，不是数学阈值。
开放¦分别写一个对现在的wish和一个对过去的wish，必须有时间提示。¦示例：I wish I had more time now. I wish I had studied yesterday. 检查过去式与过去完成。
''')

add(29, '''
否定倒装¦Never ___ I seen this before.¦Never have I seen this before.¦Never I have seen this before.¦我以前从未见过这个。¦否定副词前置后助动词在主语前。
only状语¦Only here ___ I work well.（can）¦Only here can I work well.¦Only here I can work well.¦只有这里我能好好工作。¦only修饰前置状语，发生助动词/情态倒装。
地点倒装¦Here ___ the bus!（come）¦Here comes the bus!¦Here come the bus!¦公交车来了。¦名词主语bus单数配comes。
代词不倒装¦Here ___ is!（it）¦Here it is!¦Here is it!¦它在这里。¦此类here句代词主语通常保持主谓顺序。
强调人¦It was Amy ___ helped me.（who）¦It was Amy who helped me.¦It was Amy which helped me.¦是埃米帮助了我。¦强调人可用who或that，本题指定who。
强调时间¦It was yesterday ___ he came.¦It was yesterday that he came.¦It was yesterday when he came.¦他是昨天来的，要求本章强调句型。¦该强调连接结构用that。
动词强调¦She did ___ the exam.（pass）¦She did pass the exam.¦She did passed the exam.¦她确实通过了考试。¦did后原形，过去由did表达。
不定式省略¦I'd love ___.（承接前面已知的to go）¦I'd love to.¦I'd love go.¦我很愿意，前文已明确指去。¦省重复内容，保留to。
''','''
时态串联¦用did完成过去倒装：Not until yesterday ___ she arrive.¦did；arrive保持原形。
虚拟串联¦把If I had known改成省if倒装。¦Had I known。
代词串联¦My room is small, and hers is large中hers替代什么？¦her room；不能写her来独立替代。
从句串联¦区分It was Amy that helped me与It is true that Amy helped me。¦前者强调Amy；后者it是形式主语，that从句提供true的内容。
还原¦把Never have I seen it还原普通语序。¦I have never seen it.
only主语¦Only Amy knows，是否必须倒成Only does Amy know？¦不必；only修饰主语，不是前置状语。
倒装过去¦纠正So loudly did he spoke that we heard him。¦So loudly did he speak that we heard him.；did后原形。
名词强调¦强调普通句Tom read this book中的this book。¦It was this book that Tom read.；保留其余结构。
强调省略¦It was Tom I met在非正式表达中一定因缺that而错吗？¦不一定；焦点对应宾语时可见省略，本课程正式练习先保留that。
省略条件¦When tired, I rest中省略了哪些内容？¦When I am tired，普通同主语且有be的从句省略。
固定省略¦If necessary, ask Amy能因主从主语不一致就判错吗？¦不能；可理解为If it is necessary，是常见固定省略。
比较省略¦He runs faster than I do中的do承接什么？¦run；避免重复。
让步倒装¦把Although he is young, he is wise用Young ... as结构表达。¦Young as he is, he is wise.；wise聪明/有智慧的。
名词让步¦按本章结构补全：___ as he is, he is brave.（child，孩子）¦Child；前置的此名词不带a，brave勇敢的。
不定式保留¦对Would you like to come?给出愿意的省略回答。¦I'd love to.；保留to承接come。
开放¦写一对普通句和强调句，强调对象须是人或时间。¦示例：Amy came yesterday.／It was Amy who came yesterday. 检查去掉强调框架后仍可恢复普通句。
''')

add(30, '''
否定前缀¦happy前加否定前缀：___¦unhappy¦imhappy¦不开心的。¦本词常用un-，不能随意换前缀。
否定前缀¦possible的常见否定：___¦impossible¦unpossible¦不可能的，按现代常见标准形式。¦本词常用im-。
名词后缀¦teach + er = ___¦teacher¦teached¦教师。¦-er在此形成表示人的名词。
副词后缀¦happy变副词：___¦happily¦happyly¦开心地。¦y变i后加ly。
名词后缀¦happy变名词：___¦happiness¦happyness¦幸福/开心。¦本词派生时y变i。
合成复数¦two ___（passer-by，过路人）¦two passers-by¦two passer-bys¦两位过路人。¦本合成词在主体passer上变复数。
转化¦I ___ the plants.（water作动词）¦I water the plants.¦I waters the plants.¦我给植物浇水。¦water由名词转为动词，I后用原形。
连字符¦a ___ boy（good-looking，好看的）¦a good-looking boy¦a good looking boy¦一个好看的男孩，按本章前置合成形容词拼写。¦该固定合成形式用连字符。
''','''
名词复数¦mother-in-law变复数。¦mothers-in-law；主体mother变复数。
形副¦friendly以ly结尾就一定是副词吗？¦不是；friendly通常是形容词，意为友好的。
时态¦water作动词时“她浇花”的谓语会变化吗？¦会；She waters the flowers，转化后的动词遵守相应词形规则。
前缀语义¦rebuild中的re通常给出什么意义？¦重新；build建造，rebuild重建。
派生¦careful与careless中的后缀大致表达什么？¦-ful表示有该性质，-less表示缺乏；careful小心的，careless粗心的。
词性¦education和educate通常哪个是名词？¦education为教育，educate为教育某人的动词；词尾提供线索。
合成¦classroom可分成哪两个已知词，整体什么意思？¦class与room，整体教室；不能据两个词推所有语义都完全逐字可解。
截短¦exam是否是examination的常见截短形式？¦是，均涉及考试。
首字母¦WHO来自World Health Organization，属于哪种构词方式？¦首字母缩略；不是添加后缀。
词类转化¦a clean room中的clean与clean the room中的clean用法相同吗？¦不同；前者形容词，后者动词，这里体现词类用法变化。
拼写¦sun加后缀变sunny需要什么拼写变化？¦双写n后加y。
拼写¦decide对应的名词是decision还是decidement？¦decision；派生词要按实际词形学习。
词尾判断¦-tion常提示名词，是否能保证所有生词靠词尾判准？¦不能；要结合句中位置、词义和词典用法。
感叹词¦Oh, I see中的Oh通常承担主语还是独立感叹成分？¦独立感叹成分，不是该句主语。
派生计数¦teacher变复数属于派生出新词，还是同一名词的数变化？¦teachers是同一名词的复数变化，teach到teacher才是这里的派生。
开放¦各给一个前缀、后缀、合成、转化的例子并解释。¦示例：unhappy否定、teacher教的人、classroom教室、water作浇水动词；允许其他本章已讲例子。
''')

add(31, '''
句间转折¦He is tired___ however, he will help.（两独立分句，填分号）¦He is tired; however, he will help.¦He is tired, however, he will help.¦他累了，然而会帮忙，要求分号连接独立分句。¦however本身不能替代并列连词。
连词转折¦He is tired, ___ he will help.（but）¦He is tired, but he will help.¦He is tired, however he will help.¦他累了，但会帮忙，要求连词结构。¦but直接连接两个分句。
因果副词¦It rained. ___, we stayed home.（therefore）¦It rained. Therefore, we stayed home.¦It rained. Moreover, we stayed home.¦下雨了，因此我们待在家，要求因果。¦therefore表结果，moreover表递进。
列举冒号¦I need two things___ a pen and a book.（冒号）¦I need two things: a pen and a book.¦I need two things、a pen and a book.¦我需要两样东西：笔和书。¦英语不用中文顿号，冒号可引列举。
所属撇号¦___ book（Tom的）¦Tom's book¦Toms book¦汤姆的书。¦所属撇号有结构作用，不是普通装饰。
缩写¦___ raining.（It is缩写）¦It's raining.¦Its raining.¦正在下雨。¦it's等于it is，its表所属。
句中副词¦He was, ___, tired.（however，插入转折）¦He was, however, tired.¦He was; however, tired.¦不过，他累了，要求副词作句中插入。¦不是每个however紧前都必须有句号或分号。
直接引语¦按本书外双内单示例补逗号："I am tired___" she said.¦"I am tired," she said.¦"I am tired." she said.¦“我累了，”她说，要求同一陈述引语后接引述语。¦陈述引语与后接引述语在此用逗号衔接。
''','''
从句串联¦Although I was tired, I helped her中的逗号连接的是两个独立句吗？¦不是；前面为依附的让步从句，后面主句，不能把它误判成普通逗号拼接。
所有格复习¦写“老师们的办公室”，teacher复数，office办公室。¦the teachers' office；s后撇号。
关系从句复习¦Amy, who lives here, is kind中的逗号有什么作用？¦标记补充性非限制性关系从句，非普通两独立句硬接。
多句逻辑¦把I was tired. I rested.用一个因果连接改写，不改变意思。¦I was tired, so I rested.或Because I was tired, I rested。
however位置¦however只能放在句首吗？给出句中位置的例子。¦不是；He was, however, tired.可成立。
标点¦修正：She is kind, she helps me.（保留两个独立分句）¦She is kind; she helps me.或分成两句；也可加合适连词。
逻辑¦moreover通常表示转折还是递进？¦递进，意为而且/此外。
逻辑¦nevertheless通常表达什么关系？¦让步性转折，尽管如此。
逻辑¦for example通常用于引出什么？¦例子；不是因果必然结论。
总结¦in conclusion通常用于什么位置功能？¦总结或结论；不表示另一个具体原因。
嵌套引号¦外双内单与外单内双是否只有一个全英语通用的正确体系？¦不是；英美及具体出版风格可不同，选定一套保持一致。
引号语气¦引语本身是问句，后接she asked，是否把问号强行改成逗号？¦通常不改，保留引语自身问号，如"Are you ready?" she asked。
句号¦把he is here改成规范书写。¦He is here.；句首大写，句末句号。
逻辑一致¦“It rained. Therefore, the ground was wet.”中的Therefore说明什么？¦将前面的雨作为后面地面湿的原因线索，表达结果关系。
独立输出¦用3句写一个过去事件与结果，必须用because/so/therefore之一，不得只用逗号硬接独立句。¦示例：It rained yesterday. I stayed home because I was tired. Therefore, I read my book at home.；语法、指代和逻辑通顺即可，不只认这一写法。
综合输出¦写5句介绍学习：一个习惯、一个过去事件、一个将来计划、一个原因或条件从句、一个正确句间连接。¦示例：I read every day. Yesterday I learned a word. Tomorrow I will write a story. If I need help, I will ask Amy. She is kind, and she helps me.；逐项检查要求，不要求加入未学结构。
''')

# 第23章合并了转述与整个时态体系，额外保留16道独立任务。
EXTRA = {
23: [
 ('过去将来完成','把He said, I will have finished by Friday按过去视角转述。','He said he would have finished by Friday.；Friday是否改成其他日期需看实际转述时点，题目不强制改。'),
 ('转述否定祈使','把Tom said to me, Do not run转述为told结构。',"Tom told me not to run.；不写told me don't run。"),
 ('过去进行转述','把She said, I am reading按过去视角后移。','She said she was reading.；she身份由原说话者确定。'),
 ('语境后移','She said she will come一定因said过去就错吗？','不一定；可按仍有效的计划保留当前视角；指定过去视角练习时用would。'),
 ('现在完成进行','用learn写“我已持续学英语三年”，突出持续过程。','I have been learning English for three years.'),
 ('过去完成进行','用wait写“到车来时，他已经连续等了一小时”。','He had been waiting for an hour when the bus came.'),
 ('将来完成','要求用will have，写“到周五她将已完成”。','She will have finished by Friday.'),
 ('瞬间延续','He has joined the team for two years想表达持续入队状态，如何改？','He has been in the team for two years.／He has been a member of the team for two years.'),
 ('时间与内容','When will she come?嵌入I do not know ... 后为何仍可用will？',"I don't know when she will come.；这里是宾语内容，不是普通时间状语从句。"),
 ('关系与时间','I remember the day when she came中when引导哪类从句？','定语从句，修饰day，而非整体直接作时间状语。'),
 ('目的','用so that和can写“我读英语以便能理解它”。','I read English so that I can understand it.'),
 ('因果','Because I had lost my key, I could not get in中的两个时间层次是什么？','先丢钥匙，后在过去的某时进不去；过去完成关联过去参照。'),
 ('安排与预测','I am meeting Amy tomorrow与I think Amy will come tomorrow重心一样吗？','前者常表达安排；后者常表达预测，两者都谈未来但意图不同。'),
 ('过去完成选择','before已说明先后，是否所有句子都必须用had done？','不必；一般过去也可叙事，过去完成用于需要突出更早参照等情况。'),
 ('过去持续参照','把I have lived here for two years改成“到当时为止已住两年”，用过去完成形式。','I had lived here for two years by then.；by then提供过去参照点。'),
 ('短文','写4句：某人昨天说自己次日要学习；现在你知道他在哪里；你指出一本他昨天买的书；说明你读书的原因。','示例：Tom said yesterday that he would study the next day. I know where he is. This is the book that he bought yesterday. I read because it is useful.；逐项核对转述、语序、关系与原因。'),
],
}


from 先修题目 import repair_bank
repair_bank(SEEDS,CHECKS,EXTRA)
from 基础规则校订 import repair_bank as repair_basic_rule_bank
repair_basic_rule_bank(SEEDS,CHECKS,EXTRA)
