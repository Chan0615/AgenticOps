<template>
  <div class="rag-chat-page bg-white flex">
    <!-- ===== 左侧：知识库选择 + 对话历史 ===== -->
    <aside class="aside-panel flex flex-col">
      <!-- 知识库选择器 -->
      <div class="aside-header">
        <Select
          v-model:value="selectedKbId"
          placeholder="选择知识库"
          style="width: 100%"
          :loading="kbLoading"
          allowClear
          @change="onKbChange"
        >
          <SelectOption v-for="kb in knowledgeBases" :key="kb.id" :value="kb.id">
            <span class="flex items-center gap-1.5">
              <span class="kb-dot" :class="kb.status ? 'kb-dot-active' : 'kb-dot-inactive'"></span>
              {{ kb.name }}
              <span class="kb-doc-count">({{ kb.document_count }})</span>
            </span>
          </SelectOption>
        </Select>
      </div>

      <!-- 新对话按钮 -->
      <div class="px-3 py-2">
        <button class="new-chat-btn" @click="startNewChat">+ 新对话</button>
      </div>

      <!-- 对话历史列表 -->
      <div class="flex-1 overflow-auto px-2 py-1 space-y-0.5">
        <div
          v-for="conv in conversations"
          :key="conv.id"
          class="conversation-item"
          :class="{ active: currentConversationId === conv.id }"
          @click="openConversation(conv.id)"
        >
          <span class="truncate flex-1">{{ conv.title || `会话 ${conv.id}` }}</span>
          <span class="conv-time">{{ formatTime(conv.updated_at) }}</span>
          <span class="delete-btn" title="删除会话" @click.stop="deleteConversation(conv.id)">&times;</span>
        </div>
        <div v-if="!conversations.length" class="text-center text-xs text-surface-400 py-8">
          暂无对话记录
        </div>
      </div>
    </aside>

    <!-- ===== 右侧：对话区域 ===== -->
    <main class="flex-1 min-w-0 flex flex-col">
      <!-- 顶栏 -->
      <div class="h-14 px-5 border-b border-surface-200 flex items-center justify-between">
        <div>
          <p class="text-sm font-semibold text-surface-900">
            {{ currentKbName || 'RAG 知识问答' }}
          </p>
          <p class="text-xs text-surface-400">基于知识库的智能检索问答</p>
        </div>
        <div class="flex items-center gap-2">
          <span v-if="retrieving" class="retrieval-badge">
            <span class="retrieval-dot"></span>
            正在检索知识库...
          </span>
          <span v-if="contextInfo" class="context-badge">
            检索到 {{ contextInfo.count }} 条相关内容
          </span>
        </div>
      </div>

      <!-- 消息列表 -->
      <div ref="messagesRef" class="flex-1 overflow-auto px-6 py-5">
        <!-- 空状态 -->
        <div v-if="!messages.length" class="h-full flex flex-col items-center justify-center text-center">
          <div class="empty-avatar">
            <span class="text-xl">KB</span>
          </div>
          <p class="text-lg font-semibold text-surface-900 mb-1">知识库智能问答</p>
          <p class="text-sm text-surface-400 mb-5">
            {{ selectedKbId ? '已选择知识库，可以开始提问' : '请先选择知识库，或直接提问进行通用对话' }}
          </p>
          <div class="flex flex-wrap justify-center gap-2 max-w-lg">
            <button
              v-for="tip in quickTips"
              :key="tip"
              class="quick-tip"
              @click="inputText = tip"
            >{{ tip }}</button>
          </div>
        </div>

        <!-- 消息流 -->
        <div v-else class="space-y-5">
          <div v-for="msg in messages" :key="msg.id === streamingMsgId ? `s-${msg.id}` : `d-${msg.id}`">
            <!-- 用户消息 -->
            <div v-if="msg.role === 'user'" class="flex justify-end">
              <div class="user-bubble">
                {{ msg.content }}
              </div>
            </div>
            <!-- AI 消息 -->
            <div v-else class="flex justify-start gap-2.5">
              <div class="ai-avatar">
                <span class="text-xs font-bold">KB</span>
              </div>
              <div class="ai-bubble">
                <!-- 流式输出中：纯文本 + 光标 -->
                <div v-if="msg.id === streamingMsgId" class="streaming-text">{{ msg.content }}<span class="cursor-blink">|</span></div>
                <!-- 流结束后：Markdown 渲染 -->
                <div v-else class="prose prose-sm max-w-none" v-html="renderMarkdown(msg.content)"></div>
                <!-- 来源标签 -->
                <div v-if="msg.sources && msg.sources.length && msg.id !== streamingMsgId" class="flex flex-wrap gap-1.5 mt-2 pt-2 border-t border-surface-100">
                  <span v-for="s in msg.sources" :key="s" class="source-tag">{{ s }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 思考状态：等待首个 chunk -->
          <div v-if="sending && (!streamingMsgId || !messages.find(m => m.id === streamingMsgId)?.content)" class="flex items-center gap-2.5">
            <div class="ai-avatar">
              <span class="text-xs font-bold">KB</span>
            </div>
            <div class="thinking-dots">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="border-t border-surface-200 p-4 bg-white">
        <div class="flex items-end gap-3 bg-surface-50 border border-surface-200 rounded-2xl px-4 py-3">
          <textarea
            v-model="inputText"
            rows="1"
            class="flex-1 bg-transparent resize-none outline-none text-sm text-surface-800 max-h-32"
            placeholder="输入问题，基于知识库进行智能检索..."
            @keydown.enter.exact.prevent="sendMessage"
          />
          <button class="send-btn" :disabled="!inputText.trim() || sending" @click="sendMessage">发送</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, ref, computed } from 'vue'
