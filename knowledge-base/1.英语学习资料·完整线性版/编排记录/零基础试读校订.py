"""前六章顺序试读后的定点校订；保留旧文快照，供生成器及差异核验共同使用。"""
from pathlib import Path
import re
import json
import hashlib

RECORD = Path(__file__).resolve().parent
ROOT = RECORD.parent
CHANGES = []

def add(n, old, new, reason='补充第一次使用时所需的解释'):
    CHANGES.append(dict(章=n, 原文=old, 新文=new, 原因=reason))

add(1, '你现在只需知道book和books与数量有关，下一章会完整解释单数、复数和变化规则。', '同样，student是“学生”，students在本章练习中表示不止一名学生。你现在只需认识这两组写法与数量有关，下一章会完整解释单数、复数和变化规则。', '练习先出现students，正文先给出含义')
add(2, 'many＝许多（后面通常接可数复数），much＝许多（接不可数用法）；', '先认识“可数／不可数”：英语里book（书）可以直接说one book、two books，这种用法叫可数；water表示水这种物质时，不直接按“一个水、两个水”来数，这种用法叫不可数。可数性看英语的习惯，不能只凭中文能否说“一条、一个”来判断。\n\nmany＝许多（后面通常接可数名词的复数，如many books，许多书），much＝许多（接不可数名词，如much water，许多水）；', '先定义可数性再使用数量词规则')
add(2, '动作对象叫宾语，说明身份的部分叫表语，修饰名词叫定语，给同一个人补一个身份称呼叫同位语；', '动作或感受涉及的对象叫宾语；在He is a doctor（他是医生）中，a doctor说明主语身份，叫表语；在a story book（一本故事书）中，story说明是哪类书，叫定语；给同一个人补一个身份称呼叫同位语；', '用已译例子解释句子成分')
add(2, '一句话记住：**能放进"这是____"空档里的词，多半是名词。**', '先看词在句中表示什么：book给事物命名，happy描述状态。不要只套中文“这是……”来判断英语词类。', '移除不可靠的中文套空判断法')
add(2, '- 中文里"美""聪明"这些是形容词，英语里 beauty、smartness 才是名词，别用混；', '- beautiful（美丽的）、smart（聪明的）描述特点，是形容词；beauty（美）、smartness（聪明）给这些特点命名，是名词。英语中的写法和用途要一起看；', '用英语词与中文释义比较')
add(2, '| 主语 | 动作的发出者 | **The dog** runs. 狗在跑。 |', '| 主语 | 句子正在谈论的人或事物 | **The dog** runs. 狗在跑。 |', '与第一章主语定义保持一致')
add(2, '| 宾语 | 动作的承受者 | I like **music**. 我喜欢音乐。 |', '| 宾语 | 动作或感受涉及的对象 | I like **music**. 我喜欢音乐。 |', '避免把喜欢的对象解释为承受动作')
add(2, '- 一个名词在句中只能同时担任一个主要成分（主语或宾语），不能"既当主语又当宾语"；', '- 同一个名词在不同句子里可以承担不同工作：Dogs like music（狗喜欢音乐）中Dogs作主语；I like dogs（我喜欢狗）中dogs作宾语。词类仍然是名词；', '去掉容易引起误解的抽象禁令')
add(2, '专有名词是独一无二的名字（要大写）', '专有名词是给特定的人、地点等起的名字（按名称规则大写，如Tom、Beijing）', '专有名称不等于世上唯一')
add(2, '（专有：节日，由普通词组成，要加 the）', '（专有：节日；the Spring Festival是惯用名称）', '避免把名称组成误当冠词规则')
add(2, '\t- 普通名词：wall（墙）、spring（春天）、festival（节日），单独用泛指； 组合后 the Great Wall（长城）、the Spring Festival（春节），变成**特定、唯一的事物**，就要加 the。', '', '删除与上条规则相矛盾的说明')
add(2, '不可数名词不能按个算（不能说 one water）', '不可数用法不直接按个数表达（water表示水这种物质时，不说one water；点单中的“一份水”用法在后面另讲）', '避免后文按份计量与本段打架')
add(2, '不可数名词**没有复数**，不能加 s，不能用 a/an，不能用数字直接修饰。', '名词**在不可数用法中**不变复数，不直接用a/an或数字修饰；某些词换了含义以后可以有可数用法，后面会逐项比较。', '区分一个词与它的具体用法')
add(2, '> 💡 这里 **is = 单数动词、are = 复数动词**（它们都是 be 动词的一种形式）。单数主语（把 family 当一个整体）用 **is**；复数主语（把 family 当里面的成员们）用 **are**。这条"主语单数 → is、主语复数 → are"的搭配规则叫**主谓一致**，本路线第 12 章将完整说明基础主谓一致。这里先记住：**is 配单数、are 配复数**即可。', '> **主谓一致**指动词形式要与主语相配。这里family指一个家庭整体时用is；在英国英语中，把家人作为多个成员来谈时也可配are。are watching TV整组意为“正在看电视”，此处只观察family与are的搭配。不要把这里的规则扩成“任何单个人都用is”：第1章的I am、you are仍然成立。', '解释术语，消除与I和you搭配的冲突')
add(2, '单数（one）和复数（many）', '单数（一个）和复数（两个或更多）', '复数不等于许多')
add(2, '| 以 s/x/ch/sh/o 结尾 | 加 es | bus→buses、box→boxes、watch→watches、dish→dishes、tomato→tomatoes |', '| 以s/x/sh结尾，以及watch这类ch结尾 | 通常加es | bus→buses、box→boxes、watch→watches、dish→dishes |\n| 以o结尾 | 有的加es，有的加s，随词记忆 | tomato→tomatoes；photo→photos |', '表格本身明确o词尾差异')
add(2, '| 以 f/fe 结尾 | 多数变 ves | leaf→leaves、knife→knives、wife→wives |', '| 以f/fe结尾 | 部分变ves，部分直接加s，随词记忆 | leaf→leaves、knife→knives、wife→wives；roof→roofs |', '去掉无法机械套用的多数规则')
add(2, '| 元音变化 | man→men、woman→women、foot→feet、tooth→teeth、goose→geese、mouse→mice |', '| 词中部分字母改变 | man→men、woman→women、foot→feet、tooth→teeth、goose→geese、mouse→mice |', '避免读者把音素变化误当拼写操作')
add(2, '**通俗定义**：变化不符合规则、需要单独记忆的复数形式。', '**通俗定义**：不按前面常见加s/es办法变化、需要随词记忆的复数形式。下表的“单复数同形”指一个、多个都用同样写法；“复合名词”指由几个部分组成一个名称，如passer-by（过路人）、mother-in-law（婆婆／岳母）。其中表达主要对象的名词叫主体名词：passer-by中的passer表示过路的人。', '先解释表中分类术语')
add(2, '- 只有复数形式的名词，计数要用 a pair of，如 a pair of trousers，不能说 a trousers；', '- trousers（裤子）、glasses（眼镜）、scissors（剪刀）常按一条／一副／一把计量：a pair of trousers（一条裤子）、two pairs of trousers（两条裤子）。clothes（衣服）、goods（货物）也常用复数，但不因此一律配a pair of；', '限定pair的适用对象')
add(2, '**同一个词，泛指时不可数，一旦表"具体的一件/一份/一场/多场"，就变成可数**', '**有些词既有不可数用法，也有习惯形成的可数用法，需要连同含义一起学；不能自行把任何具体事物都改成可数**', '防止把特指与可数混为一谈')
add(2, '规律一句话：**当作"整体/泛指的材料或概念"时不可数；当作"能数出来的一件/一份/一场/一个"时可数。**', '下面逐词比较两种含义。注意：the water in this cup（这个杯子里的水）已经很具体，water仍不可数；“具体”本身不能决定可数性。', '用反例解释可数性与确定对象的区别')
add(2, '| 词 | 泛指时（不可数） | 具体时（可数） |', '| 词 | 不可数用法及含义 | 可数用法及含义 |', '表头不再暗示泛指等于不可数')
add(2, '关键是看它在句子里是"整体/材料"还是"具体的一件/一份/一场"', '要看当前含义是否具有英语中已有的可数用法', '清除同段重复误导')
add(2, '**核心规则**：量词 = "计数的单位 + of + 不可数名词"。', '**量词**在这里指计量单位表达，例如a glass of water中的a glass of表示“一杯”。of把单位和内容连起来；两杯是two glasses of water，变的是glass（杯），不是water（水）。\n\n**核心规则**：这里的计量表达 = "计数的单位 + of + 不可数名词"。', '解释of连接作用与计数对象')

