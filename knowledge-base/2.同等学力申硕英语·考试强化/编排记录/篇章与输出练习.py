from 题库接口 import block, mc, op, lines


def cloze(chapter,title,text,rows,start=1):
    items=[]
    for n,(options,correct,why) in enumerate(rows,start):
        items.append(mc(f'本篇空{n}选择哪一项？',options,correct,why))
    block(chapter,title,text,items)


cloze(11,'完形一：社区班车试行','''A town introduced a small bus to connect an outlying estate with its library. The service was designed to 【1】 access for residents without cars. At first, officials expected most passengers to be older people. 【2】, the first month’s records showed that many younger workers used it too.

The driver kept a simple 【3】 of boarding times rather than asking passengers to complete a long survey. These records helped the team 【4】 the timetable. A late-afternoon journey was added because several people finished work after the original final bus had left.

The trial did not 【5】 that every proposed route would succeed. It involved only one estate, and fares were temporarily free. 【6】, the council decided to collect more information before expanding the service. It asked whether passengers would continue using the bus if a small fee was 【7】.

Residents were invited to 【8】 practical changes, including safer stops. Their comments revealed problems that passenger totals alone could not show. The council concluded that numbers and local experience should be considered 【9】. A successful service needed not only enough users but also arrangements that people could 【10】 on.

词语：outlying estate偏远住宅区；boarding上车；fare票价。''',[
(['improve','restrict','ignore','replace'],'improve','班车为无车居民改善可达性；restrict限制、ignore忽略、replace替代都不接项目目的。'),
(['However','Therefore','Similarly','For instance'],'However','预期年长者为主，实际不少年轻人使用，构成转折；非结果、相似或具体举例关系。'),
(['record','promise','refusal','reward'],'record','记录上车时间支撑后文These records；promise承诺、refusal拒绝、reward奖励不合搭配与指代。'),
(['adjust','conceal','damage','abandon'],'adjust','为增加下午班次而调整时刻表；隐藏、损坏、放弃均不对应实际动作。'),
(['prove','deny','notice','prefer'],'prove','一地免费试点不能证明所有路线成功；deny是否认，notice注意，prefer偏好都不表达证据边界。'),
(['Therefore','Nevertheless','Meanwhile','Instead of'],'Therefore','因证据有限所以继续收集，属因果；nevertheless转折、meanwhile同时不对应，instead of后结构也不合。'),
(['charged','borrowed','forgiven','discovered'],'charged','收费可说a fee was charged；借费、原谅费、发现费不合此语境。'),
(['suggest','conceal','reject','prevent'],'suggest','邀请居民提出具体改变；其余隐藏、拒绝、阻止都不是comments的来源动作。'),
(['together','secretly','accidentally','separately only'],'together','数据与经验共同考虑；秘密、偶然或仅分开考虑不对应末段总结。'),
(['rely','insist','complain','look'],'rely','rely on表示依靠可靠安排；insist on坚持、complain on搭配不当、look on看待不合可靠性语境。'),
])

