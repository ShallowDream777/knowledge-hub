from 题库接口 import block, mc, lines

block(7,'文章一：图书馆预约试点','''A city library used to provide computer help only during normal opening hours. Staff noticed that many requests came from people who worked during the day. These residents could reach the library only shortly before it closed, leaving little time for questions about online forms or job applications.

The library therefore introduced evening appointments on two days each week. Each appointment lasted twenty minutes. Residents booked by telephone or at the front desk; owning a computer or an email account was not required. Volunteers helped visitors understand the steps on a screen, but did not complete financial transactions on their behalf.

After an eight-week trial, the number of requests for help had increased. However, staff did not treat this as proof that the whole city's computer skills had improved. The trial counted visits, not changes in ability. Some residents had returned several times to practise the same task.

The service remained free, although visitors who missed an appointment were asked to cancel in advance next time. The library planned to keep the evening sessions, provided that enough trained volunteers were available. It would decide later whether to add a third evening.

词语：transaction交易；on their behalf代表他们；provided that只要／在……条件下。''',[
mc('Why were evening appointments introduced?', ['To help people unavailable during the day.','To reduce the number of volunteers.','To make all financial services free.','To replace normal opening hours.'],'To help people unavailable during the day.','第1段给白天工作、到馆太晚的困难；减少志愿者、免费金融业务和替代正常开放均未陈述。'),
mc('How could residents book help?', ['By telephone or at the front desk.','Only through a computer account.','By asking a bank to arrange it.','Without making any appointment.'],'By telephone or at the front desk.','第2段明确两个渠道，并否定必须拥有电脑或邮箱；银行和无需预约都无依据。'),
mc('What were volunteers instructed not to do?', ['Carry out financial transactions for visitors.','Explain steps on a screen.','Help people understand forms.','Take part in evening sessions.'],'Carry out financial transactions for visitors.','did not complete ... on their behalf是限制；解释步骤和表格正是服务，晚间参与也没有被禁止。'),
mc('What does the rise in requests directly show?', ['More requests for the service were recorded.','Every resident improved computer skills.','No visitor needed repeated help.','The trial measured changes in ability.'],'More requests for the service were recorded.','第3段区分访问数与能力变化；其余三项分别扩大范围、与重复来访矛盾、颠倒统计对象。'),
mc('What condition affected the continuation of evening sessions?', ['The availability of trained volunteers.','A fee paid by all visitors.','The purchase of personal computers.','Immediate approval of a third evening.'],'The availability of trained volunteers.','末段provided that给条件；收费、购买电脑和立即增加第三晚均不成立。'),
])