add(3, '两句里的I、me都指“我”，不是不同的人。', '两句里的I、me都指“我”，不是不同的人。作主语的这一组写法叫**主格**，作宾语的这一组写法叫**宾格**。She likes me中的likes仍表示“喜欢”，是like在这里与she搭配的写法；本章练习中的helps表示“帮助”，也已给出写法，暂不要求自行推导词尾变化。')
add(3, '本章会说“介词后用宾格”。', 'and表示“和”，可把两个对象连在一起：Tom and I＝汤姆和我，you and me＝你和我。\n\n本章会说“介词后用宾格”。', '先解释练习中合并主语用的and')
add(3, '**核心规则**：下表按常见用途介绍代词，后续小节会分别说明；不同语法体系的分类方式可能有所不同。', '这张图用于定位。本章依次学习人称、物主、反身、指示、疑问、相互六类；不定代词等后续用法在第24章展开，当前不用凭名称猜规则。', '修正总览声称本章会教完全部分类')
add(3, '| 人数 | 单数主格 | 单数宾格 | 复数主格 | 复数宾格 |', '| 人称 | 单数主格 | 单数宾格 | 复数主格 | 复数宾格 |', '表头准确命名')
add(3, '1. **主格作主语**，放在动词前；\n2. **宾格作宾语**，放在动词或介词后。', '1. 本章普通陈述句中，**主格作主语**，通常在动词前，如I love you；\n2. **宾格作宾语**，本章例句中在动词或介词后，如I love you中的you、for him中的him。先看句中工作，再选写法，不把位置口诀套到所有句型。', '避免把常见顺序当普遍定义')
add(3, '- 多人并列时，**单数顺序：你、他、我**：You, he and **I** are good friends.；', '- 用and连接多个人时，常出于礼貌把“我”放后面：Tom and I are friends（汤姆和我是朋友）。这里Tom and I相当于we，所以用are；顺序习惯不是主格、宾格的判断依据；', '解释并列主语并直接支撑本章题目')
add(3, '- 第三人称单数有性别区分：男的 he、女的 she、物/动物 it，中文都用"他"，要分清。', '- he通常指“他”，she通常指“她”，it可指事物或动物；谈熟悉且知道性别的动物时也常用he或she。', '修正错误中文对应')
add(3, '| 它 | its | its |', '| 它 | its | 通常不用独立形式；保留its后面的名词 |', '不把少见独立its作为基础常用对应')
add(3, 'mine = my book。', '在谈书时mine相当于my book；谈钢笔时则相当于my pen。不是mine永远只表示“我的书”。', '说明替代内容由语境决定')
add(3, '| 单数 | -self | 复数 | -selves |\n|---|---|---|---|\n| myself 我自己 | yourself 你自己 | ourselves 我们自己 | yourselves 你们自己 |\n| himself 他自己 | herself 她自己 | themselves 他们自己 | |', '| 对应人称 | 单数：一个人或事物 | 复数：多个人或事物 |\n|---|---|---|\n| 第一人称 | myself 我自己 | ourselves 我们自己 |\n| 第二人称 | yourself 你自己 | yourselves 你们自己 |\n| 第三人称 | himself 他自己；herself 她自己；itself 它自己 | themselves 他们／她们／它们自己 |', '重排错位表格并补itself')
add(3, '1. 表示"主语自己做了某事"：I did it myself.；\n2. 常搭配固定短语：by oneself（独自）、enjoy oneself（玩得开心）、teach oneself（自学）。', '1. 动作对象与主语是同一个人：She helps herself（她帮助自己），herself仍指she；若写She helps her，her通常指另一位女性；\n2. 强调亲自做：Tom makes the toy himself（汤姆亲自做这个玩具）。makes the toy意为“做这个玩具”，himself强调是汤姆亲手做的；\n3. 固定短语中的oneself是占位写法，要随人换成myself、yourself等：by myself＝我独自，by herself＝她独自；enjoy oneself表示玩得开心，teach oneself表示自学。', '同时示范反身与强调，解释oneself而非只列名字')
add(3, 'She learned to cook **by herself**. 她自学了做饭。', 'She learned to cook **by herself**. 她独自学做饭。', 'by herself不必然等于无人教授')
add(3, '**These** flowers are more beautiful than **those** in the garden. 这些花比花园里的那些好看。', '**These** are flowers and **those** are trees. 这些是花，那些是树。', '指示代词用已学be句示范，比较结构留第六章')
add(3, '- **电话里**介绍自己用 This is...，问对方用 Is that...，不说 I am...；', '- **电话里**常用This is…介绍自己，如This is Tom（我是汤姆）；确认对方身份可用Is that…? 这是常见电话表达，不表示I am在任何电话情境都不能使用；', '取消不成立的绝对禁令')
add(3, '**疑问代词用来构成特殊疑问句，放在句首提问：who、whom、whose、what、which。**', '**询问“谁、什么、哪一个”等具体信息的问题，叫特殊疑问句。** who（谁）、whom（谁，用作宾语）、whose（谁的）、what（什么）、which（哪一个）是本节的疑问代词。先看Who is she?（她是谁？）：who询问身份。下面先辨认提问词和整句意思，问句的完整构造在第11章学习。', '第一次使用特殊疑问句前给出解释')
add(3, '- **介词后面只能用 whom**：With **whom** did you go? 不用 who；\n- who 和 whom：who 作主语（Who is coming?），whom 作宾语，口语中 who 常替代 whom，但书面/介词后仍用 whom。', '- 询问人、并把介词直接放在疑问代词前时，正式表达用whom：With whom did you go?（你和谁一起去的？）。这不是说所有介词后都只能跟whom；\n- 普通交谈里常用who代替宾语whom，如Who did you go with?（你和谁一起去的？）。本章先认出两句都在问“和谁”，不要求自己调整问句顺序。', '区分人称对象、正式用法与口语')
add(3, '- 有所有格形式：each other\'s（彼此的），如 They know each other\'s names.', '- 表示“彼此的”时加\'s，写each other\'s；这种表示所属的写法叫**所有格**。They know each other\'s names＝他们知道彼此的名字。They help each other（他们互相帮助）里没有“的”，不要加\'s。', '先解释所有格并对照练习错误')

