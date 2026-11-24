"""外部资料筛选后的自编讲解；在阅读体验流程中应用，不改原始资料。

只补课程实际缺口。正文随堂练习不并入章末题库题量。
"""
from pathlib import Path
import re

FOUNDATION = '英语学习资料·完整线性版'
EXAM = '同等学力申硕英语·考试强化'

B08 = '''#### 数量范围：至少、至多与大约

数字前的小词会改变整句话的意思。**ten 是十；at least ten 是十或更多；at most ten 是十或更少。**先看三个数量，再看它们允许的范围，不要看到 ten 就都记成“恰好十”。

| 表达 | 意思 | 10 这个数是否包括在内 |
|---|---|---|
| at least ten books | 至少十本书 | 包括；也可能是十一、十二本或更多 |
| at most ten books | 至多十本书 | 包括；也可能少于十本 |
| about ten books | 大约十本书 | 可能是十本，也可能略多或略少；没有给出精确误差 |

再对照第06章见过的比较词 more（更多）和 less（更少）：**more than ten books** 是超过十本，不包括恰好十本；**less than ten minutes** 是不到十分钟，也不包括恰好十分钟。minutes 是 minute（分钟）的复数。计时用 less than；谈可数物品的个数，正式表达常用 fewer than，如 fewer than ten books（少于十本书），fewer 是 few 的比较级。

只读“数量短语”也能练明白，不必先学新的句型：at least ten students＝至少十名学生；at most ten students＝至多十名学生。数字、students 都没变，变的是数量允许到哪里。

**随堂练习：先写范围，再核对。**

1. at least five books：四本、五本、六本，哪些符合？
2. at most eight students：七人、八人、九人，哪些符合？
3. more than twenty minutes 是否包括恰好二十分钟？at least twenty minutes 呢？
4. about thirty people 是否能据此确定“恰好三十人”？用一句中文说明。

<details>
<summary>完成数量范围练习后，展开答案与解析</summary>
<p><strong>1.</strong> 五本、六本符合。at least 包含五这个下限；四本不足五本。</p>
<p><strong>2.</strong> 七人、八人符合。at most 包含八这个上限；九人超过上限。</p>
<p><strong>3.</strong> more than twenty minutes 不包括恰好二十分钟；at least twenty minutes 包括。关键不是二十这个数，而是前面的限制词。</p>
<p><strong>4.</strong> 不能。about 给的是大约数量，并未确认恰好三十，也没有规定一定在二十九到三十一之间。</p>
</details>

能分清“包括边界”“不包括边界”“只是大约”即可；不用在这里额外背一整页数量近义短语。
'''

B19 = '''#### 根据句意区分因果、转折与补充

认识 but、so、and 后，还要问：**后一句对前一句做了什么？**不要只按“一个肯定、一个否定”来判关系。下面都是自编例句，ill＝生病的，rest＝休息，still＝仍然。

| 两个意思之间的关系 | 英语例句 | 为什么这样连接 |
|---|---|---|
| 原因带来结果 | I was ill, so I did not go to work. 我病了，所以没去上班。 | 生病是没上班的原因；虽然前肯定、后否定，仍然是因果 |
| 后一句与通常预期不同 | I was ill, but I still went to work. 我病了，但仍然去上班了。 | 生病时通常会休息，实际却去上班；两句都是肯定，也可以转折 |
| 继续补充一项情况 | I stayed at home, and I rested. 我待在家里，并且休息了。 | 继续说明做了什么；and 本身没有明确说“前者导致后者” |

转折不是指两句话必须互相否定。“病了”和“去上班”可以同时是真的，but 表达的是实际情况与预期的差别。因果也不是看到两个动作先后发生就能断定；so 会明确表达说话人认为前面的情况带来了后面的结果。

有时不同连接词都能写出语法正确的句子，意思却不同。I was tired, and I went home 是补述；换成 so，才明确说“因为累，所以回家”。选词时既看结构，也看上下文要求表达什么。

**随堂练习：按括号中的意思填 and、but 或 so，并解释关系。**

1. It rained, ___ we stayed at home.（因为下雨而留在家里。）
2. It rained, ___ we still went out.（下雨了，却仍然出门。）
3. I did not buy a pen, ___ I did not buy a book.（中性补充：没买笔，也没买书；不表达因果。）
4. 有人说“两个分句都是肯定，所以不能用 but”。用本节的一个例句说明为什么错。

<details>
<summary>完成关系判断后，展开答案与解析</summary>
<p><strong>1.</strong> so。题目指定下雨是留在家里的原因，不能仅因两个分句都肯定就选 and。</p>
<p><strong>2.</strong> but。后句指出与通常预期不同的行动；still 也帮助表达“仍然”。</p>
<p><strong>3.</strong> and。两个否定是在并列补充，否定本身不决定逻辑关系。</p>
<p><strong>4.</strong> I was ill, but I still went to work. 两个肯定事实之间有反预期关系，所以可以用 but。能说清“通常怎样、实际怎样”，才真正读懂转折。</p>
</details>
'''

