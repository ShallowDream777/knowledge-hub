from pathlib import Path
from html.parser import HTMLParser
import re

ROOT=Path(__file__).resolve().parents[1]


class AnswerHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text=[]
        self.blocks=0
        self.bold=0

    def handle_starttag(self, tag, attrs):
        if tag in ('p','li','br','div','tr'):
            self.blocks+=1
        if tag=='strong':
            self.bold+=1

    def handle_data(self,data):
        self.text.append(data)


def check():
    files=[*sorted((ROOT/'章节').glob('*.md')),
           *sorted((ROOT/'强化题目').glob('*·强化练习·*.md'))]
    folds=0
    for path in files:
        s=path.read_text(encoding='utf-8')
        for match in re.finditer(r'<details>\s*<summary>.*?</summary>([\s\S]*?)</details>',s):
            content=match.group(1)
            parser=AnswerHTML()
            parser.feed(content)
            visible=''.join(parser.text)
            assert '**' not in visible,(path.name,'答案会显示Markdown星号',visible[:90])
            assert not re.search(r'`[^`]+`',visible),(path.name,'答案会显示Markdown反引号')
            assert parser.blocks>0,(path.name,'没有明确的HTML段落或换行')
            # 每个强化题编号必须独立成段，不能靠HTML中的普通空白换行。
            ids=re.findall(r'(?:\*\*|<strong>)([ABCD]\d{2})(?:\*\*|</strong>)',content)
            if ids:
                assert parser.bold>=len(ids),(path.name,'题号未渲染成粗体')
                assert parser.blocks>=len(ids),(path.name,'多道答案缺少逐题段落')
            folds+=1
    # 原有127组；外部资料吸收新增6组，祈使句带学新增1组随堂答案。
    assert len(files)==62 and folds==134,(len(files),folds)
    print(f'通过：{len(files)}份文件、{folds}个折叠块内无裸Markdown标记；答案有明确段落，强化题号使用strong。')


if __name__=='__main__':
    check()