add(4, '上一章的字母是书写符号；', '第1章讲过，字母是书写符号；', '修正前章指代')
add(4, '**冠词（article）是放在名词前的小词，告诉读者"这是特定的那个（the）还是随便一个（a/an），还是泛指（零冠词）。"**', '**冠词（article）是名词前的一类词，包括a、an、the；不加冠词的用法叫零冠词。**\n\n先把两个常用术语说清楚：**特指**是让对方能确定说的是哪个对象；**泛指**是不指定某一个对象，或谈整个类别。I have a book（我有一本书）没有说明是哪本；The book is new（那本书是新的）接着说刚才那本；Books are useful（书有用）谈的是书这一类。a/an和零冠词都能用于泛指，不能把“泛指”等同于“不加冠词”。', '补泛指特指定义，消除错误一一对应')
add(4, '**the 表示特指，指代特定的人或事物（双方都知道、上文提过、有后置定语限定）。**', '**the常用来表示双方能确定的对象。** 可以是刚提过的对象，也可以由眼前情境确定。The book on the desk（桌上的那本书）中，on the desk意为“在桌上”，放在book后说明是哪本，这叫后置定语。后置说明不自动要求the：a book about music（一本关于音乐的书）仍可用a。', '就地解释后置定语并纠正机械冠词规则')
add(4, '3. This is **the** best movie I have seen. 这是我看过的最好的电影。（最高级）', '3. This is **the** best book. 这是最好的书。（best表示最好的）\n   his best friend＝他最好的朋友，已有his（他的）就不再加the，不写his the best friend。', '去掉未学完成时从句并支撑C08')
add(4, '- 第一次提用 a/an，再次提用 the：I saw a dog. **The** dog was big.', '- 首次引入一个未确定的对象常用a/an，随后说同一个对象常用the：I have a dog. **The** dog is big.（我有一条狗。那条狗很大。）首次提及但双方已经知道指谁时，也可以用the。', '不用过去式承担最初示范，说明初次再次不是机械规则')
add(4, '- 特指三餐时要加 the：The lunch we had today was delicious.；', '- 说特定的一餐时常用the：The lunch is delicious（这顿午餐很好吃）；说日常吃早餐、午餐、晚餐常用have breakfast／lunch／dinner，不加冠词。；', '简化长例句并补练习中的breakfast')
add(4, '**易错误区**：\n- 特指三餐时要加 the，如 The lunch we had today was delicious。', '**易错误区**：\n- 特指某一餐常用the，如The lunch is delicious（这顿午餐很好吃）；已有my等限定词时不用再加the。', '归纳与正文保持同一解释')
add(4, '| 单数可数 | ✅ a book | ✅ the book | ❌ |', '| 普通单数可数名词短语 | ✅ a book | ✅ the book | 通常需a/the/my/this等限定词；my book没有冠词但有限定词 |', '表格不把无冠词与无限定词混为一谈')
add(4, '表泛指、表数量一、表每一。', '可以表示未确定的一个、数量一，或“每一”：an apple一个苹果；once a day每天一次（once＝一次，day＝天）。', '给每一用法实际例子')
add(4, '（球类）\n\n**易错误区**', '（球类；tennis表示网球，play tennis也不加冠词）\n\n**易错误区**', '补练习中的tennis意思')