block(7,'文章二：维修而非替换','''A housing association received frequent complaints about broken cupboards in its older flats. Replacing every cupboard would be expensive and disruptive. Rather than ordering new units immediately, the association asked a repair team to inspect the damaged ones.

The team found that most problems involved hinges and handles, not the wooden frames. It proposed replacing small parts where possible. Residents were given a choice between morning and afternoon visits. They were not asked to move out, but someone had to be at home to let the workers in.

During the first month, repairs cost less than the amount estimated for replacement. The association also kept usable wood out of the waste stream. Yet the report did not say repair would always be cheaper. Units with badly damaged frames still needed to be replaced, and repeated visits could increase labour costs.

Some residents wanted an entirely new kitchen rather than repaired cupboards. The association explained that the project addressed safety and function, not a complete redesign. It promised a follow-up check after six months so that faults returning after the first repair could be identified.

词语：housing association住房管理机构；hinge铰链；frame框架；disruptive造成干扰的。''',[
mc('Why did the association first request inspections?', ['To examine whether repair could avoid complete replacement.', 'To find which visiting hours residents preferred.', 'To select cupboards for a complete kitchen redesign.', 'To check whether faults had returned after six months.'], 'To examine whether repair could avoid complete replacement.', '正确依据：第1段说完整替换昂贵且干扰生活，因此先检查是否可以维修。\n\n‘visiting hours’是随后安排上门的时间选择，不是最初检查的目的；‘complete kitchen redesign’是部分住户的愿望，项目并不提供；‘after six months’属于以后复查，错置了时间。'),
mc('What caused most cupboard problems?', ['Small parts such as hinges and handles.', 'Damage to the wooden frames rather than the small fittings.', 'Residents choosing unsuitable replacement cupboards.', 'Repeated visits made by the repair workers.'], 'Small parts such as hinges and handles.', '正确依据：第2段most problems involved hinges and handles，故问题多在小配件。\n\n‘wooden frames’与not the wooden frames反向；‘residents choosing’把机构检查后的方案选择改成住户选错橱柜，文中未说；‘repeated visits’影响的是人工成本，不是原有故障的主要来源。'),
mc('What did residents need to do during a visit?', ['Ensure someone was at home to admit the workers.', 'Leave a key so workers could enter an empty flat.', 'Pay the labour costs before choosing a visiting time.', 'Arrange a frame inspection before booking the visit.'], 'Ensure someone was at home to admit the workers.', '正确依据：someone had to be at home to let the workers in明确要求有人在家开门。\n\n‘leave a key’不能替代原文有人在家的要求；文中未规定住户先交人工费；最初检查由机构安排，也未要求住户先约框架检查才可预约维修。不能把常见维修流程当成本文规定。'),
mc('Which statement is supported by the report?', ['Some cupboards still required replacement.', "The first month's savings excluded the cost of repeat visits.", 'Lower costs persuaded residents to give up requests for new kitchens.', 'Most wooden frames were replaced before repairs began.'], 'Some cupboards still required replacement.', '正确依据：第3段说框架严重损坏的橱柜仍需替换。\n\n‘excluded the cost’无依据：报告只说重复上门可能增加人工成本，未交代首月核算是否排除了它；‘persuaded residents’把机构的解释改成住户已经改变愿望；‘most wooden frames’与问题主要在小配件不符，也没有事先大量换框架的记录。'),
mc('Why was a six-month follow-up planned?', ['To detect faults that might return.', 'To compare the cost of morning and afternoon visits.', 'To decide which residents should receive a new kitchen.', 'To assess whether repaired cupboards matched a new design.'], 'To detect faults that might return.', '正确依据：末句so that faults returning after the first repair could be identified直接交代复查目的。\n\n上午下午只是预约时段，没有比较其费用；新厨房是住户提出但超出本项目的需求；项目关注安全和功能，未实施新设计，也不是验收外观是否匹配。'),
])
lines(7,'细节微练：六项',r'''
原文“Applicants must submit the form before Friday”，选项“on or after Friday”，指出问题。|时间要求被反转。|before在周五之前，不是周五及以后。
原文“The grant covers books but not travel”，问哪项不报销。|travel，出行费用。|but not明确排除，不能因covers在前就把两项都算报销。
原文“The centre lowered its fees because demand fell”，费率降低的直接原因是什么？|需求下降。|because引出原因；不能把降低收费当成需求下降的结果以外再反转。
原文“The experiment included adults aged 40 to 60”，能支持针对所有儿童的结论吗？|不能。|研究对象范围不同；不能用外部常识越过原文样本限制。
原文“New members may attend after registration”，选项说新成员都已经参加，是否成立？|不成立。|may attend表示允许或可能，注册后有资格不等于实际行为。
原文“Only two of the five sites stayed open”，问开放地点数量。|两个。|two是开放数，five是总数；不能看见总数就答五个。
''')

