import { describe, it, expect } from 'vitest';
import { renderMarkdown } from './markdown.js';

describe('Obsidian Markdown Rendering Engine', () => {
  it('renders ==highlight== as <mark class="md-highlight">', () => {
    const html = renderMarkdown('记住：==单数可数名词不能裸奔==。');
    expect(html).toContain('<mark class="md-highlight">单数可数名词不能裸奔</mark>');
  });

  it('renders Obsidian Callout boxes (> [!important] 记笔记, [!warning], [!tip], [!note])', () => {
    const md = [
      '> [!important] 记笔记',
      '> - 第一条核心结论',
      '> - 第二条结论含 ==高亮==',
      '',
      '> [!warning] 易错避坑',
      '> - ✅ `I have a dog.`'
    ].join('\n');
    const html = renderMarkdown(md);
    expect(html).toContain('callout callout-important');
    expect(html).toContain('记笔记');
    expect(html).toContain('<mark class="md-highlight">高亮</mark>');
    expect(html).toContain('callout callout-warning');
    expect(html).toContain('<code>I have a dog.</code>');
  });

  it('renders Obsidian wiki-links, in-page anchors, and exercise jump links', () => {
    const md = [
      '- [[#什么是名词　【必学】|什么是名词]]',
      '- [[02·名词基础：分类、单复数与不可数|下一章]]',
      '- [[02·强化练习·名词基础：分类、单复数与不可数|第02章专用强化题与验收 →]]'
    ].join('\n');
    const html = renderMarkdown(md);
    expect(html).toContain('class="md-wiki-anchor" data-anchor="什么是名词　【必学】"');
    expect(html).toContain('class="md-wiki-link" data-wikilink="02·名词基础：分类、单复数与不可数"');
    expect(html).toContain('class="md-exercise-link" data-exercise-ch="02"');
  });

  it('renders headings with exact data-heading and tier badges', () => {
    const html = renderMarkdown('### 什么是名词　【必学】');
    expect(html).toContain('data-heading="什么是名词　【必学】"');
    expect(html).toContain('class="md-tier-badge tag-must">必学</span>');
  });
});
