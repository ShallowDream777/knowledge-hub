from 题库接口 import block, op, mc
from 篇章与输出练习 import cloze, completion

# 第15章：75客观题＋1段翻译＋1篇作文。人物、数字和研究场景均为原创教学设定。
block(15,'Part I·Section A·Dialogue One（第1—3题）','''本卷人物与事实为原创练习设定。试卷一限时100分钟；本部分选项各使用一次。

A. Does the ticket include the exhibition?
B. You can leave it in the room beside the entrance.
C. What time is the last entry?

Visitor: I would like a ticket for this afternoon.
Clerk: Certainly. The main gallery closes at six.
Visitor: 【1】
Clerk: Five thirty, so you will have enough time.
Visitor: 【2】
Clerk: Yes, all temporary exhibitions are included.
Visitor: Great. Where can I put this large bag?
Clerk: 【3】''',[
op('第1题选哪一句？','C','下一句给最后入场时间five thirty，故问last entry；A问票的范围，B答存包。'),
op('第2题选哪一句？','A','下一句Yes与exhibitions included回答是否包含展览；不是时间或存包。'),
op('第3题选哪一句？','B','it指large bag，room beside entrance回答存放地点。'),
],分值=3)
block(15,'Part I·Section A·Dialogue Two（第4—6题）','''A. I can check the figures tonight.
B. Shall we divide the remaining work?
C. Let us meet tomorrow to put the sections together.

Alex: The report is due on Friday, and two sections are still unfinished.
Mei: 【4】
Alex: Good idea. I will write the introduction.
Mei: 【5】
Alex: Thanks. Then we can review each other’s work.
Mei: 【6】
Alex: Tomorrow afternoon is fine.''',[
op('第4题选哪一句？','B','后句Good idea与分配引言任务，承接分工建议。'),
op('第5题选哪一句？','A','另一人承担核对数字的具体工作，符合分工延续。'),
op('第6题选哪一句？','C','下一句确认明天下午，故前句需约定明天汇总。'),
],分值=3)
block(15,'Part I·Section B（第7—10题）','''A. What made you change the opening hours?
B. How did you find out what residents needed?
C. What was the main difficulty?
D. What are you planning next?

Interviewer: 【7】
Coordinator: People told us they could not visit after work because the centre closed too early.
Interviewer: 【8】
Coordinator: We asked users at the desk and also spoke to residents who had never visited.
Interviewer: 【9】
Coordinator: Finding enough trained staff for the evening sessions.
Interviewer: 【10】
Coordinator: We hope to test Saturday mornings before making a permanent decision.''',[
op('第7题选哪一句？','A','回答改变开放时间的动机。'),op('第8题选哪一句？','B','回答收集需求的两种方式。'),op('第9题选哪一句？','C','Finding enough staff是遇到的主要困难。'),op('第10题选哪一句？','D','hope to test表下一步计划。'),
],分值=4)

block(15,'Part II·Vocabulary（第11—20题）','选择目标词在本句中最接近的意思。',[
mc('The committee endorsed the proposal after a careful review. 替换endorsed。',['approved','delayed','concealed','rewrote'],'approved','endorsed指认可支持；推迟、隐藏、重写均不是审议后的批准。'),
mc('The new arrangement eased the pressure on staff. 替换eased。',['reduced','measured','ignored','created'],'reduced','减轻压力；不等于测量、忽视或制造压力。'),
mc('The information is confidential. 替换confidential。',['private','accurate','outdated','complex'],'private','保密是可传播范围，不等于准确、过时或复杂。'),
mc('A modest increase in demand was recorded. 替换modest。',['small','sudden','certain','unlimited'],'small','modest在增长量上指有限或不大；其余改变速度、确定性、范围。'),
mc('The workers were compensated for the additional hours. compensated最接近哪项？',['paid for their extra work','warned against overtime','dismissed from their jobs','asked to train others'],'paid for their extra work','额外工作得到补偿；警告、解雇、培训他人均无该含义。'),
mc('The results contradict the earlier assumption. 替换contradict。',['conflict with','depend on','summarise','come before'],'conflict with','结果与原假设矛盾；依赖、概括和时间先后不是矛盾关系。'),
mc('The effect was temporary. 替换temporary。',['short-lived','unexpected','beneficial','widespread'],'short-lived','持续时间短；意外、有益、广泛分别是别的维度。'),
mc('The policy was implemented in September. 替换implemented。',['put into effect','carefully questioned','publicly criticised','set aside'],'put into effect','落实实施；质疑、批评、搁置都没有实施义。'),
mc('She was able to detect a slight change. 替换detect。',['notice','prevent','cause','explain fully'],'notice','察觉变化；不保证能阻止、制造或完整解释变化。'),
mc('The revised instructions are more concise. 替换concise。',['brief and clear','highly technical','less reliable','open to everyone'],'brief and clear','简洁指表达紧凑清楚；技术性、可靠度、开放对象都非本词意义。'),
],分值=10)