block(8,'文章一：遮阴试点与证据边界','''During a hot summer, a local council installed temporary shade structures beside three playgrounds. Residents had reported that the metal seats became uncomfortable around midday. The structures were inexpensive enough to be removed if the trial failed.

Two weeks later, volunteers counted more visitors during the shaded hours than during the same hours earlier in the summer. Several parents said they could now stay longer with their children. The council described these observations as encouraging, but a researcher advising the project urged caution.

The researcher pointed out that the weather had also become cooler. In addition, a new school holiday programme had begun nearby. Without comparable information from playgrounds lacking shade, it was difficult to separate the effects of the structures from these other changes. This did not mean the shade had no value; it meant that a stronger claim needed stronger evidence.

For the next stage, the council planned to count visitors at similar playgrounds with and without shade. It also wanted to ask residents who did not use the spaces what prevented them from coming. A parent welcomed this approach, noting that comfortable seats would not help families who could not reach the playground safely.

The trial illustrates a useful habit in public decision-making: respond to practical problems, but distinguish promising observations from a complete explanation of their causes.

词语：shade遮阴；comparable可比较的；distinguish区分。''',[
mc('What can reasonably be inferred from the increase in visits?', ['Several changes may have contributed to it.','Shade was proved to be the only cause.','The council had solved every access problem.','Cooler weather made shade completely useless.'],'Several changes may have contributed to it.','第3段列天气和假期项目，不能排除其他解释；only、every及completely均超出证据。'),
mc('The researcher’s attitude toward the initial conclusion is best described as what?', ['Cautious.','Hostile to all public projects.','Completely convinced.','Uninterested in evidence.'],'Cautious.','要求更强证据并明确不等于否定价值；不是敌视、完全确信或漠视证据。'),
mc('Why is the nearby holiday programme mentioned?', ['To offer an alternative explanation for visitor numbers.','To prove that shade frightened children.','To advertise a new school.','To explain the cost of the structures.'],'To offer an alternative explanation for visitor numbers.','它与天气共同提示潜在混杂因素；儿童害怕、广告和结构成本都不是段落作用。'),
mc('What does the parent’s final comment suggest?', ['Benefits may depend on other practical conditions.','Safe routes matter less than attractive seats.','No family was interested in shade.','Only parents can assess research.'],'Benefits may depend on other practical conditions.','到达安全性是获得舒适座椅好处的另一条件；其余倒置比较、全否定或排他推断。'),
mc('What is the author’s main evaluative position?', ['Practical action should be accompanied by careful interpretation.','Councils should never try inexpensive ideas.','Any increase in use proves a project’s success.','Residents’ experiences should always be ignored.'],'Practical action should be accompanied by careful interpretation.','结尾同时肯定回应问题和区分观察与原因；其余三项均把平衡立场改成绝对。'),
])