add(5, '> 本章是名词与冠词的配合要点，完整冠词规则见总索引 1.1.8。', '本节接着第4章复习名词与冠词的搭配，所需规则在这里直接列出。', '移除旧体系失效编号')
add(5, '**通俗定义**：名词作主语时，它的单复数决定谓语动词用单数还是复数。', '**主谓一致**是动词形式与主语相配。先用已经熟悉的be比较：The student is happy（这个学生很开心）；The students are happy（这些学生很开心）。变的是student／students和与之搭配的is／are。\n\n本章还需要认识普通动词的一种搭配：描述现在的一般情况时，主语为he、she、it或一个人／事物，称为**第三人称单数**；常见写法是动词加s，如I like books（我喜欢书）与She likes books（她喜欢书）。同样，I help her（我帮助她）与Tom helps her（汤姆帮助她）；I speak English（我说英语）与He speaks English（他说英语）。这里的likes、helps、speaks不是复数名词。have（有）与第三人称单数搭配时写has；do（做）写does。更多拼写和时间用法在动词章节展开。', '先演示is/are，再补练习确实要用的第三人称词尾')
add(5, '1. The **student has** finished. 这个学生完成了。（单数）\n2. The **students have** finished. 学生们完成了。（复数）', '1. The **student has** a book. 这个学生有一本书。（has在这里表示“有”）\n2. The **students have** books. 这些学生有书。（have在这里表示“有”）', '用所有关系例句替换未教完成时')
add(5, '- 完整主谓一致规则（就近、就远原则）见总索引 6.1。', '- 本节先掌握普通单数、复数主语的搭配；多个成分共同作主语等情况在第12章继续讲。', '去掉没解释的术语和失效索引')
add(5, '- people、police、cattle 形式上是单数词，但意义是复数，谓语用复数；', '- people（人们）、police（警察群体）、cattle（牛群）虽然没有复数s，按这里的含义仍搭配复数动词；不要只看结尾有没有s；', '不用单数词概括复数集合名词')
add(5, '- the boy\'s books（男孩的书）和 the boys\' books（男孩们的书）意思不同，\'s 位置要看单复数。', '- the boy\'s books（男孩的书）和 the boys\' books（男孩们的书）意思不同，撇号位置要看单复数。\n- 前面已经说清是哪件东西时，所有格后面的名词可以省去：This is Tom\'s book → This book is Tom\'s（这本书是汤姆的）。这里保留Tom\'s，不是改成Tom。\n- 所有格已限定后面的名词，不再在最前加a：my father\'s book（我爸爸的书），不写a my father\'s book。', '补Tom所有格省略与冠词配合，支撑C07和C10')
add(5, '- a friend of my father（我爸爸的朋友，可能唯一）和 a friend of my father\'s（我爸爸朋友中的一个）语气不同，教学上常用后者。', '- a friend of my father与a friend of my father\'s都可以表达“我爸爸的一位朋友”，不能由这两种写法推断爸爸到底有几位朋友。\n- a picture of Tom通常指画面里的汤姆；a picture of Tom\'s指属于汤姆的一张照片，画面里不一定是汤姆。', '不把所有格形式解释成实际人数证明')
add(5, '他是我爸爸的一个朋友。（不是唯一的）', '他是我爸爸的一位朋友。（表达所属关系）', '清除同段人数断言')
add(5, '这些"拟人化"所有格是习惯用法', '这些所有格表示时间、距离或其他关联，不要求事物有生命', '免除不必要拟人化概念')
add(5, 'a **sales** man（salesman）', '**sales** figures（销售数字）', '用真正词组示范复数名词作定语')
add(5, '| 规则复数 | 一般加 s；s/x/ch/sh/o 加 es；辅音+y 变 ies；f/fe 变 ves |', '| 规则复数 | 一般加s；s/x/sh及watch这类ch结尾加es；辅音+y变ies；o、f/fe结尾随词记忆 |', '速查表与已修规则一致')
add(5, '| 只有复数 | trousers、glasses、scissors、clothes，用 a pair of |', '| 常用复数形式 | trousers、glasses、scissors常用a pair of计量；clothes不套用a pair of |', '防止复盘重新引入pair误用')
add(5, '1. 以 -f/-fe 结尾：多数变 f/fe 为 ves，如 leaf→leaves、knife→knives，少数直接加 s，如 roofs、beliefs；', '1. 以-f/-fe结尾：部分变ves，如leaf→leaves、knife→knives；部分加s，如roof→roofs、belief→beliefs，随词记忆；', '归纳规则保持准确')
add(5, '2. 以辅音字母+o 结尾：一般加 es，如 potato→potatoes、tomato→tomatoes，外来词直接加 s，如 photos、pianos；', '2. 以o结尾：potato→potatoes、tomato→tomatoes加es，photo→photos、piano→pianos加s；不能只凭o前字母或是否外来词推断；', '不要求零基础识别词源')
add(5, '- 只有复数形式的名词不能直接加 a/an，需用 a pair of。', '- trousers、glasses、scissors等成对物品可用a pair of计量；clothes等其他复数词不能照搬这个搭配。', '清理复盘中的同类错误')
add(5, '> 💡 上面例子里的 **is / are**：is = 单数动词，are = 复数动词（都是 be 动词的一种形式）。把 family/class 当一个整体用 **is**，当"里面的成员们"用 **are**——这条"主语单复数配 is/are"的规则叫**主谓一致**，到 6.1 主谓一致 会系统讲。这里先记住"**单数主语用 is、复数主语用 are**"即可，别被它卡住。', '> 上面family/class谈一个整体时用is；英国英语强调多个成员时也可用are。这里的are having a discussion整组意为“正在讨论”。这组例子不能取代已学的I am、you are搭配。', '避免复盘覆盖正确先修搭配')
add(5, '21. ✅ knowledge 前可用 a（表"某方面的知识"），具体化', '21. ✅ a good knowledge of English是本章已给的固定搭配，表示熟悉英语；不据此推成所有knowledge都能直接加a', '答案解释与正文限制一致')