block(15,'Part III·Passage One（第21—25题）','''For years, the main street of Alder Town served as both a shopping area and a route for drivers crossing the town. Shop owners complained that people hurried past their windows, while residents said it was difficult to cross the road safely. The council proposed closing one short section to through traffic on Saturday mornings, leaving access for deliveries before nine.

The proposal divided traders. A café owner expected pedestrians to stay longer, but a hardware shop worried that customers carrying heavy purchases would go elsewhere. Rather than settle the argument by predicting a permanent outcome, the council agreed to a six-week trial. A nearby car park remained open, and a temporary loading point was placed at the edge of the closed section.

During the trial, volunteers counted pedestrians at the same times each Saturday. The total rose compared with the previous six Saturdays. However, a local festival took place during two of the trial weekends, and the weather was unusually dry. The council's report acknowledged that these differences made it impossible to attribute the whole increase to the traffic restriction.

The experience of individual shops also varied. The café reported more customers, while the hardware shop said sales were roughly unchanged. Neither result established what would happen in winter. Residents using wheelchairs welcomed easier crossings but said temporary signs sometimes blocked the pavement. Their comments led the council to move the signs during the fourth week.

At the end of the trial, the council extended it for another season. It retained the delivery arrangements and asked traders to provide information voluntarily. The decision was not a declaration that every town should close its main street. It reflected a narrower judgment: the idea was worth testing further, and the details of access mattered as much as the overall pedestrian count.''',[
mc('What problem helped prompt the proposed traffic restriction?', ['Difficulty crossing the road safely.', 'Customers being unable to carry heavy purchases home.', 'The nearby car park becoming unavailable on Saturdays.', 'Delivery vehicles blocking the temporary loading point.'], 'Difficulty crossing the road safely.', '正确依据：第1段居民提出安全过街困难，是建议限制车流的起因之一。\n\n重物购物是商家随后对方案的担忧，不是已经造成该建议的事实；停车场一直开放；临时装卸点属于试点配套，文中没有送货车阻塞它的记录。'),
mc('Why was a temporary loading point provided?', ['To preserve a way of handling deliveries and heavy purchases.', 'To create a place where volunteers could count pedestrians.', 'To accommodate visitors attending the local festival.', 'To obtain comparable sales figures from the traders.'], 'To preserve a way of handling deliveries and heavy purchases.', '正确依据：第2段先写五金店担心重物购买，再给保留停车场与边缘装卸点，回应可达性。\n\n计数在第3段出现，但没有说在装卸点进行；节庆是影响客流的另一因素；商户自愿交信息是末段安排，与设置装卸点的用途不同。'),
mc('What can be concluded from the higher pedestrian count?', ['Other conditions may have contributed to the increase.', 'The trial showed that pedestrian growth continued into winter.', 'The festival explained the increase recorded on each trial weekend.', 'The rise in visitors was matched by higher sales at the hardware shop.'], 'Other conditions may have contributed to the increase.', '正确依据：第3段节庆与干燥天气妨碍将全部增长归于限制车流，所以其他条件可能有贡献。\n\n冬季尚未测量；节庆只发生在两次周末，不能解释每次，也没有被确认为唯一原因；五金店说销售大致不变，不能把客流上涨等同于销售增加。'),
mc('The wheelchair users’ comments illustrate what?', ['A beneficial aim may still require changes to practical details.', 'A six-week trial can establish whether winter access will be adequate.', 'Access concerns can be settled by keeping delivery arrangements unchanged.', 'Visitor totals provide a more useful measure than individual experiences.'], 'A beneficial aim may still require changes to practical details.', '正确依据：轮椅使用者欢迎更容易过街，同时指出标牌挡路，机构据此移走标牌，说明收益与细节改进并存。\n\n他们没有提供冬季证据；送货安排无法处理标牌占道这一问题；个体反馈反而发现了总人数不能显示的障碍，不是在贬低这些经历。'),
mc('Which best describes the council’s final position?', ['Support for further testing with attention to access.', "Approval of a permanent scheme based on the café's increased trade.", 'Continuation of the trial chiefly to raise pedestrian totals.', 'Suspension of the trial until winter sales figures became available.'], 'Support for further testing with attention to access.', '正确依据：末段延长一个季节继续测试，并强调可达细节与客流同样重要。\n\n尚未永久批准，也没有仅凭咖啡馆表现定案；‘chiefly ... totals’遗漏末句对可达性的并重；延长试验不是暂停等待数据。'),
],分值=5)