cloze(11,'完形二：从例题到独立解释','''A learner may recognise an answer immediately after reading an explanation. This feeling can be 【1】: recognising a familiar sentence is not the same as producing an explanation without help. A training group therefore changed the way it reviewed new methods.

Instead of rereading every page, participants first closed their notes and tried to 【2】 the method to a partner. When they got stuck, they wrote down the missing step. They then reopened the notes to 【3】 that specific gap. This made review more focused.

The group did not treat every hesitation as 【4】. Some difficulties showed exactly where a learner’s understanding was incomplete. 【5】, repeating an answer while looking at it gave little information about independent understanding.

After a few days, learners attempted a new example rather than the one they had already 【6】. If the method worked only with the original wording, more practice was needed. The goal was not to collect a larger 【7】 of completed pages, but to use an idea in a different situation.

Participants also kept the questions they had answered incorrectly. Reviewing the 【8】 for an error was more useful than copying the correct letter. Over time, this record helped them 【9】 between vocabulary problems and problems of reasoning. These two weaknesses often required different kinds of 【10】.

词语：hesitation犹豫；reasoning推理。''',[
(['misleading','permanent','expensive','compulsory'],'misleading','熟悉感可能误导对独立能力的判断；永久、昂贵、强制均非这里的评价。'),
(['explain','hide','purchase','interrupt'],'explain','对伙伴解释方法对应理解检验；隐藏、购买、中断不合动作。'),
(['fill','widen','ignore','celebrate'],'fill','fill a gap弥补缺口；扩大、忽略或庆祝缺口不合目的。'),
(['failure','permission','evidence of mastery','a timetable'],'failure','后文把困难看作诊断信息，不应每次犹豫就当失败；许可、掌握证据、时刻表不合hesitation的评价。'),
(['By contrast','As a result','For this purpose','Likewise'],'By contrast','对比有诊断价值的困难与看着答案重复；不是前者导致后者，也不是同类作用。'),
(['memorised','invented','paid','refused'],'memorised','新例题相对于已记熟的原例；发明、付钱、拒绝不对应already与wording。'),
(['number','price','distance','speed'],'number','a larger number of pages表示更多页数；价格、距离、速度不能与此数量搭配互换。'),
(['reason','colour','owner','date only'],'reason','找错因比抄字母有用；颜色、所有者、仅日期不能解释错误来源。'),
(['distinguish','choose','borrow','recover'],'distinguish','distinguish between A and B区分两类问题；选择、借用、恢复不合between两类的分析用途。'),
(['support','decoration','transport','payment'],'support','不同弱点需不同支持或训练；装饰、交通、付款在这里与学习诊断无关。'),
])

cloze(11,'完形三：数字展览的取舍','''A local museum created an online exhibition so that people who lived far away could view its collection. The project 【1】 access, but staff soon discovered that putting images on a website was only the first step.

Some photographs lacked clear dates or names. Without this 【2】, visitors could see an object but not understand its place in a story. Curators therefore checked labels and added short explanations. They chose simple language without 【3】 important distinctions.

The museum also avoided assuming that online access would 【4】 every physical visit. Some users wanted to see objects in person after viewing them on a screen. Others could not travel and valued the digital version for that very 【5】.

Maintaining the website required time. Links had to be tested and new formats considered as technology 【6】. Some weeks required no changes to the content, but staff still had to check that the pages worked. A digital collection was not a permanent achievement that could be left 【7】.

The team eventually limited the first release to a smaller, carefully documented group of objects. This decision 【8】 the launch but improved the quality of information. Rather than treating speed as the only measure of success, the museum looked for a 【9】 between reach and reliability. Clear explanations helped more people use the collection while preserving the necessary details; staff rejected the idea that one goal had to be sacrificed for the other. Its experience suggests that widening access and protecting accuracy should be 【10】 goals.

词语：curator策展人；documented有资料记录的；reach触达范围。''',[
(['expanded','restricted','measured','restored'],'expanded','正确依据：让远处的人在线参观，扩大了可达范围。restricted方向相反；measured是测量，项目不是在统计可达性；restored预设此前失去访问条件，文章没有给出这种恢复背景。'),
(['context','permission','sequence','recognition'],'context','正确依据：日期和名称帮助物件进入故事，合称背景语境context。permission是许可，缺的不是授权；sequence是顺序，无法覆盖物件身份信息；recognition是辨认或认可，不是this承接的具体背景资料。'),
(['losing','introducing','emphasising','explaining'],'losing','正确依据：simple language与important distinctions要兼顾，without losing说明简明而不丢重要区别。without introducing会变成不引入区别；without emphasising／explaining会说避免强调或解释，均不表达保留必要区分的目标。'),
(['replace','require','delay','organise'],'replace','数字访问不一定取代每次实地参观；后句有人更想亲临作解释，其他动词不对应online/physical对比。'),
(['reason','purpose','occasion','condition'],'reason','正确依据：for that very reason回指不能出行这一原因。purpose会把已有困难改成做事目的；occasion是场合，非理由；condition在for that very condition中不构成这里的因果表达。'),
(['changed','stabilised','slowed','recovered'],'changed','正确依据：new formats considered说明格式要随技术变化重新考虑。stabilised是稳定下来，slowed是放慢，recovered是从低谷恢复，均添加文章未给的特定趋势，不能代替这里一般的变化。'),
(['unattended','unchanged','unfinished','unpublished'],'unattended','正确依据：tested links、new formats与Maintaining共同强调不能放任不管。unchanged是内容不改，定期检查却不一定每次都须更改；unfinished和unpublished分别说未完成和未发布，与已上线并继续维护的情境不同。'),
(['delayed','accelerated','announced','repeated'],'delayed','正确依据：更谨慎地整理较小首批，文中用but将时间代价与信息质量提高对照。accelerated加快与该对照不合；announced只是宣布，不说明发布节奏的代价；repeated需要先前已启动再重复的背景。'),
(['balance','distinction','comparison','conflict'],'balance','正确依据：look for a balance between是在触达范围与可靠程度之间协调权衡。distinction是区分，comparison是比较，均不足以表达如何兼顾目标；look for a conflict变成寻求冲突，与末句目标可相互配合的总结不合。'),
(['complementary','competing','identical','independent'],'complementary','正确依据：文章放弃只看速度，转向同时兼顾触达与可靠，末句将两目标视作可相互支持。competing强调相互竞争而非总结的协调；identical把两个不同目标说成同一个；independent抹去二者需共同考虑的关系。'),
])


