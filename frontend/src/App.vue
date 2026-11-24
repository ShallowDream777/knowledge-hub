<template>
  <div class="kh-root">
    <!-- ==================== 登录 / 注册弹窗（非强制） ==================== -->
    <div v-if="showAuthModal" class="modal-backdrop" @click.self="showAuthModal = false">
      <div class="auth-modal">
        <div class="auth-modal-header">
          <h3>{{ authMode === 'login' ? '🔑 登录账号' : '✨ 注册新账号' }}</h3>
          <button class="ghost-btn" @click="showAuthModal = false">✕</button>
        </div>
        <p class="auth-modal-desc">
          登录后，你的<strong>刷题记录</strong>与<strong>上次阅读章节</strong>将持久化到服务器数据库（多端同步，优先读取数据库），同时本地浏览器缓存也会同步保存一份。不登录也可直接使用本地缓存学习。
        </p>

        <div class="auth-tabs">
          <button
            class="auth-tab"
            :class="{ active: authMode === 'login' }"
            @click="authMode = 'login'; authError = ''"
          >
            已有账号登录
          </button>
          <button
            class="auth-tab"
            :class="{ active: authMode === 'register' }"
            @click="authMode = 'register'; authError = ''"
          >
            注册新账号
          </button>
        </div>

        <form class="auth-form" @submit.prevent="submitAuth">
          <label class="auth-label">
            <span>用户名</span>
            <input
              v-model="authUsername"
              class="q-input"
              type="text"
              placeholder="请输入用户名（至少 2 个字符）"
              required
            />
          </label>
          <label class="auth-label">
            <span>密码</span>
            <input
              v-model="authPassword"
              class="q-input"
              type="password"
              placeholder="请输入密码（至少 4 个字符）"
              required
            />
          </label>

          <div v-if="authError" class="auth-error">{{ authError }}</div>

          <div class="auth-actions">
            <button type="button" class="ghost-btn" @click="showAuthModal = false">暂不登录</button>
            <button type="submit" class="primary-btn" :disabled="authSubmitting">
              {{ authSubmitting ? '处理中…' : (authMode === 'login' ? '立即登录' : '注册并登录') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- ==================== 1. 多知识库主入口门户 ==================== -->
    <div v-if="currentView === 'portal'" class="portal-page">
      <header class="portal-header">
        <div class="portal-brand">
          <span class="portal-logo">🏛️</span>
          <div>
            <h1>Knowledge Hub · 个人知识库中心</h1>
            <p>底层 Markdown 实时渲染驱动 · 数据库与浏览器缓存双持久化</p>
          </div>
        </div>

        <div class="header-right-tools">
          <template v-if="currentUser">
            <span class="user-badge logged-in" title="已开启数据库优先 + 本地缓存双存">
              🟢 {{ currentUser.username }}（云端同步）
            </span>
            <button class="ghost-btn" @click="handleLogout">退出登录</button>
          </template>
          <template v-else>
            <span class="user-badge guest" title="当前未登录，进度保存在当前浏览器缓存">
              ⚪ 未登录（本地缓存）
            </span>
            <button class="secondary-btn" @click="openAuthModal('login')">🔑 登录 / 注册</button>
          </template>

          <button class="ghost-btn" @click="toggleTheme" title="切换深浅色护眼模式">
            {{ theme === 'dark' ? '☀️ 浅色' : '🌙 深色' }}
          </button>
        </div>
      </header>

      <main class="portal-main">
        <div class="section-heading">
          <h2>选择一个知识库进入</h2>
          <span class="section-sub">
            {{ currentUser ? '已登录：优先读取数据库记录并同步写入浏览器缓存' : '未登录：读取当前浏览器缓存，登录后可跨设备同步' }}
          </span>
        </div>

        <div v-if="loadingPortal" class="empty-state">正在加载知识库列表…</div>

        <div v-else class="kb-grid">
          <article
            v-for="kb in decoratedKbs"
            :key="kb.id"
            class="kb-card"
            @click="enterKbReading(kb)"
          >
            <div class="kb-card-top">
              <span class="kb-icon">{{ kb.icon }}</span>
              <span class="kb-badge">{{ kb.badge }}</span>
            </div>
            <h3 class="kb-title">{{ kb.title }}</h3>
            <p class="kb-sub">{{ kb.subtitle }}</p>

            <div class="kb-modules-list">
              <span v-for="m in kb.modules" :key="m" class="kb-mod-chip">{{ m }}</span>
            </div>

            <div class="kb-stats-grid">
              <div class="kb-stat-box kb-stat-box-wide">
                <span class="kb-stat-label">上次阅读章节</span>
                <span
                  class="kb-stat-chapter"
                  :class="{ 'not-started': !kb.effectiveLastRead }"
                  :title="kb.effectiveLastRead?.docTitle || '尚未开始阅读'"
                >
                  {{ kb.effectiveLastRead?.docTitle || '尚未开始' }}
                </span>
              </div>
              <div class="kb-stat-box">
                <span class="kb-stat-num">{{ kb.effectiveStats.masteredQuestions }}</span>
                <span class="kb-stat-label">已掌握题目</span>
              </div>
              <div class="kb-stat-box">
                <span
                  class="kb-stat-num"
                  :class="{ 'text-warn': kb.effectiveStats.wrongQuestions > 0 }"
                >
                  {{ kb.effectiveStats.wrongQuestions }}
                </span>
                <span class="kb-stat-label">错题/不稳</span>
              </div>
            </div>

            <div class="kb-actions" @click.stop>
              <button class="primary-btn" @click="enterKbReading(kb)">
                {{ kb.effectiveLastRead ? '📖 继续上次阅读' : '📖 进入阅读学习' }}
              </button>
              <button class="secondary-btn" @click="enterKb(kb.id, 'exercise')">
                ✍️ 交互刷题中心
              </button>
              <button
                v-if="kb.effectiveStats.wrongQuestions > 0"
                class="warn-btn"
                @click="enterKb(kb.id, 'wrongbook')"
              >
                📕 错题本 ({{ kb.effectiveStats.wrongQuestions }})
              </button>
            </div>
          </article>

          <!-- 扩展提示卡片 -->
          <article class="kb-card kb-card-placeholder">
            <div class="kb-card-top">
              <span class="kb-icon">➕</span>
              <span class="kb-badge">可扩展</span>
            </div>
            <h3 class="kb-title">新增其他学科知识库</h3>
            <p class="kb-sub">
              后续只需在项目 <code>knowledge-base/</code> 目录下放入新的 Markdown 知识库文件夹，系统将自动识别并在此处生成新的知识库入口。
            </p>
          </article>
        </div>
      </main>
    </div>

    <!-- ==================== 2. 知识库阅读与交互刷题工作台 ==================== -->
    <div v-else class="workspace-page">
      <!-- 移动端顶栏 -->
      <div class="mobile-bar">
        <button class="ghost-btn" @click="sidebarOpen = !sidebarOpen">☰ 目录</button>
        <strong class="mobile-title">{{ treeData?.kb?.title || '知识库' }}</strong>
        <div style="display:flex;gap:5px;align-items:center;">
          <button
            v-if="!currentUser"
            class="ghost-btn"
            @click="openAuthModal('login')"
          >
            登录
          </button>
          <span v-else class="mobile-user-dot" :title="currentUser.username">🟢</span>
          <button class="ghost-btn" @click="goPortal">门户</button>
          <button class="ghost-btn" @click="toggleTheme">🌓</button>
        </div>
      </div>

      <div class="app-layout">
        <!-- 移动端遮罩 -->
        <div v-if="sidebarOpen" class="sidebar-backdrop" @click="sidebarOpen = false"></div>

        <!-- 左侧导航栏 -->
        <aside class="sidebar" :class="{ open: sidebarOpen }">
          <div class="sidebar-header">
            <div class="brand-row">
              <button class="back-portal-btn" @click="goPortal" title="返回多知识库门户">
                ← 门户
              </button>
              <span class="brand-title">{{ treeData?.kb?.icon }} {{ treeData?.kb?.title }}</span>
              <button class="ghost-btn" @click="toggleTheme" title="切换深浅色">🌓</button>
            </div>

            <!-- 登录状态栏（侧边栏顶部） -->
            <div class="sidebar-auth-bar">
              <template v-if="currentUser">
                <span class="sidebar-auth-text">🟢 <strong>{{ currentUser.username }}</strong> · 数据库同步中</span>
                <button class="tiny-link-btn" @click="handleLogout">退出</button>
              </template>
              <template v-else>
                <span class="sidebar-auth-text">⚪ 本地缓存模式</span>
                <button class="tiny-link-btn" @click="openAuthModal('login')">登录同步云端</button>
              </template>
            </div>

            <!-- 继续上次阅读快捷条（当存在上次阅读记录且当前未处在该章时显示） -->
            <div
              v-if="activeLastRead && currentDoc?.path !== activeLastRead.docPath"
              class="continue-banner"
              @click="openDocument(activeLastRead.docPath)"
            >
              <span class="continue-label">📖 继续上次阅读：</span>
              <span class="continue-title">{{ activeLastRead.docTitle }} →</span>
            </div>

            <!-- 三大模式切换：章节阅读 / 交互刷题 / 错题本 -->
            <div class="nav-mode-tabs">
              <button
                class="mode-tab"
                :class="{ active: workMode === 'read' }"
                @click="switchWorkMode('read')"
              >
                📖 章节阅读
              </button>
              <button
                class="mode-tab"
                :class="{ active: workMode === 'exercise' }"
                @click="switchWorkMode('exercise')"
              >
                ✍️ 交互刷题
              </button>
              <button
                class="mode-tab"
                :class="{ active: workMode === 'wrongbook', 'has-wrong': effectiveWrongTotal > 0 }"
                @click="switchWorkMode('wrongbook')"
              >
                📕 错题 ({{ effectiveWrongTotal }})
              </button>
            </div>

            <!-- 模块切换（在章节阅读或交互刷题模式下，有多个模块时显示） -->
            <div v-if="(workMode === 'read' || workMode === 'exercise') && treeData?.modules?.length > 1" class="mod-select-row">
              <select v-model="selectedModuleIdx" class="mod-select" @change="handleModuleChange">
                <option
                  v-for="(mod, idx) in treeData.modules"
                  :key="mod.name"
                  :value="idx"
                  :disabled="workMode === 'exercise' && !mod.hasExercises"
                >
                  {{ mod.name }}{{ workMode === 'exercise' && !mod.hasExercises ? '（无题库）' : '' }}
                </option>
              </select>
            </div>

            <input
              v-model="searchKw"
              class="search-input"
              type="text"
              :placeholder="workMode === 'read' ? '搜索文档或章节名…' : '搜索刷题章节号或标题…'"
            />
          </div>

          <!-- A. 阅读目录列表 -->
          <div v-if="workMode === 'read'" class="chapter-list">
            <template v-if="currentModule">
              <div v-if="filteredRootDocs.length" class="stage-label">导学与总览</div>
              <div
                v-for="doc in filteredRootDocs"
                :key="doc.path"
                class="ch-item"
                :class="{ active: currentDoc?.path === doc.path }"
                @click="openDocument(doc.path)"
              >
                <div class="ch-item-top">
                  <span class="ch-name" :title="doc.title">{{ doc.title }}</span>
                  <span
                    v-if="activeLastRead?.docPath === doc.path"
                    class="last-read-pill"
                    title="上次阅读位置"
                  >
                    上次
                  </span>
                  <span v-if="isDocCompleted(doc.path)" class="done-check" title="已学完">✓</span>
                </div>
              </div>

              <template v-for="grp in filteredDocGroups" :key="grp.path">
                <div class="stage-label">{{ grp.name }} ({{ grp.docs.length }})</div>
                <div
                  v-for="doc in grp.docs"
                  :key="doc.path"
                  class="ch-item"
                  :class="{ active: currentDoc?.path === doc.path }"
                  @click="openDocument(doc.path)"
                >
                  <div class="ch-item-top">
                    <span v-if="doc.code" class="ch-code">{{ doc.code }}</span>
                    <span class="ch-name" :title="doc.title">{{ doc.title.replace(/^\d{2}\s*·\s*/, '') }}</span>
                    <span
                      v-if="activeLastRead?.docPath === doc.path"
                      class="last-read-pill"
                      title="上次阅读位置"
                    >
                      上次
                    </span>
                    <span v-if="isDocCompleted(doc.path)" class="done-check" title="已学完">✓</span>
                  </div>
                </div>
              </template>
            </template>
          </div>

          <!-- B. 交互刷题 31 章列表 -->
          <div v-else class="chapter-list">
            <template v-for="grp in groupedExercises" :key="grp.stage">
              <div class="stage-label">{{ grp.stage }}</div>
              <div
                v-for="ex in grp.items"
                :key="ex.code"
                class="ch-item"
                :class="{ active: workMode === 'exercise' && currentExCode === ex.code }"
                @click="openExercise(ex.code)"
              >
                <div class="ch-item-top">
                  <span class="ch-code">{{ ex.rawCode || ex.code }}</span>
                  <span class="ch-name" :title="ex.title">{{ ex.title }}</span>
                  <span class="ch-stat">{{ ex.okRequiredCount }}/{{ ex.requiredCount }}</span>
                </div>
                <div class="mini-bar">
                  <div
                    class="mini-bar-fill"
                    :style="{ width: (ex.requiredCount ? Math.round((ex.okRequiredCount / ex.requiredCount) * 100) : 0) + '%' }"
                  ></div>
                </div>
              </div>
            </template>
          </div>
        </aside>

        <!-- 右侧主内容区 -->
        <main class="main">
          <!-- ==================== 视图 A：Markdown 实时渲染阅读器 ==================== -->
          <template v-if="workMode === 'read'">
            <div v-if="loadingDoc" class="empty-state">正在读取并渲染 Markdown 文档…</div>
            <template v-else-if="currentDoc">
              <section class="header-card doc-toolbar-card">
                <div class="header-top">
                  <div>
                    <div class="doc-path-crumb">
                      {{ currentDoc.path }} · 已自动记录为“上次阅读章节”
                    </div>
                    <h1 class="ch-title">{{ currentDoc.title }}</h1>
                  </div>
                  <div class="doc-toolbar-actions">
                    <button
                      class="check-complete-btn"
                      :class="{ completed: isDocCompleted(currentDoc.path) }"
                      @click="toggleDocCompleted"
                    >
                      {{ isDocCompleted(currentDoc.path) ? '✅ 已标记学完（点击取消）' : '○ 标记本章已学完' }}
                    </button>
                    <button
                      v-if="currentDoc.exerciseCode"
                      class="primary-btn"
                      @click="openExercise(currentDoc.exerciseCode)"
                    >
                      ✍️ 进入第 {{ currentDoc.exerciseCode }} 章交互刷题 →
                    </button>
                  </div>
                </div>
              </section>

              <!-- 实时 Markdown 渲染容器 -->
              <article
                class="md-article"
                v-html="renderedDocHtml"
                @click="handleMarkdownClick"
              ></article>

              <!-- 底部翻章与跳刷题栏 -->
              <div class="bottom-nav">
                <button
                  class="nav-btn"
                  :disabled="!currentDoc.prevDoc"
                  @click="currentDoc.prevDoc && openDocument(currentDoc.prevDoc.path)"
                >
                  ← 上一篇：{{ currentDoc.prevDoc?.title || '无' }}
                </button>
                <button
                  v-if="currentDoc.exerciseCode"
                  class="primary-btn"
                  @click="openExercise(currentDoc.exerciseCode)"
                >
                  ✍️ 做本章强化与验收题
                </button>
                <button
                  class="nav-btn"
                  :disabled="!currentDoc.nextDoc"
                  @click="currentDoc.nextDoc && openDocument(currentDoc.nextDoc.path)"
                >
                  下一篇：{{ currentDoc.nextDoc?.title || '无' }} →
                </button>
              </div>
            </template>
          </template>

          <!-- ==================== 视图 B：单章交互刷题中心（DB + 本地缓存双持久化） ==================== -->
          <template v-else-if="workMode === 'exercise'">
            <div v-if="loadingEx" class="empty-state">正在从 Markdown 解析题目并同步进度…</div>
            <template v-else-if="currentEx">
              <section class="header-card">
                <div class="header-top">
                  <div>
                    <div class="doc-path-crumb">{{ currentEx.moduleName }} · {{ currentEx.stage }}</div>
                    <h1 class="ch-title">第 {{ currentEx.rawCode || currentEx.code }} 章　{{ currentEx.title }}</h1>
                    <p class="ch-scope">{{ currentEx.scope || '按首轮必做题完成练习与独立验收即可进入下一章。' }}</p>
                  </div>
                  <button class="ghost-btn" @click="jumpToChapterDoc(currentEx.code)">
                    📖 返回阅读第 {{ currentEx.rawCode || currentEx.code }} 章正文
                  </button>
                </div>

                <div class="summary-pills">
                  <span class="stat-pill">
                    首轮必做：{{ exStats.okReq }} / {{ exStats.totalReq }} 会了（已自评 {{ exStats.doneReq }}）
                  </span>
                  <span
                    v-if="currentEx.cPass > 0"
                    class="stat-pill"
                    :class="exStats.cPassed ? 'pass' : (exStats.cGraded > 0 ? 'warn' : '')"
                  >
                    C组独立验收：{{ exStats.cScore }} / {{ exStats.cMax }} 分（建议 ≥ {{ currentEx.cPass }} 分{{ exStats.cPassed ? ' · 已达标 🎉' : '' }}）
                  </span>
                  <span class="stat-pill">本章错题/不稳：{{ exStats.reviewCount }} 题</span>
                </div>

                <details v-if="currentEx.coverage?.length" class="drawer">
                  <summary>📋 展开本章练习范围与易错点（{{ currentEx.coverage.length }} 个核心情境）</summary>
                  <div class="table-scroll">
                    <table class="cov-table">
                      <thead>
                        <tr><th>核心情境</th><th>主要检查</th><th>关联题号</th></tr>
                      </thead>
                      <tbody>
                        <tr v-for="(r, idx) in currentEx.coverage" :key="idx">
                          <td>{{ r.scene }}</td>
                          <td>{{ r.point }}</td>
                          <td>{{ r.ids }}</td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </details>
              </section>

              <section class="controls">
                <div class="ctrl-row">
                  <div class="pill-group">
                    <button
                      class="pill"
                      :class="{ active: filterMode === 'required' }"
                      @click="filterMode = 'required'"
                    >
                      ⭐ 首轮必做
                    </button>
                    <button
                      class="pill"
                      :class="{ active: filterMode === 'all' }"
                      @click="filterMode = 'all'"
                    >
                      全部题目
                    </button>
                    <button
                      class="pill"
                      :class="{ active: filterMode === 'todo' }"
                      @click="filterMode = 'todo'"
                    >
                      未自评
                    </button>
                    <button
                      class="pill"
                      :class="{ active: filterMode === 'review' }"
                      @click="filterMode = 'review'"
                    >
                      错题/不稳 ({{ exStats.reviewCount }})
                    </button>
                  </div>
                  <div class="pill-group">
                    <button class="ghost-btn" @click="expandAllVisible(filteredQuestions, currentEx.code)">
                      全部展开答案
                    </button>
                    <button class="ghost-btn" @click="collapseAllVisible(filteredQuestions, currentEx.code)">
                      全部隐藏答案
                    </button>
                    <button class="ghost-btn" @click="resetCurrentChapter">重置本章</button>
                  </div>
                </div>

                <div class="ctrl-row">
                  <div class="pill-group">
                    <button
                      class="pill"
                      :class="{ active: groupTab === 'ALL' }"
                      @click="groupTab = 'ALL'"
                    >
                      全部组 ({{ currentEx.questions.length }})
                    </button>
                    <button
                      v-for="g in currentEx.groups"
                      :key="g.key"
                      class="pill"
                      :class="{ active: groupTab === g.key }"
                      @click="groupTab = g.key"
                    >
                      {{ g.label }} ({{ g.count }})
                    </button>
                  </div>
                </div>
              </section>

              <div v-if="!filteredQuestions.length" class="empty-state">
                当前筛选条件下没有题目 🎉<br />
                <span style="font-size:13px;">可以切换“全部题目”或“全部组”查看其他题目。</span>
              </div>

              <div v-else class="q-list">
                <template v-for="q in filteredQuestions" :key="q.id">
                  <div v-if="q.introHtml" class="section-passage-box">
                    <div class="passage-title">📄 {{ q.groupLabel }} · 阅读材料 / 说明</div>
                    <div class="passage-body" v-html="q.introHtml"></div>
                  </div>
                  <article
                    class="q-card"
                    :class="q.grade ? 'st-' + q.grade : ''"
                  >
                  <div class="q-meta">
                    <span class="q-id">{{ q.id }}</span>
                    <span
                      class="q-tag"
                      :class="q.tag === '选做' ? 'opt' : (q.tag === '识读必做' ? 'read' : 'req')"
                    >
                      {{ q.tag }}
                    </span>
                    <span class="q-topic">{{ q.topic }}</span>
                  </div>

                  <div class="q-prompt" v-html="q.prompt"></div>

                  <div class="q-input-row">
                    <input
                      v-model="q.userInput"
                      class="q-input"
                      type="text"
                      placeholder="在此输入你的答案（自动存入缓存与数据库；按回车直接查看解析）…"
                      @change="savePracticeRecord(currentEx.code, q)"
                      @keydown.enter="toggleAnswer(currentEx.code, q.id)"
                    />
                  </div>

                  <div class="q-actions">
                    <button
                      class="ans-toggle"
                      :class="{ open: isAnswerOpen(currentEx.code, q.id) }"
                      @click="toggleAnswer(currentEx.code, q.id)"
                    >
                      {{ isAnswerOpen(currentEx.code, q.id) ? '🙈 隐藏答案' : '👁 显示答案' }}
                    </button>

                    <div class="grade-group">
                      <button
                        class="grade-btn"
                        :class="{ 'active-ok': q.grade === 'ok' }"
                        @click="setQuestionGrade(currentEx.code, q, 'ok')"
                      >
                        ✅ 会了
                      </button>
                      <button
                        class="grade-btn"
                        :class="{ 'active-warn': q.grade === 'warn' }"
                        @click="setQuestionGrade(currentEx.code, q, 'warn')"
                      >
                        ⚠️ 不稳
                      </button>
                      <button
                        class="grade-btn"
                        :class="{ 'active-bad': q.grade === 'bad' }"
                        @click="setQuestionGrade(currentEx.code, q, 'bad')"
                      >
                        ❌ 错了
                      </button>
                    </div>
                  </div>

                  <div v-if="isAnswerOpen(currentEx.code, q.id)" class="ans-box show">
                    <div class="ans-label">参考答案与解析</div>
                    <div class="ans-body" v-html="q.answer"></div>
                  </div>
                </article>
                </template>
              </div>

              <div class="bottom-nav">
                <button
                  class="nav-btn"
                  :disabled="!prevExerciseCode"
                  @click="prevExerciseCode && openExercise(prevExerciseCode)"
                >
                  ← 上一章刷题
                </button>
                <button class="ghost-btn" @click="jumpToChapterDoc(currentEx.code)">
                  📖 阅读第 {{ currentEx.rawCode || currentEx.code }} 章正文
                </button>
                <button
                  class="nav-btn"
                  :disabled="!nextExerciseCode"
                  @click="nextExerciseCode && openExercise(nextExerciseCode)"
                >
                  下一章刷题 →
                </button>
              </div>
            </template>
          </template>

          <!-- ==================== 视图 C：全局错题与不稳题本 ==================== -->
          <template v-else-if="workMode === 'wrongbook'">
            <section class="header-card">
              <h1 class="ch-title">📕 全局错题与不稳题本</h1>
              <p class="ch-scope">
                集中复盘你在全书 31 章中标记为“❌ 错了”或“⚠️ 不稳”的题目（{{ currentUser ? '已登录：从数据库加载并同步缓存' : '未登录：从当前浏览器缓存加载' }}）；重新做稳并点“✅ 会了”后会自动移出。
              </p>
              <div class="summary-pills">
                <span class="stat-pill warn">待修复题目：{{ wrongbookItems.length }} 题</span>
              </div>
            </section>

            <section class="controls">
              <div class="ctrl-row">
                <span style="font-size:13px;color:var(--text-muted);">
                  提示：每题独立点击“显示答案”核对，做稳后点“✅ 会了”。
                </span>
                <div class="pill-group">
                  <button class="ghost-btn" @click="expandAllWrongbook">全部展开答案</button>
                  <button class="ghost-btn" @click="openAnswers.clear()">全部隐藏答案</button>
                </div>
              </div>
            </section>

            <div v-if="!wrongbookItems.length" class="empty-state">
              目前没有错题或不稳项，继续保持！ 🎉
            </div>

            <div v-else class="q-list">
              <article
                v-for="item in wrongbookItems"
                :key="item.chapterCode + ':' + item.id"
                class="q-card"
                :class="item.grade ? 'st-' + item.grade : ''"
              >
                <div class="q-meta">
                  <span class="q-id">{{ item.id }}</span>
                  <span
                    class="q-tag"
                    :class="item.tag === '选做' ? 'opt' : (item.tag === '识读必做' ? 'read' : 'req')"
                  >
                    {{ item.tag }}
                  </span>
                  <span class="q-topic">{{ item.topic }}</span>
                  <span
                    class="q-chapter-badge"
                    style="cursor:pointer"
                    @click="openExercise(item.chapterCode)"
                  >
                    第{{ item.chapterCode }}章 · {{ item.chapterTitle }} →
                  </span>
                </div>

                <div class="q-prompt" v-html="item.prompt"></div>

                <div class="q-input-row">
                  <input
                    v-model="item.userInput"
                    class="q-input"
                    type="text"
                    placeholder="重新输入你的答案（按回车查看解析）…"
                    @change="savePracticeRecord(item.chapterCode, item)"
                    @keydown.enter="toggleAnswer(item.chapterCode, item.id)"
                  />
                </div>

                <div class="q-actions">
                  <button
                    class="ans-toggle"
                    :class="{ open: isAnswerOpen(item.chapterCode, item.id) }"
                    @click="toggleAnswer(item.chapterCode, item.id)"
                  >
                    {{ isAnswerOpen(item.chapterCode, item.id) ? '🙈 隐藏答案' : '👁 显示答案' }}
                  </button>

                  <div class="grade-group">
                    <button
                      class="grade-btn"
                      :class="{ 'active-ok': item.grade === 'ok' }"
                      @click="setWrongbookGrade(item, 'ok')"
                    >
                      ✅ 会了（移出）
                    </button>
                    <button
                      class="grade-btn"
                      :class="{ 'active-warn': item.grade === 'warn' }"
                      @click="setWrongbookGrade(item, 'warn')"
                    >
                      ⚠️ 不稳
                    </button>
                    <button
                      class="grade-btn"
                      :class="{ 'active-bad': item.grade === 'bad' }"
                      @click="setWrongbookGrade(item, 'bad')"
                    >
                      ❌ 错了
                    </button>
                  </div>
                </div>

                <div v-if="isAnswerOpen(item.chapterCode, item.id)" class="ans-box show">
                  <div class="ans-label">参考答案与解析</div>
                  <div class="ans-body" v-html="item.answer"></div>
                </div>
              </article>
            </div>
          </template>
        </main>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick } from 'vue';
import { renderMarkdown } from './utils/markdown.js';

const THEME_KEY = 'eng_linear_theme_v1';
const LEGACY_PRACTICE_KEY = 'eng_linear_practice_v1'; // 兼容单文件交互刷题 HTML 的键名
const LOCAL_READING_KEY = 'kh_reading_state_v1'; // { [kbId]: { docPath, docTitle, updatedAt } }
const LOCAL_COMPLETED_KEY = 'kh_completed_docs_v1'; // { [kbId]: [docPath, ...] }
const AUTH_TOKEN_KEY = 'kh_auth_token_v1';

const theme = ref('light');
const currentView = ref('portal'); // 'portal' | 'workspace'
const activeKbId = ref('english');
const workMode = ref('read'); // 'read' | 'exercise' | 'wrongbook'
const sidebarOpen = ref(false);
const searchKw = ref('');

// Auth state
const authToken = ref(localStorage.getItem(AUTH_TOKEN_KEY) || '');
const currentUser = ref(null);
const showAuthModal = ref(false);
const authMode = ref('login'); // 'login' | 'register'
const authUsername = ref('');
const authPassword = ref('');
const authError = ref('');
const authSubmitting = ref(false);

// Local cache reactive mirror (始终与 localStorage 同步；已登录时由 DB 优先覆盖并写回 localStorage)
const localPractice = reactive({ grades: {}, inputs: {} });
const localReading = reactive({}); // kbId -> { docPath, docTitle, updatedAt }
const localCompleted = reactive({}); // kbId -> Set/Array of docPaths

// Portal state
const loadingPortal = ref(false);
const kbs = ref([]);

// Workspace tree state
const treeData = ref(null);
const selectedModuleIdx = ref(0);

// Document reader state
const loadingDoc = ref(false);
const currentDoc = ref(null);

// Exercise state
const loadingEx = ref(false);
const currentExCode = ref('01');
const currentEx = ref(null);
const filterMode = ref('required');
const groupTab = ref('ALL');
const openAnswers = ref(new Set());

// Wrongbook state
const wrongbookItems = ref([]);

// ==================== LocalStorage Persistence Helpers ====================
function loadLocalCache() {
  try {
    const rawPrac = localStorage.getItem(LEGACY_PRACTICE_KEY);
    if (rawPrac) {
      const parsed = JSON.parse(rawPrac);
      Object.assign(localPractice.grades, parsed.grades || {});
      Object.assign(localPractice.inputs, parsed.inputs || {});
    }
  } catch {}
  try {
    const rawRead = localStorage.getItem(LOCAL_READING_KEY);
    if (rawRead) Object.assign(localReading, JSON.parse(rawRead));
  } catch {}
  try {
    const rawComp = localStorage.getItem(LOCAL_COMPLETED_KEY);
    if (rawComp) Object.assign(localCompleted, JSON.parse(rawComp));
  } catch {}
}

function saveLocalPractice() {
  try {
    localStorage.setItem(
      LEGACY_PRACTICE_KEY,
      JSON.stringify({ grades: localPractice.grades, inputs: localPractice.inputs })
    );
  } catch {}
}

function saveLocalReading() {
  try {
    localStorage.setItem(LOCAL_READING_KEY, JSON.stringify(localReading));
  } catch {}
}

function saveLocalCompleted() {
  try {
    localStorage.setItem(LOCAL_COMPLETED_KEY, JSON.stringify(localCompleted));
  } catch {}
}

function authHeaders(extra = {}) {
  const h = { ...extra };
  if (authToken.value) {
    h.Authorization = `Bearer ${authToken.value}`;
  }
  return h;
}

// ==================== Auth Flows ====================
async function checkAuthSession() {
  if (!authToken.value) {
    currentUser.value = null;
    return;
  }
  try {
    const res = await fetch('/api/auth/me', { headers: authHeaders() });
    if (res.ok) {
      const data = await res.json();
      currentUser.value = data.user || null;
      if (!currentUser.value) {
        authToken.value = '';
        localStorage.removeItem(AUTH_TOKEN_KEY);
      }
    }
  } catch {}
}

function openAuthModal(mode = 'login') {
  authMode.value = mode;
  authError.value = '';
  showAuthModal.value = true;
}

async function submitAuth() {
  authError.value = '';
  authSubmitting.value = true;
  try {
    const url = authMode.value === 'login' ? '/api/auth/login' : '/api/auth/register';
    const res = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: authUsername.value.trim(),
        password: authPassword.value
      })
    });
    const data = await res.json();
    if (!res.ok) {
      authError.value = data.error || '操作失败，请重试';
      return;
    }
    authToken.value = data.token;
    localStorage.setItem(AUTH_TOKEN_KEY, data.token);
    currentUser.value = data.user;
    showAuthModal.value = false;
    authPassword.value = '';

    // 登录成功后：先把本地已有但数据库还没有的记录补齐上云（数据库已有的记录绝不被覆盖，保证数据库优先！）
    await syncLocalToDbIfNeeded(activeKbId.value);
    await refreshCurrentViewData();
  } finally {
    authSubmitting.value = false;
  }
}