block(15,'Part III·Passage Two（第26—30题）','''When a training centre received donated laptops, the staff first celebrated the number of devices. They expected a shortage that had prevented learners from practising at home to disappear almost immediately. The machines looked clean and switched on successfully, so the centre advertised a new lending scheme.

The first borrowers revealed difficulties that the initial count had hidden. Some batteries lasted less than an hour. Several machines could not run the software used in class. Others required a password that the donor no longer remembered. A device that appeared to be available was not necessarily ready for a particular learner's task.

The centre hired a technician to check the laptops before lending them again. She assessed battery condition, installed appropriate software and removed personal files left by previous owners. Machines that could not be made suitable at a reasonable cost were used for spare parts. The aim was to provide fewer dependable devices rather than a larger total that users could not rely on.

Borrowing rules changed too. Staff explained what support the centre could provide and asked learners to report faults without fear of being blamed automatically. This helped distinguish existing damage from problems arising during a loan. A short return form also recorded which tasks a learner had been unable to complete.

After three months, the number of laptops in circulation was lower than the number originally donated, yet complaints about unexpected failures had decreased. Staff no longer treated the size of the cupboard as the most important measure. They looked instead at whether learners could complete the work for which a device had been borrowed.

The scheme remained valuable, but its success depended on maintenance, clear expectations and a match between equipment and purpose. Donation was the beginning of a service, not its completion.''',[
mc('Why did the centre initially expect the shortage to disappear?', ['The donated machines appeared usable when switched on.', 'A technician had already checked their batteries and software.', 'The donor had supplied passwords and continuing technical support.', 'Borrowers had successfully completed their class tasks on the machines.'], 'The donated machines appeared usable when switched on.', '正确依据：首段clean和switched on successfully是最初乐观判断的依据。\n\n技术员检查是暴露问题之后的措施；捐赠者反而忘记一些密码，持续支持也未提及；借用者最初发现故障，不能把后来的功能目标当已完成测试。'),
mc('Which issue was discovered by early borrowers?', ['Some devices could not run the required software.', 'The centre lacked a clear way to count the donated machines.', "Removing users' files had caused several passwords to stop working.", 'Learners were charged for faults that the technician had already repaired.'], 'Some devices could not run the required software.', '正确依据：第2段Several machines could not run the software used in class直接对应。\n\n首段已经以设备总数乐观，并未说无法计数；忘记密码发生在清理前，不能归因于删文件；后来避免自动责怪借用者，也不证明曾对已修故障收费。'),
mc('Dependable in Paragraph 3 most nearly means what?', ['Reliable.', 'Compatible.', 'Affordable.', 'Accessible.'], 'Reliable.', '正确依据：users could rely on直接解释dependable，指能可靠完成用途。\n\ncompatible是兼容，只对应某一软件问题；affordable是价格可承受，维修成本虽被考虑却不是本词意思；accessible是可获得、可接近，不能保证借到后正常工作。'),
mc('Why were learners asked to report faults without automatic blame?', ['To help identify when and how problems arose.', 'To decide which borrowers should receive the remaining laptops.', "To replace technical checks with users' accounts of damage.", "To show that faults usually came from learners' unfamiliarity with software."], 'To help identify when and how problems arose.', '正确依据：第4段distinguish existing damage from problems arising during a loan说明要区分故障原有还是借用期间出现。\n\n没有按报错分配设备的规则；用户反馈补充检查，没有替代技术检查；原文没有把多数故障归因于学习者不会软件。'),
mc('What is the main lesson of the passage?', ['Useful access depends on a functioning service, not merely a device count.', 'Donated equipment works best when software is standardised before acceptance.', 'A smaller stock reduces the effort required to manage a lending service.', "Learners' ability to repair devices determines the value of a donation."], 'Useful access depends on a functioning service, not merely a device count.', '正确依据：从按数量乐观，到检查维护、借用规则和任务完成，全文强调捐赠只是服务的起点。\n\n软件是一个问题，但接收前统一软件不是全篇方案；设备减少不等于管理工作量已经降低；维修由技术员承担，并未要求学习者先有修理能力。'),
],分值=5)