def completion(chapter,title,words,phrases,text,word_answers,placements,start=1):
    labels='ABCD';p_labels='PQRS';n=len(words)
    assert len(phrases)==len(word_answers)==len(placements)==n
    intro='词框：'+ '　'.join(f'{labels[i]}. {w}' for i,w in enumerate(words))+'\n\n先补短语：\n\n'
    for i,p in enumerate(phrases):intro+=f'- {p_labels[i]}. '+p.replace('___',f'【{start+i}】')+'\n'
    intro+='\n再用完成的短语P/Q/R'+('/S' if n==4 else '')+'回填文章（每项用一次）：\n\n'+text
    items=[]
    for i,(wi,why) in enumerate(word_answers):
        items.append(op(f'第一轮空{start+i}：选词框中的哪一项？',f'{labels[wi]}. {words[wi]}',why))
    for i,(pi,why) in enumerate(placements):
        items.append(op(f'第二轮空{start+n+i}：选完成后的哪条短语？',p_labels[pi]+'. '+phrases[pi].replace('___',words[word_answers[pi][0]]),why))
    block(chapter,title,intro,items)


completion(12,'第一套·Text 1：成人课程',['access','flexible','reduce'],
 ['offers ___ hours','have ___ to online materials','___ travel costs'],
 '''A college opened an evening course for adults with fixed daytime jobs. The programme 【4】, so participants can choose a suitable study period. They do not have to travel to the college to read every document: from home, participants can 【5】. This is especially helpful for those who live far away. Studying online may also 【6】, although learners still need time and a reliable connection. The college will keep face-to-face sessions for tasks that require shared equipment.''',
 [(1,'hours前用形容词flexible，灵活的时间。'),(0,'have access to是能够使用的固定结构。'),(2,'reduce作原形动词，接travel costs形成降低费用。')],
 [(0,'主语programme后接offers；后面choose a suitable period解释时间灵活。'),(1,'前有can，后接have原形；不出门读取资料对应online materials。'),(2,'may后需原形，住得远与在家学习共同支持减少出行费用。')])
completion(12,'第一套·Text 2：培训交通支持',['support','checks','transport'],
 ['depend on public ___','provide financial ___','carry out regular ___'],
 '''A training centre discovered that distance prevented some residents from attending. Many of them 【10】 because they do not own cars. A local fund agreed to 【11】 for eligible learners, helping with bus fares. Staff did not assume that payments alone would solve every problem. To learn whether the arrangement remained useful, they would 【12】 and speak to participants about missed sessions. The aim was to identify practical obstacles before interpreting absence as a lack of motivation.''',
 [(2,'public transport公共交通。'),(0,'financial support经济支持，support作名词。'),(1,'regular checks定期检查，checks是复数名词。')],
 [(0,'them指无车居民，后面because ... do not own cars直接解释依靠公共交通。'),(1,'基金对符合条件者提供资金帮助，与bus fares对应。'),(2,'would后接carry原形，后文说继续了解安排效果，对应定期检查。')],start=7)
