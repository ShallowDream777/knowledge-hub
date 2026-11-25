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

test('Knowledge Hub HTTP API + Flat Top-Level KBs + Optional Auth + Dual-Storage SQLite', async () => {
  await withTestServer(async baseUrl => {
    const kb1 = encodeURIComponent('1.大白话英语-无脑跟学');
    const kb2 = encodeURIComponent('2.同等学力申硕英语·考试强化');
    const kb3 = encodeURIComponent('3.英语语法知识字典');

    // 1. Portal lists each top-level folder under knowledge-base/ directly as a Knowledge Base
    const kbsGuest = await (await fetch(`${baseUrl}/api/kbs`)).json();
    assert.equal(kbsGuest.length, 3);
    assert.equal(kbsGuest[0].id, '1.大白话英语-无脑跟学');
    assert.equal(kbsGuest[0].stats.totalExercises, 31);
    assert.equal(kbsGuest[1].id, '2.同等学力申硕英语·考试强化');
    assert.equal(kbsGuest[1].stats.totalExercises, 16);
    assert.ok(kbsGuest[2].id.startsWith('3.英语语法知识字典'));
    assert.equal(kbsGuest[2].hasExercises, false);

    // 2. Dynamic stage parsing from 00·*.md (zero hardcoded stage names in parser)
    const tree1 = await (await fetch(`${baseUrl}/api/kbs/${kb1}/tree`)).json();
    const ex01Summary = tree1.exercises.find(e => e.code === '01');
    assert.equal(ex01Summary.stage, '第一阶段：先把词与句子认清');

    const tree2 = await (await fetch(`${baseUrl}/api/kbs/${kb2}/tree`)).json();
    const ex207Summary = tree2.exercises.find(e => e.code === '07');
    assert.equal(ex207Summary.stage, '阅读理解');

    // Verify KB2 reading passage + MCQ exercise parsing works generically
    const ex207 = await (await fetch(`${baseUrl}/api/kbs/${kb2}/exercise/07`)).json();
    assert.equal(ex207.questions.length, 16);
    assert.ok(ex207.questions[0].introHtml.includes('A city library'));
    assert.ok(ex207.questions[0].prompt.includes('q-options-block'));

    // 3. Register & Login user
    const regRes = await fetch(`${baseUrl}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: 'blue', password: 'secret123' })
    });
    assert.equal(regRes.status, 201);
    const { token, user } = await regRes.json();
    assert.equal(user.username, 'blue');

    const authHeaders = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    };

    // 4. Save reading state (last read chapter) to DB for KB1
    const docRes = await fetch(
      `${baseUrl}/api/kbs/${kb1}/doc?path=${encodeURIComponent('02·名词基础：分类、单复数与不可数')}`,
      { headers: authHeaders }
    );
    const doc = await docRes.json();

    const rsRes = await fetch(`${baseUrl}/api/kbs/${kb1}/reading-state`, {
      method: 'PUT',
      headers: authHeaders,
      body: JSON.stringify({
        docPath: doc.path,
        docTitle: doc.title,
        scrollY: 1280,
        scrollRatio: 0.42,
        heading: '二、可数与不可数'
      })
    });
    assert.equal(rsRes.status, 200);
    assert.equal((await rsRes.json()).savedToDb, true);

    const kbsAuth = await (await fetch(`${baseUrl}/api/kbs`, { headers: authHeaders })).json();
    const kb1Auth = kbsAuth.find(k => k.id === '1.大白话英语-无脑跟学');
    assert.equal(kb1Auth.lastRead.docPath, doc.path);
    assert.equal(kb1Auth.lastRead.docTitle, doc.title);
    assert.equal(kb1Auth.lastRead.scrollY, 1280);
    assert.equal(kb1Auth.lastRead.scrollRatio, 0.42);
    assert.equal(kb1Auth.lastRead.heading, '二、可数与不可数');

    // 5. Save practice record to DB & test DB-priority sync-local
    await fetch(`${baseUrl}/api/kbs/${kb1}/practice`, {
      method: 'PUT',
      headers: authHeaders,
      body: JSON.stringify({
        chapterCode: '01',
        questionId: 'A01',
        userInput: 'DB answer',
        grade: 'ok'
      })
    });

    await fetch(`${baseUrl}/api/kbs/${kb1}/sync-local`, {
      method: 'POST',
      headers: authHeaders,
      body: JSON.stringify({
        practice: {
          '01:A01': { userInput: 'local old answer', grade: 'bad' },
          '01:A02': { userInput: 'She are happy', grade: 'bad' }
        }
      })
    });

    const ex01 = await (
      await fetch(`${baseUrl}/api/kbs/${kb1}/exercise/01`, { headers: authHeaders })
    ).json();
    const qA01 = ex01.questions.find(q => q.id === 'A01');
    const qA02 = ex01.questions.find(q => q.id === 'A02');
    assert.equal(qA01.grade, 'ok', 'DB record must take priority over local cache');
    assert.equal(qA02.grade, 'bad', 'Missing DB record is backfilled from local cache');
  });
});
