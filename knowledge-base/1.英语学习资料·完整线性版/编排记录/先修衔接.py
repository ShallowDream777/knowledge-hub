"""从零基础读者的已知内容出发，修复先修顺序；在生成目录前应用。"""
import re

CHAPTER_ONE='''### 字母、单词、短语与句子

英语用字母拼成单词。book是一个单词，意思是“书”；a book是两个单词组成的一组话，意思是“一本书”。这种组合叫**短语**。I am a student. 表达“我是一名学生”，是一句完整的话，叫**句子**。例句中的空格把单词分开，句末的英文句号是一个小点。

同一个字母有大写、小写两种写法，如A和a、B和b。句子的第一个字母大写；表示“我”的单词I总是大写。I与小写字母l不是同一个字符。

本章先用到这些词，先读中文意思，不需要猜：

| 英语 | 中文 | 英语 | 中文 |
|---|---|---|---|
| I | 我 | you | 你／你们 |
| he | 他 | she | 她 |
| it | 它 | we | 我们 |
| they | 他们／她们／它们 | student | 学生 |
| teacher | 老师 | book | 书 |
| happy | 开心的 | red | 红色的 |
| like | 喜欢 | not | 不 |

student、teacher、book给人或事物命名，这类词叫**名词**。like表示“喜欢”，run表示“跑”，这类表达动作、情况或状态的词叫**动词**。happy、red描述“什么样”，这类词叫**形容词**。I、you、she等指代人或事物，这类词叫**代词**。这些名称是在给词分类，合称**词类／词性**。

先用一小步检查：book表示事物名称，所以是名词；happy描述状态，所以是形容词。本章不要求掌握所有词类。

“修饰”是提供说明信息，例如a red book中red说明书是红色的，整个短语是“一本红色的书”。在这个短语中red放book前，不写a book red。本章先理解这种关系，不要求背诵全部句子成分。

### be、am、is、are：同一个词的不同写法

英语的一个词可能有不同写法。**这里的“形式”就是“同一个词在句子里使用的某种写法”，不是与原词毫无关系的另一个词。** 不同形式还可能表达时间或搭配的区别。用来在词表中列出一个动词的基本写法，叫**动词原形**。

**be是一个动词的原形，am、is、are是这个动词的其他形式。** 在本章，be这个词用于说“是谁／是什么”或“处于什么状态”。例如词表写be，实际说“我是学生”时写I am a student，而不是I be a student。be的拼写与am差别很大，这组变化需要按实际搭配认识，不能靠给be加几个字母推出来。

先看三个句子，下面逐个拆开：

1. **I am a student.** 我是一名学生。I＝我；这里am对应“是”；a＝一个；student＝学生。
2. **You are happy.** 你很开心。you＝你；happy＝开心的；are把“你”和“开心”连接起来，中文这里通常不另译一个“是”。
3. **She is a teacher.** 她是一名老师。she＝她；这里is对应“是”；a teacher＝一名老师。

在本章这些描述现在身份、状态的简单句中，按下面的搭配使用：

| 说的是谁 | 使用的写法 | 完整例句 |
|---|---|---|
| I（我） | am | I am happy. 我很开心。 |
| he／she／it（他／她／它） | is | She is happy. 她很开心。 |
| you／we／they（你／你们／我们／他们等） | are | We are happy. 我们很开心。 |

这不是“be永远写成am/is/are”的规则。这里先建立这组具体句子的搭配；表达过去、将来或其他结构时，会在相应章节学习其他写法。

### 先认识句子里的两个位置

**主语**是句子正在谈论的人或事物；**谓语部分**是对它的说明。在She is a teacher中，she是主语，is a teacher是谓语部分。其中is是动词，a teacher说明她的身份。

名词、代词是**词的类别**，主语是**在这句话里的工作**。例如Tom is happy（汤姆很开心）：Tom是名字，属于名词；它在这句话里作主语。I am happy中的I属于代词，也作主语。不能把“名词”和“主语”当成一个意思。

再看 **I like books. 我喜欢书。** I＝我，like＝喜欢，books在这里表示不止一本书。I是主语，like是动词，books是“喜欢的对象”，这个位置叫**宾语**。你现在只需知道book和books与数量有关，下一章会完整解释单数、复数和变化规则。

两类句子分开观察：I am happy需要am；I like books中的like本身已经是动词，不要另加am写成I am like books来表达“我喜欢书”。

### 只练本章已讲的否定

“否定”就是表达“不……”或“不是……”。not在本节表示“不”。在刚才的am/is/are句子中，把not放在am/is/are后面：

| 原句 | 否定句 |
|---|---|
| I am happy. 我开心。 | I am not happy. 我不开心。 |
| She is a teacher. 她是老师。 | She is not a teacher. 她不是老师。 |
| You are happy. 你开心。 | You are not happy. 你不开心。 |

先不缩写，按完整的not看清位置。本章不要求把I like books改成否定，也不要求自己给动词增加s；这些操作会在讲清所需规则后练习。

### 英语字母小常识：元音字母 vs 辅音字母（读后续词法内容前先认识）

26个字母中，**a、e、i、o、u**通常称为元音字母，其余21个通常称为辅音字母。这里是在给书写的字母分类：

- 元音字母：a、e、i、o、u。
- 辅音字母：b、c、d、f、g、h、j、k、l、m、n、p、q、r、s、t、v、w、x、y、z。

“辅音字母＋y结尾”表示y前面紧挨着的字母是辅音字母。例如city（城市）的y前是t；boy（男孩）的y前是o，所以属于“元音字母＋y”。下一章会用这个区别解释cities、boys。

字母的名字与单词中的声音不是一回事。字母A的名称不等于cat（猫）里a的声音；y在cry（哭）中也可以表示元音。**字母分类看拼写；元音／辅音声音的分类看发音，不能直接互换。** ch、sh是两个字母的组合，不是单个辅音字母；o仍是元音字母。

本章只验收：词与句子的区别、基本词类、be与am/is/are的关系、已给的搭配及not位置、简单主语和宾语、字母分类。练习只使用上面已经逐项说明的概念与操作。

'''