async function handleLogout() {
  try {
    await fetch('/api/auth/logout', { method: 'POST', headers: authHeaders() });
  } catch {}
  authToken.value = '';
  currentUser.value = null;
  localStorage.removeItem(AUTH_TOKEN_KEY);
  await refreshCurrentViewData();
}

async function syncLocalToDbIfNeeded(kbId) {
  if (!currentUser.value) return;
  const practicePayload = {};
  for (const [k, g] of Object.entries(localPractice.grades)) {
    practicePayload[k] = { grade: g, userInput: localPractice.inputs[k] || '' };
  }
  for (const [k, inp] of Object.entries(localPractice.inputs)) {
    if (!practicePayload[k]) practicePayload[k] = { grade: '', userInput: inp };
  }
  try {
    await fetch(`/api/kbs/${kbId}/sync-local`, {
      method: 'POST',
      headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({
        practice: practicePayload,
        completedDocs: localCompleted[kbId] || [],
        lastRead: localReading[kbId] || null
      })
    });
  } catch {}
}

async function refreshCurrentViewData() {
  if (currentView.value === 'portal') {
    await fetchPortal();
  } else {
    await fetchTree(activeKbId.value);
    if (workMode.value === 'exercise' && currentExCode.value) {
      await openExercise(currentExCode.value);
    } else if (workMode.value === 'wrongbook') {
      await fetchWrongbook();
    }
  }
}