completion(12,'第一套·Text 3：公共项目',['concerned','evidence','failure','change'],
 ['are ___ about costs','collect ___ before deciding','learn from ___','lead to lasting ___'],
 '''A council wanted to improve a public square, but some residents 【17】. They feared that an attractive design would require expensive maintenance. The project team promised to 【18】 instead of claiming immediate certainty. It would compare different layouts and record how people used them. Not every initial design would work, and the team needed to 【19】 rather than hide unsuccessful trials. Small, carefully tested improvements might 【20】 if users and maintenance staff remained involved.''',
 [(0,'are concerned about表示担忧，concerned作表语。'),(1,'collect evidence收集证据；before deciding给决策前的顺序。'),(2,'learn from failure从失败中学习。'),(3,'lasting change持久改变，形容词lasting修饰名词。')],
 [(0,'residents复数接are；下一句feared解释成本担忧。'),(1,'promised to后用collect，compare和record说明收集证据。'),(2,'needed to后接learn，未成功设计对应failure。'),(3,'might后用lead，长期参与是产生持久改变的条件。')],start=13)

completion(12,'第二套·Text 1：工具借用',['available','loss','training'],
 ['make equipment ___','prevent the ___ of small parts','provide basic ___'],
 '''A workshop began lending tools to neighbourhood residents. Its aim was to 【4】 without requiring every family to buy a complete set. Tools were stored in numbered boxes to 【5】. Before borrowing unfamiliar items, users attended a short session. Experienced volunteers would 【6】, explaining safe handling and how to report faults. Sharing depended not simply on owning useful objects, but on a system that kept them ready for the next borrower.''',
 [(0,'make＋宾语＋形容词，available说明equipment可用。'),(1,'the loss of表示……的遗失；空白处名词。'),(2,'provide basic training提供基础培训。')],
 [(0,'aim was to后接make；无需每家买设备对应使设备可供借用。'),(1,'numbered boxes用来减少小零件遗失，非培训内容。'),(2,'volunteers解释使用与报修，属于基础培训。')])
completion(12,'第二套·Text 2：校内反馈',['attention','methods','purpose'],
 ['explain the ___ of a task','direct ___ to a specific problem','try different ___'],
 '''A teacher found that marking every error at once overwhelmed some learners. Before giving feedback, she would 【10】 so that students knew what they were trying to achieve. Her comments would then 【11】 rather than list everything that might be improved. If the first explanation did not help, she would 【12】, using a diagram or asking the student to explain the idea aloud. The goal was understanding, not simply a larger number of corrections on the page.''',
 [(2,'the purpose of a task指任务目的。'),(0,'direct attention to把注意力引向。'),(1,'different methods不同方法；different后此处复数名词。')],
 [(0,'学生先知道要达成什么，对应解释任务目的。'),(1,'comments聚焦specific problem，与不列全部问题形成对照。'),(2,'首种解释无效则改用图示或口述，对应尝试不同方法。')],start=7)
completion(12,'第二套·Text 3：观测与维护',['reliable','compare','record','sources'],
 ['keep a clear ___ of changes','use ___ equipment','___ results from different sites','identify possible ___ of error'],
 '''A group of students planned to observe the temperature in several school buildings. They first needed to 【17】, since faulty devices could produce misleading readings. Each team would 【18】, noting the time and location of every measurement. Later, they could 【19】 and ask why some rooms were warmer. A difference did not automatically prove a building defect. Before drawing a conclusion, the group would 【20】, including direct sunlight or a device left near a heater.''',
 [(2,'keep a record of保留记录。'),(0,'reliable是形容词，修饰equipment。'),(1,'compare作动词，results是比较对象。'),(3,'sources of error误差来源；possible修饰名词。')],
 [(1,'先用可靠设备，后句faulty devices作反证。'),(0,'团队记录每次时间地点，配合record of changes。'),(2,'后文追问房间温差，需要比较不同地点结果。'),(3,'日照和加热器属于可能误差来源，不能只凭差异断言缺陷。')],start=13)

