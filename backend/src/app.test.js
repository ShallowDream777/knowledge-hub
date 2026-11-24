import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createApp } from './app.js';

async function withTestServer(fn) {
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'kb-hub-test-'));
  const dbPath = path.join(tmpDir, 'test.db');
  const { app, db } = createApp({ dbPath });
  const server = app.listen(0);
  const port = server.address().port;
  const baseUrl = `http://127.0.0.1:${port}`;
  try {
    await fn(baseUrl);
  } finally {
    await new Promise(resolve => server.close(resolve));
    db.close();
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
}

test('Knowledge Hub HTTP API + SQLite + Real Markdown KB integration', async () => {
  await withTestServer(async baseUrl => {
    // 1. Health check
    const healthRes = await fetch(`${baseUrl}/api/health`);
    assert.equal(healthRes.status, 200);
    assert.deepEqual(await healthRes.json(), { status: 'ok' });

    // 2. Portal list (/api/kbs)
    const kbsRes = await fetch(`${baseUrl}/api/kbs`);
    assert.equal(kbsRes.status, 200);
    const kbs = await kbsRes.json();
    assert.ok(kbs.length >= 1);
    const eng = kbs.find(k => k.id === 'english');
    assert.ok(eng, 'english KB should exist');
    assert.equal(eng.stats.totalExercises, 31);
    assert.ok(eng.stats.totalDocs >= 32);

    // 3. Tree & exercise summaries (/api/kbs/english/tree)
    const treeRes = await fetch(`${baseUrl}/api/kbs/english/tree`);
    assert.equal(treeRes.status, 200);
    const tree = await treeRes.json();
    assert.equal(tree.exercises.length, 31);
    const totalQs = tree.exercises.reduce((acc, c) => acc + c.totalQuestions, 0);
    assert.equal(totalQs, 1278);

    // 4. Read real Markdown doc by wiki-link stem
    const docRes = await fetch(
      `${baseUrl}/api/kbs/english/doc?path=${encodeURIComponent('02·名词基础：分类、单复数与不可数')}`
    );
    assert.equal(docRes.status, 200);
    const doc = await docRes.json();
    assert.ok(doc.content.includes('# 第 02 章'));
    assert.ok(doc.content.includes('## 本章核心记忆笔记'));
    assert.equal(doc.exerciseCode, '02');
    assert.equal(doc.completed, false);

    // 5. Persist chapter completion to SQLite
    const progRes = await fetch(`${baseUrl}/api/kbs/english/chapter-progress`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ docPath: doc.path, completed: true })
    });
    assert.equal(progRes.status, 200);
    const docAfter = await (
      await fetch(`${baseUrl}/api/kbs/english/doc?path=${encodeURIComponent(doc.path)}`)
    ).json();
    assert.equal(docAfter.completed, true);

    // 6. Parse Exercise Chapter 01 & persist practice records in SQLite
    const ex01 = await (await fetch(`${baseUrl}/api/kbs/english/exercise/01`)).json();
    assert.equal(ex01.code, '01');
    assert.equal(ex01.questions.length, 40);
    assert.ok(ex01.questions.every(q => q.answer && !q.answer.includes('暂无解析')));

    // Save one bad answer and one ok answer
    await fetch(`${baseUrl}/api/kbs/english/practice`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chapterCode: '01',
        questionId: 'A01',
        userInput: 'i am happy',
        grade: 'bad'
      })
    });
    await fetch(`${baseUrl}/api/kbs/english/practice`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chapterCode: '01',
        questionId: 'C01',
        userInput: 'I am, she is, they are',
        grade: 'ok'
      })
    });

    // Verify wrongbook contains A01
    const wb1 = await (await fetch(`${baseUrl}/api/kbs/english/wrongbook`)).json();
    assert.equal(wb1.total, 1);
    assert.equal(wb1.items[0].id, 'A01');
    assert.equal(wb1.items[0].userInput, 'i am happy');
    assert.equal(wb1.items[0].grade, 'bad');

    // Upgrade A01 to 'ok' -> wrongbook becomes empty
    await fetch(`${baseUrl}/api/kbs/english/practice`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chapterCode: '01',
        questionId: 'A01',
        grade: 'ok'
      })
    });
    const wb2 = await (await fetch(`${baseUrl}/api/kbs/english/wrongbook`)).json();
    assert.equal(wb2.total, 0);

    // Reset Chapter 01 practice records
    const delRes = await fetch(`${baseUrl}/api/kbs/english/practice/01`, { method: 'DELETE' });
    assert.equal(delRes.status, 200);
    const ex01After = await (await fetch(`${baseUrl}/api/kbs/english/exercise/01`)).json();
    assert.ok(ex01After.questions.every(q => q.grade === '' && q.userInput === ''));
  });
});
