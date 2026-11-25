"""第11章祈使句试改：从交际目的到结构理解与独立表达。"""
from pathlib import Path
import re

LESSON = '''#### 祈使句

**学习目的：**当你想直接请求、提醒或制止对方做某件事时，能正确组织句子、使用动词形式；阅读时，能看懂这些行动要求。

例如，描述“你很安静”用 **You are quiet.**；提醒“安静一点”用 **Be quiet.**。quiet＝安静的。表达目的变了，句子结构也随之改变：普通祈使句通常不写 you，动词用原形，所以这里用 **be**，不用 are。

**常用表达：**

| 你想表达什么 | 句子怎样组成 | 例句 |
|---|---|---|
| 让对方做某事 | 动词原形 + 必要的内容 | Open the door. 打开门。 |
| 提醒对方保持某种状态 | Be + 形容词 | Be careful. 小心。careful＝小心的。 |
| 不让对方做某事 | Don't + 动词原形 | Don't run. 不要跑。 |
| 提醒对方不要处于某种状态 | Don't be + 形容词 | Don't be late. 别迟到。late＝迟到的。 |
| 提议一起做或不做 | Let's + 动词原形；Let's not + 动词原形 | Let's go. 我们走吧。Let's not run. 我们别跑了。 |

通常不写出的 you 指听话人，可以是“你”或“你们”；对一个人或几个人说，动词都用原形。Don't 是 do not 的缩写；Let's 是 let us 的缩写，在表中的用法是提出共同建议。

**please 只表示“请”，不决定句子是不是祈使句。**Open the door. 和 Please open the door. 都是祈使句。please 也可以放句末，如 **Open the door, please.** 语气是否礼貌还要看场合和说话方式。

**试着使用：**

1. 在图书馆，你想请同伴安静一点。用 quiet 写一句祈使句。
2. 提醒朋友别迟到，有人写成 Don't are late.。请改正，并说明动词为什么这样写。
3. 你想建议和朋友一起休息一下。用 take a break（休息一下）表达。

<details>
<summary>先独立作答，再展开答案与解析</summary>
<p><strong>1.</strong> Be quiet, please. / Please be quiet. 你是在提醒对方，使用原形 be；You are quiet. 则是在描述对方的状态。</p>
<p><strong>2.</strong> Don't be late. Don't 后接动词原形，are 的原形是 be。</p>
<p><strong>3.</strong> Let's take a break. Let's 明确提出一起做；Take a break. 是直接劝对方休息，没有明确提出共同休息。</p>
</details>
'''

RECAP = '''###### （6）祈使句

**补充 let 的另一种用法：让某人做。**Let him go. 是“让他走”；Let me help you. 是“让我帮你”。结构为 **Let + 人的宾格形式 + 动词原形**，him、me 是前面学过的宾格。这与 Let's go（我们一起走吧）的共同建议不同。

句尾有时加一句征求意见的话：**Let's go for a walk, shall we?**（我们去散步，好吗？go for a walk＝去散步。）共同建议常接 shall we；**Let us go, will you?** 若表示请求别人放行，则是“让我们走，好吗？”，常接 will you。按具体用意区分，不单凭是否缩写判断是否包括听话人；句尾表达先能识别即可。
'''

def revise(text, path):
    path = Path(path)
    if path.parent.name != '章节' or path.parent.parent.name != '英语学习资料·完整线性版' or not path.name.startswith('11·'):
        return text
    for title, body in [('#### 祈使句', LESSON), ('###### （6）祈使句', RECAP)]:
        level = len(title.split(' ')[0])
        pattern = '^' + re.escape(title) + r'\n[\s\S]*?(?=^#{1,' + str(level) + r'} |\Z)'
        text, count = re.subn(pattern, lambda _: body.strip() + '\n\n', text, count=1, flags=re.M)
        assert count == 1, ('祈使句小节定位失败', title)
    # 原目录未单列祈使句；试读入口直接指向正文原有标题。
    item = '- [[#祈使句|祈使句：用途、表达与情境练习]]'
    if item not in text:
        pattern = r'^- \[\[#句子种类[^\n]+\n'
        text, count = re.subn(pattern, lambda m: m[0] + item + '\n', text, count=1, flags=re.M)
        assert count == 1, '缺少句子种类目录项'
    return text
