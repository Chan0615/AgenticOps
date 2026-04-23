<template>
  <div class="query-chat-page">
    <!-- ===== 左侧：查询历史 ===== -->
    <aside class="chat-aside">
      <div class="aside-header">
        <span class="aside-title">查询历史</span>
      </div>
      <div class="aside-body">
        <div
          v-for="h in histories"
          :key="h.id"
          class="history-item"
          @click="loadHistory(h)"
        >
          <div class="history-question">{{ h.question }}</div>
          <div style="display: flex; align-items: center; gap: 8px; margin-top: 4px">
            <Tag :color="h.status === 'success' ? 'green' : 'red'" style="font-size: 10px">
              {{ h.status === 'success' ? '成功' : '失败' }}
            </Tag>
            <span style="font-size: 10px; color: #94a3b8">{{ formatTime(h.created_at) }}</span>
          </div>
        </div>
        <div v-if="!histories.length" class="empty-hint">暂无查询记录</div>
      </div>
    </aside>

    <!-- ===== 右侧：主区域 ===== -->
    <main class="chat-main">
      <!-- 顶栏 -->
      <div class="chat-topbar">
        <span style="font-size: 13px; color: #64748b">数据源：</span>
        <Select
          v-model:value="selectedDatasourceId"
          placeholder="请选择数据源"
          style="width: 280px"
          :loading="dsLoading"
          @change="onDatasourceChange"
        >
          <SelectOption v-for="ds in datasources" :key="ds.id" :value="ds.id">
            <Tag :color="ds.db_type === 'mysql' ? 'blue' : 'green'" style="font-size: 10px; margin-right: 4px">
              {{ ds.db_type === 'mysql' ? 'MySQL' : 'PG' }}
            </Tag>
            {{ ds.name }}
          </SelectOption>
        </Select>
        <span v-if="activePhase" class="phase-badge">
          <span class="phase-dot"></span>
          {{ activePhase }}
        </span>
      </div>

      <!-- 对话内容区 -->
      <div ref="contentRef" class="chat-content">
        <!-- 空状态 -->
        <div v-if="!messages.length" class="empty-state">
          <div class="empty-icon">Q</div>
          <p class="empty-title">智能问数</p>
          <p class="empty-desc">选择数据源，用自然语言提问，AI 自动生成 SQL 查询</p>
          <div class="quick-tips">
            <button
              v-for="tip in quickTips"
              :key="tip"
              class="quick-tip"
              :disabled="!selectedDatasourceId"
              @click="inputText = tip"
            >{{ tip }}</button>
          </div>
        </div>

        <!-- 消息流 -->
        <div v-else class="messages">
          <div v-for="(msg, idx) in messages" :key="idx">
            <!-- 用户消息 -->
            <div v-if="msg.type === 'user'" class="msg-user">
              <div class="msg-user-bubble">{{ msg.content }}</div>
            </div>

            <!-- SQL 展示 -->
            <div v-else-if="msg.type === 'sql'" class="msg-ai">
              <div class="msg-avatar msg-avatar-sql">SQL</div>
              <div class="msg-sql-card">
                <div class="msg-sql-header">
                  <span style="font-size: 12px; font-weight: 500; color: #475569">生成的 SQL</span>
                  <span style="font-size: 12px; color: #94a3b8">{{ msg.explanation }}</span>
                </div>
                <pre class="msg-sql-code"><code>{{ msg.content }}</code></pre>
              </div>
            </div>

            <!-- 查询结果 -->
            <div v-else-if="msg.type === 'result'" class="msg-ai">
              <div class="msg-avatar msg-avatar-result">R</div>
              <div class="msg-result-card">
                <div class="msg-result-header">
                  <span style="font-size: 12px; font-weight: 500; color: #475569">
                    查询结果（{{ msg.result.row_count }} 行，耗时 {{ msg.result.execution_time }}ms）
                  </span>
                  <Button v-if="msg.result.has_more && currentHistoryId" type="link" size="small" @click="handleExport">
                    导出 Excel
                  </Button>
                </div>
                <div class="msg-result-table">
                  <Table
                    :columns="buildResultColumns(msg.result.columns)"
                    :data-source="msg.result.rows"
                    :pagination="false"
                    size="small"
                    :scroll="{ x: 'max-content' }"
                    row-key="_idx"
                  />
                </div>
                <div v-if="msg.result.chart_type && msg.result.chart_type !== 'table' && msg.result.rows.length > 1" class="msg-result-chart">
                  <div ref="chartRef" style="width: 100%; height: 320px"></div>
                </div>
              </div>
            </div>

            <!-- AI 摘要 -->
            <div v-else-if="msg.type === 'summary'" class="msg-ai">
              <div class="msg-avatar msg-avatar-ai">AI</div>
              <div class="msg-ai-bubble">
                <div v-if="msg.streaming" class="streaming-text">{{ msg.content }}<span class="cursor-blink">|</span></div>
                <div v-else class="prose prose-sm" v-html="renderMarkdown(msg.content)"></div>
              </div>
            </div>

            <!-- 错误 -->
            <div v-else-if="msg.type === 'error'" class="msg-ai">
              <div class="msg-avatar msg-avatar-error">!</div>
              <div class="msg-error-bubble">{{ msg.content }}</div>
            </div>
          </div>

          <!-- 思考动画 -->
          <div v-if="sending && !activePhase" class="msg-ai">
            <div class="msg-avatar msg-avatar-ai">AI</div>
            <div class="thinking-dots"><span></span><span></span><span></span></div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="chat-input-area">
        <div class="chat-input-box">
          <textarea
            v-model="inputText"
            rows="1"
            class="chat-textarea"
            placeholder="用自然语言描述你想查询的数据，如：最近一周新增了多少用户..."
            :disabled="!selectedDatasourceId"
            @keydown.enter.exact.prevent="sendMessage"
          />
          <button class="send-btn" :disabled="!inputText.trim() || sending || !selectedDatasourceId" @click="sendMessage">
            查询
          </button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue'