B20 = '''###### although 与 in spite of：意思相近，接法不同

**Although it rained, we went out.** 虽然下雨了，我们还是出去了。although 后面的 it rained 有自己的主语 it 和谓语 rained，是一个分句。

也可以写：**In spite of the rain, we went out.** 尽管下雨，我们还是出去了。in spite of 是一个整体，相当于介词，后面的 the rain 是名词短语；不能直接接 it rained 这个完整分句。这里 rain 是名词“雨”，rained 是动词 rain 的过去式“下雨了”。

| 保留完整分句 | 改用名词短语 |
|---|---|
| Although it rained, we went out. | In spite of the rain, we went out. |
| Although he was ill, he went to work. | In spite of his illness, he went to work. |

第二组中 ill 是形容词“生病的”，illness 是名词“疾病”；his illness 表示“他的病”。换表达时，不能只把 although 换掉，后面原来的主语和谓语照抄。先判断后面给的是哪种结构，再选择连接方式。这和第07章 because it rained / because of the rain 的区别相通，但这里表达的是让步，不是原因。

**随堂练习：填 Although 或 In spite of；第3题按要求改写。**

1. ___ the rain, we played outside.（虽然下雨，仍在外面玩。）
2. ___ it rained, we played outside.（意思同上。）
3. 把 In spite of he was ill, he went to work. 改成两种正确表达：一种保留 he was ill，一种保留 In spite of。

<details>
<summary>完成让步表达练习后，展开答案与解析</summary>
<p><strong>1.</strong> In spite of。the rain 是名词短语。</p>
<p><strong>2.</strong> Although。it rained 是有主语和谓语的分句。</p>
<p><strong>3.</strong> Although he was ill, he went to work. / In spite of his illness, he went to work. 第一种改连接方式，第二种把 he was ill 改成名词短语 his illness。两句都没有因为中文有“虽然……但是……”而再添 but。</p>
</details>
'''

B25 = '''#### 表达目的：to do、in order to do 与 so that

先问“做这件事，是为了什么？”例如：**I study hard to pass the exam.** 我努力学习，为的是通过考试。study hard 是努力学习，pass the exam 是通过考试；to pass 说明学习的目的。

同一个目的还可以这样表达：

| 写法 | 后面的结构 | 例句 |
|---|---|---|
| to + 动词原形 | 不定式，不另外写一个主语 | I study hard to pass the exam. |
| in order to + 动词原形 | 明确表示目的，不能接完整分句 | I study hard in order to pass the exam. |
| so that + 分句 | 写出主语和谓语，本例用 can | I study hard so that I can pass the exam. |

三句在这个语境下都表达“努力学习，以便通过考试”，并不保证最后一定考过。第20章已经见过 so that 目的从句；现在把它与不定式放在一起看，就能知道为什么不能写 in order to I can pass。

**改写前还要看：两个动作是不是同一个人做。**上面是“我学习，我通过考试”，用省去另一个主语的 to pass 很清楚。再看：The teacher speaks slowly so that we can understand. 老师说得慢，以便我们听懂。speaks slowly＝说得慢，understand＝理解；说话的是老师，听懂的是我们。不能机械改成 The teacher speaks slowly to understand，那样通常变成“老师为了自己理解而说得慢”，对象变了。

本节先掌握这三种最直接的表达。看到 to do 仍要先判断作用：I want to pass the exam 中的 to pass 是 want 的宾语，不能因为都带 to 就统称为目的状语。

**随堂练习：选择或改写，并说出结构依据。**

1. I read every day in order to ___ more words.（learn / I learn；learn＝学习。）
2. 用 so that 改写 I practice every day to improve my English.（practice＝练习，improve＝提高；保留“我想提高英语”的目的。）
3. The teacher writes clearly so that the students can read the words. 能否直接把后半句改成 to read the words，仍保留“学生读懂”的意思？为什么？（clearly＝清楚地。）
4. I hope to win. 中的 to win 能否直接换成 in order to win，仍表达“我希望获胜”？

<details>
<summary>完成目的表达练习后，展开答案与解析</summary>
<p><strong>1.</strong> learn。in order to 后接动词原形，不能在这里接 I learn 这个分句。</p>
<p><strong>2.</strong> I practice every day so that I can improve my English. so that 后补出主语 I 和谓语 can improve；保留的是练习的目的。</p>
<p><strong>3.</strong> 不能这样直接改写。writes 的动作由老师发出，read 的动作由学生发出；原从句把两者交代清楚了。直接换成 to read 会改变目的动作的执行者。</p>
<p><strong>4.</strong> 不能保持原来的结构和意思。hope to win 是“希望获胜”，to win 补出希望的内容；in order to win 表示“为了获胜”，不是 hope 所需的同一种补充。</p>
</details>
'''