import { Select, message } from 'ant-design-vue'
import { marked } from 'marked'
import dayjs from 'dayjs'
import {
  ragApi,
  type KnowledgeBase,
  type Conversation,
  type Message as ApiMessage,
} from '@/api/agent/index'

const SelectOption = Select.Option

// ============ 类型 ============

interface DisplayMessage {
  id: number
  role: 'user' | 'assistant'
  content: string
  sources?: string[]
  created_at?: string
}

// ============ 状态 ============

const knowledgeBases = ref<KnowledgeBase[]>([])
const kbLoading = ref(false)
const selectedKbId = ref<number | undefined>(undefined)

const conversations = ref<Conversation[]>([])
const currentConversationId = ref<number | null>(null)
const messages = ref<DisplayMessage[]>([])
const inputText = ref('')
const sending = ref(false)
const retrieving = ref(false)
const contextInfo = ref<{ count: number; sources: string[] } | null>(null)
const messagesRef = ref<HTMLElement | null>(null)
const streamingMsgId = ref<number | null>(null)

const quickTips = [
  '这个知识库包含哪些内容？',
  '帮我总结一下核心要点',
  '有哪些常见问题和解答？',
  '解释一下相关的技术原理',
]

// ============ 计算属性 ============

const currentKbName = computed(() => {
  if (!selectedKbId.value) return ''
  const kb = knowledgeBases.value.find((k) => k.id === selectedKbId.value)
  return kb ? kb.name : ''
})

// ============ 工具方法 ============

const renderMarkdown = (content: string) => {
  return marked.parse(content || '') as string
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}

const formatTime = (timeStr: string) => {
  if (!timeStr) return ''
  const d = dayjs(timeStr)
  const now = dayjs()
  if (d.isSame(now, 'day')) return d.format('HH:mm')
  if (d.isSame(now.subtract(1, 'day'), 'day')) return '昨天'
  return d.format('MM/DD')
}

// ============ 知识库管理 ============