// ==================== Theme ====================
function initTheme() {
  const saved = localStorage.getItem(THEME_KEY);
  if (saved === 'dark') {
    theme.value = 'dark';
    document.documentElement.setAttribute('data-theme', 'dark');
  }
}

function toggleTheme() {
  theme.value = theme.value === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', theme.value);
  localStorage.setItem(THEME_KEY, theme.value);
}

// ==================== Portal & Dual-Storage Resolution ====================
async function fetchPortal() {
  loadingPortal.value = true;
  try {
    const res = await fetch('/api/kbs', { headers: authHeaders() });
    const list = await res.json();
    // 若已登录且数据库返回了 lastRead，同步写回本地缓存（数据库优先！）
    for (const kb of list) {
      if (currentUser.value && kb.lastRead) {
        localReading[kb.id] = kb.lastRead;
      }
    }
    saveLocalReading();
    kbs.value = list;
  } finally {
    loadingPortal.value = false;
  }
}

// 计算门户卡片的最终展示数据（已登录优先用 DB，未登录或 DB 为空则读取 localStorage）
const decoratedKbs = computed(() => {
  const localGrades = Object.values(localPractice.grades);
  const localMastered = localGrades.filter(g => g === 'ok').length;
  const localWrong = localGrades.filter(g => g === 'bad' || g === 'warn').length;

  return kbs.value.map(kb => {
    const effectiveLastRead =
      (currentUser.value && kb.lastRead) ? kb.lastRead : (localReading[kb.id] || null);
    const effectiveStats = currentUser.value
      ? {
          masteredQuestions: kb.stats.masteredQuestions,
          wrongQuestions: kb.stats.wrongQuestions
        }
      : {
          masteredQuestions: localMastered,
          wrongQuestions: localWrong
        };
    return {
      ...kb,
      effectiveLastRead,
      effectiveStats
    };
  });
});