B31_PAIRS = '''### 连接表达的接法：补充、结果与举例　【必学】

有些表达的中文很相近，但接法不同。这里用已经学过的“完整分句”和“名词短语”来辨认，不再把它们当成互相替换的一串近义词。

**补充：in addition 与 in addition to。**

- I study English. **In addition, I study French.** 我学英语。另外，我还学法语。French＝法语；in addition 放在新句开头，后面接完整的 I study French。
- **In addition to English, I study French.** 除英语外，我还学法语。in addition to 后面接 English 这个名词；后面的逗号再引出主句。

后一句不是 In addition to I study English，因为 to 在这个固定表达里是介词，不能直接带这个完整分句。不要看到 to 就套用上一阶段学过的不定式。

**结果与原因：as a result 与 as a result of。**

- It rained heavily. **As a result, the match was canceled.** 雨下得很大，因此比赛取消了。heavily＝大量地，was canceled＝被取消；as a result 引出结果。
- **As a result of the heavy rain, the match was canceled.** 由于大雨，比赛取消了。as a result of 后面的 the heavy rain 是原因，后面的主句说明结果。

两个表达不能只背成“因此”。多了 of，不仅接法变了，它后面给出的也是原因，不能把因果方向读反。

**举例：for example 与 such as。**

- I like fruit. **For example, I eat apples every day.** 我喜欢水果。例如，我每天吃苹果。for example 在这里引出完整例句。
- I like fruit **such as apples and oranges.** 我喜欢苹果、橙子这样的水果。such as 在这里紧跟 fruit，列出它的具体例子。

fruit 是总称，apples、oranges 是例子。for example 也能用于较短的举例或插入位置，不能背成“它后面永远必须是完整句”；先掌握这里两种清楚、稳妥的写法。例子只说明“比如这些”，不等于穷尽全部种类。

**随堂练习：按句子结构选表达，并解释所选表达的作用。**

1. ___ English, she also studies French.（In addition / In addition to）
2. The road was closed ___ the heavy rain.（as a result / as a result of；closed＝关闭的。）大雨是原因还是结果？
3. I like sports ___ tennis and football.（such as / as a result）能由此认定“我只喜欢这两种运动”吗？

<details>
<summary>完成连接表达练习后，展开答案与解析</summary>
<p><strong>1.</strong> In addition to。后面先接名词 English，逗号后才是主句；不能把两个写法当成无条件互换。</p>
<p><strong>2.</strong> as a result of。其后 the heavy rain 是原因；道路关闭是结果。若用 As a result 开新句，则应先交代下雨，再说 As a result, the road was closed.</p>
<p><strong>3.</strong> such as。tennis 和 football 是 sports 的具体例子，不能推断只有这两种。</p>
</details>
'''