lines(13,'单句翻译：八项',r'''
Although the service was designed for new residents, people who had lived there for years also used it.|这项服务虽然原本面向新居民，但已在那里住了多年的居民也使用了它。|保留让步、原定对象与实际另一群体；who修饰people，不是service。
What matters is not how many pages you finish, but whether you can explain the idea without looking at the book.|重要的不是你读完多少页，而是你能否不看书就解释这个观点。|not ... but ...对比两个评价标准；whether为是否内容，不是无论。
The figures collected during the trial suggest a possible link, rather than proving that one change caused the other.|试行期间收集的数据提示可能存在联系，而不是证明一种变化导致了另一种变化。|collected修饰figures；possible与rather than限制结论，不得译成已证实因果。
Whether the meeting is held online or in person, participants should receive the necessary information in advance.|无论会议在线上还是线下举行，与会者都应提前获得必要信息。|保留无论、被动举行、应当和提前；不能把whether译为是否而丢主句关系。
The proposal, which had been discussed for months, was rejected because its costs were higher than expected.|这项已经讨论了几个月的提案，由于成本高于预期而被否决。|讨论时间是补充；because给否决原因，不能把两者混成因讨论太久而否决。
Not all the problems identified in the report can be solved by increasing the budget.|报告指出的问题并非都能靠增加预算解决。|部分否定，identified修饰problems；不是所有问题都不能解决。
Having compared the two versions, the editor asked the author to make the main argument clearer.|比较两个版本后，编辑请作者把主要论点表达得更清楚。|先比较后要求；editor提出要求，author负责修改，角色不可倒置。
The more information a system collects, the more important it becomes to explain how that information will be used.|一个系统收集的信息越多，说明这些信息将如何使用就越重要。|the more ... the more相关比较；it为形式主语，how内容说明使用方式。
''')

translation_passages=[
('整段一：公共信息','''When a city changes the way a public service works, clear information matters as much as the change itself. Residents who understand the reason for a new rule are better placed to prepare for it. This does not mean that everyone will agree. Some people may still face difficulties that the designers did not expect. Asking for comments before a decision is final can reveal these problems. However, collecting comments is only a beginning. Officials also need to explain which suggestions they accepted, which they rejected, and why. Without that response, participation may feel like a formality rather than a genuine opportunity to influence a decision.''',
 '城市改变公共服务的运行方式时，清楚地提供信息与改变本身同样重要。理解新规定原因的居民，更有条件做好准备。这并不意味着所有人都会同意。有些人仍可能面临设计者未曾预料的困难。在决定最终确定前征求意见，可以发现这些问题。不过，收集意见只是开始。管理者还需说明采纳了哪些建议、拒绝了哪些，以及原因。如果没有这种回应，参与可能会让人觉得只是走形式，而非真正影响决定的机会。',
 ['信息与改变同样重要','理解原因与准备的关系','并非人人同意','可能有未预料困难','决定前征询可发现问题','收集仅是开始','说明采纳与拒绝及原因','没有回应的条件','可能流于形式而非真实机会','中文衔接与自然表达']),
('整段二：工作中的学习','''Learning at work is often described as something that happens in a formal course. Yet a worker may learn just as much by explaining a problem to a colleague or reviewing an unsuccessful attempt. What makes these experiences useful is not simply the passage of time, but the opportunity to notice a gap and try a different approach. A workplace that punishes every question may discourage this process. By contrast, managers who ask what can be learned from a mistake can make discussion more productive. This does not remove responsibility; it connects responsibility with improvement rather than with silence.''',
 '人们常把工作中的学习描述为参加正式课程。然而，员工向同事解释问题，或回顾一次未成功的尝试，也可能学到同样多的东西。使这些经历有价值的，并非只是时间流逝，而是发现不足并尝试不同方法的机会。对每个提问都加以惩罚的工作环境，可能妨碍这一过程。相反，管理者若询问能从错误中学到什么，就能使讨论更有成效。这并非免除责任，而是把责任与改进联系起来，而不是与沉默联系起来。',
 ['正式课程的传统描述','yet转折','解释与回顾两类经历','可能学到同样多','not ... but ...标准','惩罚问题可能妨碍','管理者提问的对比','更有成效的可能','责任不是被免除','责任连接改进而非沉默']),
('整段三：技术与使用条件','''A tool may be easy to use for the person who designed it and confusing for someone encountering it for the first time. Designers therefore need to observe real users rather than assume that written instructions solve every problem. A repeated mistake may point to an unclear label, not a careless user. Changing that label can be more effective than adding another page of explanation. Even after a tool is improved, however, some users may need individual support. Accessibility is not a feature that can be declared complete once and then forgotten. It depends on continued attention to the different conditions in which people use a service.''',
 '一种工具对其设计者来说可能容易使用，对第一次接触它的人却可能令人困惑。因此，设计者需要观察真实用户，而不能假定书面说明能解决所有问题。反复出现的错误，可能说明标签不清楚，而非用户粗心。修改那个标签，可能比再增加一页解释更有效。不过，即便工具得到改进，有些用户仍可能需要个别帮助。可及性并非一种宣告完成一次就能置之不理的特征。它取决于持续关注人们使用服务时的不同条件。',
 ['设计者与新用户对比','可能性保留','因此观察真实用户','不假定说明解决全部','标签不清与粗心区分','改标签可能更有效','改进后仍可能需帮助','不能一次宣告后忘记','持续关注不同使用条件','中文自然与指代连贯']),
]
for title,text,answer,units in translation_passages:
    block(13,title,text,[op('独立翻译整段，再逐项核对意义单元。',answer,'建议10分：以下10个单元每项1分；意思准确可用不同措辞。'+ '；'.join(units),意义单元=units)])