const activeLastRead = computed(() => {
  if (currentUser.value && treeData.value?.lastRead) {
    return treeData.value.lastRead;
  }
  return localReading[activeKbId.value] || null;
});

function isDocCompleted(docPath) {
  const list = localCompleted[activeKbId.value] || [];
  return list.includes(docPath);
}

async function fetchTree(kbId) {
  const res = await fetch(`/api/kbs/${kbId}/tree`, { headers: authHeaders() });
  if (!res.ok) return;
  const data = await res.json();

  // 若已登录：以数据库数据为权威来源（DB 优先），同时将 DB 数据同步刷入本地缓存！
  if (currentUser.value && data.dbState) {
    if (data.dbState.lastRead) {
      localReading[kbId] = data.dbState.lastRead;
      saveLocalReading();
    }
    localCompleted[kbId] = data.dbState.completedDocs || [];
    saveLocalCompleted();

    for (const [k, val] of Object.entries(data.dbState.practice || {})) {
      if (val.grade !== undefined) localPractice.grades[k] = val.grade;
      if (val.userInput !== undefined) localPractice.inputs[k] = val.userInput;
    }
    saveLocalPractice();
  }

  treeData.value = data;
}

// 点击门户卡片或“进入阅读学习 / 继续上次阅读”按钮
async function enterKbReading(kb) {
  activeKbId.value = kb.id;
  currentView.value = 'workspace';
  workMode.value = 'read';
  await fetchTree(kb.id);

  // 优先取数据库的上次阅读章节，其次取本地缓存的上次阅读章节
  const lastRead =
    (currentUser.value && treeData.value?.lastRead)
      ? treeData.value.lastRead
      : (localReading[kb.id] || null);

  if (lastRead?.docPath) {
    await openDocument(lastRead.docPath);
    return;
  }

  const firstMod = treeData.value?.modules?.[0];
  const defaultDoc =
    firstMod?.rootDocs?.[0]?.path ||
    firstMod?.groups?.[0]?.docs?.[0]?.path;
  if (defaultDoc) {
    await openDocument(defaultDoc);
  }
}