block(15,'Part III·Passage Three（第31—35题）','''A school science club began measuring the temperature of a stream that crossed the edge of town. Students hoped their records would show whether a small shaded section remained cooler than an exposed one. They borrowed identical devices and agreed to take readings at the same time each week.

During the first month, one group repeatedly recorded higher temperatures than the others. Its members suggested that a nearby building might be warming the water. Before presenting this as a finding, the teacher asked every group to place its device in the same container of water. The unusually high readings followed one device rather than one location.

The discovery did not make the project pointless. It gave students a reason to discuss calibration: checking whether instruments provide comparable results. They adjusted their procedure, labelled the devices clearly and repeated measurements at several locations. They also noted recent rainfall and the amount of sunlight reaching the water.

At the end of the term, the records suggested that the shaded section was often cooler, but the difference was not identical every week. Students explained that their observations described a limited period. They could not establish what happened in other seasons, nor could they conclude that shade was the only influence on temperature.

The teacher considered this careful statement a success. The project had not produced a dramatic accusation against the nearby building. Instead, it had taught students to test an explanation against alternatives and to preserve information about conditions that might matter.

Local residents were invited to read a summary. The students included their changed method and the initial instrument problem rather than presenting only the cleanest final figures. They argued that an honest account of uncertainty made the records more useful to anyone who wanted to continue the work.''',[
mc('What were students originally trying to compare?', ['Water temperatures in shaded and exposed sections.', 'Temperatures recorded with devices of different designs.', "The stream's temperature before and after construction of a building.", 'The amount of rainfall at several measuring sites.'], 'Water temperatures in shaded and exposed sections.', '正确依据：首段明确比较遮阴段与暴露段水温，并借相同设备、约定每周同一时间。\n\n不同设计设备不是研究目标；建筑增温是首月高读数引出的后续假说，不是原始比较；降雨是后来附记条件，没有以各点降雨量为最初研究对象。'),
mc('What did placing all devices in one container help reveal?', ['One instrument produced unusually high readings.', "The building's effect depended on where a device was placed.", 'Temperature differences between sites disappeared after rainfall.', 'The students had taken their weekly readings at different times.'], 'One instrument produced unusually high readings.', '正确依据：第2段高读数跟随一个设备，而非某地点，支持仪器异常。\n\n没有证明建筑的空间效应；容器对照与降雨变化不是一回事；约定同一时刻并不等于实际违反约定，文中未指出错时测量。'),
mc('Calibration is explained as a process of what?', ['Checking comparability between instruments.', 'Recording differences in sunlight at measuring sites.', 'Repeating observations to cover a longer season.', "Comparing student explanations with residents' memories."], 'Checking comparability between instruments.', '正确依据：第3段冒号后checking whether instruments provide comparable results就是本词在文中的解释。\n\n日照属于环境记录；延长季节属于观察范围；居民是阅读总结的人，文中没有拿他们的记忆校验学生解释。不能把项目的其他环节替代词义。'),
mc('What can be inferred about the teacher’s view of a successful project?', ['Careful reasoning can matter more than a dramatic claim.', 'Accurate instruments make it unnecessary to record surrounding conditions.', 'A stable numerical difference matters more than revising the method.', 'Identifying a local cause is the main value of school research.'], 'Careful reasoning can matter more than a dramatic claim.', '正确依据：教师把谨慎结论视作成功，随后以未指控建筑而学会检验其他解释作对照。\n\n校准后仍记录降雨日照，故准确仪器不能替代环境记录；教师认可发现仪器问题、改方法并报告变化，并未把恒定数差置于方法修正之上；‘local cause’把被放下的指控变成主要价值。'),
mc('Why did students describe the initial instrument problem in their summary?', ['To make the limitations and revised method transparent.', 'To explain why future observations should use a different stream.', 'To establish that the corrected figures applied to other seasons.', 'To persuade residents that equipment checks could replace repeated observations.'], 'To make the limitations and revised method transparent.', '正确依据：末段说明初始问题与修改方法一并公开，诚实描述不确定性方便别人接续工作。\n\n没有换河的建议；他们明确不能推广到其他季节；校准之后仍重复测量，不是以设备检查代替观察。'),
],分值=5)