add(6, '**核心分类**：时间、地点、方式、程度、频度、疑问、连接副词。', '**时间**回答何时（later＝稍后），**地点**回答何地（here＝这里），**方式**回答怎样做（quickly＝迅速地），**程度**回答多大程度（very＝很），**频度**回答多久做一次（often＝经常）。用于提问的how（怎样）等叫疑问副词；连接前后意思的however（然而）等叫连接副词。先把名称与具体作用对应起来。', '副词分类不只列术语')
add(6, '- 感官系动词后接形容词：', '- 表示感官感受、并把主语与特点连接起来的动词用法叫**感官系动词**，如taste（尝起来）、smell（闻起来）、look（看起来）。这些用法后接形容词：', '就地解释感官系动词')
add(6, '2. 以 y 结尾变 y 为 i 加 ly：happy → happily；', '2. happy这类辅音字母+y结尾的常见词，变y为i再加ly：happy → happily；并非所有y结尾词都照搬，如shy → shyly；', '不把happy的变化套到所有y')
add(6, '4. 不规则：good → well、bad → badly。', '4. 不规则对应：good → well；bad → badly是直接加ly的规则例子。', '修正错误分类')
add(6, '| 重读闭音节 | 双写末字母 + er/est | 同左 | big → bigger → biggest |', '| big/hot这类重读且以一个元音字母加一个辅音字母收尾 | 双写末辅音字母 + er/est（w/x/y通常除外） | 同左 | big → bigger → biggest；short不双写 |', '表格保留开头已说明的双写条件')
add(6, '| 多音节 | more + 原级 | most + 原级 | beautiful → more beautiful → most beautiful |', '| 三个及以上音节通常用此法；不少双音节词也用此法 | more + 原级 | most + 原级 | beautiful → more beautiful → most beautiful；careful → more careful → most careful |', '避免把双音节happy误归另一规则')
add(6, '| as...as / not so...as | 和……一样/不如…… | She is as tall as her mother. |', '| as + 原级 + as；否定用not as/so + 原级 + as | 和……一样／不如…… | She is as tall as her mother. 她和妈妈一样高。 |', '补两个as之间的具体填法')
add(6, '3. 常接不定式：old enough to go to school。', '3. 表示“足够……，可以做某事”时，用“形容词 + enough + to + 动词原形”：old enough to go to school（年龄够大，可以上学）。to go这类“to + 动词原形”叫**不定式**；本节只使用这个具体搭配，例如old enough to drive（年龄够大，可以开车）。', '先给意思和步骤，再引入不定式名称')
add(6, '**核心规则**：频度副词（always、often、usually、never）放在实义动词前、be 动词后。', '**频度**指发生的频繁程度：always总是、often经常、usually通常、never从不。like（喜欢）、work（工作）、go（去）这类本身表达具体动作或情况的动词，叫**实义动词**。本节普通句子中的常见位置是：频度副词放实义动词前、be动词后。', '解释频度与实义动词后再讲位置')
add(6, '3. I have **never** been to Beijing. 我从没去过北京。', '3. I **never** drink coffee. 我从不喝咖啡。（drink＝喝，never放drink前）', '用本节规则能解释的例句替换完成时')
add(6, '**易错误区**：副词不能随意插在动宾之间：', '**动宾之间**就是动词与其宾语之间，如I like music中的like与music之间。副词不能随意插在这个位置：', '拆开压缩术语')
add(6, '3. afraid、asleep等在本节作表语；它们还可按搭配作补语或后置修饰语，不宜直接前置普通名词：The girl is **afraid**.', '3. afraid（害怕的）、asleep（睡着的）不宜直接放普通名词前：The girl is **afraid**（女孩害怕），The baby is asleep（婴儿睡着了）。a sleeping baby表示“一个睡着的婴儿”，先认清这一组用法，sleeping的形成会在动词章节继续讲。', '主讲位置时不突然添加补语名称')
add(6, '15. sleeping（现在分词作定语，asleep 是表语形容词）', '15. sleeping（正文已给a sleeping baby；这里同样放名词前。asleep通常不直接放名词前）', '答案不要求未学的现在分词术语')
add(6, '**通俗定义**：形容词在句中可作定语、表语、补语，位置有前置和后置两种。', '**通俗定义**：形容词可说明名词的特点，也可在句中补充说明主语或宾语的状态。放在名词前叫前置，放在名词后叫后置；后面例子里的“宾补”是“宾语补足语”的简称，即补充说明宾语的部分，如keep him awake（让他保持清醒）中awake说明him的状态。', '在复盘第一次用宾补前就地解释')
add(6, '4. 不规则副词：well（好地，good 的副词）、badly（bad 的副词）。', '4. 不规则对应：good → well（好地）；bad → badly属于规则加ly。', '复盘分类一致')

