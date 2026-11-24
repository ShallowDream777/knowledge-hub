"""早期原自测补中文语境，避免用未提供词义和后章规则作验收门槛。"""
from 内容校订 import fix_questions
import re

MEANINGS={
5:'''我有许多信息
她给了我一条好建议
农场上有三只羊
这些孩子很开心
我买了两条裤子
这是我父母共用的一间房
房子的屋顶是红色的
我喝了两杯水
他是我的一位朋友
我们有许多家庭作业
这个消息很好
我的家庭是个大家庭
两位过路人走了进来
我需要一片面包
房间里有一些家具
一杯咖啡
我有一副眼镜
老师们的办公室在楼上
我喜欢这些苹果
水对我们很重要
熟悉英语／具备良好的英语知识
春节很重要
河里有许多鱼
我每天早上吃面包
汤姆和杰里的各自房间都很干净
天空的颜色是蓝色
我在公园里看见两位女士
她留着长发
今天车辆很多
这是我朋友的一张照片'''.splitlines(),
6:'''她是个漂亮的女孩
他跑得快
这食物尝起来不错
他是班里最好的学生
这本书比那本更有趣
她唱得比我更动听
天气越来越冷
他年龄足够大，可以开车
我有重要的事告诉你
她和她妈妈一样高
你练习越多，就会说得越好
这个箱子是那个的三倍重
他每天努力工作
她很漂亮
那个正在睡觉的男孩是我的兄弟
我们有足够时间完成
他在所有人中最高
他总是迟到；使用本章中性的常见副词位置
我非常喜欢音乐
他英语说得好
这里的天气比广州的天气更冷
她比以前仔细得多
人越多越热闹；merry在这里表示欢乐的
他是我们班最勤奋的学生
这是一张好看的新木桌'''.splitlines(),
8:'''我们班有二十五位学生
他是第一位学生
今天是我在这里的第一天
学生中三分之二是女生
这个箱子是那个的三倍重
他赢得二等奖
我七点起床
现在差十分八点
我有一本字典
桌上有一个橙子
他是一个诚实的男孩；honest首音是元音
这是一本有用的书；useful首音是辅音
桌上那本双方确定的书是我的
她弹钢琴
他踢足球
我们十二点吃午饭
水很重要；泛指水
我看见一条狗，那条狗很大
他是我们班最高的学生
请给我一杯咖啡
这些水的三分之二是脏的；dirty表示脏的
这里有两百位学生
数百位学生来到这里
一等奖给汤姆
我们有足够的时间'''.splitlines(),
}


def revise(s,n):
    if n==5:
        s=fix_questions(s,n,0,{4:('The children are happy.','✅ children是child的不规则复数，搭配are；happy表示开心的。'),22:('The Spring Festival is important.','✅ the Spring Festival是本课程已经给出的习惯名称，important表示重要的；本题只核对名词名称与限定。')})
    if n==6:
        s=fix_questions(s,n,0,{18:('He ______ late. (is always / always is / is alwaysly)（按本章中性常见位置表达“他总是迟到”）','is always（频度副词在本题中放be后）；特殊重音可能改变位置，本题限定中性常见顺序，不要求尚未演示的动词变换。')})
    if n==8:
        s=fix_questions(s,n,0,{
          21:('Two thirds of the water ______ dirty. (is / are / am)（dirty＝脏的）','is（water在本题为不可数名词，比例后的整体与is搭配）'),
          22:('There are two ______ students here. (hundred / hundreds / hundred of)','hundred（前面有具体数字two，写two hundred）'),
          23:('______ of students came here. (Hundreds / Hundred / Three hundred)','Hundreds（概数“数百”用hundreds of，不是具体three hundred）'),
          24:('The ______ prize is for Tom. (first / one / oneth)','first（一等奖用序数词first；prize意为奖）'),
        })
    pattern=r'(?m)^### [^\n]*高频易错自查[^\n]*\n[\s\S]*?(?=<details>)'
    m=re.search(pattern,s);assert m,n
    block=m.group();meanings=MEANINGS[n]
    assert len(re.findall(r'^\d+\. ',block,re.M))==len(meanings)
    block=re.sub(r'^(\d+)\. (.+)$',lambda x:x.group()+f'（句意：{meanings[int(x.group(1))-1]}。）',block,flags=re.M)
    first,rest=block.split('\n',1)
    block=first+'\n\n本组只检查本章已教的部位；句意已附，不要求凭未学过的其他结构判断整句。\n'+rest
    return s[:m.start()]+block+s[m.end():]