block(15,'Part III·Passage Four（第36—40题）','''After a storm damaged the building used by a small local museum, its staff had to decide what to restore first. They could not display every object, and several written descriptions had been lost. A quick solution would have been to select the most attractive objects and give each a short name. The curator thought this would produce a room that looked complete while leaving much of its meaning absent.

She asked former residents and workers to help reconstruct the stories connected with the collection. A plain wooden box, for example, had once held tools shared by families employed at the nearby mill. The box was not valuable because of its material. Its importance lay in the arrangements that allowed families with little money to repair household items.

Personal memories brought detail, but they did not always agree. One person recalled that the box had been kept in a shop, while another placed it in a meeting room. Rather than choose the more confident speaker automatically, the museum compared the accounts with photographs, dates and surviving records. Where uncertainty remained, the label said so.

The reopened display contained fewer objects than before the storm. Some visitors missed the crowded shelves, yet others said that they now understood why ordinary things had been saved. An audio recording allowed them to hear different accounts without treating every memory as an equally verified fact.

The curator did not argue that an object was unimportant without a story. She argued that the way an institution interprets its collection shapes what visitors can learn from it. Restoration therefore involved more than repairing walls or polishing wood. It required rebuilding the connections between objects, evidence and the lives in which those objects had played a part.''',[
mc('Why did the curator reject a display based only on attractive objects and names?', ['It could appear complete while lacking important meaning.', 'It would leave too little room for the objects saved from the storm.', 'It would make visitors rely too heavily on conflicting personal memories.', 'It would delay reopening while damaged objects were being repaired.'], 'It could appear complete while lacking important meaning.', '正确依据：首段looked complete与meaning absent形成对比，担心外观完整而意义缺失。\n\n选择部分漂亮物件不是空间过挤的问题；口述记忆是后续方案中的证据来源，不是仅摆物件加名称的后果；快速方案恰是quick solution，未说会拖延重开。'),
mc('The wooden box is mentioned mainly to illustrate what?', ['An ordinary object can reveal social arrangements.', "Repairing an object's material can recover its historical value.", "Factory records are more accurate than residents' memories.", 'Objects shared by families were usually kept in a meeting room.'], 'An ordinary object can reveal social arrangements.', '正确依据：木箱材质普通，价值在于它承载低收入家庭共享工具、修理用品的安排。\n\n例子强调意义而非修木材；它没有比较工厂档案与记忆的普遍准确度；放在何处恰有冲突，且不能由一个箱子推出共享物件通常放会议室。'),
mc('How were conflicting memories handled?', ['They were compared with other available evidence.', 'They were resolved by choosing the account with the most detail.', 'They were combined into a single account before the labels were written.', 'They were left to visitors to judge without the museum checking them.'], 'They were compared with other available evidence.', '正确依据：第3段列出photographs, dates and surviving records，说明以其他证据交叉核对。\n\n细节多不等于已证实，文中也未按详细程度裁决；有些不确定性留在标签，不是先合并成唯一说法；录音呈现多种记忆也不表示馆方省去核查。'),
mc('What does interprets in the last paragraph most nearly mean?', ['Explains the meaning and context of.', 'Restores the appearance and condition of.', 'Determines the source and ownership of.', 'Selects the most representative examples of.'], 'Explains the meaning and context of.', '正确依据：末段谈游客能从藏品学到什么，并连起物件、证据与生活，interprets是阐释意义和语境。\n\n修外观是物理修复，不涵盖故事解释；来源所有权只是可能的资料问题，不等于阐释；选代表物件是筛选，也不是本句的意义说明。'),
mc('Which title best captures the passage?', ['Restoring the Connections Behind Museum Objects.', 'Choosing Attractive Objects for a Smaller Museum.', 'Recording the Memories of a Mill Community.', 'Reopening a Museum by Repairing Its Collection.'], 'Restoring the Connections Behind Museum Objects.', '正确依据：全文从物理受损写到重建故事、核验证据、解释物件与生活的联系，正确标题覆盖整个转向。\n\n选漂亮物件是被拒的捷径；记录工厂社区记忆仅覆盖木箱及部分口述工作；维修藏品重开只覆盖物理层面，漏掉末段强调的意义连接。'),
],分值=5)