async function enterKb(kbId, initialMode = 'read') {
  activeKbId.value = kbId;
  currentView.value = 'workspace';
  workMode.value = initialMode;
  await fetchTree(kbId);

  if (initialMode === 'read') {
    const lr = activeLastRead.value;
    if (lr?.docPath) {
      await openDocument(lr.docPath);
      return;
    }
    const firstMod = treeData.value?.modules?.[0];
    const defaultDoc =
      firstMod?.rootDocs?.[0]?.path ||
      firstMod?.groups?.[0]?.docs?.[0]?.path;
    if (defaultDoc) await openDocument(defaultDoc);
  } else if (initialMode === 'exercise') {
    await openExercise(currentExCode.value || '01');
  } else if (initialMode === 'wrongbook') {
    await fetchWrongbook();
  }
}

async function goPortal() {
  currentView.value = 'portal';
  await fetchPortal();
}

async function switchWorkMode(mode) {
  workMode.value = mode;
  searchKw.value = '';
  if (mode === 'exercise') {
    const targetCode = currentDoc.value?.exerciseCode || currentExCode.value || '01';
    await openExercise(targetCode);
  } else if (mode === 'wrongbook') {
    await fetchWrongbook();
  } else if (mode === 'read' && !currentDoc.value) {
    const lr = activeLastRead.value;
    if (lr?.docPath) {
      await openDocument(lr.docPath);
      return;
    }
    const firstMod = treeData.value?.modules?.[selectedModuleIdx.value];
    const firstPath = firstMod?.rootDocs?.[0]?.path || firstMod?.groups?.[0]?.docs?.[0]?.path;
    if (firstPath) await openDocument(firstPath);
  }
}

async function handleModuleChange() {
  if (workMode.value === 'exercise') {
    const modExercises = (treeData.value?.exercises || []).filter(
      ex => ex.moduleIdx === selectedModuleIdx.value
    );
    if (modExercises.length > 0) {
      await openExercise(modExercises[0].code);
    }
  }
}

const currentModule = computed(() => {
  return treeData.value?.modules?.[selectedModuleIdx.value] || null;
});

const filteredRootDocs = computed(() => {
  if (!currentModule.value) return [];
  const kw = searchKw.value.trim().toLowerCase();
  if (!kw) return currentModule.value.rootDocs;
  return currentModule.value.rootDocs.filter(d => d.title.toLowerCase().includes(kw));
});

const filteredDocGroups = computed(() => {
  if (!currentModule.value) return [];
  const kw = searchKw.value.trim().toLowerCase();
  return currentModule.value.groups
    .map(g => ({
      ...g,
      docs: kw ? g.docs.filter(d => d.title.toLowerCase().includes(kw)) : g.docs
    }))
    .filter(g => g.docs.length > 0);
});

const currentModuleExercises = computed(() => {
  const all = treeData.value?.exercises || [];
  const byMod = all.filter(ex => ex.moduleIdx === selectedModuleIdx.value);
  return byMod.length > 0 ? byMod : all;
});

const prevExerciseCode = computed(() => {
  const list = currentModuleExercises.value;
  const idx = list.findIndex(ex => ex.code === currentExCode.value);
  return idx > 0 ? list[idx - 1].code : null;
});

const nextExerciseCode = computed(() => {
  const list = currentModuleExercises.value;
  const idx = list.findIndex(ex => ex.code === currentExCode.value);
  return idx >= 0 && idx + 1 < list.length ? list[idx + 1].code : null;
});

// 侧边栏练习进度（按当前所选模块展示，已登录用 DB 统计，未登录实时用 localPractice 计算）
const groupedExercises = computed(() => {
  const rawList = currentModuleExercises.value;
  const list = rawList.map(ex => {
    if (currentUser.value) return ex;
    let okCount = 0;
    for (const [k, g] of Object.entries(localPractice.grades)) {
      if (k.startsWith(ex.code + ':') && g === 'ok') {
        okCount++;
      }
    }
    return {
      ...ex,
      okRequiredCount: Math.min(okCount, ex.requiredCount)
    };
  });

  const kw = searchKw.value.trim().toLowerCase();
  const filtered = kw
    ? list.filter(ex => (ex.rawCode || ex.code).includes(kw) || ex.title.toLowerCase().includes(kw))
    : list;
  const groups = [];
  let lastStage = '';
  for (const ex of filtered) {
    if (ex.stage !== lastStage) {
      groups.push({ stage: ex.stage, items: [] });
      lastStage = ex.stage;
    }
    groups[groups.length - 1].items.push(ex);
  }
  return groups;
});

const effectiveWrongTotal = computed(() => {
  if (currentUser.value && treeData.value) {
    return treeData.value.wrongTotal || 0;
  }
  return Object.values(localPractice.grades).filter(g => g === 'bad' || g === 'warn').length;
});

const renderedDocHtml = computed(() => {
  return currentDoc.value ? renderMarkdown(currentDoc.value.content) : '';
});

async function openDocument(pathOrStem, anchor = '') {
  loadingDoc.value = true;
  workMode.value = 'read';
  sidebarOpen.value = false;
  try {
    const res = await fetch(
      `/api/kbs/${activeKbId.value}/doc?path=${encodeURIComponent(pathOrStem)}`,
      { headers: authHeaders() }
    );
    if (!res.ok) return;
    const doc = await res.json();
    currentDoc.value = doc;

    if (treeData.value?.modules) {
      const mIdx = treeData.value.modules.findIndex(m => doc.path.startsWith(m.name + '/'));
      if (mIdx >= 0) selectedModuleIdx.value = mIdx;
    }

    // 双写保存“上次阅读章节”：① 写入 localStorage ② 若已登录写入后端 SQLite 数据库
    const record = {
      docPath: doc.path,
      docTitle: doc.title,
      updatedAt: new Date().toISOString()
    };
    localReading[activeKbId.value] = record;
    saveLocalReading();
    if (treeData.value) {
      treeData.value.lastRead = record;
    }
    if (currentUser.value) {
      fetch(`/api/kbs/${activeKbId.value}/reading-state`, {
        method: 'PUT',
        headers: authHeaders({ 'Content-Type': 'application/json' }),
        body: JSON.stringify({ docPath: doc.path, docTitle: doc.title })
      }).catch(() => {});
    }

    await nextTick();
    if (anchor) {
      scrollToHeadingAnchor(anchor);
    } else {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  } finally {
    loadingDoc.value = false;
  }
}

function scrollToHeadingAnchor(anchorText) {
  const target = anchorText.trim();
  const headings = document.querySelectorAll('.md-article [data-heading]');
  for (const el of headings) {
    const h = el.getAttribute('data-heading') || '';
    if (h === target || h.startsWith(target) || target.startsWith(h)) {
      el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }
  }
}

async function handleMarkdownClick(e) {
  const anchorEl = e.target.closest('.md-wiki-anchor');
  if (anchorEl) {
    e.preventDefault();
    scrollToHeadingAnchor(anchorEl.dataset.anchor || '');
    return;
  }

  const exEl = e.target.closest('[data-exercise-ch]');
  if (exEl) {
    e.preventDefault();
    const rawCh = exEl.dataset.exerciseCh;
    // 若当前文档有关联的带模块前缀的 exerciseCode（如 m2-01），优先使用对应模块前缀
    const targetExCode =
      currentDoc.value?.exerciseCode && currentDoc.value.exerciseCode.endsWith(rawCh)
        ? currentDoc.value.exerciseCode
        : (selectedModuleIdx.value > 0 ? `m${selectedModuleIdx.value + 1}-${rawCh}` : rawCh);
    await openExercise(targetExCode);
    return;
  }

  const wikiEl = e.target.closest('.md-wiki-link');
  if (wikiEl) {
    e.preventDefault();
    const targetDoc = wikiEl.dataset.wikilink;
    const targetAnchor = wikiEl.dataset.anchor || '';
    if (targetDoc) {
      await openDocument(targetDoc, targetAnchor);
    }
  }
}

async function toggleDocCompleted() {
  if (!currentDoc.value) return;
  const docPath = currentDoc.value.path;
  const curList = new Set(localCompleted[activeKbId.value] || []);
  const nextVal = !curList.has(docPath);
  if (nextVal) curList.add(docPath);
  else curList.delete(docPath);
  localCompleted[activeKbId.value] = [...curList];
  saveLocalCompleted();

  if (currentUser.value) {
    await fetch(`/api/kbs/${activeKbId.value}/chapter-progress`, {
      method: 'PUT',
      headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ docPath, completed: nextVal })
    });
    await fetchTree(activeKbId.value);
  }
}