block(8,'文章二：反馈工具与教师判断','''A college tested a writing tool that highlighted repeated words and unusually long sentences. Students could use it before showing a draft to their teacher. The tool did not grade arguments or decide whether evidence was convincing.

Some students welcomed the immediate response. They could correct simple problems without waiting a week for a tutorial. Others complained that a long sentence sometimes expressed a relationship more clearly than several short ones. The teacher responsible for the trial agreed: a warning was an invitation to think, not an order to delete.

To make this distinction visible, she showed the class two versions of the same paragraph. The first had short, accurate sentences but no clear connection between them. The second contained a longer sentence explaining why one event followed another. The tool flagged the second version, yet the class found it easier to understand.

At the end of the trial, the teacher recommended keeping the tool as an aid to revision. She opposed using the number of warnings as a score for writing quality. Students still needed to consider purpose, audience and the relationship between ideas.

The lesson was not that automatic feedback was worthless. It was that useful information becomes misleading when treated as a complete judgment. A device that notices a feature cannot, by that fact alone, explain what the writer ought to do about it.

词语：draft草稿；flag标记；revision修改。''',[
mc('What can be inferred about the tool?', ['Its warnings identify features rather than settle every writing decision.', 'Its warnings assess the logical links between ideas in a draft.', 'It measures clarity by counting how many warnings a revision removes.', 'It identifies which long sentences should be split before a tutorial.'], 'Its warnings identify features rather than settle every writing decision.', '正确依据：第1段限定工具标记重复词和长句，第3段又显示被标记的长句反而更清楚，故标记特征不等于决定怎样修改。\n\n‘assess the logical links’把教师和读者的判断交给工具，超出其功能；‘counting warnings’把警告数当清晰度指标，正是教师反对的做法；‘should be split’把长句警告当拆句指令，与an invitation to think冲突。'),
mc('Why does the teacher compare two paragraphs?', ['To show that short sentences alone do not ensure clarity.', 'To identify the sentence length the tool should accept as normal.', 'To show how immediate feedback can reduce the need for tutorials.', 'To demonstrate how stronger arguments result from shorter sentences.'], 'To show that short sentences alone do not ensure clarity.', '正确依据：短句版准确却缺少连接，较长版解释因果，班级认为后者更易懂。比较说明短并不自动清楚。\n\n例子未设定正常长度阈值；及时反馈省去等待是前段学生谈的好处，不是两段比较的目的；‘stronger arguments’把清晰度换成论据质量，且‘shorter’与该例结果相反。'),
mc('Which best describes the teacher’s position?', ['Support for a limited use of the tool.', 'Using warning totals as a starting score for writing quality.', 'Keeping the tool while treating shorter sentences as the clearer choice.', 'Postponing use until the tool can judge arguments and evidence.'], 'Support for a limited use of the tool.', '正确依据：第4段同时有keeping the tool as an aid和反对警告数评分，构成有边界的支持。\n\n‘starting score’仍把警告数用作写作质量分数，与opposed相反；‘shorter ... clearer’抹去了教师用长句说明关系的反例；‘postponing use’把当前保留使用改成等待功能升级，文中没有这种计划。'),
mc('The phrase an invitation to think suggests that students should do what?', ['Examine whether a warning is relevant to their intended meaning.', 'Shorten a flagged sentence before asking why it was marked.', 'Compare warning totals to decide which draft is clearer.', 'Ask the tool to supply more convincing evidence for an argument.'], 'Examine whether a warning is relevant to their intended meaning.', '正确依据：教师把warning与order to delete区分，要求结合表达意图判断警告是否需要处理。\n\n先缩短再问原因仍将警告当指令；按总数选择草稿重复了被反对的评分办法；让工具提供论据超出其已说明的标记功能。'),
mc('Which conclusion is consistent with the last paragraph?', ['A useful measure can mislead when taken as a complete assessment.', 'A measure becomes reliable once students learn to apply it consistently.', 'Better revision depends on reducing the features a tool can identify.', 'Class preference should settle disagreements about automatic warnings.'], 'A useful measure can mislead when taken as a complete assessment.', '正确依据：useful information becomes misleading when treated as a complete judgment概括工具信息与完整判断的区别。\n\n使用一致并不补足工具没有评价的内容；减少可标记特征不一定改善意义，长句例子就是反证；班级觉得某段清楚只是一个例证，没有把班级偏好设成最终裁定规则。'),
])
lines(8,'推断与作用微练：六项',r'''
原文“The pilot attracted 30 volunteers; a larger test is planned”，能否选“方案已经被证明适用于全国”？|不能。|小试点和计划中的扩大测试都不能证明全国适用。
作者写“promising, but too early for firm conclusions”，态度是全盘反对还是谨慎认可？|谨慎认可。|promising给正面空间，too early保留证据边界。
段首说“规定会造成意外负担”，后举一位老人不会用手机缴费的例子，例子的作用是什么？|具体说明规定怎样给一类人带来意外负担。|不能仅答“介绍手机”或把一个老人扩成所有老人。
A公司称工具革命性；作者说缺独立测试。能把revolutionary直接归为作者态度吗？|不能。|评价属于公司；作者指出证据不足，需分开立场来源。
原文“members who attended more sessions improved more”，能证明多参加必然导致提高吗？|仅凭这句不能。|动机、原有能力等未被排除；相关程度不能直接变成唯一因果。
原文说“The figures should not be dismissed, but their limitations matter”，作者是否认为数据毫无价值？|不是。|不应忽略与需注意限制并存，不能只抓but后半就抹去前半。
''')