BRIDGES={
2:'''### 先把例句中要用的小词说清

**单数**表示一个，**复数**表示两个或更多：one book一本书，two books两本书。a/an在下面的例子里表示“一个”，the用于指双方能够确定的对象，如the book可理解为“这／那本已确定的书”；a/an/the这类词叫**冠词**。在名词前帮助明确“哪个／谁的／多少”的词，统称**限定词**，冠词是其中一类。本章先认识这些具体用法，选择a还是an的读音条件在冠词章实际展开，不作为本章的新判断任务。

many＝许多（后面通常接可数复数），much＝许多（接不可数用法）；some＝一些；any在本章例句中常表示否定、疑问里的“一些／任何”；a little＝一点，a few＝几个。它们叫数量表达，因为说明有多少。a piece of paper逐块理解是“一张＋纸”，two pieces of paper是“两张＋纸”。

例句里I have…表示“我有……”；There is/are…整组用于介绍“有……”。本章先按给出的is搭配单个或不可数内容、are搭配复数内容观察数量，不要求独立变换存在句。

“短语”是一组共同表达一个内容的词，如a red book；“修饰”是说明或限定对象，red说明book的颜色。下面的名词职位表是观察这些已经翻译好的例句：动作对象叫宾语，说明身份的部分叫表语，修饰名词叫定语，给同一个人补一个身份称呼叫同位语；本章不要求独立构造后面几类复杂句子。Tom, my brother, is tall意为“汤姆，我的兄弟，个子高”，my brother仍指Tom。

看数量时，不把“名词复数”和“动词搭配”混成一条规则：book→books表示书的数量；a book is / two books are是另一类搭配。family作整体或成员的不同表达会在下方例句就地说明。

''',
3:'''### 主格、宾格与介词：先看位置再记名称

“格”在这里表示代词因所处位置而有的不同形式：I like her（我喜欢她）中I作主语；She likes me（她喜欢我）中me作宾语。两句里的I、me都指“我”，不是不同的人。第一人称指说话的我／我们，第二人称指听话的你／你们，第三人称指被谈论的他／她／它／他们等。

本章会说“介词后用宾格”。先认识三个例子：for me＝给我／为我，with her＝和她，between you and me＝在你和我之间。for、with、between在这里表示关系，叫介词；把这些词和后面的对象合起来才得到相应关系。可以先完整使用for me、with her，不需要凭一个陌生词猜它是不是介词。

“缩写”是把已经明确的一组词写短，如it is→it's，撇号'标记省去的字母。its（它的）没有撇号，意思不同。本章的比较例句bigger than ours意为“比我们的更大”，ours代替our house；这里只检查所属形式，不要求自行构造比较级。

''',
4:'''### 元音字母与元音声音：本章判断所需的读音线索

上一章的字母是书写符号；**音素**是区别单词读音的基本声音单位。本章说“元音／辅音音素”，是在说声音类别。元音发音时气流通常较通畅；辅音发音时通常有阻碍或收窄。选择a/an要看紧接着的实际声音，不能只看首字母是不是a/e/i/o/u。

斜杠里的/j/是标记声音的**音标**，不是英文字母j的名称。这里不要求先读懂整套音标：下表已经给出本章和配套题用到的判断线索。

| 词及含义 | 本章已给的开头声音信息 | 本章用法 |
|---|---|---|
| book书、dictionary字典 | 辅音开头 | a book、a dictionary |
| apple苹果、orange橙子 | 元音开头 | an apple、an orange |
| hour小时、honest诚实的 | h在这里不发音，第一个实际声音是元音 | an hour、an honest person |
| useful有用的、university大学 | 第一个实际声音是辅音/j/，不要按u这个字母判断 | a useful book、a university |

第一次做题可依据这张已知信息表。未给读音、自己也不会读的新词，不能靠拼写可靠地推断a/an；本章验收不要求盲猜这种新词。a useful book看紧接a的useful，不跳过它去看book。

“限定词”是给名词限定范围、数量或所属的词：a book一本书、the book那本已确定的书、my book我的书、this book这本书。a/the、my、this在普通名词短语的这个位置不能任意叠放。first表示“第一”，best表示“最好的”，下文只用这些已给意思观察the first、the best的搭配。

''',
5:'''### 撇号、所属与名词修饰

所有格在本章表示“……的”。Tom's book＝汤姆的书，teachers' books＝老师们的书。'是撇号；先看拥有者是Tom一个人还是teachers多位老师，再按规则添加。它与it's＝it is这类缩写中的撇号用途不同。

名词作定语指一个名词说明另一个名词是哪种事物：a story book中story（故事）说明book的种类。复合名词是几个部分构成一个名称，如passer-by（过路人）；这些名称怎样变复数按下方实例学习。“谓语单数／复数”说的是动词与主语的搭配，不表示给动词加s就变成多个动作。

本章自测还有一条固定搭配：a good knowledge of English表示“熟悉英语／具备良好的英语知识”。knowledge在这个结构里与a good搭配，不据此推成所有普通“知识”用法都能直接加a。遇到具体固定搭配，要与一般材料、概念义区分。

''',
6:'''### 音节、重音与本章拼写条件

第1章已经用happy说明形容词描述“什么样”。本章把连接主语与身份／状态说明的动词用法称为**系动词**，如She is happy中的is；happy说明she，叫**表语**。The food tastes good＝食物尝起来不错，tastes在此起连接作用，good说明食物；不要因为动词在前就一律选副词。

**音节**可以理解为单词读音中的节拍，通常围绕一个元音声音组织。big（大的）一节，happy（开心的）两节，beautiful（漂亮的）三节。为了标出节拍，可写hap-py、beau-ti-ful；这不是实际单词的拼写，也不是按元音字母个数机械数音节。

**重音**是读一个词时某一节更突出。happy重在第一节，about（关于）重在第二节。后面遇到“重读”就是该节读得更突出。“闭音节”以辅音声音结尾；但看到闭音节三个字，不等于任何词尾都要双写。

本章big→bigger、hot→hotter这类常见双写：词尾相关音节重读，并呈现一个元音字母后接一个辅音字母的拼写；big→bigger/biggest，hot→hotter/hottest。clean（干净的）有两个相邻元音字母，short（短的）末尾有两个辅音字母，不能套成cleanner、shortter；词尾w/x/y通常也不这样双写。本章表格与题目使用已给出的词，不要求根据不会读的新词判断重音。双音节词也不能一律归为more类：happy用happier。

“不定代词”先看本章所需的三个词：something＝某件事／某物，anything＝任何事物，nothing＝没有什么。something important意为“某件重要的事”，important放在something后；这就是下面“修饰不定代词后置”的具体意思。afraid（害怕的）、asleep（睡着的）通常不直接放普通名词前，可说The baby is asleep（婴儿睡着了）；完整句中它们还可能有其他位置，不能概括成只准在系动词后。

''',
7:'''### 介词后的活动：先学会这一项用法

动词原形是词表里的基本写法，如read（读）、swim（游泳）。如果把活动当成谈论的内容，某些位置要换一种写法：read→reading，swim→swimming。by reading＝通过阅读，after swimming＝游泳之后；这里的reading、swimming是活动名称，叫**动名词**。它们与介词by、after合起来表达关系。

这就足够理解本章“介词后谈某项活动时常用-ing形式”：不能把by reading任意改成by read。不必先掌握全部非谓语功能，也不要反过来认为每一个-ing都是动名词。

look forward to整体表示“期待”，其中to在这个固定词组中是介词；I look forward to seeing you＝我期待见到你，seeing来自see（见到）。give up studying English＝放弃学英语，studying来自study（学习）。本章按整组搭配使用，不把所有to都当同一种用法。

because of the rain＝因为这场雨，后面是名词内容；because it rained＝因为下雨了，后面有it和rained这样的主语、动词结构。前者是介词短语，后者连接一句原因说明，称为连词用法。这两个例子直接说明区别，不要求提前掌握整套从句。

''',
8:'''### 数量、顺序、分数与时间的读法入口

one、two、three表示“一、二、三”的数量，叫基数词；first、second、third表示“第一、第二、第三”的顺序，叫序数词。分子是分数上面的数，分母是下面的数：2/3的分子是2，分母是3。2.5里的小点是小数点，读point；小数点后通常逐位读，2.5读two point five。

of在Two thirds of the water中把比例与“水”联系起来，整个表达是“三分之二的水”；对应is。换成students（学生们）对应are。这一组只应用已给的数量搭配，不把所有名词后都加s。倍数比较先确定参照：A是B的三倍表示A=3×B，优先用three times as…as明确表达。

''',
9:'''### 读懂动词形式和教学代号

第1章的“原形”是动词在词表中的基本写法：like、read、be。不同句子会用到likes、reading、am等形式，这些不是彼此没有关系的新词。do、doing、done在结构公式中经常是**代表实际动词形式的代号**：can + do可换成can swim（会游泳），不是必须写can do；have + done可换成have finished（已经完成）。实际单词do本身另有“做”的意思，要看是在写公式还是实际例句。

sb是somebody的缩写，代表“某人”；sth是something的缩写，代表“某事／某物”。explain sth to sb是一条搭配说明，换成实际内容可写explain the rule to me（向我解释这条规则）；不把sb、sth照抄进自己的实际句子。

帮助其他动词组成完整表达的动词用法叫**助动词**。先比较两个整体：I have a book＝我有一本书，have自己表达“有”；I have finished＝我已经完成，finished来自finish（完成），have与finished一起表达“已经完成”，这里have是助动词。finished在这个组合里叫过去分词，是finish的一种形式；它不意味着句中每个动词都在叙述过去。“进行”先看is reading＝正在读，“被动”先看The book was written by Tom＝这本书由汤姆写成。“时态变化”先看run→ran，ran可用来叙述过去的跑；这类名称分别说明时间关系和从谁的角度叙述。下面只据已给例句识别帮助组成表达的词，不要求独立选择所有时态或被动变换。

**补足语**补充说明一个对象：We made him happy＝我们让他开心，him是被影响的对象，happy说明him的状态，叫宾语补足语，简称宾补。“宾语和宾补有逻辑主谓关系”在这个例子里指happy说明him，不是说happy也是第二个被给出去的物品。SVOC是“主语、动词、宾语、补足语”四个位置的字母标签；下文先按已解释的例子识别，下一章系统对照句型。

助动词也可承接上下文中已经明确的内容：Do you like tea?＝你喜欢茶吗？Yes, I do＝是的，我喜欢。简答里的do承接前面的like tea，不另译“做”。这只是在识别已给问答，不要求在本章独立推导所有提问。have表示“有”时可见I have a book／She has a book，has是have与she这类主语搭配的写法；do也有does等形式，否定、提问章会按具体句子练操作。

''',
10:'''### 一个句子位置可以放一个词，也可以放一组内容

主语、宾语等是职位，名词、代词等是词类。短语是一组词；**分句**是围绕自己的主语和动词组织的单位。I know that she is here＝我知道她在这里，其中she is here带有自己的she、is；它作为“知道的内容”接在I know后，叫**从句**，不是另一个随意堆上的动词。

接下来职位表会列出几类尚未完整展开的形式，这里先给足本章识别所需的信息：

| 形式名称 | 在这几个例子中的意思和工作 |
|---|---|
| 不定式to read | to加read这样的动词原形；To read is useful＝阅读是有用的，to read整个作主语 |
| 动名词reading | 表示阅读活动；Reading is useful＝阅读是有用的，reading作主语；I enjoy reading＝我喜欢阅读，reading作宾语 |
| 分词 | 动词的一类形式，可在特定结构中说明对象；a broken cup＝一个破杯子，broken来自break（打破），说明杯子的状态 |
| 主语从句 | What he said is true＝他说的话是真的；what he said整个作为被谈论的内容 |

这里已给出各形式的意思与职位，练习只要求识别对应关系；独立选择复杂动词形式的操作在后面的专题中进行。主语／宾语之后“补充说明它是谁或什么状态”的部分叫补足语，下面会用两句话对照说明。

''',
11:'''### 先完整学会本章的否定和提问操作

陈述句是在说一个情况；否定句表示“不／不是”；一般疑问句是在问情况是否成立，常能用“是／否”回答。在下面先描述现在身份或平时习惯，不用陌生的过去形式操作。

动作词也会随搭配改变写法：I/you/we/they like，he/she/it likes；Tom相当于he，也用likes。“第三人称单数”指he/she/it或Tom这样的一个被谈论对象，不包含I（我）和you（你）。名词books的s表多本书，动词likes的s在这里标搭配，不表示多个喜欢。

对普通动作句，I like tea的否定是I do not like tea，提问是Do you like tea?；She likes tea的否定是She does not like tea，提问是Does she like tea?。do/does在这里帮助表示否定、提问，不另译“做”；用了does，后面的like用词表原形，不再重复写likes。do not常缩写don't，does not常缩写doesn't，is not常缩写isn't。提问时句首字母仍大写。

对am/is/are句子直接加not或把am/is/are放在主语前：She is happy→She is not happy→Is she happy?。对can（能／会）同样观察：She can swim→She cannot swim→Can she swim?，cannot可缩写can't。对问句Is she happy的简短回答是Yes, she is／No, she isn't。下面的表格据此实际操作。

“陈述语序”在本书常指主语在有关动词前的基本排列，如she is here；提问Is she here把is提前，叫疑问排列。Who is here?中who自己就是被询问的主语，不再另加do。

原分类例句还会出现过去的提问，这里先给出一个完整对照：I worked yesterday＝我昨天工作了；I did not work yesterday＝我昨天没工作；Did you work yesterday?＝你昨天工作了吗？worked是work叙述过去时的写法；did在否定和提问中帮忙，后面的work不再写worked；did not缩写didn't。完整过去时规则在第14章展开，本章只操作这个已演示的模式。将来存在句先给一个固定表达：There will be a meeting tomorrow＝明天将有一个会议，will be在这里表示“将会有”。

''',
12:'''### 名词的数量与动词的搭配分开看

| 句子 | 名词或代词表示什么 | 动词怎样搭配 |
|---|---|---|
| The boy plays. 这个男孩玩耍。 | boy，一个男孩 | plays在这里与一个被谈论的男孩搭配 |
| The boys play. 这些男孩玩耍。 | boys，多个男孩 | play与复数主语搭配 |
| I play. 我玩耍。 | I只有一位说话者，但属于第一人称 | 用play，不用plays |
| You play. 你玩耍。 | you可指一人或多人，但属于第二人称 | 都用play |

因此不能把“单数主语”一概等同于“动词加s”。本节描述习惯、一般情况时，普通动作动词的s主要对应第三人称单数；I、you是重要区别。be使用已经学过的am/is/are。主语后附带with me（和我一起）等内容时，先找真正被谈论的主语，而不是数离动词最近的单词。

''',
13:'''### 先分清时间、观察点与动词写法

这里的“时态”是本书整理时间表达的教学名称；同一件事可以从现在、过去或将来的位置观察。“参照时间”就是用来判断先后、持续的那个时间点；“完成”不是单说动作结束，而是从参照点回看此前情况；“进行”突出某时正在展开的过程。

| 形式名称 | 具体例子 | 先理解什么 |
|---|---|---|
| 动词原形 | go去、work工作 | 词表中的基本写法 |
| 第三人称单数形式 | goes、works | 本书已用she works说明这种搭配 |
| 过去式 | went、worked | 可在I went home昨天回家这类过去叙述中使用；went是go的不同写法 |
| -ing形式／现在分词 | going、working | 在is working中与is合起来表达正在工作；并非所有-ing都单独表示正在 |
| 过去分词 | gone、worked | 在has gone等组合中参与表达此前情况；名称中有“过去”不等于整个句子一定是一般过去时 |

“规则变化”指可以按常见拼写规则变，如work→worked；“不规则变化”指不能只套同一条拼写规则，如go→went→gone，要分开认识。过去式went与过去分词gone不能混填：She went home（她回家了）与She has gone home（她已经回家了）使用不同结构。公式里的done代表所用动词的过去分词，如write换成written。

现在完成时会用到for和since：for two years＝持续两年，给出时长；since 2020＝从2020年起，给出起点；不能把since two years当作“两年来”。下文会在完整句子中使用。

''',
14:'''### 过去动作句的操作顺序

was/were来自be，用于本章的过去身份、状态：I/she/he/it was，you/we/they were。动作词的过去式在词表列出，或按拼写规则变化，如work→worked、go→went。

I worked yesterday（我昨天工作了）否定为I did not work yesterday，提问为Did you work yesterday?；did在这里帮助否定、提问，后面的work恢复词表原形。did not缩写didn't。She was tired（她当时累了）则用She was not tired／Was she tired?，was not缩写wasn't，不再额外加did。

''',
15:'''### 把公式里的be换成实际搭配

will＋原形表示本章要学的将来表达：I will read＝我将读，will后不把read改成reads。be going to中的be不是照抄的字母串，要按说的是谁换成am/is/are：I am going to read，She is going to read，They are going to read。

will be reading说未来某时正在读，will have read从未来参照点回看此前的阅读，will have been reading着重到该参照点的持续过程。先找“明天几点／到周五为止”之类参照，再看下面每组例句的完整意思，不只数有几个小词。

''',
16:'''### 本章公式与已学形式的对接

can／must／should后面的do是“实际动词的原形”的位置：can read、must go、should rest，不能把公式理解成每句都写do。have done里的done是过去分词位置，如must have left，left来自leave（离开）；它与前面的must一起表达对先前情况的判断。

本章说“本应该做却没做”时，先按明确的中文情境理解should have done；不要求已经掌握整套“虚拟语气”的分类。对照used to work（过去常工作）与be used to working（习惯工作）：后者的to按第7章的介词用法，后接名词或活动内容；前者后接原形。这两组在本章已有具体搭配，不要求自行推导全部非谓语规则。

''',
17:'''### 特殊被动例句中省去的to是什么意思

to read这样的“to＋动词原形”叫不定式；在某些固定搭配中也用不带to的原形。主动句I saw him enter（我看见他进来）按see＋人＋enter这个搭配；相应的被动句是He was seen to enter（有人看见他进来）。在本节这些see／hear／make等常见结构中，转为被动后用to enter，而不是原样照搬enter。

这就是下文“被动时还原to”的具体操作。它受动词搭配限制，不能据此推成所有make／let／have或所有原形结构都能机械转换。playing来自play，是已见过的-ing形式：They saw him playing＝他们看见他正在玩，playing补充说明him的动作；变成He was seen playing时仍保留playing。

''',
18:'''### 先在已学句子里定位限定形式

“限定形式”是动词结构中承担本句时间、人称搭配等的部分：She is reading里is负责与she及本句时间搭配，reading不独自完成这件事。I know she works here里I know与she works here各有自己的主语和动词，是主从两个分句；She sings and dances则有并列的动作说明，不能只数整句有几个动词来判错。

to read、reading、written这些非限定形式已经在前面的具体例句里出现。本章把名称归纳起来；选形式仍要结合所在结构，不把“非谓语”理解为它们永远不能出现在谓语动词短语内部。

''',
19:'''### 连接词、短语与分句的边界

and在tea and coffee里连接两个名词；在I read and she writes里连接两个各有主语、动词的分句。because在I stayed home because it rained（我待在家，因为下雨了）中引出原因，because it rained是附属的从句；前面说明主要情况的I stayed home是主句。

所以“主句／从句”不是看谁的词更多，也不是看是否有逗号。本章先按明确的中文关系选择“而且／但是／因为／如果”等连接表达，再在下一章分类使用。

''',
20:'''### 判断从句关系所需的两个前提

时间参照与事件持续在第13章已有例子：I was reading表示当时的背景活动，the phone rang表示发生的电话铃响事件。while I was reading＝在我正在读的时候；这里先按这种持续背景理解while，而不是见到while就禁止所有短暂事件或其他意义。

普通条件If it rains tomorrow, I will stay home意为“如果明天下雨，我就待在家”：条件仍被当成现实可能性。as if表示“好像”，本章先看It looks as if it is going to rain（看起来好像要下雨），从句采用已经学过的将来表达。与事实不同的假设形式在其专题中完整讲解，本章不据它作独立验收。

''',
21:'''### 连接作用与从句内职位不是一回事

I know that she is here＝我知道她在这里。she是从句主语，is here已经说明她在哪里；that把这段内容接到know后，自己不代替“谁”或某个动作对象，这叫“只连接、不充当从句成分”。

对照the book that I read＝我读的那本书。I read后面“读什么”的位置对应book，that在这里把book与那个位置联系起来，属于修饰book的定语从句用法。现在用这组已解释的例子区分“说明消息内容”与“修饰哪个对象”，不要求提前掌握全部关系词选择。

whether和if在“是否”内容里有部分重合用法；if还可表示“如果”，不是每个if都是同一功能。具体句子按下方所在职位和例句判断。

''',
22:'''### 先行词与关系词的缺位检查

先行词就是被后面的从句说明的那个名词：the girl who works here中是girl；the book that I bought中是book。who对应“谁在这里工作”，在从句里作主语；I bought后“买什么”的位置对应book，that在从句里作宾语。判断依据是从句里面缺哪个职位，不是看句子长短。

“限制性”说明用哪些信息识别对象；“非限制性”在已确定对象之外补充信息，书面通常用逗号隔开。删除一段后是否仍合语法，不是唯一判断标准。

''',
23:'''### 转述中的说话者与参照时间

直接引语是保留原话：Tom said, “I will come tomorrow.”＝汤姆说：“我明天来。”转述是换成现在的叙述者说明内容：Tom said that he would come the next day。he指Tom；would从过去“说”的时点看之后的“来”；日期表达按实际叙述时点调整，不是把tomorrow永远机械换成the next day。

本章只把已经学过的时态和从句关系合起来使用。普通条件与时间背景可验收；需要先学习反事实假设才能决定的as if虚拟形式不纳入本章自测。

''',
24:'''### 形式主语与形式宾语先看一组替换

To read is useful＝阅读是有用的，to read整个作主语。把它放后面可说It is useful to read：it先占主语位置，后面的to read才说明“什么有用”，这叫形式主语，不是指前面某一本书。

I find it useful to read＝我发现阅读有用，it先占据宾语位置，to read说明具体活动，这叫形式宾语。to read和reading的基础含义在第10章已给过；这里识别谁占位、实际内容在哪里，不要求独立选择复杂完成或被动变体。

''',
25:'''### 本章开始完整选择非谓语形式

第7章已经用by reading说明“活动在介词后”的-ing用法，第10章已经用To read is useful说明to结构作主语。本章从已见例子归纳完整功能和搭配，而不再把这些写法当作第一次见到的新符号。

**逻辑主语**是“意思上是谁做这件事”，要与句子里实际的主语位置分开：I want to read中read的执行者是I；I want Tom to read中read的执行者是Tom。判断分词状语与独立主格前，先问这件事是谁做、由谁承受。

''',
26:'''### 完成形式表示相对先后

having finished表示该活动先于后面的参照活动；being repaired表示正在被修；having been repaired兼有“先前已经”和“被修”的关系。公式里的having、been、being都是具体形式，finished／repaired代表可替换的实际动词分词，不把它们全部等同于“过去时”。

独立主格的“独立”是带着自己的意思主体：Weather permitting（天气允许），天气与主句里的we不是同一个对象；普通分词状语Walking home, I met Tom中walk与met的执行者则都是I。

''',
27:'''### 先看整个主语的核心，再决定搭配

Reading books is useful中reading books整个活动作主语；the students who work here are friendly中主语核心是students，who work here只是说明是哪群学生。句子中出现多个动词不等于它们全部与同一个最近名词搭配。

本章使用的非谓语和关系从句都已讲过；遇到数量表达，先辨认谈的是“数量这个数值”还是“那群人／物”，再按例句核对。

''',
28:'''### 过去形式不总是在谈过去时间

I had time yesterday是在叙述昨天有空；If I had more time now, I would read more是在设想“现在时间更多”，had在这里表达与现实有距离的假设，不能一见过去形式就翻成过去发生。这是本章开始新增的判断要求。

wish表示愿望，if only表示“要是……就好了”；建议、命令、要求从句中的原形又是另一种结构。先按每组完整语境区别，不把“虚拟”当成一个只需统一换过去式的按钮。

''',
29:'''### 倒装与省略都先还原普通句

She has never seen it是普通排列，Never has she seen it把has放在she前，叫部分倒装；Here comes the bus把comes放在名词主语the bus前，叫完全倒装。主语是代词时的地点句Here it is仍用普通排列，这不禁止其他类别中代词参与倒装。

“省略”是在上下文已明确时不重复某些内容，如I'd love to后面可承接已知活动。先明确原本完整说法和所指内容，再判断本节允许省哪部分。

''',
30:'''### 构词与同一个词的变化分开

book→books仍是“书”这个词的数量变化；teach→teacher则形成表示“老师”的新词。前缀加在词前，如un＋happy；后缀加在词后，如teach＋er。词根在这里指承载主要意义的基础部分，不能靠一个熟悉词尾保证所有生词都猜对。

''',
31:'''### 先区分完整分句与句间关系

I was tired与I kept working各自有主语、动词，是两个可以独立表达的分句。but能把它们连接起来；however表达转折时通常还需要句号或分号安排：I was tired. However, I kept working／I was tired; however, I kept working。

本章要检查的不是“是否看见逗号”而是逗号两边分别在做什么。圆括号、撇号、连字符和引号在下文按实际用途区分。

''',
}