B31_PASSAGE = '''### 语篇连接综合运用（案例短文）　【必学】

**语篇就是围绕一定意思组织起来的一段话或一篇文章。**把句子读成一段话，除了看连接词，还要追踪“在说谁、哪件事、有没有换时间”。下面是自编短文：

> Maya bought a bicycle. The bike was cheap, but it was useful. She rides it to work every day. In the past, she took the bus. Now, she saves money on travel.

Maya 买了一辆自行车。车很便宜，但很实用。她每天骑车上班。过去，她坐公交。现在，她在出行上省了钱。bicycle / bike＝自行车，cheap＝便宜的，useful＝有用的，saves money＝省钱，travel＝出行。

先串起对象：a bicycle 首次介绍一辆车，the bike 换了一个词继续说同一辆车；两个 it 都指这辆车，She / she 都指 Maya。这些词虽然外形不同，仍让文章围绕同一个人和同一个物体展开。不是每换一句就要写 however 或 therefore。

再看关系：cheap 后面的 but 不是否定“便宜”这个事实，而是说它虽便宜，却仍实用。最后两句用 In the past / Now 比较同一个人过去和现在的情况；不能把它读成“Maya 过去坐公交，另一个人现在省钱”。这里 bought、was、took 叙述过去；rides、saves 说明现在的习惯或情况，与前面学过的时态一致。

还有一种联系是“先说一类，再举具体例子”：The club needs equipment, such as balls and nets. 俱乐部需要设备，例如球和网。equipment＝设备，balls＝球，nets＝网。balls 和 nets 是 equipment 的例子，却不是它的两个同义词：不能把 equipment 在任何句子里都换成 balls。

**随堂练习：先找文字依据，再写答案。**

1. 短文中的 The bike 指哪一个对象？最后一个 it 呢？
2. 哪两处明确提示过去与现在？变化发生在同一个人身上吗？
3. Nina lent Anna a book. She liked it.（Nina 借给 Anna 一本书。她喜欢它；lent＝借出。）it 指什么？She 是否能仅靠这两句唯一确定？怎样改写得清楚？
4. 从 balls and nets 能否推出“设备只有球和网”？为什么？

<details>
<summary>完成句间联系练习后，展开答案与解析</summary>
<p><strong>1.</strong> 都指 Maya 买的自行车。the bike 与 a bicycle 是同一个对象，rides it 中的 it 继续指它。</p>
<p><strong>2.</strong> In the past 与 Now 明确提示时间；took 与 saves 等动词形式也相应变化。两句都谈 Maya，不能只看到过去、现在就忽略对象。</p>
<p><strong>3.</strong> it 指书；She 可能指 Nina，也可能指 Anna，缺少进一步上下文，不能凭“离得最近”硬选。若想说 Anna 喜欢，可写 Nina lent Anna a book. Anna liked it. 必要时重复名字比指代不清更好。</p>
<p><strong>4.</strong> 不能。such as 只是举例；文中没有说设备仅有这两类。</p>
</details>

检查句间联系时，先试着把代词换回具体的人或物，再看意思是否连贯；无法唯一确定时，承认信息不足，不要自行补故事。
'''

B31_WRITING = '''### 写作练习：用时态与连接词叙述学习经历　【必学】

这次仍写 5—7 句，但先把每句话的作用想清楚。**语法正确解决“句子能不能成立”，句间联系解决“为什么下一句接在这里”。**不需要每句话都换一个高级连接词。

先看一个只有重复、没有展开的初稿：I study English every day. English is useful. English is very useful. I like English. 每句大致看得懂，却没有解释“每天怎么学、学了有什么具体变化”。再加一个 very，内容也没有往前走。

把“每天学习”变成一个可以展开的中心意思：我每天读一点，并用例句理解新词。围绕它安排三步：先说做法，再说明怎样做，最后用一次具体经历说明。先在草稿回答这三个问题，不急着套句型。

下面把过去经历和未来计划也接进同一段自编示范：

> I study English for twenty minutes every day. I read short stories because they show me how to use words. Yesterday I learned the word “borrow” from a story. It means “借入”. Then I wrote a sentence with it: “I borrow books from my friend.” Tomorrow I am going to read another story and write two new sentences.

我每天学二十分钟英语。我读短故事，因为它们能让我看到怎样使用单词。昨天，我从一个故事里学到 borrow。它表示“借入”。随后我用它写了一句话：“我向朋友借书。”明天，我准备再读一个故事，写两个新句子。

前两句交代习惯和理由；中间几句给出真正的例子；最后一句延续同一种做法，说下一步计划。they 指 short stories，两个 it 指单词 borrow。没有为了增加连接词而凭空制造转折，也没有把“有用”换着词说三遍。

**独立写作：换成你自己的内容，写 5—7 句。**包括一个现在的学习习惯、一个过去发生的具体例子、一个未来计划；至少用一次 because、but 或 if，而且关系要符合原意。不要照抄 borrow 的故事，可以写学一个词、读一小段或修改一个错误。

写完按五项各记 1 分：①有明确的学习做法；②给出一个具体例子而非重复评价；③过去、现在、计划的动词形式对应；④代词指向明确；⑤每句话完整，连接词和标点合适。5 项都做到再继续；缺哪项就改哪项，不用为了词数另添空话。这是本段练习的自查办法，不是考试评分标准。

<details>
<summary>先独立写完，再展开另一种参考写法</summary>
<p>I check my English sentences every evening. This helps me find mistakes. Yesterday I wrote “She go to school”. I changed “go” to “goes” because the subject was “she”. Now I understand that sentence better. Tomorrow I am going to check three more sentences.</p>
<p>我每天晚上检查自己的英语句子。这帮助我找出错误。昨天，我写了“She go to school”。因为主语是 she，我把 go 改成 goes。现在，我更理解那句话了。明天，我准备再检查三个句子。mistakes＝错误，changed＝改动了，subject＝主语。</p>
<p>第一句给习惯；第二句的 This 指检查句子的做法；第三、四句给一件具体修改；第五句说明现在的理解；第六句接计划。引号里的错误句是等待修改的材料，不是要求模仿的正确句子。开放题无需与范文相同，但五项自查都要有可指出的依据。</p>
</details>
'''