block(15,'Part III·Section B（第41—45题）','''Blog

Our community centre has proposed opening on Sunday afternoons. The aim is to give families and people who work on Saturdays another chance to use the rooms. I support a trial, but I do not think a new timetable alone guarantees access. A caretaker must be present, someone needs to check the equipment, and users need a clear way to book. The centre has suggested a small room fee to cover these costs, with exemptions for groups that cannot afford it. After three months, it should ask both users and people who stayed away what helped or prevented them from attending. Counting bookings alone could overlook people excluded by transport or cost.

Comment 1
Sunday would help my family, but the last bus home leaves at four. If sessions end later, we would still be unable to attend. The centre should talk to the transport provider before announcing success.

Comment 2
Our group could pay a modest fee, but not everyone can. I support the proposed exemptions, provided that applying for them is simple and does not require people to disclose unnecessary personal details.

Comment 3
We tried longer hours in another centre. It worked when a trained caretaker was on duty. When staff cover became unreliable, people arrived to find doors locked. Clear responsibility matters more than a poster advertising new hours.

Comment 4
Three months will give some information, but the centre should also check what happens in winter. A timetable that works in light evenings may not meet the same needs in cold, dark weather.''',[
mc('What does the blogger recommend?', ['A trial evaluated through more than booking totals.', 'A three-month trial judged by feedback from groups that booked rooms.', 'Longer opening hours funded by charging each group for staff costs.', 'A permanent Sunday timetable once a caretaker has been appointed.'], 'A trial evaluated through more than booking totals.', '正确依据：正文要求同时询问参加与未参加者，避免预订数漏掉受交通或费用排除的人。\n\n只问已预订群体漏掉people who stayed away；费用安排有豁免，并非每组分担；支持的是试行，不是聘好管理员就立即永久确定。'),
mc('Which comment focuses on a transport obstacle?', ['Comment 1.','Comment 2.','Comment 3.','Comment 4.'],'Comment 1.','1给末班车时间；2费用豁免，3值守，4季节评价。'),
mc('Which comment supports fee exemptions while adding a condition?', ['Comment 2.','Comment 1.','Comment 3.','Comment 4.'],'Comment 2.','2支持exemptions并要求申请简便保护个人资料；其他不是费用条件。'),
mc('Which comment offers experience showing the need for dependable staffing?', ['Comment 3.','Comment 1.','Comment 2.','Comment 4.'],'Comment 3.','3描述另一中心人到门锁的经历；其余没有这项实践证据。'),
mc('Which comment questions whether the initial trial period covers enough conditions?', ['Comment 4.','Comment 1.','Comment 2.','Comment 3.'],'Comment 4.','4要求检查冬季，讨论季节代表性；其他是交通、豁免、值守条件。'),
],分值=5)

