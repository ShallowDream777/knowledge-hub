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

test('Knowledge Hub HTTP API + Optional Auth + Dual-Storage SQLite integration', async () => {
  await withTestServer(async baseUrl => {
    // 1. Guest mode works without login
    const meGuest = await (await fetch(`${baseUrl}/api/auth/me`)).json();
    assert.equal(meGuest.user, null);

    const kbsGuest = await (await fetch(`${baseUrl}/api/kbs`)).json();
    const engGuest = kbsGuest.find(k => k.id === 'english');
    assert.ok(engGuest);
    assert.equal(engGuest.lastRead, null);
    assert.equal(engGuest.stats.totalExercises, 31);

    // Guest wrongbook query via ?keys=01:A01
    const wbGuest = await (await fetch(`${baseUrl}/api/kbs/english/wrongbook?keys=01:A01`)).json();
    assert.equal(wbGuest.total, 1);
    assert.equal(wbGuest.items[0].id, 'A01');

    // 2. Register & Login user
    const regRes = await fetch(`${baseUrl}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: 'blue', password: 'secret123' })
    });
    assert.equal(regRes.status, 201);
    const { token, user } = await regRes.json();
    assert.equal(user.username, 'blue');
    assert.ok(token);

    const authHeaders = {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`
    };

    const meAuth = await (await fetch(`${baseUrl}/api/auth/me`, { headers: authHeaders })).json();
    assert.equal(meAuth.user.username, 'blue');

    // 3. Save reading state (last read chapter) to DB
    const docRes = await fetch(
      `${baseUrl}/api/kbs/english/doc?path=${encodeURIComponent('02·名词基础：分类、单复数与不可数')}`,
      { headers: authHeaders }
    );
    const doc = await docRes.json();

    const rsRes = await fetch(`${baseUrl}/api/kbs/english/reading-state`, {
      method: 'PUT',
      headers: authHeaders,
      body: JSON.stringify({ docPath: doc.path, docTitle: doc.title })
    });
    assert.equal(rsRes.status, 200);
    assert.equal((await rsRes.json()).savedToDb, true);

    // Verify /api/kbs returns lastRead from DB
    const kbsAuth = await (await fetch(`${baseUrl}/api/kbs`, { headers: authHeaders })).json();
    const engAuth = kbsAuth.find(k => k.id === 'english');
    assert.equal(engAuth.lastRead.docPath, doc.path);
    assert.equal(engAuth.lastRead.docTitle, doc.title);

    // 4. Save practice record to DB & test DB-priority sync-local
    await fetch(`${baseUrl}/api/kbs/english/practice`, {
      method: 'PUT',
      headers: authHeaders,
      body: JSON.stringify({
        chapterCode: '01',
        questionId: 'A01',
        userInput: 'DB answer',
        grade: 'ok'
      })
    });

    // Sync local cache: A01 already exists in DB ('ok') so local ('bad') must NOT overwrite DB;
    // A02 does not exist in DB so local ('bad') is backfilled into DB!
    await fetch(`${baseUrl}/api/kbs/english/sync-local`, {
      method: 'POST',
      headers: authHeaders,
      body: JSON.stringify({
        practice: {
          '01:A01': { userInput: 'local old answer', grade: 'bad' },
          '01:A02': { userInput: 'She are happy', grade: 'bad' }
        },
        lastRead: { docPath: 'other.md', docTitle: 'Other' }
      })
    });

    const ex01 = await (
      await fetch(`${baseUrl}/api/kbs/english/exercise/01`, { headers: authHeaders })
    ).json();
    const qA01 = ex01.questions.find(q => q.id === 'A01');
    const qA02 = ex01.questions.find(q => q.id === 'A02');
    assert.equal(qA01.grade, 'ok', 'DB record must take priority over local cache');
    assert.equal(qA01.userInput, 'DB answer');
    assert.equal(qA02.grade, 'bad', 'Missing DB record is backfilled from local cache');

    // Wrongbook has only A02
    const wbAuth = await (
      await fetch(`${baseUrl}/api/kbs/english/wrongbook`, { headers: authHeaders })
    ).json();
    assert.equal(wbAuth.total, 1);
    assert.equal(wbAuth.items[0].id, 'A02');
  });
});