lines(14,'句子修复：八项',r'''
改正：Lifelong learning important for workers.|Lifelong learning is important for workers.|主语后缺系动词is，不能把名词短语与形容词直接拼成完整陈述句。
改正：Online courses saves time for many students.|Online courses save time for many students.|courses复数，普通现在时配save；不能因后面time不可数而改主谓关系。
改正：Many people study online, they need flexible hours.|Many people study online because they need flexible hours. 也可用合适标点拆句。|两个独立分句仅用逗号连接不规范；because表达本题给出的原因。
改正：Although the method is useful, but it has limits.|Although the method is useful, it has limits.|本课标准让步句不重复使用but连接同一主从关系。
改正：People should to check the information before sharing it.|People should check the information before sharing it.|情态should后用原形，不带to；before sharing表达分享前。
改正：This experience made me to understand the value of practice.|This experience made me understand the value of practice.|主动make＋宾语＋原形；不能把被动was made to do的搭配直接套来。
改正想表达“并非每个问题都能由技术解决”：Every problem cannot be solved by technology.|Not every problem can be solved by technology. 或Technology cannot solve every problem.|把否定范围写清楚，避免原句产生全否定／部分否定的理解歧义。
改正：The people which work at night need different arrangements.|The people who/that work at night need different arrangements.|指人的限制性定语从句主语通常用who或that，不用which；不另重复they。
''')
block(14,'段落展开与审题：三项','写出要求的组织内容，不追求唯一措辞。',[
op('围绕“灵活的课程时间让学习更可行”写4句：主题、解释、例子、回扣。','Flexible course times make learning more accessible. Workers can choose sessions that fit their shifts. For example, a shop assistant may attend an evening class after work. This gives adults with fixed duties a realistic way to develop new skills.','检查四句功能是否不同；例子须具体，不把假想个例当现实统计。'),
op('题目讨论self-employment的利弊。列一个好处、一个风险和一个有条件结论，再写80—100词段落。','要点示例：时间自主；收入不稳定；有储备与规划时更可行。可写：Self-employment can give people greater control over their schedules. This may help them combine paid work with family duties. However, freedom does not guarantee a stable income. A person who depends on one client may face serious difficulty when that contract ends. For this reason, preparation matters as much as enthusiasm. People considering this path should assess their likely expenses, develop useful skills and avoid relying on one source of work. With realistic planning and some financial reserves, self-employment can be a worthwhile option, but it is not equally suitable for everyone.','示例只是一种论证；不能只列好处而漏风险，也不要把有条件结论写成适用于所有人。'),
op('给定图表：某培训班线上学习者占比，2020年20%、2022年35%、2024年50%。写两句准确描述和一句有限解释。','The share of learners studying online rose from 20 percent in 2020 to 50 percent in 2024. It increased by 30 percentage points over the period. The change may reflect a growing need for flexible study, though the chart alone does not establish its causes.','图表数据是原创练习设定。保留起止年份、占比与百分点；可能解释不能当图表已证实原因。'),
])