add(2, 'one book一本书，two books两本书。', 'one book一本书，two books两本书。本章数量词先认one（一）、two（二）、three（三）、four（四）、five（五），做题时直接用给出的数量。', '补第二章练习需要的数字含义')
add(4, '不加冠词。；', '不加冠词。', '清理修改产生的重复标点')
add(5, '| 单数可数 | ✅ a book | ✅ the book | ❌ |', '| 普通单数可数名词短语 | ✅ a book | ✅ the book | 通常需a/the/my/this等限定词；my book没有冠词但有限定词 |', '第五章复盘与第四章表格一致')
add(6, '**形容词有三级：原级（本身）、比较级（两者比）、最高级（三者及以上比）。**', '**原级**是词本来的程度表达，如tall（高的）；**比较级**表示“更……”，如taller（更高的）；**最高级**表示在一个范围内“最……”，如tallest（最高的）。\n\n把对象说出来时常用than（比）：Tom is taller than Amy＝汤姆比艾米高。taller说明比较的特点，than后给出比较对象Amy。比较级不只是给中文加一个“更”，还要按下方规则选择英语写法。', '把本身两者比的简称展开成能操作的示范')
add(6, '**通俗定义**：副词多数由形容词加后缀 -ly 构成，也有与原形相同的副词及不规则副词。', '**通俗定义**：许多副词由形容词在词尾加-ly构成。接在词尾、帮助构成另一个词的部分叫后缀；-ly中的短横线只是标记，quick + ly写成quickly。也有同形副词和不规则对应，如fast、well。', '先解释后缀而不要求构词法前置')
add(2, '**⚠️ 最该记住的一类：同一个词，泛指 vs 具体，可数性会变**', '**同一个词：不同含义下的可数性可能不同**', '小标题不再把具体等同可数')
add(2, '| 物质类 | water、milk、tea、coffee、juice、bread、rice、meat、air、money、paper |', '| 物质及类似用法 | water水、milk牛奶、tea茶、coffee咖啡、juice果汁、bread面包、rice米饭、meat肉、air空气、money钱、paper纸 |', '常用词表直接给义，减少查词跳转')
add(2, '| 抽象类 | advice、information、knowledge、news、fun、work、homework、progress、health |', '| 抽象及活动类 | advice建议、information信息、knowledge知识、news消息、fun乐趣、work工作、homework家庭作业、progress进步、health健康 |', '常用词表直接给义')
add(2, '| 总称类 | furniture、equipment、luggage/baggage、traffic、machinery、clothing、jewelry |', '| 总称类 | furniture家具、equipment设备、luggage/baggage行李、traffic交通／车流、machinery机械设备、clothing衣物、jewelry珠宝 |', '常用词表直接给义')
add(5, '**通俗定义**：of + 名词性物主代词/\'s 所有格，表达"（众多中的）一个"。', '**通俗定义**：of后接名词性物主代词或\'s所有格，如a friend of mine（我的一位朋友）。这种组合叫双重所有格；本章先掌握这种“一位／一件……属于谁”的常用表达。', '定义不靠实际拥有数量推导')
add(5, '- 双重所有格表"其中之一、部分"，不表唯一所属；', '- of后用mine、yours等名词性物主代词，或my father\'s等所有格，不用me、my，如a friend of mine，不写a friend of me／my；', '改成可执行的位置规则')
add(5, '- 双重所有格表部分概念，不表唯一所属。', '- 本章a friend of mine这类表达说明所属关系；不要用形式推断实际只有一位还是多位朋友。', '归纳不重复人数误解')
add(6, '3. 常接不定式：形容词 + enough + to do。', '3. 常接不定式：形容词 + enough + to + 动词原形。规则有时简写为to do，其中do代表要放进去的具体动作，如to drive（开车）、to go（去），不是所有句子都必须写do。', '解释语法公式中的占位词')