const loadKnowledgeBases = async () => {
  kbLoading.value = true
  try {
    const data = await ragApi.getKnowledgeBases()
    knowledgeBases.value = Array.isArray(data) ? data : []
  } catch {
    knowledgeBases.value = []
  } finally {
    kbLoading.value = false
  }
}

const onKbChange = async (val: number | undefined) => {
  selectedKbId.value = val
  currentConversationId.value = null
  messages.value = []
  contextInfo.value = null
  await loadConversations()
}

// ============ 对话管理 ============

const loadConversations = async () => {
  try {
    const data = await ragApi.getConversations(selectedKbId.value)
    conversations.value = Array.isArray(data) ? data : []
  } catch {
    conversations.value = []
  }
}

const openConversation = async (id: number) => {
  currentConversationId.value = id
  contextInfo.value = null
  try {
    const detail = await ragApi.getConversation(id)
    messages.value = (detail.messages || []).map((m: ApiMessage) => ({
      id: m.id,
      role: m.role === 'system' ? 'assistant' : m.role,
      content: m.content,
      sources: m.sources,
      created_at: m.created_at,
    })) as DisplayMessage[]
    await scrollToBottom()
  } catch {
    messages.value = []
    message.error('加载对话失败')
  }
}

const startNewChat = () => {
  currentConversationId.value = null
  messages.value = []
  inputText.value = ''
  contextInfo.value = null
  retrieving.value = false
}

const deleteConversation = async (id: number) => {
  try {
    await ragApi.deleteConversation(id)
    conversations.value = conversations.value.filter((c) => c.id !== id)
    if (currentConversationId.value === id) {
      currentConversationId.value = null
      messages.value = []
    }
    message.success('已删除')
  } catch {
    message.error('删除失败')
  }
}

// ============ 发送消息（SSE 流式） ============

const sendMessage = async () => {
  const text = inputText.value.trim()
  if (!text || sending.value) return

  messages.value.push({ id: Date.now(), role: 'user', content: text })
  inputText.value = ''
  sending.value = true
  retrieving.value = false
  contextInfo.value = null
  await scrollToBottom()

  // 预创建 AI 消息占位
  const aiMsgId = Date.now() + 1
  messages.value.push({ id: aiMsgId, role: 'assistant', content: '', sources: [] })
  streamingMsgId.value = aiMsgId

  await ragApi.chatStream(
    {
      message: text,
      kb_id: selectedKbId.value,
      conversation_id: currentConversationId.value || undefined,
    },
    {
      onRetrieving() {
        retrieving.value = true
      },

      onContext(info: { count: number; sources: string[] }) {
        retrieving.value = false
        contextInfo.value = info
        // 将来源信息附加到 AI 消息
        const aiMsg = messages.value.find((m) => m.id === aiMsgId)
        if (aiMsg) {
          aiMsg.sources = info.sources
        }
      },

      onChunk(chunk: string) {
        retrieving.value = false
        const aiMsg = messages.value.find((m) => m.id === aiMsgId)
        if (aiMsg) {
          aiMsg.content += chunk
          scrollToBottom()
        }
      },

      onDone(info: { conversation_id: number; sources: string[]; retrieved_chunks: number }) {
        if (info.conversation_id) {
          currentConversationId.value = info.conversation_id
        }
        const aiMsg = messages.value.find((m) => m.id === aiMsgId)
        if (aiMsg) {
          if (info.sources && info.sources.length) {
            aiMsg.sources = info.sources
          }
          if (!aiMsg.content) {
            messages.value = messages.value.filter((m) => m.id !== aiMsgId)
          }
        }
        streamingMsgId.value = null
        messages.value = [...messages.value]
        sending.value = false
        retrieving.value = false
        loadConversations()
        nextTick(() => scrollToBottom())
      },

      onError(error: string) {
        const idx = messages.value.findIndex((m) => m.id === aiMsgId)
        if (idx !== -1) {
          messages.value[idx] = { ...messages.value[idx], content: `请求失败：${error}` }
        }
        streamingMsgId.value = null
        messages.value = [...messages.value]
        sending.value = false
        retrieving.value = false
        message.error('对话请求失败')
        nextTick(() => scrollToBottom())
      },
    },
  )
}