E04 = '''## 数量限制：下限、上限与确定值

基础阶段已经分过 at least（至少）、at most（至多）和 about（大约）。读选项时，要再检查它有没有偷偷把范围改成确定数字。下面都是自编材料，不是历年原题。

原文：**At least 30 of the 50 students completed the course.** 50 名学生中，至少 30 人完成课程。30 是已知下限，实际可能是 30—50 中的任一人数；不能确定恰好 30 人，也不能确定其余 20 人都没有完成。

因此，More than half of the students completed the course（超过一半完成了）有依据：一半是 25，至少 30 已超过 25。Exactly 30 students completed it（恰好 30 人完成了）则把下限当成了确定值。分析范围时，允许作这样的简单计算，但不要替原文补未知人数。

再看报名规则：**Each group can have no more than 10 members.** 每组最多可有 10 名成员。这里 no more than 表示上限，等同于 at most；8、9、10 都可能符合规则。与它不同，The group has only 10 members 明确说该组有 10 人，并带“只有”的评价。no more than 在其他叙述语境中也可能带“仅仅”的语气，所以读规则、统计和评论时必须结合整句，不把它永远机械译成同一个中文词。

**随堂练习：逐项判断“有依据 / 与原文冲突 / 信息不足”，并指出范围词。**

1. 原文：At least 18 of the 30 volunteers arrived. 判断：a. More than half arrived. b. Exactly 18 arrived. c. Fewer than 18 arrived.
2. 原文：A team may include at most six people. 判断：a. A team of six is permitted by this size rule. b. Every team has six people. c. The rule permits seven people in a team.
3. 原文：About 100 people attended. 判断：Exactly 100 people attended.

<details>
<summary>完成数量限制练习后，展开答案与解析</summary>
<p><strong>1.</strong> a 有依据：30 的一半为 15，至少 18 超过一半。b 信息不足：可能恰好 18，也可能更多。c 冲突：少于 18 不满足 at least 18。</p>
<p><strong>2.</strong> a 有依据：at most 包括六这个上限；本项只问人数规则是否允许。b 信息不足：允许最多六人，不等于每队实际都有六人。c 冲突：七人超过上限。</p>
<p><strong>3.</strong> 信息不足。about 是估计，不能直接升级成 exactly。也不能因为没有确认“恰好”就认定“一定不等于 100”。</p>
</details>

复盘时把“与原文相反”和“原文没说到这个精确程度”分开记录。两者都可能使选项不能选，但错因不同。
'''