cloze(15,'Part IV·Cloze（第46—55题）','''A company introduced a mentoring scheme for new employees. The aim was to help them understand work that was difficult to describe in a manual. Experienced staff could 【46】 practical advice, while newcomers could ask questions before a small mistake became a larger problem.

The first version of the scheme depended on informal meetings. 【47】, some pairs rarely found time to talk. The company therefore set aside a short period each week and asked mentors to agree on a clear 【48】 for each session.

Managers were told not to use the meetings as a hidden performance test. If employees feared that every question would count 【49】 them, they might stay silent. Trust was therefore an essential 【50】 of the arrangement.

The scheme also needed evaluation. The number of meetings held could not, by itself, 【51】 that useful learning had occurred. Staff were asked to describe a problem they had handled differently as a 【52】 of the discussions. These examples helped the company identify where advice had been practical and where it had remained too 【53】.

At the end of the trial, the company kept the regular sessions but allowed teams to 【54】 them to local needs. It had learned that a clear structure and some flexibility were not opposing goals. Used together, they could make support more 【55】.
''',[
(['offer','conceal','consume','doubt'],'offer','offer advice提供建议；隐藏、消耗、怀疑不对应帮助新人。'),
(['However','Therefore','Similarly','For example'],'However','原先依赖非正式会面但难找时间，转折；不是前句结果或有效会面实例。'),
(['purpose','location','duration','sequence'],'purpose','正确依据：会面需要有清楚的学习目的，后文要求说明解决了什么问题，呼应purpose。location只说地点；duration是时长，前面已安排short period，这里不是用clear来交代长短；sequence是顺序，文中没有一场会面内部的步骤安排。'),
(['against','beside','through','among'],'against','count against someone表示对某人不利；其他介词不形成该评价搭配。'),
(['condition','outcome','assessment','incentive'],'condition','正确依据：担心被扣分就保持沉默，因此信任是正常交流得以开展的前提。outcome将前提改成结果；assessment是评估；incentive是激励因素，比不上本句essential所强调的必要条件，文中也未将信任设为参与奖励。'),
(['demonstrate','prevent','prefer','hide'],'demonstrate','会面数不能单独证明学习；阻止、偏好、隐藏均非证据判断。'),
(['result','matter','piece','means'],'result','as a result of由于……；其他词不组成这里的因果表达。'),
(['general','useful','specific','relevant'],'general','与practical对比，建议可能太泛；有用、具体、相关不是需要改进的反方向。'),
(['adapt','submit','attribute','restrict'],'adapt','正确依据：adapt sessions to local needs表示按当地需要调整，与后文flexibility呼应。submit是提交，不能自然说提交会面给需求；attribute ... to是把原因归于某事，不是安排调整；restrict ... to是限于某范围，不能表达这里保留结构同时因地制宜的意思。'),
(['effective','expensive','secret','accidental'],'effective','结构与灵活性共同使支持有效；昂贵、秘密、偶然不合结尾正面目标。'),
],start=46)

completion(15,'Part V·Text One（第56—61题）',['access','demand','maintain'],
 ['improve ___ to services','respond to local ___','___ the equipment'],
 '''A centre decided to open a small workshop in a neighbourhood that had few shared facilities. The aim was to 【59】 for people who could not travel far. Before choosing its activities, staff asked residents what they wanted. The resulting timetable would 【60】 rather than simply copy another centre. The project also needed a repair budget. Volunteers could help with daily tasks, but qualified workers would 【61】 so that users could rely on it.''',
 [(0,'access to services是可获得服务。'),(1,'local demand当地需求，local修饰名词。'),(2,'maintain接equipment表示维护。')],
 [(0,'远处出行困难对应改善服务可达性。'),(1,'先问需求再排时刻，非机械照搬别处。'),(2,'repair budget与qualified workers共同支持维护设备。')],start=56)
completion(15,'Part V·Text Two（第62—67题）',['aware','limits','explain'],
 ['be ___ of uncertainty','recognise the ___ of a sample','___ how the figures were collected'],
 '''A research group published a report on travel habits. It included a section designed to 【65】 so that readers could assess the method. The researchers had interviewed people at only two stations and therefore needed to 【66】. They did not claim to describe every resident. Readers, too, should 【67】 rather than treat a single percentage as an unquestionable account of the whole city.''',
 [(0,'be aware of意识到；aware为形容词。'),(1,'the limits of a sample样本限制，limits为名词。'),(2,'explain how ...解释方式内容，需动词。')],
 [(2,'前有to，后面readers assess method要求说明采集方法。'),(1,'仅两站样本，对应recognise limits。'),(0,'should后接be原形；不要把单一比例当绝对描述，需意识到不确定性。')],start=62)
