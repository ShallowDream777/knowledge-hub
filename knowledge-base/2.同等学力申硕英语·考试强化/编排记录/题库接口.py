BLOCKS = {n: [] for n in range(1, 17)}


def op(question, answer, explanation='', **extra):
    return {'题目':question, '答案':answer, '解析':explanation, '类型':'开放', **extra}


def mc(question, options, answer, explanation):
    assert len(options)==4 and len(set(options))==4
    assert answer in options
    return {'题目':question,'选项':options,'正确项':answer,'解析':explanation,'类型':'单选'}


def block(chapter,title,context,items,**extra):
    BLOCKS[chapter].append({'标题':title,'材料':context,'题目':items,**extra})


def lines(chapter,title,rows):
    items=[]
    for row in rows.strip().splitlines():
        q,a,why=row.split('|')
        items.append(op(q,a,why))
    block(chapter,title,'每题先独立分析，再用完整中文或英文作答。题中的限定信息也要保留。',items)