E06 = '''## 固定搭配：整体含义与使用条件

固定搭配不能只按每个单词分别翻译，也不必一次背完两百条。下面选三组演示如何学：先读完整意思，再看后面接什么，最后放回上下文。例句与练习均为自编，不据此宣称这些词组“必考”。

**第一组：on purpose 与 by mistake。**on purpose 表示故意，by mistake 表示误做。He sent the file to the wrong person by mistake. 他误把文件发给了别人。若换成 on purpose，就变成有意发错对象。仅有“发错了”不能确定是故意还是无意；需要 looked similar、did not notice 等证据支持误做，或 meant to、wanted to 等证据支持意图。

**第二组：by means of、by no means 与 by all means。**三者虽共享 means，作用不同：

| 表达 | 在本例中的意思 | 自编例句 |
|---|---|---|
| by means of + 名词短语 | 借助某种手段 | They sent the message by means of a radio. 他们用无线电发出消息。 |
| by no means | 绝不、完全不 | The task is by no means easy. 这个任务绝不轻松。 |
| by all means | 当然可以，常用于同意请求 | “May I use this chair?” “By all means.” “我可以用这把椅子吗？”“当然可以。” |

这里不要把 by all means 按字面误读成“用所有方法”，也不需要为了掌握 by no means 再另背一组句首倒装。先在普通语序中认清它对 easy 的否定即可。

**第三组：in terms of 与 in return for。**in terms of 指“从某个方面衡量”：In terms of cost, the bus is cheaper. 从费用看，公交更便宜。它限定比较角度，并没有说公交在速度、舒适度上也更好。in return for 指“作为……的回报”：She gave him a meal in return for his help. 她请他吃了一顿饭，作为帮助她的回报。后面的名词短语，一个是评价方面，一个是得到回报的帮助，不能只因都能接名词就互换。

**随堂练习：先写最关键的语境证据，再选填。**

1. The two names looked similar, and I did not notice the difference. I chose the wrong person ___.（on purpose / by mistake）
2. “May I open the window?” “___.”（By all means / By no means easy）
3. At first the task looked simple. After three failed attempts, we found it was ___ easy.（by no means / by means of）
4. ___ price, plan A is better. Plan B, however, provides more support.（In terms of / In return for）能否据此说 A 在所有方面更好？
5. He repaired her bicycle, and she cooked dinner for him ___ his help.（in return for / in terms of）

<details>
<summary>完成搭配辨析后，展开答案与解析</summary>
<p><strong>1.</strong> by mistake。names looked similar 和 did not notice 支持“误做”；不能仅凭 wrong person 就断定动机。</p>
<p><strong>2.</strong> By all means。对方在请求许可，回答表示同意。另一项是一段不能独立完成此处回应的“不轻松”表达。</p>
<p><strong>3.</strong> by no means。三次失败后认定“不轻松”；by means of 后要接手段，不能直接修饰 easy。</p>
<p><strong>4.</strong> In terms of。只从 price（价格）比较 A 更好；B 在 support（支持）方面另有优势，不能把单一角度扩大为全面优越。</p>
<p><strong>5.</strong> in return for。修车与做饭构成回报关系；这里不是从“帮助”这个维度评价一件东西。</p>
</details>

答对后再尝试口头解释“换成另一项，错在含义、接法还是证据不足”。能够解释区别，比认出熟悉词形更可靠。
'''

E11 = '''## 跨句线索：同义呼应、总称与具体例子

基础阶段已经练过：bike 可以继续指前面的 bicycle，it 可以指已经介绍的对象。到完形里，还要利用这种联系判断空白处需要哪一类意思。**这类联系是证据，不是“看到同义词就选”的口诀。**下面的材料均为自编。

先看总称与例子：The center provides basic ___, including food, clean water and a place to sleep.（中心提供基本的……，包括食物、净水和睡觉的地方。）备选 necessities / opinions / competitions / instructions。food、water、a place to sleep 共同属于生活必需品，所以选 necessities；它们不是意见、比赛或指令。空白前的 basic 也支持“基本必需品”。这是从具体例子反推总称，不是只因某一个词离空格最近。

再看同义呼应：The claim sounded convincing, but the report offered no ___ for it. Without supporting evidence, readers could not check whether it was true.（说法听起来可信，但报告没有为它提供……；没有支持证据，读者无法核实。）备选 evidence / permission / equipment / payment。下一句的 supporting evidence 回应第一句缺少的东西，答案是 evidence。两句都缺证据，不能因为词重复就反而排除它。

同义联系也可能被否定或转折改变方向：The device was cheap. Yet few customers thought it was good ___.（设备很便宜，但很少顾客认为它……。）若选项是 value / weather / traffic / silence，应选 value，good value 指物有所值。这里的 few 与 Yet 告诉我们：便宜不等于顾客认为值得购买；不能看见 cheap 就擅自把整句理解成肯定评价。

作答时先给空白写一个简短中文意思，再向前后各读一句，找能支持它的对象、例子和否定范围。线索可以隔一句出现；距离近不保证相关。

**随堂练习：完成下面自编片段的三空，并为每空抄出一处证据。**

> At the repair club, members share tools. Hammers, screwdrivers and drills are kept in one cupboard. This (1) ___ is available to everyone. Beginners often need (2) ___: experienced members show them how to use the tools safely. Such guidance helps them avoid accidents. The club is inexpensive, but it is (3) ___ free; each member pays a small monthly fee.

repair club＝维修俱乐部；hammer＝锤子；screwdriver＝螺丝刀；drill＝电钻；cupboard＝柜子；guidance＝指导；accident＝事故；fee＝费用。

1. A. equipment　B. furniture　C. transport　D. clothing
2. A. permission　B. advice　C. payment　D. praise
3. A. always　B. already　C. completely　D. not

<details>
<summary>完成三空并找出证据后，展开答案与解析</summary>
<p><strong>1. A，equipment。</strong> hammers、screwdrivers、drills 都是工具设备；This 继续指刚才列出的器材。cupboard 虽然是最近的名词，却是存放位置，不能据它选 furniture（家具）。transport 是交通运输，clothing 是衣物。</p>
<p><strong>2. B，advice。</strong> show them how to use the tools safely 和后句 Such guidance 都说明得到操作指导。permission 是许可，payment 是付款，praise 是表扬；仅仅得到许可或表扬不能准确概括此处“教怎样安全使用”。</p>
<p><strong>3. D，not。</strong> each member pays a small monthly fee 证明不是免费。but 从 inexpensive（便宜）转向“仍要付钱”的限制；always（总是）、already（已经）、completely（完全）都把 free 保持为肯定，与每人付费的说明冲突。</p>
</details>

三空各查两项：答案正确、证据能解释该选项。只凭“哪个词眼熟”碰对的空，仍回读说明关系，再进入章末完整十空训练。
'''