ESSAYS = [
('完整写作一：终身学习','Write at least 150 words on The Importance of Lifelong Learning. Discuss both personal and professional development, with examples and reasons.', '''Lifelong learning matters because neither our working lives nor our personal needs remain unchanged. Education should therefore continue beyond the classroom. It helps people respond to new demands while giving them more choices about the lives they want to lead.

In professional life, continued learning makes it easier to adapt. A worker who learns to use a new system may perform familiar tasks more effectively and become ready for different responsibilities. For example, an office assistant who develops basic data skills can contribute to projects that were previously beyond reach. Learning does not guarantee promotion, but it can create opportunities.

On a personal level, learning builds confidence and curiosity. Studying a language, exploring local history or practising a practical skill can make daily life more rewarding. It may also bring people into contact with others who share their interests.

To make lifelong learning realistic, people need manageable goals and regular practice. A short, consistent habit is often more useful than an ambitious plan that is soon abandoned. With this approach, learning becomes a lasting part of life rather than a temporary obligation.''','第1段回答重要性；第2段职业发展及具体例子并保留不保证晋升；第3段个人发展；第4段可行做法收束。'),
('完整写作二：技术与人的作用','Write at least 150 words on whether machine translation can fully replace human translators. Consider speed, accuracy and performance in context.', '''Machine translation has become a useful part of communication. It can produce a draft quickly and help readers understand the general meaning of an unfamiliar text. However, speed alone does not show that it can fully replace human translators.

For simple and repetitive material, automatic translation may save considerable time. A traveller who needs the basic meaning of a notice may prefer an immediate answer to a perfect one. Professional translators can also use an automatic draft as a starting point, provided that they check it carefully.

The difficulty becomes greater when meaning depends on context. A phrase may express politeness, humour or criticism rather than its most direct dictionary meaning. In such cases, an inaccurate choice can change the writer's intention even if the sentence sounds fluent. A human translator must consider the audience, the purpose and the consequences of misunderstanding.

I therefore see machine translation as a powerful aid rather than a complete substitute. Its appropriate use depends on the task. The more important precision and responsibility become, the more necessary careful human judgment is likely to remain.''','明确立场；速度用具体场景解释；准确性连接语境；讨论不同任务表现与责任，避免通篇只说科技方便。'),
('完整写作三：让生活更简单','Write at least 150 words on Ways to Live a Simpler Life in a Modern World. Explain practical methods and why they may help.', '''Modern life offers many choices, but managing them can become a burden. Living more simply does not require rejecting technology or giving up every comfort. It means choosing activities and possessions that serve a clear purpose.

One practical step is to reduce unnecessary commitments. Before accepting a new task, people can ask whether it supports an important goal and whether they have enough time to do it properly. Leaving some space in a schedule can make existing responsibilities easier to handle.

Another step is to use technology deliberately. Turning off nonessential notifications, for example, can protect a period of study or conversation. The aim is not to avoid all messages, but to decide when they deserve attention. A similar principle applies to buying things: delaying a purchase gives us time to consider whether it will actually be useful.

Finally, simple routines can reduce repeated decisions. Planning a few regular study periods or preparing the next day's essentials may save both time and effort. These small changes will not remove every difficulty, but they can help people focus on what matters most.''','建议题必须给方法与作用；拒绝把简化生活写成拒绝一切技术；例子落到时间、通知、购买和习惯。'),
]
for title,prompt,essay,why in ESSAYS:
    block(14,title,prompt,[op('先独立列提纲，再写完整文章，完成后展开示范。',essay,why,类型='作文')])
