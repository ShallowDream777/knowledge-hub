"""Obsidian不解析HTML内部的Markdown；折叠内容全部输出为明确HTML。"""
from html import escape
import re


def inline(text):
    # 先转义正文，防止英语比较符号等被误当HTML。
    text=escape(text,quote=False)
    text=re.sub(r'`([^`]+)`',r'<code>\1</code>',text)
    text=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',text)
    return text


def html_body(body):
    output=[]
    for paragraph in re.split(r'\n\s*\n',body.strip()):
        lines=[line.strip() for line in paragraph.splitlines() if line.strip()]
        if not lines:
            continue
        if all(re.fullmatch(r'-{3,}',line) for line in lines):
            output.append('<hr>')
        else:
            # 显式段落和行内换行；数字题号保留原样，不能依赖HTML空白。
            output.append('<p>'+'<br>\n'.join(inline(line) for line in lines)+'</p>')
    return '\n'.join(output)


def format_answers(markdown):
    def convert(match):
        content=match.group(2)
        # 可以对已修正文件重复调用，不重复转义strong/p等标签。
        if re.match(r'\s*<(?:p|hr|div|ol|ul)\b',content):
            return match.group()
        summary=escape(match.group(1).strip(),quote=False)
        return '<details>\n<summary>'+summary+'</summary>\n'+html_body(content)+'\n</details>'
    return re.sub(r'<details>\s*<summary>(.*?)</summary>([\s\S]*?)</details>',convert,markdown,flags=re.S)


def markdown_answers_for_check(markdown):
    """仅供旧的题号/答案检查恢复编号，不用于输出文档。"""
    markdown=re.sub(r'<strong>(.*?)</strong>',r'**\1**',markdown,flags=re.S)
    markdown=markdown.replace('<br>','\n').replace('<p>','').replace('</p>','\n\n')
    return markdown