import {
  Button,
  Select,
  Table,
  Tag,
  message,
} from 'ant-design-vue'
import { marked } from 'marked'
import { datasourceApi, dataqueryApi, type DataSource, type QueryResult } from '@/api/dataquery'
import dayjs from 'dayjs'

const SelectOption = Select.Option

// ============ 类型 ============
interface ChatMessage {
  type: 'user' | 'sql' | 'result' | 'summary' | 'error'
  content: string
  explanation?: string
  result?: QueryResult & { rows: Record<string, any>[] }
  streaming?: boolean
}

// ============ 状态 ============
const datasources = ref<DataSource[]>([])
const dsLoading = ref(false)
const selectedDatasourceId = ref<number | undefined>(undefined)
const messages = ref<ChatMessage[]>([])
const inputText = ref('')
const sending = ref(false)
const activePhase = ref('')
const contentRef = ref<HTMLElement | null>(null)
const chartRef = ref<HTMLElement | null>(null)
const histories = ref<any[]>([])
const currentHistoryId = ref<number | null>(null)

const quickTips = [
  '这个数据库有哪些表？',
  '统计每张表的数据量',
  '最近创建的10条记录',
  '按状态分组统计数量',
]

// ============ 工具 ============
const renderMarkdown = (content: string) => marked.parse(content || '') as string
const formatTime = (t: string) => dayjs(t).format('MM-DD HH:mm')

const scrollToBottom = async () => {
  await nextTick()
  if (contentRef.value) {
    contentRef.value.scrollTop = contentRef.value.scrollHeight
  }
}

const buildResultColumns = (columns: string[]) => {
  if (!columns?.length) return []
  return columns.map((col) => ({
    title: col,
    dataIndex: col,
    key: col,
    width: Math.max(100, col.length * 12 + 32),
    ellipsis: true,
  }))
}

// ============ 数据源 ============
const loadDatasources = async () => {
  dsLoading.value = true
  try {
    const res = await datasourceApi.list({ page: 1, page_size: 100, status: 'active' })
    datasources.value = res.data || []
  } catch {
    datasources.value = []
  } finally {
    dsLoading.value = false
  }
}

const onDatasourceChange = () => {
  messages.value = []
  currentHistoryId.value = null
  loadHistories()
}