async function openExercise(chapterCode) {
  const raw = String(chapterCode).trim();
  const code = raw.includes('-') ? raw : raw.padStart(2, '0');
  currentExCode.value = code;
  workMode.value = 'exercise';
  groupTab.value = 'ALL';
  openAnswers.value.clear();
  sidebarOpen.value = false;
  loadingEx.value = true;
  try {
    const res = await fetch(`/api/kbs/${activeKbId.value}/exercise/${code}`, {
      headers: authHeaders()
    });
    if (res.ok) {
      const data = await res.json();
      if (typeof data.moduleIdx === 'number') {
        selectedModuleIdx.value = data.moduleIdx;
      }
      // 合并策略：已登录时优先用 DB 返回值（若 DB 为空则用本地缓存兜底），同时双写回 localPractice
      for (const q of data.questions) {
        const k = qKey(code, q.id);
        if (currentUser.value) {
          const finalGrade = q.grade || localPractice.grades[k] || '';
          const finalInput = q.userInput || localPractice.inputs[k] || '';
          q.grade = finalGrade;
          q.userInput = finalInput;
          if (finalGrade) localPractice.grades[k] = finalGrade;
          if (finalInput) localPractice.inputs[k] = finalInput;
        } else {
          q.grade = localPractice.grades[k] || '';
          q.userInput = localPractice.inputs[k] || '';
        }
      }
      saveLocalPractice();
      currentEx.value = data;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  } finally {
    loadingEx.value = false;
  }
}

async function jumpToChapterDoc(chapterCode) {
  const ex = currentEx.value;
  const modIdx = typeof ex?.moduleIdx === 'number' ? ex.moduleIdx : selectedModuleIdx.value;
  const rawCode = ex?.rawCode || String(chapterCode).replace(/^m\d+-/, '').padStart(2, '0');
  const mod = treeData.value?.modules?.[modIdx];
  const chapGroup = mod?.groups?.find(g => g.name === '章节');
  const doc = chapGroup?.docs?.find(d => d.code === rawCode);
  if (doc) {
    await openDocument(doc.path);
  }
}

const exStats = computed(() => {
  const ex = currentEx.value;
  if (!ex) {
    return { totalReq: 0, doneReq: 0, okReq: 0, reviewCount: 0, cScore: 0, cMax: 24, cGraded: 0, cPassed: false };
  }
  const reqQs = ex.questions.filter(q => q.required);
  const doneReq = reqQs.filter(q => q.grade).length;
  const okReq = reqQs.filter(q => q.grade === 'ok').length;
  const reviewCount = ex.questions.filter(q => q.grade === 'bad' || q.grade === 'warn').length;

  const cReq = ex.questions.filter(q => q.group === 'C' && q.required);
  let cScore = 0;
  let cGraded = 0;
  for (const q of cReq) {
    if (q.grade) {
      cGraded++;
      if (q.grade === 'ok') cScore += 2;
      else if (q.grade === 'warn') cScore += 1;
    }
  }
  const cMax = cReq.length * 2;
  const cPassed = cGraded === cReq.length && cScore >= ex.cPass;

  return {
    totalReq: reqQs.length,
    doneReq,
    okReq,
    reviewCount,
    cScore,
    cMax,
    cGraded,
    cPassed
  };
});

const filteredQuestions = computed(() => {
  if (!currentEx.value) return [];
  return currentEx.value.questions.filter(q => {
    if (groupTab.value !== 'ALL' && q.group !== groupTab.value) return false;
    if (filterMode.value === 'required' && !q.required) return false;
    if (filterMode.value === 'todo' && q.grade) return false;
    if (filterMode.value === 'review' && q.grade !== 'bad' && q.grade !== 'warn') return false;
    return true;
  });
});

function qKey(chCode, qid) {
  return `${chCode}:${qid}`;
}

function isAnswerOpen(chCode, qid) {
  return openAnswers.value.has(qKey(chCode, qid));
}

function toggleAnswer(chCode, qid) {
  const k = qKey(chCode, qid);
  const next = new Set(openAnswers.value);
  if (next.has(k)) next.delete(k);
  else next.add(k);
  openAnswers.value = next;
}

function expandAllVisible(questions, chCode) {
  const next = new Set(openAnswers.value);
  questions.forEach(q => next.add(qKey(chCode, q.id)));
  openAnswers.value = next;
}

function collapseAllVisible(questions, chCode) {
  const next = new Set(openAnswers.value);
  questions.forEach(q => next.delete(qKey(chCode, q.id)));
  openAnswers.value = next;
}

function expandAllWrongbook() {
  const next = new Set(openAnswers.value);
  wrongbookItems.value.forEach(it => next.add(qKey(it.chapterCode, it.id)));
  openAnswers.value = next;
}

// 双写保存刷题记录：① 始终写 localStorage ② 若已登录同步写 SQLite 数据库
async function savePracticeRecord(chapterCode, q) {
  const k = qKey(chapterCode, q.id);
  if (q.grade) localPractice.grades[k] = q.grade;
  else delete localPractice.grades[k];

  if (q.userInput) localPractice.inputs[k] = q.userInput;
  else delete localPractice.inputs[k];
  saveLocalPractice();

  if (currentUser.value) {
    await fetch(`/api/kbs/${activeKbId.value}/practice`, {
      method: 'PUT',
      headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({
        chapterCode,
        questionId: q.id,
        userInput: q.userInput,
        grade: q.grade
      })
    });
    await fetchTree(activeKbId.value);
  }
}

async function setQuestionGrade(chapterCode, q, val) {
  q.grade = q.grade === val ? '' : val;
  await savePracticeRecord(chapterCode, q);
}

async function resetCurrentChapter() {
  if (!currentEx.value) return;
  const code = currentEx.value.code;
  if (!confirm(`确定重置第 ${code} 章的全部作答输入与自评记录吗？`)) return;

  for (const q of currentEx.value.questions) {
    const k = qKey(code, q.id);
    delete localPractice.grades[k];
    delete localPractice.inputs[k];
  }
  saveLocalPractice();

  if (currentUser.value) {
    await fetch(`/api/kbs/${activeKbId.value}/practice/${code}`, {
      method: 'DELETE',
      headers: authHeaders()
    });
    await fetchTree(activeKbId.value);
  }
  await openExercise(code);
}

async function fetchWrongbook() {
  if (currentUser.value) {
    const res = await fetch(`/api/kbs/${activeKbId.value}/wrongbook`, {
      headers: authHeaders()
    });
    if (res.ok) {
      const data = await res.json();
      wrongbookItems.value = data.items || [];
    }
    return;
  }

  // 未登录模式：从 localPractice 找出所有 bad / warn 的题号，向后端换取题目详情
  const keys = Object.entries(localPractice.grades)
    .filter(([, g]) => g === 'bad' || g === 'warn')
    .map(([k]) => k)
    .sort();
  if (!keys.length) {
    wrongbookItems.value = [];
    return;
  }
  const res = await fetch(
    `/api/kbs/${activeKbId.value}/wrongbook?keys=${encodeURIComponent(keys.join(','))}`
  );
  if (res.ok) {
    const data = await res.json();
    wrongbookItems.value = (data.items || []).map(it => {
      const k = qKey(it.chapterCode, it.id);
      return {
        ...it,
        grade: localPractice.grades[k] || '',
        userInput: localPractice.inputs[k] || ''
      };
    });
  }
}

async function setWrongbookGrade(item, val) {
  item.grade = val;
  await savePracticeRecord(item.chapterCode, item);
  await fetchWrongbook();
}

onMounted(async () => {
  initTheme();
  loadLocalCache();
  await checkAuthSession();
  if (currentUser.value) {
    await syncLocalToDbIfNeeded(activeKbId.value);
  }
  await fetchPortal();
});
</script>

<style>
:root {
  --bg: #f6f5f0;
  --surface: #ffffff;
  --surface-soft: #faf9f5;
  --border: #e6e3da;
  --border-strong: #d4cfc2;
  --text: #22242a;
  --text-muted: #666a73;
  --accent: #2c6bed;
  --accent-soft: #eaf1ff;
  --ok: #1d8a4e;
  --ok-soft: #e8f7ee;
  --warn: #b86e00;
  --warn-soft: #fff5e0;
  --bad: #c93434;
  --bad-soft: #fdecec;
  --hl-bg: #fff1a8;
  --hl-text: #22242a;
  --code-bg: #f0eee7;
  --shadow: 0 2px 10px rgba(25, 28, 36, 0.05);
  --radius: 12px;
}

[data-theme="dark"] {
  --bg: #14171d;
  --surface: #1d212a;
  --surface-soft: #232834;
  --border: #2e3442;
  --border-strong: #3f4759;
  --text: #e7eaf0;
  --text-muted: #9aa2b2;
  --accent: #6aa0ff;
  --accent-soft: #1e2c47;
  --ok: #4cd084;
  --ok-soft: #173324;
  --warn: #f2b44c;
  --warn-soft: #362a16;
  --bad: #f26d6d;
  --bad-soft: #3a1d21;
  --hl-bg: #54430a;
  --hl-text: #ffe58f;
  --code-bg: #29303e;
  --shadow: 0 2px 12px rgba(0, 0, 0, 0.28);
}

* { box-sizing: border-box; }
html, body {
  margin: 0;
  padding: 0;
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}

/* ==================== Auth Modal ==================== */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.48);
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
}
.auth-modal {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  max-width: 420px;
  width: 100%;
  padding: 22px 24px;
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.22);
}
.auth-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}
.auth-modal-header h3 { margin: 0; font-size: 18px; }
.auth-modal-desc {
  font-size: 13px;
  color: var(--text-muted);
  margin: 0 0 14px;
  line-height: 1.6;
}
.auth-tabs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 14px;
}
.auth-tab {
  padding: 7px 10px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  border: 1px solid var(--border);
  background: var(--surface-soft);
  color: var(--text-muted);
  cursor: pointer;
}
.auth-tab.active {
  background: var(--accent-soft);
  border-color: var(--accent);
  color: var(--accent);
}
.auth-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.auth-label {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
  font-weight: 600;
}
.auth-error {
  font-size: 13px;
  color: var(--bad);
  background: var(--bad-soft);
  padding: 7px 10px;
  border-radius: 8px;
}
.auth-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 6px;
}