# 表格可能被编辑器补齐空格，按单元格内容匹配，其他正文按原文精确匹配。
def table_key(line):
    return '|'.join(x.strip() for x in line.strip().split('|'))

def replace(text, old, new):
    if old.startswith('|') and '\n' not in old:
        lines=text.split('\n')
        for i,line in enumerate(lines):
            if line.lstrip().startswith('|') and table_key(line)==table_key(old):lines[i]=new
        return '\n'.join(lines)
    # 新文中有时保留旧句作为示范；防止重复插入。
    if new and old in new and new in text:return text
    return text.replace(old,new)

def revise(text):
    match=re.search(r'^# 第 (\d{2}) 章[　 ]',text,re.M)
    if not match:return text
    n=int(match[1])
    for item in CHANGES:
        if item['章']==n:text=replace(text,item['原文'],item['新文'])
    return text

def apply():
    from 阅读体验优化 import foundation_chapter
    changed=[]
    for path in sorted((ROOT/'章节').glob('0[1-6]·*.md')):
        raw=path.read_bytes(); before=raw.decode('utf-8').replace('\r\n','\n')
        after=foundation_chapter(before)
        assert revise(after)==after,('非幂等',path.name)
        if after==before:continue
        snapshot=RECORD/'零基础试读前快照'/(path.name+'.snapshot')
        snapshot.parent.mkdir(exist_ok=True)
        if not snapshot.exists():snapshot.write_bytes(raw)
        newline='\r\n' if b'\r\n' in raw else '\n'
        final=after.replace('\n',newline).encode('utf-8')
        path.write_bytes(final)
        changed.append({'文件':path.name,'修改前SHA256':hashlib.sha256(raw).hexdigest(),'修改后SHA256':hashlib.sha256(final).hexdigest()})
    # 同一轮再次修订时，仍从首次快照登记总变化，避免覆盖掉之前五章的记录。
    all_rows=[]
    for path in sorted((ROOT/'章节').glob('0[1-6]·*.md')):
        snapshot=RECORD/'零基础试读前快照'/(path.name+'.snapshot')
        if snapshot.exists():
            all_rows.append({'文件':path.name,'修改前SHA256':hashlib.sha256(snapshot.read_bytes()).hexdigest(),'修改后SHA256':hashlib.sha256(path.read_bytes()).hexdigest()})
    (RECORD/'零基础试读校订明细.json').write_text(json.dumps({'修改文件':all_rows,'定点校订':CHANGES},ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'试读校订：{len(changed)}章，登记{len(CHANGES)}条定点变更。')

if __name__=='__main__':apply()