// ============ 初始化 ============

onMounted(async () => {
  await loadKnowledgeBases()
  await loadConversations()
})
</script>

<style scoped>
.rag-chat-page {
  height: calc(100vh - 96px);
  min-height: 540px;
  overflow: hidden;
  border-radius: 14px;
  border: 1px solid #f1f5f9;
}

/* ===== 左侧面板 ===== */
.aside-panel {
  width: 280px;
  border-right: 1px solid #e2e8f0;
  background: #fffbf0;
}

.aside-header {
  padding: 14px 12px 10px;
  border-bottom: 1px solid #fde68a;
}

.kb-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
}
.kb-dot-active {
  background: #22c55e;
}
.kb-dot-inactive {
  background: #d1d5db;
}
.kb-doc-count {
  font-size: 11px;
  color: #94a3b8;
  margin-left: 2px;
}

.new-chat-btn {
  width: 100%;
  border: 1px solid #fde68a;
  background: #fef9ee;
  color: #92400e;
  border-radius: 10px;
  padding: 9px 12px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}
.new-chat-btn:hover {
  background: #fef3c7;
  border-color: #fbbf24;
}

/* 对话列表 */
.conversation-item {
  width: 100%;
  display: flex;
  align-items: center;
  text-align: left;
  border: 1px solid transparent;
  background: transparent;
  border-radius: 10px;
  padding: 9px 10px;
  font-size: 13px;
  color: #475569;
  cursor: pointer;
  transition: all 0.15s;
}
.conversation-item:hover {
  background: #fefce8;
}
.conversation-item.active {
  background: #fef3c7;
  color: #92400e;
  border-color: #fde68a;
}

.conv-time {
  font-size: 10px;
  color: #94a3b8;
  flex-shrink: 0;
  margin-left: 6px;
}

.delete-btn {
  display: none;
  flex-shrink: 0;
  width: 22px;
  height: 22px;
  line-height: 20px;
  text-align: center;
  border-radius: 6px;
  font-size: 16px;
  color: #94a3b8;
  cursor: pointer;
  margin-left: 2px;
}
.delete-btn:hover {
  background: #fee2e2;
  color: #dc2626;
}
.conversation-item:hover .delete-btn {
  display: inline-block;
}
.conversation-item:hover .conv-time {
  display: none;
}

/* ===== 顶栏状态徽章 ===== */
.retrieval-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #fef3c7;
  border: 1px solid #fde68a;
  border-radius: 6px;
  padding: 3px 10px;
  font-size: 11px;
  color: #92400e;
  font-weight: 500;
}
.retrieval-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #f59e0b;
  animation: pulse-dot 1s infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.context-badge {
  display: inline-flex;
  align-items: center;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 6px;
  padding: 3px 10px;
  font-size: 11px;
  color: #16a34a;
  font-weight: 500;
}

/* ===== 空状态 ===== */
.empty-avatar {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  background: #fef3c7;
  color: #b45309;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
  font-weight: 700;
}

.quick-tip {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 12px;
  color: #92400e;
  cursor: pointer;
  transition: all 0.15s;
}
.quick-tip:hover {
  background: #fef3c7;
  border-color: #fbbf24;
  color: #78350f;
}

/* ===== 消息气泡 ===== */
.user-bubble {
  max-width: 72%;
  background: #f59e0b;
  color: #fff;
  padding: 10px 16px;
  border-radius: 16px;
  border-bottom-right-radius: 6px;
  font-size: 14px;
  white-space: pre-wrap;
  line-height: 1.6;
}

.ai-avatar {
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: #fef3c7;
  color: #b45309;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
}