// ============ 查询历史 ============
const loadHistories = async () => {
  if (!selectedDatasourceId.value) {
    histories.value = []
    return
  }
  try {
    const res = await dataqueryApi.getHistory({
      page: 1,
      page_size: 30,
      datasource_id: selectedDatasourceId.value,
    })
    histories.value = res.data || []
  } catch {
    histories.value = []
  }
}

const loadHistory = async (h: any) => {
  try {
    const detail = await dataqueryApi.getHistoryDetail(h.id)
    messages.value = []
    messages.value.push({ type: 'user', content: detail.question })
    if (detail.generated_sql) {
      messages.value.push({ type: 'sql', content: detail.generated_sql })
    }
    if (detail.status === 'error') {
      messages.value.push({ type: 'error', content: detail.error_message || '查询失败' })
    } else if (detail.result_data) {
      messages.value.push({
        type: 'result',
        content: '',
        result: {
          columns: detail.result_data.length ? Object.keys(detail.result_data[0]) : [],
          rows: detail.result_data.map((r: any, i: number) => ({ ...r, _idx: i })),
          row_count: detail.row_count,
          execution_time: detail.execution_time || 0,
          chart_type: detail.chart_type || 'table',
          chart_config: detail.chart_config,
          has_more: false,
        },
      })
      if (detail.result_summary) {
        messages.value.push({ type: 'summary', content: detail.result_summary })
      }
    }
    currentHistoryId.value = detail.id
    await scrollToBottom()
  } catch {
    message.error('加载历史记录失败')
  }
}

// ============ 发送消息（SSE 流式） ============
const sendMessage = async () => {
  const text = inputText.value.trim()
  if (!text || sending.value || !selectedDatasourceId.value) return

  messages.value.push({ type: 'user', content: text })
  inputText.value = ''
  sending.value = true
  activePhase.value = '生成 SQL ...'
  await scrollToBottom()

  let summaryMsgIdx = -1

  await dataqueryApi.askStream(
    { datasource_id: selectedDatasourceId.value, question: text },
    {
      onSQL(info) {
        activePhase.value = '执行查询 ...'
        messages.value.push({ type: 'sql', content: info.sql, explanation: info.explanation })
        scrollToBottom()
      },
      onExecuting() {
        activePhase.value = '执行中 ...'
      },
      onResult(result) {
        activePhase.value = '生成分析 ...'
        const rows = (result.rows || []).map((r: any, i: number) => ({ ...r, _idx: i }))
        messages.value.push({ type: 'result', content: '', result: { ...result, rows } })
        scrollToBottom()
        if (result.chart_type && result.chart_type !== 'table' && rows.length > 1) {
          nextTick(() => renderChart(result, rows))
        }
      },
      onSummaryChunk(chunk) {
        if (summaryMsgIdx === -1) {
          messages.value.push({ type: 'summary', content: chunk, streaming: true })
          summaryMsgIdx = messages.value.length - 1
        } else {
          messages.value[summaryMsgIdx].content += chunk
        }
        scrollToBottom()
      },
      onDone(info) {
        if (summaryMsgIdx >= 0) {
          messages.value[summaryMsgIdx].streaming = false
          messages.value = [...messages.value]
        }
        currentHistoryId.value = info.history_id || null
        sending.value = false
        activePhase.value = ''
        loadHistories()
        nextTick(() => scrollToBottom())
      },
      onError(error) {
        messages.value.push({ type: 'error', content: error })
        sending.value = false
        activePhase.value = ''
        scrollToBottom()
      },
    },
  )
}