block(9,'文章一：种子共享与长期条件','''A neighbourhood group began a seed library in a small cupboard beside a public hall. People could take a few packets for their gardens and were encouraged to return seeds from plants they later grew. The aim was not to create a commercial seed shop, but to help residents exchange useful varieties and gardening experience.

At first, donations arrived in envelopes with little information. Volunteers often could not tell when the seeds had been collected or whether they suited the local climate. Rather than reject every unlabelled packet, the group created a simple form asking for the plant name, collection date and growing conditions. This made the collection easier to use.

The organisers also discovered that popularity was not the only useful quality. A vegetable that produced less in a wet summer might survive a dry season better than a fast-growing alternative. They therefore kept some varieties that were less productive but more resilient. Visitors were encouraged to ask why a seed had been saved, not merely how many plants it could produce.

The cupboard needed regular care. Seeds had to be kept dry, old packets checked, and labels corrected. Sharing worked because volunteers did this quiet work and gardeners returned information as well as seeds. Without such effort, an attractive cupboard could quickly become a collection of mysteries.

词语：variety品种；productive高产的。词义题的目标词不提前给释义。''',[
mc('Which title best covers the passage?', ['What Makes a Seed Library Useful and Sustainable.','How to Open a Commercial Seed Shop.','Why Every Garden Must Grow the Same Plant.','The History of the Public Hall.'],'What Makes a Seed Library Useful and Sustainable.','目标、标签、适应性和维护共同说明运作条件；商店被否定，统一作物及大厅历史未展开。'),
mc('What does This in This made the collection easier to use refer to?', ['Introducing a form with information about the seeds.','Rejecting every donation.','Moving the public hall.','Selling all unlabelled packets.'],'Introducing a form with information about the seeds.','This概括前句创建信息表这一做法；没有拒绝全部、搬大厅或出售的事件。'),
mc('In context, resilient most nearly means what?', ['Able to cope with difficult conditions.','Certain to produce the largest crop.','Available only in commercial shops.','Difficult to identify by name.'],'Able to cope with difficult conditions.','干旱时能存活提供解释；低产但适应性强，不等于最高产、商店专属或叫不出名字。'),
mc('The collection of mysteries most likely refers to what?', ['Seeds whose identity or growing requirements are unclear.','A set of detective novels.','A secret business hidden in the hall.','Plants that cannot exist in dry weather.'],'Seeds whose identity or growing requirements are unclear.','结尾回扣信息与标签维护；不是真正小说或秘密生意，也不是断言植物不耐旱。'),
mc('Which statement reflects the passage as a whole?', ['Sharing objects may require sharing information and maintenance work.','Popularity is the only basis for choosing seeds.','Volunteers should accept no donations.','Once a cupboard is installed, no further effort is needed.'],'Sharing objects may require sharing information and maintenance work.','末段明确information as well as seeds及quiet work；其余都与品种选择或维护事实冲突。'),
])