E14 = '''## 从提纲到句子：按表达任务选句式

知道“要写理由”，不等于能马上写出理由。这里把前面的段落写法拆成几个可以起笔的位置。**先确定要说的具体内容，再选择表达；不必每篇把下表全部用一遍。**这些是自编写作支架，不是要求原样背诵的万能范文。

| 当前要完成的任务 | 一个简单写法 | 本题可以怎样写 |
|---|---|---|
| 给出立场 | I believe that + 完整分句 | I believe that learning should continue throughout life. 我认为学习应贯穿一生。 |
| 解释理由 | One reason is that + 完整分句 | One reason is that jobs and tools change. 一个原因是工作和工具会变化。 |
| 说明具体收益 | This can help + 人 + 动词原形 | This can help workers use new tools. 这能帮助员工使用新工具。 |
| 举具体例子 | For example, + 完整分句 | For example, an office worker can learn to use a new program. 例如，办公室员工可以学习使用新程序。 |
| 承认限制 | However, + 完整分句 | However, some workers have little time for study. 不过，一些员工学习时间很少。 |
| 提出对应建议 | To solve this problem, + 完整分句 | To solve this problem, employers can offer short lessons during working hours. 为解决这个问题，雇主可以在工作时间提供短课。 |

最后一句借用了已学过的目的不定式。要解决什么问题，前一句必须说清：这里针对的是时间不足，所以提出工作时间内的短课；不能前面谈费用，后面忽然提出与费用无关的口号。This 同样要能指回明确做法，不能空悬在段首，让读者猜它指什么。

接着做一次从中文到英语的展开。中文提纲不是“学习很重要、非常重要”，而是：工作工具会变化 → 员工学习新软件 → 能更准确完成工作。先写：Workers can learn to use new software. 再解释收益：This can help them complete tasks more accurately. 最后给具体情境：For example, an office worker can learn to check a table with a computer program. 三句分别讲行动、作用和例子；accurately＝准确地，software＝软件，table＝表格。没有必要再硬添“社会飞速发展”作为背景。

这三句是一段的材料，不是完整作文。写整篇时仍先检查题目要求几个角度、每段要完成什么，再决定哪些句子有用。题目没有要求解决问题，就不必套进建议段；若使用建议，也要服务于题目而不是换了话题。

**随堂练习：先独立写，再看参考改写。**

1. 给 Some adults have little time to study. 接一句针对“时间不足”的可行建议，使用 To solve this problem。不要只写“我们应该重视它”。
2. 修正 One reason is that can help workers.：补清 that 后面的主语，并具体说明帮助做什么。
3. 把 Learning is useful. It is very important. Everyone should learn. 改成 3—4 句：明确一个收益，解释如何产生，再给一个具体例子。可以自选学习电脑、语言或工作技能，不编统计数字。

<details>
<summary>完成句子与段落改写后，展开参考答案与检查方法</summary>
<p><strong>1.</strong> To solve this problem, employers can offer short lessons during working hours. 这项措施把学习安排进工作时间，针对前面的时间不足。其他合理措施也可，例如学习者安排每天一小段时间；须说明是谁做什么，而不是只换一句“学习重要”。</p>
<p><strong>2.</strong> One reason is that learning new skills can help workers solve problems at work. that 后的主语是 learning new skills，谓语是 can help；help 后再说明帮助员工解决工作中的问题。也可使用其他明确、合理的主语和收益。</p>
<p><strong>3.</strong> Learning computer skills can make daily work easier. Workers can use a program to check tables instead of checking every number by hand. For example, an office worker can learn to find repeated names in a list. This can save time and reduce mistakes.</p>
<p>检查：是否只谈一个清楚的收益；中间是否解释了“为什么能更容易”；例子是否真的说明同一收益；This 是否有清楚的所指。instead of＝代替，by hand＝手工，repeated names＝重复的姓名。示范中的 can 表示可能的帮助，没有把例子夸成保证每个人都取得相同效果的结论。</p>
</details>

进入章末完整作文时，尽量不看这张表独立表达；卡住后再借用一个写法。复测换一个主题，检查自己能否替换内容并保留正确结构，而不是只复写熟悉的范文。
'''