// ============ 图表渲染 ============
const renderChart = async (result: QueryResult, rows: Record<string, any>[]) => {
  try {
    const echarts = await import('echarts')
    await nextTick()
    const el = chartRef.value
    if (!el) return

    const chart = echarts.init(el)
    const config = result.chart_config || {}
    const columns = result.columns || []
    const xField = config.x_field || columns[0]
    const yField = config.y_field || (columns.length > 1 ? columns[1] : columns[0])
    const chartType = result.chart_type

    const xData = rows.map((r) => String(r[xField] ?? ''))
    const yData = rows.map((r) => Number(r[yField]) || 0)

    let option: any = {}
    if (chartType === 'line') {
      option = {
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: xData },
        yAxis: { type: 'value' },
        series: [{ data: yData, type: 'line', smooth: true, areaStyle: { opacity: 0.15 } }],
        grid: { left: 50, right: 20, bottom: 30, top: 20 },
      }
    } else if (chartType === 'bar') {
      option = {
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: xData, axisLabel: { rotate: xData.length > 8 ? 30 : 0 } },
        yAxis: { type: 'value' },
        series: [{ data: yData, type: 'bar', barMaxWidth: 40 }],
        grid: { left: 50, right: 20, bottom: 50, top: 20 },
      }
    } else if (chartType === 'pie') {
      option = {
        tooltip: { trigger: 'item' },
        series: [{
          type: 'pie', radius: ['40%', '70%'],
          data: rows.map((r) => ({ name: String(r[xField] ?? ''), value: Number(r[yField]) || 0 })),
        }],
      }
    }
    if (Object.keys(option).length) chart.setOption(option)
  } catch (e) {
    console.warn('图表渲染失败:', e)
  }
}

// ============ 导出 ============
const handleExport = () => {
  if (!currentHistoryId.value) return
  const token = localStorage.getItem('token') || ''
  const url = dataqueryApi.getExportUrl(currentHistoryId.value)
  fetch(url, { headers: { Authorization: `Bearer ${token}` } })
    .then((res) => res.blob())
    .then((blob) => {
      const blobUrl = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = blobUrl
      a.download = `query_result_${currentHistoryId.value}.xlsx`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(blobUrl)
    })
    .catch(() => message.error('导出失败'))
}

// ============ 初始化 ============
onMounted(async () => {
  await loadDatasources()
})
</script>

<style scoped>
.query-chat-page {
  display: flex;
  height: calc(100vh - 96px);
  min-height: 540px;
  overflow: hidden;
  border-radius: 14px;
  border: 1px solid #f1f5f9;
  background: #fff;
}

/* 左侧边栏 */
.chat-aside {
  width: 288px;
  border-right: 1px solid #e2e8f0;
  background: rgba(248, 250, 252, 0.6);
  display: flex;
  flex-direction: column;
}
.aside-header {
  padding: 16px;
  border-bottom: 1px solid #e2e8f0;
}
.aside-title {
  font-size: 13px;
  font-weight: 600;
  color: #334155;
}
.aside-body {
  flex: 1;
  overflow: auto;
  padding: 12px 8px;
}
.history-item {
  padding: 8px 10px;
  border: 1px solid transparent;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 4px;
}
.history-item:hover {
  background: #f8fafc;
  border-color: #e2e8f0;
}
.history-question {
  font-size: 12px;
  color: #334155;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.empty-hint {
  text-align: center;
  font-size: 12px;
  color: #94a3b8;
  padding: 32px 0;
}

/* 主区域 */
.chat-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}
.chat-topbar {
  height: 56px;
  padding: 0 20px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  gap: 16px;
}
.chat-content {
  flex: 1;
  overflow: auto;
  padding: 20px 24px;
}
.chat-input-area {
  border-top: 1px solid #e2e8f0;
  padding: 16px;
  background: #fff;
}
.chat-input-box {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 12px 16px;
}
.chat-textarea {
  flex: 1;
  background: transparent;
  resize: none;
  outline: none;
  font-size: 13px;
  color: #1e293b;
  max-height: 128px;
  border: none;
  font-family: inherit;
}

/* 空状态 */
.empty-state {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}
.empty-icon {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: #ede9fe;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  color: #7c3aed;
  margin-bottom: 16px;
}
.empty-title {
  font-size: 18px;
  font-weight: 600;
  color: #0f172a;
  margin-bottom: 4px;
}
.empty-desc {
  font-size: 13px;
  color: #94a3b8;
  margin-bottom: 20px;
}
.quick-tips {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  max-width: 480px;
}
.quick-tip {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 12px;
  color: #64748b;
  cursor: pointer;
}
.quick-tip:hover:not(:disabled) {
  background: #f5f3ff;
  border-color: #c4b5fd;
  color: #6d28d9;
}
.quick-tip:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