def insert_before(s,anchor,block):
    assert anchor in s,anchor
    return s.replace(anchor,block+anchor,1)


def revise_course(bodies):
    s=bodies[0]
    # 保留原先修的独有知识，移到读者已能理解的位置，不再用高级概览充当起点。
    table=re.search(r'### 八大句子成分 · 一眼看懂表\n[\s\S]*?(?=### 零基础最常见)',s).group()
    s=s[:s.index('> **本章入口：**')]+'> **本章入口：**从单词、句子和具体搭配开始。所有需要用来做题的名称，都在使用前解释。\n\n'+CHAPTER_ONE+'## 本章收束\n\n能说明be与am/is/are的关系，使用本章搭配和not，识别简单主语、宾语与词类后，再进入名词章。\n'
    s=s.replace('基础句型要能自己变换和写出，不能只在看答案时认识。','只变换本章已经演示的am/is/are否定，不要求提前处理普通动作句的否定、提问。')
    bodies[0]=s
    bodies[9]=insert_before(bodies[9],'### 什么是句子',table+'\n')
    # 原先修高级术语的知识在完成前提后归纳，保留to/doing、逻辑主语与SVOC内容。
    recap='''### 术语串联：词类、句子职位与逻辑关系

从句带自己的主语和动词结构，可以作另一结构中的内容或说明；to read是不定式，reading在作活动名称时是动名词。直接宾语是所给或所涉及的内容，间接宾语是接受者等，不能单凭“人／物”判定。宾补说明宾语：We made him happy中happy说明him，形成主语＋动词＋宾语＋宾补的SVOC框架；S、V、O、C分别是这些位置的字母标签。

逻辑主语是意思上的动作主体，不是“忽略全部语法”后凭感觉猜。状态动词如know、like、have在表示稳定状态时通常不用进行形式；实际用法还受词义变化和语境影响。这些原先提前列出的关系现在已有实例，不需要跳回先修表辨认。

'''
    bodies[24]=insert_before(bodies[24],'## 本章收束',recap)
    for n,bridge in BRIDGES.items():
        # 旧入口本身含有尚未定义的术语；不能把新解释仍放在它后面。
        bodies[n-1]=re.sub(r'^> \*\*本章入口：\*\*[^\n]*\n\n','',bodies[n-1],flags=re.M)
        pos=re.search(r'^### ',bodies[n-1],re.M)
        assert pos,n
        bodies[n-1]=bodies[n-1][:pos.start()]+bridge+bodies[n-1][pos.start():]
    # 名称的必要说明放到实际使用前，避免“先看术语、最后再见解释”。
    for i,s in enumerate(bodies):
        s=s.replace('（雨水，U）','（雨水，不可数；U是uncountable的缩写）').replace('（多场大雨，C）','（多场大雨，可数；C是countable的缩写）')
        if i>0:
            s=s.replace('基础句型要能自己变换和写出，不能只在看答案时认识。','按本章已经演示的步骤完成对应练习；用于说明当前知识点的例句，不额外验收尚未教过的其他规则。')
        s=s.replace('单数主语的一般现在时动作动词常加 s','第三人称单数主语的一般现在时普通动作动词常加 s')
        s=s.replace('单数主语 + 单数谓语（is/has/does/动词+s）','在本节第三人称单数的例句中，主语搭配is/has/does或动词+s；I和you按已经学过的特殊搭配判断')
        bodies[i]=s
    bodies[3]=bodies[3].replace('first表示“第一”，best表示“最好的”，下文只用这些已给意思观察the first、the best的搭配。','first表示“第一”，这类表示顺序的词叫序数词；best表示“最好的”，这种表达最高程度的形式叫最高级。下文只用这些已给意思观察the first、the best的搭配。')
    # 第一遍不把完整时态地图当作进入现在时态的门槛；16格移至全部16组已学后的23章。
    s=bodies[12];m=re.search(r'#### 16 种时态总表\n[\s\S]*?(?=\n---)',s)
    assert m
    grid=m.group();bodies[12]=s[:m.start()]+s[m.end():]
    overview='**核心规则**：时间有 4 种（现在、过去、将来、过去将来），状态有 4 种（一般、进行、完成、完成进行），4 × 4 = **16 种时态**。'
    assert overview in bodies[12]
    bodies[12]=bodies[12].replace(overview,'本章先学习常见的现在表达：习惯或一般情况、正在展开、与此前情况关联、持续的过程。每一组都配完整例句，完整时间组合读完后再汇总。')
    grid=overview+'\n\n'+grid
    bodies[22]=insert_before(bodies[22],'## 本章收束','### 已学时态的完整对照\n\n'+grid+'\n\n')
    timeline='''### 持续状态、单次事件与for／since

buy是“买到”这个事件，have可表达“拥有”状态。I bought the book two years ago＝我两年前买了这本书；I have had the book for two years＝我拥有这本书已经两年。join表示加入的事件；have been in the team for two years表示在队里这一状态持续两年。

教学中把某些单次发生的事件用法称为“瞬间”，把可持续的状态或活动用法称为“延续”。这里是在判断所表达的意义，不是说某个词在任何语境都不能与for/since同现。例如I haven't bought a book for two years＝我两年没买书，是否定一段时间内的购买，不能机械套“buy不能与for连用”。

'''
    bodies[12]=insert_before(bodies[12],'#### 现在完成时',timeline)
    # 去掉补充说明中“下章才懂”的循环提示，换成当下已解释的可执行范围。
    replacements={
      '瞬间动词（buy、join、leave）不能和 for/since 连用，要转化为延续性动词':'表达持续拥有、留在组织等状态时，应换成相应持续表达；次数统计、否定等其他语境不能机械套用这一限制',
      '**瞬间动词**（buy、join、leave）不能和 for/since 连用，要转化为延续性动词':'本节若要表达持续状态，buy、join等单次事件应换成相应状态表达',
      'while 引导的从句必须用延续性动词':'本节while表示时间背景时常描述持续活动；它也可表示对比、让步等，不能把本条当作全部while用法的禁令',
      'while 引导的从句必须用延续性动词，不能用瞬间动词':'本节时间背景用法常描述持续活动；不要推广成所有while用法都禁止短暂事件',
      '表语形容词只放系动词后':'afraid、asleep等在本节作表语；它们还可按搭配作补语或后置修饰语，不宜直接前置普通名词',
      '从句**用陈述语序**':'本节普通内容从句按主语在前的陈述排列；其他类别还有专门结构',
    }
    for i,s in enumerate(bodies):
        for a,b in sorted(replacements.items(),key=lambda x:-len(x[0])):s=s.replace(a,b)
        bodies[i]=s
    # 用现实可能的方式从句教学，不在20/23章提前检验反事实形式。
    bodies[19]=bodies[19].replace('5. as if 表"好像"，从句常使用虚拟语气。','5. as if 表“好像”；本章先按已给语境使用陈述形式。')
    bodies[19]=re.sub(r'- as if 引导的从句常使用虚拟语气。例：[\s\S]*?这里先记住[^\n]*', '- as if表示“好像”：It looks as if it is going to rain. 看起来好像要下雨。本节依据现实迹象，不考非真实假设的形式选择。',bodies[19])
    # 原第23章的超前自测改为已经学习的过去背景；对应虚拟知识仍完整保留在第28章。
    from 内容校订 import fix_questions
    bodies[22]=fix_questions(bodies[22],23,0,{13:('While I ______ a book, the phone rang. (was reading / will read / am reading)（表达过去正在阅读时电话响了）','was reading（过去进行表示当时正在展开的背景活动；不使用尚未学习的虚拟形式作本章判断）')})
    # 对于尚未建立的分类名称，用当前情境本身表述，正式名称留在第28章。
    bodies[15]=bodies[15].replace('本应/本不该"的虚拟意味','本应/本不该"的未实现评价').replace('本应/本不该\"的虚拟意味','本应/本不该\"的未实现评价')
    bodies[15]=bodies[15].replace('是虚拟用法','是在评价先前没有发生的事').replace('表推测与虚拟','表过去推测与未实现情况').replace('虚拟体系有联系','后面的假设体系有联系').replace('虚拟语气','假设与愿望表达').replace('“虚拟语气”','“假设与愿望表达”')
    bodies[15]=bodies[15].replace('虚拟意味','对未实现情况的评价')
    bodies[22]=bodies[22].replace('需要先学习反事实假设才能决定的as if虚拟形式不纳入本章自测。','本章的题目不要求使用尚未建立的假设规则。').replace('不使用尚未学习的虚拟形式作本章判断','本题只检查已经学过的时间背景')
    bodies[22]=bodies[22].replace('间接引语和虚拟语气','本章的过去视角转述').replace('间接引语和虚拟语气中','本章的过去视角转述中')
    # 第3章只教代词，不要求在讲问句前独立生成问句。
    bodies[2]=bodies[2].replace('再把 She is happy 改为否定和一般疑问句。','再按第1章已演示的not位置，把She is happy改为否定句。')
    bodies[2]=bodies[2].replace('She is not happy.／She isn’t happy.；Is she happy?','She is not happy. 后面会专门学习缩写和提问操作；这里先完整写not。')
    # be used to do的被动辨析移到被动章；保留原有知识与例句关系。
    for i in [15]:
        bodies[i]=bodies[i].replace('；be used to do：被用来做某事（被动）','')
    passive='''### be used to do与习惯表达的区别

A knife is used to cut bread＝刀被用来切面包。这里used是use（使用）的过去分词，is used构成已学的被动，to cut说明用途；be按主语和时间换成相应写法。它不同于第16章be used to doing（习惯于做），例如I am used to reading＝我习惯阅读；也不同于used to read（过去常读）。

'''
    bodies[16]=insert_before(bodies[16],'## 本章收束',passive)
    # 早期原自测也补全句意，替换原先要求后章规则的少数操作。
    from 早期自测释义 import revise as revise_early_questions
    for n in [5,6,8]:bodies[n-1]=revise_early_questions(bodies[n-1],n)
    bodies[8]=bodies[8].replace('基本助动词有三个：be、do、have，必须和实义动词搭配使用','基本助动词有be、do、have等；完整表达中与相关动词形式组合，上下文明确的简答可省去已知部分')
    bodies[8]=bodies[8].replace('助动词不能单独作谓语，后面必须接动词原形或分词','完整表达中助动词与相应动词形式组合；简答中可承接已知内容，如Yes, I do，不要求把后续内容每次重复写出')
    # 已解释的先修现在明确承接，不再用“暂按、先混眼熟”代替定义。
    bodies[9]=bodies[9].replace('例句中的 have done 暂按完成结构理解，be doing 按进行结构理解，后面逐一展开。','本章先识别整组内容放在哪个位置；下面会就地解释涉及的形式。')
    bodies[23]=bodies[23].replace('to read 暂按“阅读这件事”理解，下一章展开。','to read就是前面已经解释过的“to＋动词原形”结构，在这里表达阅读这件事。')
    return bodies