block(9,'文章二：日程之间的空隙','''When a small design company moved its meetings online, employees initially filled the time between them with more appointments. Travelling between rooms was no longer necessary, so a calendar could look impressively efficient: one video call ended at ten and the next began at the same moment.

Within weeks, however, workers reported difficulty remembering decisions. Some began the next call still thinking about the previous one. A manager responded by asking teams to leave a short buffer between meetings. The interval was not intended for another task. People could write down decisions, prepare a question, or simply stop looking at a screen.

The change reduced the number of meetings that could fit into a day. This initially worried managers who counted appointments as evidence of activity. Yet several teams found that clearer notes and fewer repeated discussions helped them finish projects on time. A full calendar, they realised, was not the same as a useful day.

The company did not ban long meetings or require everyone to take breaks at identical times. Instead, it asked teams to discuss which pauses helped their particular work. The aim was to protect attention rather than enforce a new ritual. A gap that looks empty on a timetable may still perform an important function.

词语：interval间隔；ritual固定仪式。词义题的目标词不提前给释义。''',[
mc('What is the main point of the passage?', ['Time between tasks can support effective work.', 'Online meetings improve work by removing the need to travel.', 'Shortening meetings helps employees record decisions more clearly.', 'Uniform break routines help teams use busy calendars efficiently.'], 'Time between tasks can support effective work.', '正确依据：全篇从无缝排会造成的问题写到预留间隔的作用，末段又解释看似空白也有功能。\n\n取消路程是最初塞满日程的背景，不能概括后续调整；措施是会议之间留空，不是把会议本身缩短；公司让各团队讨论适合自己的停顿，而非统一休息规则。'),
mc('Buffer in Paragraph 2 most nearly means what?', ['A short protected interval.', 'A slot reserved for finishing an unfinished assignment.', 'A gap caused by a delay in starting the next call.', 'A period spent travelling between two meeting rooms.'], 'A short protected interval.', '正确依据：紧接的The interval及记决策、准备问题、离屏等用途说明buffer是有意保留的短暂间隔。\n\n它not intended for another task，不是赶另一项未完作业；安排是主动留空，不是下场迟开造成的延误；会议已线上化，往返房间是之前被省去的路程。'),
mc('This initially worried managers refers to what?', ['Reducing the number of meetings that fitted into a day.', "Moving the company's meetings online.", 'Workers beginning a call while still thinking about the previous one.', 'Asking teams to choose pauses that suited their particular work.'], 'Reducing the number of meetings that fitted into a day.', '正确依据：This承接紧邻的The change reduced the number of meetings ...，管理者又把会面数量当作活动证据，因此担心。\n\n线上迁移是首段背景；注意力仍留在上场会议是第二段员工遇到的问题；由团队决定停顿是末段安排。后三项都在文中出现，却不是本处回指的事件。'),
mc('The contrast between a full calendar and a useful day supports which idea?', ['Visible activity and effective results are not identical.', 'Meeting notes provide a reliable count of productive hours.', 'Successful teams fit preparation into meetings already scheduled.', 'Meeting frequency increased after teams began recording decisions.'], 'Visible activity and effective results are not identical.', '正确依据：较少会议仍能因笔记更清楚、重复讨论更少而按时完成项目，说明可见忙碌与有效成果不同。\n\n笔记帮助工作，但文中没有用它计算生产时数；准备发生在预留间隔，不是塞回既有会议；会议可容纳数量降低，并未因记笔记而增加频次。'),
mc('Which title is most appropriate?', ['The Value of Leaving Space Between Meetings.', 'Keeping Online Meetings on Schedule.', 'Using Meeting Counts to Measure Team Progress.', 'Writing Clearer Notes to Avoid Long Discussions.'], 'The Value of Leaving Space Between Meetings.', '正确依据：标题需覆盖起初无缝排会的问题、留空措施和保护注意力的价值。\n\n‘on schedule’把主题缩成准时开会；‘meeting counts’把被修正的评价方式当主旨；‘clearer notes’是留空的一项收益，但遗漏准备、休息和因团队而异的安排，范围偏窄。'),
])
lines(9,'主旨、猜词和指代微练：六项',r'''
文章讲共享自行车的便利、维护成本和停放规则，标题“自行车的发明史”能覆盖吗？|不能。|对象虽相关，但文章没有展开历史，标题需覆盖主要方向。
The device is portable: it fits in a small bag. 不查词推测portable。|便于携带的。|冒号后的可装小包提供解释，不是说明昂贵或精确。
Unlike the rigid old timetable, the new one can be changed. rigid表示什么方向？|不灵活、难改变的。|unlike与can be changed构成对比，不能选灵活。
The town postponed the launch. This allowed more testing. This承接什么？|推迟启动这一做法／事件。|不是单纯某个最近名词，而是整个事件带来更多测试时间。
All three paragraphs discuss access, but only the last mentions price. 标题应只围绕价格吗？|不应只围绕价格。|标题需覆盖全篇，单段细节不能替代共同主题。
She said the answer was just around the corner. 在问题解决的语境中如何理解？|答案或解决办法很快就会出现。|这是时间接近的比喻，不是要求去街角找答案。
''')