def insert_before(text, anchor, block):
    heading = block.splitlines()[0]
    if heading in text:
        return text
    matches = list(re.finditer(r'^' + re.escape(anchor) + r'(?=\s|$)', text, re.M))
    assert len(matches) == 1, ('插入位置不唯一', anchor)
    start = matches[0].start()
    return text[:start] + block.strip() + '\n\n' + text[start:]


def replace_section(text, title, block):
    pattern = r'^### ' + re.escape(title) + r'(?:　【[^】]+】)?\n[\s\S]*?(?=^#{1,3} |\Z)'
    text, count = re.subn(pattern, lambda _: block.strip() + '\n\n', text, count=1, flags=re.M)
    assert count == 1, ('找不到待升级小节', title)
    return text


def refresh_toc(text, extra=()):
    """保留原目录收录范围，仅增加本次新增同级标题；顺序与正文一致。"""
    m = re.search(r'^## 本章目录\n([\s\S]*?)(?=^#{1,6} |^---\s*$)', text, re.M)
    assert m, '缺少本章目录'
    old = set(re.findall(r'\[\[#([^]|]+)', m[1]))
    bare = lambda s: re.sub(r'　【[^】]+】$', '', s)
    wanted = {bare(h) for h in old} | set(extra)
    lines = []
    for h in re.findall(r'^#{1,6} (.+)$', text[m.end():], re.M):
        if bare(h) in wanted:
            lines.append(f'- [[#{h}|{bare(h)}]]')
    return text[:m.start()] + '## 本章目录\n\n' + '\n'.join(lines) + '\n\n' + text[m.end():]


def revise(text, path):
    path = Path(path)
    if path.parent.name != '章节' or path.parent.parent.name not in (FOUNDATION, EXAM):
        return text
    kind = path.parent.parent.name
    n = int(path.name[:2])
    extra = []
    if kind == FOUNDATION:
        if n == 8:
            text = insert_before(text, '### 序数词', B08)
        elif n == 19:
            text = insert_before(text, '### 从属连词', B19)
        elif n == 20:
            text = insert_before(text, '###### whether … or …：无论哪一种情况', B20)
        elif n == 25:
            text = insert_before(text, '#### 不定式的变体', B25)
        elif n == 31:
            text = insert_before(text, '### 标点符号', B31_PAIRS)
            text = replace_section(text, '语篇连接综合运用（案例短文）', B31_PASSAGE)
            text = replace_section(text, '写作练习：用时态与连接词叙述学习经历', B31_WRITING)
            extra = ['连接表达的接法：补充、结果与举例']
        else:
            return text
    else:
        blocks = {4: ('## 条件、让步与选择关系的区别', E04),
                  6: ('## 词汇复习记录：语境、搭配与替换限制', E06),
                  11: ('## 完形填空的全文回读与答案核对', E11),
                  14: ('## 句子修复：四种常见错误要知道为什么改', E14)}
        if n not in blocks:
            return text
        anchor, block = blocks[n]
        text = insert_before(text, anchor, block)
        extra = [block.splitlines()[0][3:]]
    return refresh_toc(text, extra)