/* ==================== Portal Styles ==================== */
.portal-page {
  max-width: 1080px;
  margin: 0 auto;
  padding: 28px 24px 64px;
}
.portal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
  padding-bottom: 22px;
  border-bottom: 1px solid var(--border);
  margin-bottom: 28px;
}
.portal-brand {
  display: flex;
  align-items: center;
  gap: 14px;
}
.portal-logo { font-size: 34px; }
.portal-brand h1 { font-size: 22px; margin: 0 0 2px; }
.portal-brand p { font-size: 13px; color: var(--text-muted); margin: 0; }
.header-right-tools {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.user-badge {
  font-size: 12.5px;
  padding: 5px 10px;
  border-radius: 99px;
  border: 1px solid var(--border);
  background: var(--surface-soft);
}
.user-badge.logged-in {
  border-color: var(--ok);
  background: var(--ok-soft);
  color: var(--ok);
  font-weight: 600;
}

.section-heading {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}
.section-heading h2 { font-size: 18px; margin: 0; }
.section-sub { font-size: 13px; color: var(--text-muted); }

.kb-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 20px;
}
.kb-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 22px 24px;
  box-shadow: var(--shadow);
  cursor: pointer;
  transition: transform .15s, border-color .15s;
  display: flex;
  flex-direction: column;
}
.kb-card:hover {
  transform: translateY(-2px);
  border-color: var(--accent);
}
.kb-card-placeholder {
  cursor: default;
  border-style: dashed;
  background: var(--surface-soft);
}
.kb-card-placeholder:hover {
  transform: none;
  border-color: var(--border-strong);
}
.kb-card-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}
.kb-icon { font-size: 30px; }
.kb-badge {
  font-size: 12px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 99px;
  background: var(--accent-soft);
  color: var(--accent);
}
.kb-title { font-size: 20px; margin: 0 0 6px; }
.kb-sub { font-size: 13.5px; color: var(--text-muted); margin: 0 0 14px; }
.kb-modules-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 16px;
}
.kb-mod-chip {
  font-size: 12px;
  padding: 2px 9px;
  border-radius: 6px;
  background: var(--surface-soft);
  border: 1px solid var(--border);
  color: var(--text-muted);
}
.kb-stats-grid {
  display: grid;
  grid-template-columns: 1.6fr 1fr 1fr;
  gap: 10px;
  margin-bottom: 18px;
  padding: 12px;
  border-radius: 10px;
  background: var(--surface-soft);
  border: 1px solid var(--border);
  align-items: center;
}
.kb-stat-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.kb-stat-box-wide {
  align-items: flex-start;
  text-align: left;
  padding-right: 8px;
  border-right: 1px dashed var(--border-strong);
  overflow: hidden;
}
.kb-stat-chapter {
  font-size: 13px;
  font-weight: 700;
  color: var(--accent);
  margin-top: 3px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.35;
}
.kb-stat-chapter.not-started {
  color: var(--text-muted);
  font-weight: 500;
}
.kb-stat-num { font-size: 16px; font-weight: 700; }
.kb-stat-num.text-warn { color: var(--bad); }
.kb-stat-label { font-size: 11.5px; color: var(--text-muted); }
.kb-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: auto;
}

/* Buttons */
.primary-btn {
  padding: 8px 14px;
  border-radius: 9px;
  font-size: 13px;
  font-weight: 600;
  border: 1px solid var(--accent);
  background: var(--accent);
  color: #fff;
  cursor: pointer;
  transition: opacity .15s;
}
.primary-btn:hover { opacity: .92; }
.secondary-btn {
  padding: 8px 14px;
  border-radius: 9px;
  font-size: 13px;
  font-weight: 600;
  border: 1px solid var(--accent);
  background: var(--accent-soft);
  color: var(--accent);
  cursor: pointer;
}
.warn-btn {
  padding: 8px 12px;
  border-radius: 9px;
  font-size: 13px;
  font-weight: 600;
  border: 1px solid var(--bad);
  background: var(--bad-soft);
  color: var(--bad);
  cursor: pointer;
}
.ghost-btn {
  padding: 6px 11px;
  border-radius: 8px;
  font-size: 12.5px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  transition: all .15s;
}
.ghost-btn:hover {
  color: var(--text);
  border-color: var(--border-strong);
  background: var(--surface-soft);
}

/* ==================== Workspace Layout ==================== */
.app-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  min-height: 100vh;
}
.sidebar {
  background: var(--surface);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow: hidden;
}
.sidebar-header {
  padding: 14px 14px 12px;
  border-bottom: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.brand-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}
.back-portal-btn {
  padding: 4px 8px;
  font-size: 12px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface-soft);
  color: var(--text-muted);
  cursor: pointer;
}
.back-portal-btn:hover { color: var(--accent); border-color: var(--accent); }
.brand-title { font-size: 15px; font-weight: 700; }

.sidebar-auth-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 5px 9px;
  border-radius: 7px;
  background: var(--surface-soft);
  border: 1px solid var(--border);
  font-size: 11.5px;
}
.sidebar-auth-text { color: var(--text-muted); }
.tiny-link-btn {
  border: none;
  background: transparent;
  color: var(--accent);
  font-size: 11.5px;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
}
.tiny-link-btn:hover { text-decoration: underline; }

.continue-banner {
  padding: 6px 9px;
  border-radius: 8px;
  background: var(--accent-soft);
  border: 1px solid var(--accent);
  font-size: 12px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 1px;
}
.continue-label { font-size: 11px; color: var(--text-muted); }
.continue-title {
  font-weight: 700;
  color: var(--accent);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.nav-mode-tabs {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 5px;
}
.mode-tab {
  padding: 6px 4px;
  font-size: 12px;
  font-weight: 600;
  border-radius: 7px;
  border: 1px solid var(--border);
  background: var(--surface-soft);
  color: var(--text-muted);
  cursor: pointer;
  text-align: center;
}
.mode-tab.active {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
}
.mode-tab.has-wrong:not(.active) {
  color: var(--bad);
  border-color: var(--bad);
  background: var(--bad-soft);
}

.mod-select {
  width: 100%;
  padding: 7px 9px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--surface-soft);
  color: var(--text);
  font-size: 12.5px;
}
.search-input {
  width: 100%;
  padding: 7px 10px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--surface-soft);
  color: var(--text);
  font-size: 13px;
  outline: none;
}
.search-input:focus { border-color: var(--accent); }

.chapter-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px 10px 24px;
}
.stage-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--text-muted);
  padding: 12px 8px 4px;
}
.ch-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px 10px;
  margin-bottom: 3px;
  border-radius: 9px;
  cursor: pointer;
  border: 1px solid transparent;
}
.ch-item:hover { background: var(--surface-soft); }
.ch-item.active { background: var(--accent-soft); border-color: var(--accent); }
.ch-item-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
}
.ch-code {
  font-size: 11px;
  font-weight: 700;
  color: var(--accent);
  background: var(--accent-soft);
  padding: 1px 6px;
  border-radius: 5px;
  flex-shrink: 0;
}
.ch-item.active .ch-code { background: var(--accent); color: #fff; }
.ch-name {
  font-size: 13px;
  font-weight: 500;
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.ch-stat { font-size: 11px; color: var(--text-muted); flex-shrink: 0; }
.last-read-pill {
  font-size: 10.5px;
  font-weight: 700;
  padding: 1px 5px;
  border-radius: 4px;
  background: var(--warn-soft);
  color: var(--warn);
  flex-shrink: 0;
}
.done-check {
  color: var(--ok);
  font-weight: 800;
  font-size: 13px;
}
.mini-bar {
  height: 3px;
  background: var(--border);
  border-radius: 99px;
  overflow: hidden;
}
.mini-bar-fill {
  height: 100%;
  background: var(--ok);
  transition: width .25s;
}

/* Main Content */
.main {
  padding: 24px 32px 64px;
  max-width: 960px;
  width: 100%;
  margin: 0 auto;
}
.mobile-bar {
  display: none;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 25;
}
.mobile-title {
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.mobile-user-dot { font-size: 12px; }

.header-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 18px 22px;
  box-shadow: var(--shadow);
  margin-bottom: 16px;
}
.header-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}
.doc-path-crumb {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 2px;
}
.doc-toolbar-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  align-items: center;
}
.check-complete-btn {
  padding: 7px 12px;
  border-radius: 8px;
  font-size: 12.5px;
  font-weight: 600;
  border: 1px solid var(--border-strong);
  background: var(--surface-soft);
  color: var(--text);
  cursor: pointer;
}
.check-complete-btn.completed {
  border-color: var(--ok);
  background: var(--ok-soft);
  color: var(--ok);
}

.ch-title { font-size: 21px; font-weight: 700; margin: 0 0 4px; }
.ch-scope { font-size: 13.5px; color: var(--text-muted); margin: 0; }
.summary-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}
.stat-pill {
  font-size: 12.5px;
  padding: 4px 10px;
  border-radius: 99px;
  background: var(--surface-soft);
  border: 1px solid var(--border);
}
.stat-pill.pass { background: var(--ok-soft); border-color: var(--ok); color: var(--ok); font-weight: 600; }
.stat-pill.warn { background: var(--warn-soft); border-color: var(--warn); color: var(--warn); font-weight: 600; }

/* ==================== Obsidian Markdown Rendered Styles ==================== */
.md-article {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 26px 30px;
  box-shadow: var(--shadow);
  font-size: 15.5px;
  line-height: 1.8;
}
.md-h { margin-top: 1.5em; margin-bottom: 0.6em; line-height: 1.35; }
.md-h1 { font-size: 23px; border-bottom: 1px solid var(--border); padding-bottom: 10px; margin-top: 0; }
.md-h2 { font-size: 19px; border-bottom: 1px dashed var(--border); padding-bottom: 6px; }
.md-h3 { font-size: 17px; color: var(--accent); }
.md-h4 { font-size: 15.5px; }
.md-p { margin: 0 0 13px; }
.md-ul, .md-ol { margin: 0 0 14px; padding-left: 22px; }
.md-ul li, .md-ol li { margin-bottom: 6px; }
.md-hr { border: none; border-top: 1px solid var(--border); margin: 22px 0; }