completion(15,'Part V·Text Three（第68—75题）',['evidence','understand','unnecessary','responsibility'],
 ['take ___ for decisions','help users ___ the choices','avoid ___ complexity','provide supporting ___'],
 '''When an organisation changes an important rule, it should 【72】 rather than present the change as something nobody controls. A clear explanation can 【73】, especially when several alternatives have been considered. This does not mean every document must be long. Writers should 【74】 by removing repetitions and defining unfamiliar terms. At the same time, a brief statement should still 【75】 so that readers can examine the reasons instead of merely accepting a conclusion.''',
 [(3,'take responsibility for承担责任。'),(1,'help users understand为help＋宾语＋原形。'),(2,'unnecessary修饰complexity，不必要的复杂。'),(0,'supporting evidence支持性证据。')],
 [(0,'组织对决定负责，与nobody controls对比。'),(1,'清楚解释帮助用户理解选项。'),(2,'去重复、释术语旨在避免不必要复杂。'),(3,'让读者审查理由，需要支持证据。')],start=68)

block(15,'试卷二·Part VI·Translation（第76项，10分）','''试卷二限时50分钟，翻译与作文共用。将下段译成中文。

Public information is useful only when people can understand what action they are expected to take. A notice may contain every required detail and still leave readers confused if those details are presented in an unfamiliar order. Before adding another paragraph, writers should ask which question a reader is likely to raise first. Testing a draft with a few people can reveal difficulties that its author no longer notices. This does not guarantee that everyone will interpret the message in exactly the same way. It does, however, provide an opportunity to improve the notice before misunderstandings affect a much larger audience.''',[
op('独立翻译整段。','公共信息只有在人们能理解自己需要采取什么行动时才有用。一则通知即使包含了所有必要细节，如果这些细节按读者不熟悉的顺序呈现，仍可能让人困惑。在再增加一段内容前，撰写者应先想一想读者最可能首先提出什么问题。请少数人试读草稿，可以发现作者本人已注意不到的困难。这不能保证所有人都会以完全相同的方式理解信息。不过，它确实提供了一个机会，让通知能在误解影响更多读者之前得到改进。','按10个意义单元各1分：有用的条件；预期行动；细节齐全仍可能困惑；顺序原因；先想读者首问；小范围试读；作者不再注意到；不保证完全同解；however转折与强调；扩大影响前改进。'),
],分值=10)
block(15,'试卷二·Part VII·Writing（第77项，15分）','''Write a composition of at least 150 words on The Value of Asking Questions. Explain how asking questions can help learning or work. Give reasons and at least one example, and discuss how to ask questions responsibly.''',[
op('先列简短提纲，再完成全文。','''Asking questions is an important part of both learning and work. It allows people to discover what they do not yet understand and can prevent a small uncertainty from developing into a larger mistake. A question should therefore be treated as a possible starting point for improvement.

In learning, questions make vague difficulties more specific. A student who says that a whole chapter is confusing may not know how to begin. If the student asks why one form is used in a particular sentence, a teacher can identify the missing step and provide useful guidance. The student can then apply the explanation to a new example rather than simply memorise an answer.

At work, asking for clarification can also protect shared goals. Before carrying out an unfamiliar task, an employee may need to confirm the deadline or the required result. However, responsible questioning involves preparation. People should check the information already available, explain what they have tried and listen carefully to the response.

Questions are most valuable when they lead to thought and action. Used with preparation and respect, they support understanding, cooperation and better decisions.''','训练量表15分：任务5（价值、学习或工作、例子、负责提问）；组织4；准确4；表达2。示范讨论具体提问如何定位缺口，并给准备与倾听的边界；不是一味鼓励不做任何准备地追问。',类型='作文'),
],分值=15)