/* 消息 */
.messages {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.msg-user {
  display: flex;
  justify-content: flex-end;
}
.msg-user-bubble {
  max-width: 72%;
  background: #8b5cf6;
  color: #fff;
  padding: 10px 16px;
  border-radius: 16px 16px 4px 16px;
  font-size: 13px;
  white-space: pre-wrap;
}
.msg-ai {
  display: flex;
  justify-content: flex-start;
  gap: 10px;
}
.msg-avatar {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
  font-size: 11px;
  font-weight: 700;
}
.msg-avatar-sql { background: #ede9fe; color: #7c3aed; }
.msg-avatar-result { background: #d1fae5; color: #047857; }
.msg-avatar-ai { background: #ede9fe; color: #7c3aed; }
.msg-avatar-error { background: #fee2e2; color: #dc2626; }

.msg-sql-card {
  max-width: 78%;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px 16px 16px 4px;
  overflow: hidden;
}
.msg-sql-header {
  padding: 8px 16px;
  background: #f8fafc;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.msg-sql-code {
  padding: 12px 16px;
  font-size: 12px;
  background: #1e293b;
  color: #6ee7b7;
  overflow-x: auto;
  margin: 0;
}

.msg-result-card {
  max-width: 100%;
  width: 100%;
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 16px 16px 16px 4px;
  overflow: hidden;
}
.msg-result-header {
  padding: 8px 16px;
  background: #f8fafc;
  border-bottom: 1px solid #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.msg-result-table {
  overflow-x: auto;
  max-height: 400px;
  overflow-y: auto;
}
.msg-result-chart {
  padding: 16px;
  border-top: 1px solid #f1f5f9;
}

.msg-ai-bubble {
  max-width: 78%;
  background: #fff;
  border: 1px solid #e2e8f0;
  padding: 12px 16px;
  border-radius: 16px 16px 16px 4px;
  font-size: 13px;
  color: #1e293b;
}
.msg-error-bubble {
  max-width: 78%;
  background: #fef2f2;
  border: 1px solid #fecaca;
  padding: 12px 16px;
  border-radius: 16px 16px 16px 4px;
  font-size: 13px;
  color: #b91c1c;
}

/* 状态指示 */
.phase-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #f5f3ff;
  border: 1px solid #ddd6fe;
  border-radius: 6px;
  padding: 3px 10px;
  font-size: 11px;
  color: #7c3aed;
  font-weight: 500;
}
.phase-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #7c3aed;
  animation: pulse-dot 1s infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.send-btn {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}
.send-btn:disabled { opacity: 0.45; cursor: not-allowed; }

.streaming-text {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.65;
}
.cursor-blink {
  display: inline;
  color: #94a3b8;
  animation: blink 0.8s step-end infinite;
}
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.thinking-dots {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 16px 16px 16px 4px;
}
.thinking-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #94a3b8;
  animation: thinking 1.2s infinite;
}
.thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
.thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes thinking {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30% { transform: translateY(-4px); opacity: 1; }
}

/* Markdown 渲染 */
.prose :deep(table) { width: 100%; border-collapse: collapse; margin: 10px 0; font-size: 13px; }
.prose :deep(th) { padding: 8px 12px; text-align: left; font-weight: 600; color: #334155; border-bottom: 2px solid #e2e8f0; }
.prose :deep(td) { padding: 7px 12px; border-bottom: 1px solid #f1f5f9; color: #475569; }
.prose :deep(code) { background: #f1f5f9; color: #7c3aed; padding: 1px 5px; border-radius: 4px; font-size: 12px; }
.prose :deep(pre) { background: #1e293b; color: #e2e8f0; padding: 14px 16px; border-radius: 10px; overflow-x: auto; margin: 10px 0; font-size: 12px; }
.prose :deep(pre code) { background: none; color: inherit; padding: 0; }
.prose :deep(p) { margin: 6px 0; line-height: 1.65; }
.prose :deep(strong) { font-weight: 600; color: #1e293b; }
</style>
