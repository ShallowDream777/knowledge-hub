const CALLOUT_META = {
  important: { icon: '📝', defaultTitle: '记笔记', cls: 'callout-important' },
  warning: { icon: '⚠️', defaultTitle: '易错避坑', cls: 'callout-warning' },
  caution: { icon: '⚠️', defaultTitle: '注意', cls: 'callout-warning' },
  tip: { icon: '💡', defaultTitle: '小贴士', cls: 'callout-tip' },
  note: { icon: '📌', defaultTitle: '说明', cls: 'callout-note' }
};

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

export function renderInline(raw) {
  if (!raw) return '';

  // 1. Protect inline code `...` with placeholders first
  const codeSlots = [];
  let text = String(raw).replace(/`([^`\n]+)`/g, (_m, code) => {
    const idx = codeSlots.length;
    codeSlots.push(`<code>${escapeHtml(code)}</code>`);
    return `\u0000CODE_${idx}\u0000`;
  });

  // Escape remaining HTML entities
  text = escapeHtml(text);

  // 2. Obsidian Wiki-links: [[target|label]] or [[target]]
  text = text.replace(/\[\[([^\]|#]+)?(?:#([^\]|]+))?(?:\|([^\]]+))?\]\]/g, (_m, docPart, anchorPart, labelPart) => {
    const doc = (docPart || '').trim();
    const anchor = (anchorPart || '').trim();
    const label = (labelPart || anchor || doc).trim();

    // Pure in-page anchor [[#heading|label]]
    if (!doc && anchor) {
      return `<a href="#" class="md-wiki-anchor" data-anchor="${anchor}">${label}</a>`;
    }

    // Check if target is an exercise file like 01·强化练习·...
    const exMatch = doc.match(/^(\d{2})·强化练习/);
    if (exMatch) {
      return `<a href="#" class="md-exercise-link" data-exercise-ch="${exMatch[1]}">✍️ ${label}</a>`;
    }

    return `<a href="#" class="md-wiki-link" data-wikilink="${doc}"${anchor ? ` data-anchor="${anchor}"` : ''}>${label}</a>`;
  });

  // 3. Standard Markdown links [label](url)
  text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_m, label, url) => {
    const cleanUrl = url.trim();
    const exEntry = cleanUrl.match(/第(\d{2})章\.html/) || cleanUrl.match(/#ch=(\d{2})/);
    if (exEntry) {
      return `<a href="#" class="md-exercise-btn" data-exercise-ch="${exEntry[1]}">✍️ ${label}</a>`;
    }
    if (cleanUrl.endsWith('交互刷题.html')) {
      return `<a href="#" class="md-exercise-btn" data-exercise-ch="01">✍️ ${label}</a>`;
    }
    return `<a href="${cleanUrl}" target="_blank" rel="noopener" class="md-ext-link">${label}</a>`;
  });

  // 4. Obsidian Highlight ==text==
  text = text.replace(/==([^=\n]+)==/g, '<mark class="md-highlight">$1</mark>');

  // 5. Bold **text**
  text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');

  // 6. Italic *text*
  text = text.replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g, '$1<em>$2</em>');

  // 7. Blank slots ___
  text = text.replace(/_{3,}/g, '<span class="blank-slot">_____</span>');

  // 8. Restore inline code slots
  text = text.replace(/\u0000CODE_(\d+)\u0000/g, (_m, idx) => codeSlots[Number(idx)]);

  return text;
}

function renderHeadingBadge(headingText) {
  // Turn trailing 【必学】 / 【识读即可】 / 【选做·综合复盘】 into styled pills
  return renderInline(headingText).replace(
    /【(必学|识读即可|选做[^】]*|同主题复盘)】/g,
    (_m, tag) => {
      const cls =
        tag === '必学' ? 'tag-must' : tag === '识读即可' ? 'tag-read' : 'tag-opt';
      return `<span class="md-tier-badge ${cls}">${tag}</span>`;
    }
  );
}

export function renderMarkdown(markdown) {
  if (!markdown) return '';
  const lines = String(markdown).replace(/\r\n/g, '\n').split('\n');
  const out = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];
    const trimmed = line.trim();

    // 1. Blank line
    if (!trimmed) {
      i++;
      continue;
    }

    // 2. Fenced code block ```
    if (trimmed.startsWith('```')) {
      const codeLines = [];
      i++;
      while (i < lines.length && !lines[i].trim().startsWith('```')) {
        codeLines.push(escapeHtml(lines[i]));
        i++;
      }
      if (i < lines.length) i++; // skip closing ```
      out.push(`<pre class="md-pre"><code>${codeLines.join('\n')}</code></pre>`);
      continue;
    }

    // 3. Native <details> block
    if (trimmed.startsWith('<details')) {
      const detailLines = [];
      while (i < lines.length) {
        const cur = lines[i];
        detailLines.push(cur);
        i++;
        if (cur.trim().includes('</details>')) break;
      }
      const rawBlock = detailLines.join('\n');
      const mSum = rawBlock.match(/<summary>([\s\S]*?)<\/summary>/);
      const summaryText = mSum ? renderInline(mSum[1].trim()) : '展开查看答案与解析';
      let inner = rawBlock
        .replace(/<details[^>]*>/, '')
        .replace(/<\/details>/, '')
        .replace(/<summary>[\s\S]*?<\/summary>/, '')
        .trim();

      // Format inner <p> lines or markdown lines inside details
      const innerHtml = inner
        .split('\n')
        .map(l => {
          const t = l.trim();
          if (!t) return '';
          if (t.startsWith('<p>') && t.endsWith('</p>')) {
            const content = t.slice(3, -4);
            // preserve <strong> tags while formatting inline code/highlights
            const parts = content.replace(/<strong>([\s\S]*?)<\/strong>/g, '**$1**');
            return `<p>${renderInline(parts)}</p>`;
          }
          return `<p>${renderInline(t)}</p>`;
        })
        .join('');
      out.push(
        `<details class="md-details"><summary>${summaryText}</summary><div class="md-details-body">${innerHtml}</div></details>`
      );
      continue;
    }

    // 4. Horizontal rule ---
    if (/^-{3,}$/.test(trimmed)) {
      out.push('<hr class="md-hr" />');
      i++;
      continue;
    }

    // 5. Headings # .. ######
    const mHeading = line.match(/^(#{1,6})\s+(.+)$/);
    if (mHeading) {
      const level = mHeading[1].length;
      const rawHeading = mHeading[2].trim();
      const escapedAttr = escapeHtml(rawHeading);
      out.push(
        `<h${level} class="md-h md-h${level}" data-heading="${escapedAttr}">${renderHeadingBadge(rawHeading)}</h${level}>`
      );
      i++;
      continue;
    }

    // 6. Blockquote OR Obsidian Callout (> [!important] 记笔记)
    if (trimmed.startsWith('>')) {
      const quoteLines = [];
      while (i < lines.length && lines[i].trim().startsWith('>')) {
        quoteLines.push(lines[i].trim().replace(/^>\s?/, ''));
        i++;
      }
      const firstLine = quoteLines[0] || '';
      const mCallout = firstLine.match(/^\[!([a-zA-Z]+)\]\s*(.*)$/);
      if (mCallout) {
        const typeKey = mCallout[1].toLowerCase();
        const meta = CALLOUT_META[typeKey] || CALLOUT_META.note;
        const customTitle = mCallout[2].trim() || meta.defaultTitle;
        const bodyMd = quoteLines.slice(1).join('\n');
        const bodyHtml = bodyMd ? renderMarkdown(bodyMd) : '';
        out.push(
          `<div class="callout ${meta.cls}">` +
            `<div class="callout-title"><span class="callout-icon">${meta.icon}</span><span>${renderInline(customTitle)}</span></div>` +
            `<div class="callout-body">${bodyHtml}</div>` +
          `</div>`
        );
      } else {
        const innerHtml = quoteLines.map(ql => `<p>${renderInline(ql)}</p>`).join('');
        out.push(`<blockquote class="md-quote">${innerHtml}</blockquote>`);
      }
      continue;
    }

    // 7. Markdown Table
    if (trimmed.startsWith('|') && i + 1 < lines.length && /^\|\s*[-:]+/.test(lines[i + 1].trim())) {
      const parseRow = rowLine =>
        rowLine
          .trim()
          .replace(/^\|/, '')
          .replace(/\|$/, '')
          .split('|')
          .map(c => renderInline(c.trim()));

      const headers = parseRow(lines[i]);
      i += 2; // skip header + separator
      const rows = [];
      while (i < lines.length && lines[i].trim().startsWith('|')) {
        rows.push(parseRow(lines[i]));
        i++;
      }
      const thead = `<thead><tr>${headers.map(h => `<th>${h}</th>`).join('')}</tr></thead>`;
      const tbody = `<tbody>${rows
        .map(r => `<tr>${r.map(c => `<td>${c}</td>`).join('')}</tr>`)
        .join('')}</tbody>`;
      out.push(`<div class="table-scroll"><table class="md-table">${thead}${tbody}</table></div>`);
      continue;
    }

    // 8. Unordered list (- or *)
    if (/^[-*]\s+/.test(trimmed)) {
      const items = [];
      while (i < lines.length && /^\s*[-*]\s+/.test(lines[i])) {
        const itemText = lines[i].replace(/^\s*[-*]\s+/, '').trim();
        // Task list checkbox - [ ] or - [x]
        const mTask = itemText.match(/^\[([ xX])\]\s+(.+)$/);
        if (mTask) {
          const checked = mTask[1].toLowerCase() === 'x';
          items.push(
            `<li class="md-task-item"><span class="task-box ${checked ? 'checked' : ''}">${checked ? '✓' : ''}</span><span>${renderInline(mTask[2])}</span></li>`
          );
        } else {
          items.push(`<li>${renderInline(itemText)}</li>`);
        }
        i++;
      }
      out.push(`<ul class="md-ul">${items.join('')}</ul>`);
      continue;
    }

    // 9. Ordered list (1. 2. ...)
    if (/^\d+\.\s+/.test(trimmed)) {
      const items = [];
      while (i < lines.length && /^\s*\d+\.\s+/.test(lines[i])) {
        const firstLine = lines[i].replace(/^\s*\d+\.\s+/, '').trim();
        const subLines = [renderInline(firstLine)];
        i++;
        // Continuation indented lines
        while (
          i < lines.length &&
          lines[i].trim() &&
          /^\s{2,}/.test(lines[i]) &&
          !/^\s*\d+\.\s+/.test(lines[i]) &&
          !/^\s*[-*]\s+/.test(lines[i])
        ) {
          subLines.push(renderInline(lines[i].trim()));
          i++;
        }
        items.push(`<li>${subLines.join('<br/>')}</li>`);
      }
      out.push(`<ol class="md-ol">${items.join('')}</ol>`);
      continue;
    }

    // 10. Regular paragraph (merge consecutive non-special lines)
    const paraLines = [];
    while (
      i < lines.length &&
      lines[i].trim() &&
      !lines[i].trim().startsWith('#') &&
      !lines[i].trim().startsWith('>') &&
      !lines[i].trim().startsWith('```') &&
      !lines[i].trim().startsWith('<details') &&
      !lines[i].trim().startsWith('|') &&
      !/^-{3,}$/.test(lines[i].trim()) &&
      !/^\s*[-*]\s+/.test(lines[i]) &&
      !/^\s*\d+\.\s+/.test(lines[i])
    ) {
      paraLines.push(renderInline(lines[i].trim()));
      i++;
    }
    if (paraLines.length > 0) {
      out.push(`<p class="md-p">${paraLines.join('<br/>')}</p>`);
    }
  }

  return out.join('\n');
}