mark.md-highlight {
  background: var(--hl-bg);
  color: var(--hl-text);
  padding: 2px 6px;
  border-radius: 5px;
  font-weight: 600;
}

.md-tier-badge {
  display: inline-block;
  font-size: 11.5px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 99px;
  margin-left: 8px;
  vertical-align: middle;
}
.md-tier-badge.tag-must { background: var(--accent-soft); color: var(--accent); }
.md-tier-badge.tag-read { background: var(--warn-soft); color: var(--warn); }
.md-tier-badge.tag-opt { background: var(--surface-soft); color: var(--text-muted); border: 1px solid var(--border); }

.callout {
  border-radius: 10px;
  padding: 13px 16px;
  margin: 14px 0;
  border-left: 4px solid var(--accent);
  background: var(--surface-soft);
}
.callout-title {
  display: flex;
  align-items: center;
  gap: 7px;
  font-weight: 700;
  font-size: 14.5px;
  margin-bottom: 6px;
}
.callout-body p:last-child, .callout-body ul:last-child { margin-bottom: 0; }
.callout-important {
  border-left-color: var(--accent);
  background: var(--accent-soft);
}
.callout-important .callout-title { color: var(--accent); }
.callout-warning {
  border-left-color: var(--warn);
  background: var(--warn-soft);
}
.callout-warning .callout-title { color: var(--warn); }
.callout-tip {
  border-left-color: var(--ok);
  background: var(--ok-soft);
}
.callout-tip .callout-title { color: var(--ok); }
.callout-note {
  border-left-color: var(--border-strong);
  background: var(--surface-soft);
}

.md-quote {
  margin: 12px 0;
  padding: 10px 14px;
  border-left: 4px solid var(--border-strong);
  background: var(--surface-soft);
  border-radius: 8px;
}
.md-quote p { margin: 0; }

.md-article code, .q-prompt code, .ans-body code {
  background: var(--code-bg);
  padding: 2px 6px;
  border-radius: 5px;
  font-family: ui-monospace, SFMono-Regular, Consolas, monospace;
  font-size: 0.92em;
}
.md-pre {
  background: var(--code-bg);
  padding: 12px 16px;
  border-radius: 9px;
  overflow-x: auto;
  font-size: 13.5px;
  line-height: 1.5;
}
.md-pre code { background: transparent; padding: 0; }

.table-scroll {
  width: 100%;
  overflow-x: auto;
  margin: 12px 0 16px;
}
.md-table, .cov-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}
.md-table th, .md-table td, .cov-table th, .cov-table td {
  text-align: left;
  padding: 8px 11px;
  border: 1px solid var(--border);
}
.md-table th, .cov-table th {
  background: var(--surface-soft);
  font-weight: 700;
}

.md-wiki-link, .md-wiki-anchor {
  color: var(--accent);
  text-decoration: none;
  font-weight: 500;
  border-bottom: 1px dashed var(--accent);
}
.md-wiki-link:hover, .md-wiki-anchor:hover { opacity: 0.8; }
.md-exercise-btn, .md-exercise-link {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 8px;
  background: var(--accent);
  color: #fff !important;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
}

.md-details {
  margin: 12px 0;
  border: 1px solid var(--border);
  border-radius: 9px;
  background: var(--surface-soft);
  padding: 10px 14px;
}
.md-details summary {
  cursor: pointer;
  font-weight: 600;
  color: var(--accent);
}
.md-details-body {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed var(--border);
}

/* ==================== Exercise Interactive Cards ==================== */
details.drawer {
  margin-top: 14px;
  border-top: 1px dashed var(--border);
  padding-top: 10px;
}
details.drawer summary {
  cursor: pointer;
  font-size: 13px;
  font-weight: 600;
  color: var(--accent);
}
.controls {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 12px 16px;
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  position: sticky;
  top: 10px;
  z-index: 10;
  box-shadow: var(--shadow);
}
.ctrl-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  flex-wrap: wrap;
}
.pill-group { display: flex; gap: 6px; flex-wrap: wrap; }
.pill {
  padding: 6px 12px;
  border-radius: 99px;
  font-size: 13px;
  font-weight: 500;
  border: 1px solid var(--border);
  background: var(--surface-soft);
  color: var(--text);
  cursor: pointer;
}
.pill.active {
  background: var(--accent);
  border-color: var(--accent);
  color: #fff;
  font-weight: 600;
}

.q-list { display: flex; flex-direction: column; gap: 12px; }
.section-passage-box {
  background: var(--surface);
  border: 1px solid var(--accent);
  border-left: 4px solid var(--accent);
  border-radius: var(--radius);
  padding: 16px 20px;
  margin-top: 6px;
}
.passage-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 8px;
}
.passage-body p {
  margin: 0 0 10px;
  font-size: 14.5px;
  line-height: 1.75;
}
.passage-body p:last-child { margin-bottom: 0; }
.q-options-block {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding-left: 8px;
}
.q-option-line {
  font-size: 14.5px;
  color: var(--text);
}
.q-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-left: 4px solid var(--border-strong);
  border-radius: var(--radius);
  padding: 16px 20px;
  box-shadow: var(--shadow);
}
.q-card.st-ok { border-left-color: var(--ok); }
.q-card.st-warn { border-left-color: var(--warn); }
.q-card.st-bad { border-left-color: var(--bad); }

.q-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}
.q-id { font-weight: 700; font-size: 14px; color: var(--accent); }
.q-tag {
  font-size: 11.5px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 6px;
}
.q-tag.req { background: var(--accent-soft); color: var(--accent); }
.q-tag.read { background: var(--warn-soft); color: var(--warn); }
.q-tag.opt { background: var(--surface-soft); color: var(--text-muted); border: 1px solid var(--border); }
.q-topic { font-size: 12.5px; color: var(--text-muted); }
.q-chapter-badge {
  font-size: 11.5px;
  padding: 2px 8px;
  border-radius: 6px;
  background: var(--code-bg);
  color: var(--accent);
  margin-left: auto;
}
.q-prompt { font-size: 15.5px; margin: 0 0 12px; line-height: 1.75; }
.blank-slot {
  display: inline-block;
  padding: 0 6px;
  border-bottom: 2px solid var(--accent);
  color: var(--accent);
  font-weight: 600;
}
.ref-chip {
  font-size: 12px;
  padding: 1px 7px;
  border-radius: 5px;
  background: var(--surface-soft);
  border: 1px solid var(--border);
  color: var(--text-muted);
}

.q-input-row { margin-bottom: 12px; }
.q-input {
  width: 100%;
  padding: 9px 12px;
  border-radius: 8px;
  border: 1px solid var(--border);
  background: var(--surface-soft);
  color: var(--text);
  font-size: 14px;
  outline: none;
}
.q-input:focus { border-color: var(--accent); background: var(--surface); }

.q-actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  flex-wrap: wrap;
}
.ans-toggle {
  padding: 7px 14px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  border: 1px solid var(--accent);
  background: var(--accent-soft);
  color: var(--accent);
  cursor: pointer;
}
.ans-toggle.open {
  background: var(--surface-soft);
  border-color: var(--border-strong);
  color: var(--text-muted);
}
.grade-group { display: flex; gap: 6px; }
.grade-btn {
  padding: 6px 10px;
  border-radius: 8px;
  font-size: 12.5px;
  border: 1px solid var(--border);
  background: var(--surface-soft);
  color: var(--text-muted);
  cursor: pointer;
}
.grade-btn.active-ok { background: var(--ok-soft); border-color: var(--ok); color: var(--ok); font-weight: 700; }
.grade-btn.active-warn { background: var(--warn-soft); border-color: var(--warn); color: var(--warn); font-weight: 700; }
.grade-btn.active-bad { background: var(--bad-soft); border-color: var(--bad); color: var(--bad); font-weight: 700; }

.ans-box {
  margin-top: 12px;
  padding: 12px 14px;
  border-radius: 9px;
  background: var(--surface-soft);
  border: 1px solid var(--border);
}
.ans-label { font-size: 11.5px; font-weight: 700; color: var(--ok); margin-bottom: 4px; }
.ans-body { font-size: 14.5px; line-height: 1.7; }

.empty-state {
  text-align: center;
  padding: 48px 20px;
  color: var(--text-muted);
  background: var(--surface);
  border: 1px dashed var(--border-strong);
  border-radius: var(--radius);
}
.bottom-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 24px;
  gap: 12px;
  flex-wrap: wrap;
}
.nav-btn {
  padding: 10px 16px;
  border-radius: 10px;
  font-size: 13.5px;
  font-weight: 600;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  cursor: pointer;
}
.nav-btn:hover:not(:disabled) { border-color: var(--accent); color: var(--accent); }
.nav-btn:disabled { opacity: .4; cursor: not-allowed; }

@media (max-width: 860px) {
  .app-layout { grid-template-columns: 1fr; }
  .mobile-bar { display: flex; }
  .sidebar-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    z-index: 35;
  }
  .sidebar {
    position: fixed;
    left: -310px;
    top: 0;
    width: 295px;
    z-index: 40;
    transition: left .2s ease;
  }
  .sidebar.open { left: 0; }
  .main { padding: 14px 12px 48px; }
  .md-article { padding: 18px 16px; font-size: 15px; }
  .controls { position: static; }
  .portal-page { padding: 18px 14px 48px; }
  .kb-grid { grid-template-columns: 1fr; }
  .kb-stats-grid { grid-template-columns: 1fr; }
  .kb-stat-box-wide { border-right: none; border-bottom: 1px dashed var(--border-strong); padding-bottom: 8px; }
}
</style>
