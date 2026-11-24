"""题目必须依赖本章之前已经给出的可操作说明。"""


def repair_bank(seeds,checks,extra):
    seeds[1][5]=('名词短语','补全“一本红色的书”：a ___ book。','a red book','a book red','一本红色的书。','red说明book的颜色，本章这个短语中放在book前。')
    seeds[1][6]=('动作句','补全“我喜欢书”：I ___ books.','I like books.','I am like books.','我喜欢书。','like本身已经是动词，这个句子不另加am；本章只使用已经解释的肯定表达。')
    checks[1][2]=('修饰关系','a red book中的red说明什么？','说明book的颜色；red是红色的。这里只说明关系，不要求说出后面章节的全部成分名称。')
    checks[1][6]=('主语','I like books（我喜欢书）谈论的是谁？','I（我），在这里作主语。')
    checks[1][7]=('动词','I like books中表示“喜欢”的动词是哪一个？','like；句子中不需要再加am。')
    checks[1][8]=('原形与形式','be与am是否是毫无关系的两个词？说明它们的关系。','不是；be是这个动词的原形，am是它在本章I am搭配中的形式。')
    checks[1][9]=('词类','book与happy分别表示名称还是特点，属于本章哪类词？','book是事物名称，属于名词；happy表示开心的状态或特点，属于形容词。')
    checks[1][10]=('形式','“am是be的一种形式”中的“形式”是什么意思？','同一个词在具体句子里的某种写法；不是说am是一种外形或一个与be毫无关系的词。')
    checks[1][11]=('否定','用she／is／not／happy写“她不开心”。','She is not happy. not放在is后。')
    checks[1][15]=('原形','既然be是原形，是否“我是一名学生”就该写I be a student？说明理由。','不该；本章这个句子按I am搭配写I am a student。原形是列词的基本形式，不等于所有句子都直接使用原形。')
    # 第3章先应用代词，不在第11章问句操作之前验收独立构造问句。
    checks[3][11]=('疑问代词','“谁是她的老师？”中的“谁”，从who／whose／what中选对应词；不要求写出整个英文问句。','who表示谁；whose表示谁的，what表示什么。')
    # 新词的首音线索在题目中也明确给出，避免把语法验收变成生词读音考试。
    for n in [4,8]:
        checks[n]=[(tag,q.replace('university前为何用a？','university（大学，已知首音是辅音/j/）前为何用a？').replace('___ honest person','___ honest person（honest的h不发音，首音是元音）'),a) for tag,q,a in checks[n]]
    checks[9]=[(tag,'已知Do you like tea?＝你喜欢茶吗；回答Yes, I do时，do在承接前面的什么内容？','承接已经明确的like tea；简答省略重复内容，不把do在这里另译成“做”。') if tag=='助动词省略' else (tag,q,a) for tag,q,a in checks[9]]