block(10,'博客一：社区共享厨房','''Blog

Our neighbourhood is considering a shared kitchen in an unused room of the community centre. Residents could book it to cook for a large family gathering or learn a new skill. The room already has water and electricity, but it would need safe appliances and clear cleaning rules. I support the idea if these practical conditions can be met. A low booking fee could pay for repairs, while a small number of free sessions could help residents who cannot afford it. The project should begin with a trial rather than an expensive permanent redesign.

Comment 1
The idea appeals to me, but I work late. If booking is possible only during office hours, many of us will never use it. An evening booking option would matter more than new decoration.

Comment 2
We ran a similar kitchen in my previous town. It worked while a trained person checked equipment and users signed a cleaning record. Once that routine stopped, complaints increased.

Comment 3
I would not support a charge for every session. People already struggling with food costs should not be excluded. Keeping some sessions free is essential, not an optional extra.

Comment 4
Before buying new appliances, test demand using the safe equipment already available. If few people book the room, there is little reason to spend a large amount on rebuilding it.

词语：appliance电器；routine固定维护流程；exclude排除。''',[
mc('Which comment focuses on access for people who work late?', ['Comment 1.','Comment 2.','Comment 3.','Comment 4.'],'Comment 1.','1说work late与evening booking；2讲维护，3讲负担能力，4讲先测试需求。'),
mc('Which comment provides experience from another place?', ['Comment 2.','Comment 1.','Comment 3.','Comment 4.'],'Comment 2.','previous town与ran a similar kitchen是已往经历；其他是当前要求或建议。'),
mc('Which comment most directly supports the blogger’s proposal for free sessions?', ['Comment 3.','Comment 1.','Comment 2.','Comment 4.'],'Comment 3.','3用keeping some sessions free说明低收入人群；1不是免费而是时段，2是安全维护，4是投资节奏。'),
mc('Which comment agrees with testing the idea before a major investment?', ['Comment 4.','Comment 1.','Comment 2.','Comment 3.'],'Comment 4.','4明确Before buying与test demand，呼应正文trial before redesign；其他评论关注别的条件。'),
mc('What do the blogger and Comment 2 have in common?', ['Both recognise that practical arrangements affect success.','Both reject any shared kitchen.','Both want to eliminate all cleaning rules.','Both claim that repairs are unnecessary.'],'Both recognise that practical arrangements affect success.','正文列安全和清洁，2以经历说明维护必要；全拒绝、取消清洁、不需维修均相反。'),
])

block(10,'博客二：学校手机规则','''Blog

The school plans to ask pupils to keep phones in their bags during lessons. I support reducing interruptions, but a successful rule needs more than a slogan. Teachers should explain when a device can be used for a class task and what happens if a family needs to reach a pupil urgently. A school office contact number could deal with most emergencies. We should evaluate the policy after one term, asking pupils and teachers about concentration rather than simply counting confiscated phones.

Comment 1
The school should explain the reason, not only the punishment. Pupils are more likely to cooperate when they understand what a rule is trying to achieve.

Comment 2
I agree with fewer interruptions, but some pupils use a phone to manage a medical condition. The policy needs an exception for them rather than treating every device alike.

Comment 3
As a parent, I need a reliable way to get an urgent message through. If the office can guarantee that, I do not need my child to check a phone in every lesson.

Comment 4
One term is too short to announce that the problem is solved forever. Compare attention in lessons over a longer period, and ask whether teachers apply the rule consistently.

词语：confiscate没收；medical condition健康状况；consistently一致地。''',[
mc('Which comment emphasises explaining the purpose of the rule?', ['Comment 1.','Comment 2.','Comment 3.','Comment 4.'],'Comment 1.','1对比reason与punishment；其余分别谈健康例外、紧急联系、评价时间。'),
mc('Which comment supports the aim but requests a health-related exception?', ['Comment 2.','Comment 1.','Comment 3.','Comment 4.'],'Comment 2.','2先同意减少干扰，再提出医疗用途例外；不能看but就说反对目标。'),
mc('Which comment accepts the blogger’s proposed route for urgent contact?', ['Comment 3.','Comment 1.','Comment 2.','Comment 4.'],'Comment 3.','3明确office与urgent message，并以此为接受条件；其他不是联系渠道。'),
mc('Which comment is most cautious about claims of long-term success?', ['Comment 4.','Comment 1.','Comment 2.','Comment 3.'],'Comment 4.','4反对一学期就宣布永久解决，要求较长观察；不是反对所有手机管理。'),
mc('Which statement about the comments is supported?', ['They raise different conditions for applying or evaluating the rule.', 'The blogger and commenters agree that a one-term review can establish lasting benefits.', 'Comments 2 and 3 seek phone access without distinguishing between different uses.', 'Comments 1 and 4 give priority to enforcement rather than explaining or evaluating the rule.'], 'They raise different conditions for applying or evaluating the rule.', '正确依据：四条分别补充解释目的、医疗例外、紧急联系渠道和评价时间，均在讨论实施或评估条件。\n\n一学期可确定长期效果被Comment 4质疑；Comments 2、3恰在区分医疗、紧急联系与上课干扰；Comment 1要求解释，Comment 4要求观察注意力与执行一致性，不能概括成优先处罚执法。'),
])