.ai-bubble {
  max-width: 78%;
  background: #fff;
  border: 1px solid #e2e8f0;
  padding: 12px 16px;
  border-radius: 16px;
  border-bottom-left-radius: 6px;
  font-size: 14px;
  color: #334155;
}

/* 来源标签 */
.source-tag {
  display: inline-block;
  background: #f0fdf4;
  color: #16a34a;
  border: 1px solid #bbf7d0;
  border-radius: 4px;
  padding: 1px 6px;
  font-size: 11px;
}

/* ===== 思考动画 ===== */
.thinking-dots {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 16px;
  border-bottom-left-radius: 4px;
}
.thinking-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #f59e0b;
  animation: thinking 1.2s infinite;
}
.thinking-dots span:nth-child(2) { animation-delay: 0.2s; }
.thinking-dots span:nth-child(3) { animation-delay: 0.4s; }
@keyframes thinking {
  0%, 60%, 100% { transform: translateY(0); opacity: 0.4; }
  30% { transform: translateY(-4px); opacity: 1; }
}

/* ===== 流式输出 ===== */
.streaming-text {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.65;
}
.cursor-blink {
  display: inline;
  color: #f59e0b;
  animation: blink 0.8s step-end infinite;
  font-weight: 300;
}
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* ===== 发送按钮 ===== */
.send-btn {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.15s;
}
.send-btn:hover {
  opacity: 0.9;
}
.send-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

/* ===== 响应式 ===== */
@media (max-width: 900px) {
  .rag-chat-page {
    height: calc(100vh - 96px);
    min-height: 480px;
  }
  .aside-panel {
    width: 220px;
  }
}

/* ===== Markdown prose 样式 ===== */
.prose :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 10px 0;
  font-size: 13px;
}
.prose :deep(thead) {
  background: #fffbeb;
}
.prose :deep(th) {
  padding: 8px 12px;
  text-align: left;
  font-weight: 600;
  color: #334155;
  border-bottom: 2px solid #fde68a;
  white-space: nowrap;
}
.prose :deep(td) {
  padding: 7px 12px;
  border-bottom: 1px solid #f1f5f9;
  color: #475569;
}
.prose :deep(tr:hover td) {
  background: #fffbeb;
}
.prose :deep(code) {
  background: #fef3c7;
  color: #92400e;
  padding: 1px 5px;
  border-radius: 4px;
  font-size: 12px;
  font-family: 'Menlo', 'Monaco', 'Consolas', monospace;
}
.prose :deep(pre) {
  background: #1e293b;
  color: #e2e8f0;
  padding: 14px 16px;
  border-radius: 10px;
  overflow-x: auto;
  margin: 10px 0;
  font-size: 12px;
  line-height: 1.6;
}
.prose :deep(pre code) {
  background: none;
  color: inherit;
  padding: 0;
  font-size: inherit;
}
.prose :deep(ul),
.prose :deep(ol) {
  padding-left: 1.4em;
  margin: 6px 0;
}
.prose :deep(li) {
  margin: 3px 0;
  line-height: 1.6;
}
.prose :deep(p) {
  margin: 6px 0;
  line-height: 1.65;
}
.prose :deep(strong) {
  font-weight: 600;
  color: #1e293b;
}
.prose :deep(h1),
.prose :deep(h2),
.prose :deep(h3),
.prose :deep(h4) {
  font-weight: 600;
  color: #0f172a;
  margin: 12px 0 6px;
  line-height: 1.4;
}
.prose :deep(h3) { font-size: 15px; }
.prose :deep(h4) { font-size: 14px; }
.prose :deep(blockquote) {
  border-left: 3px solid #fde68a;
  padding-left: 12px;
  margin: 8px 0;
  color: #92400e;
  font-style: italic;
}
.prose :deep(hr) {
  border: none;
  border-top: 1px solid #e2e8f0;
  margin: 12px 0;
}
.prose :deep(a) {
  color: #d97706;
  text-decoration: none;
}
.prose :deep(a:hover) {
  text-decoration: underline;
}
</style>
