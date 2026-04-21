<template>
  <div class="assistant-page bg-white flex">
    <!-- ===== 左侧：对话列表 ===== -->
    <aside class="w-80 border-r border-surface-200 bg-surface-50/60 flex flex-col">
      <div class="p-4 border-b border-surface-200">
        <button class="w-full new-chat-btn" @click="startNewChat">+ 新对话</button>
      </div>

      <div class="flex-1 overflow-auto px-2 py-3 space-y-1">
        <div
          v-for="conv in conversations"
          :key="conv.id"
          class="conversation-item"
          :class="{ active: currentConversationId === conv.id }"
          @click="openConversation(conv.id)"
        >
          <span class="truncate flex-1">{{ conv.title || `会话 ${conv.id}` }}</span>
          <span class="delete-btn" title="删除会话" @click.stop="deleteConversation(conv.id)">×</span>
        </div>
        <div v-if="!conversations.length" class="text-center text-xs text-surface-400 py-8">
          暂无对话记录
        </div>
      </div>
    </aside>

    <!-- ===== 右侧：对话区域 ===== -->
    <main class="flex-1 min-w-0 flex flex-col">
      <div class="h-14 px-5 border-b border-surface-200 flex items-center justify-between">
        <div>
          <p class="text-sm font-semibold text-surface-900">AI 助手</p>
          <p class="text-xs text-surface-400">可查询服务器、脚本、任务、日志等系统数据</p>
        </div>
        <div class="flex items-center gap-2">
          <span v-if="activeToolName" class="tool-badge">
            <span class="tool-dot"></span>
            {{ activeToolName }}
          </span>
        </div>
      </div>

      <!-- 消息列表 -->
      <div ref="messagesRef" class="flex-1 overflow-auto px-6 py-5">
        <!-- 空状态：快捷提示 -->
        <div v-if="!messages.length" class="h-full flex flex-col items-center justify-center text-center">
          <div class="w-14 h-14 rounded-2xl bg-brand-100 flex items-center justify-center mb-4">
            <span class="text-brand-600 text-xl">AI</span>
          </div>
          <p class="text-lg font-semibold text-surface-900 mb-1">你好，我是系统助手</p>
          <p class="text-sm text-surface-400 mb-5">我可以查询系统数据、执行运维操作，也可以回答平台使用问题</p>
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
          <div v-for="(msg, idx) in messages" :key="msg.id === streamingMsgId ? `s-${msg.id}` : `d-${msg.id}`">
            <!-- 用户消息 -->
            <div v-if="msg.role === 'user'" class="flex justify-end">
              <div class="max-w-[72%] bg-brand-500 text-white px-4 py-2.5 rounded-2xl rounded-br-md text-sm whitespace-pre-wrap">
                {{ msg.content }}
              </div>
            </div>
            <!-- AI 消息 -->
            <div v-else class="flex justify-start gap-2.5">
              <div class="w-7 h-7 rounded-lg bg-brand-100 flex items-center justify-center flex-shrink-0 mt-0.5">
                <span class="text-brand-600 text-xs font-bold">AI</span>
              </div>
              <div class="max-w-[78%] bg-white border border-surface-200 px-4 py-3 rounded-2xl rounded-bl-md text-sm text-surface-800">
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

          <!-- 思考状态：仅在等待首个 chunk 时显示 -->
          <div v-if="sending && (!streamingMsgId || !messages.find(m => m.id === streamingMsgId)?.content)" class="flex items-center gap-2.5">
            <div class="w-7 h-7 rounded-lg bg-brand-100 flex items-center justify-center flex-shrink-0">
              <span class="text-brand-600 text-xs font-bold">AI</span>
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
            placeholder="输入问题，如：查看所有在线服务器、最近失败的任务..."
            @keydown.enter.exact.prevent="sendMessage"
          />
          <button class="send-btn" :disabled="!inputText.trim() || sending" @click="sendMessage">发送</button>
        </div>
      </div>
    </main>

    <!-- ===== 写操作确认弹窗 ===== -->
    <div v-if="pendingAction" class="modal-overlay" @click.self="cancelPendingAction">
      <div class="modal-card">
        <div class="modal-header">
          <span class="text-sm font-semibold text-surface-900">操作确认</span>
          <button class="modal-close" @click="cancelPendingAction">×</button>
        </div>
        <div class="modal-body prose prose-sm max-w-none" v-html="renderMarkdown(pendingAction.description)"></div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="cancelPendingAction">取消</button>
          <button class="confirm-btn" :disabled="confirming" @click="confirmAction">
            {{ confirming ? '执行中...' : '确认执行' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue'
import { marked } from 'marked'
import {
  assistantApi,
  type AssistantConversation,
  type AssistantMessage,
  type PendingAction,
} from '@/api/assistant'

// ============ 状态 ============

const conversations = ref<AssistantConversation[]>([])
const currentConversationId = ref<number | null>(null)
const messages = ref<AssistantMessage[]>([])
const inputText = ref('')
const sending = ref(false)
const messagesRef = ref<HTMLElement | null>(null)
const activeToolName = ref('')
const pendingAction = ref<PendingAction | null>(null)
const confirming = ref(false)
const streamingMsgId = ref<number | null>(null)

const quickTips = [
  '查看所有在线服务器',
  '最近有哪些失败的任务',
  '查询所有定时任务',
  '查看脚本列表',
  '系统整体运行情况',
]

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

// ============ 对话管理 ============

const loadConversations = async () => {
  try {
    const data = await assistantApi.getConversations()
    conversations.value = Array.isArray(data) ? data : []
  } catch {
    conversations.value = []
  }
}

const openConversation = async (id: number) => {
  currentConversationId.value = id
  try {
    const detail = await assistantApi.getConversation(id)
    messages.value = (detail.messages || []).map((m) => ({
      id: m.id,
      role: m.role,
      content: m.content,
      sources: m.sources,
      created_at: m.created_at,
    }))
    await scrollToBottom()
  } catch {
    messages.value = []
  }
}

const startNewChat = () => {
  currentConversationId.value = null
  messages.value = []
  inputText.value = ''
  activeToolName.value = ''
}

const deleteConversation = async (id: number) => {
  try {
    await assistantApi.deleteConversation(id)
    conversations.value = conversations.value.filter((c) => c.id !== id)
    if (currentConversationId.value === id) {
      currentConversationId.value = null
      messages.value = []
    }
  } catch {
    // 静默处理
  }
}

// ============ 发送消息（SSE 流式） ============

const sendMessage = async () => {
  const text = inputText.value.trim()
  if (!text || sending.value) return

  messages.value.push({ id: Date.now(), role: 'user', content: text })
  inputText.value = ''
  sending.value = true
  activeToolName.value = ''
  await scrollToBottom()

  // 预创建 AI 消息占位，用于流式追加
  const aiMsgId = Date.now() + 1
  messages.value.push({ id: aiMsgId, role: 'assistant', content: '', sources: [] })
  streamingMsgId.value = aiMsgId

  await assistantApi.chatStream(
    {
      message: text,
      conversation_id: currentConversationId.value || undefined,
    },
    {
      onChunk(chunk: string) {
        const aiMsg = messages.value.find((m) => m.id === aiMsgId)
        if (aiMsg) {
          aiMsg.content += chunk
          scrollToBottom()
        }
      },

      onToolCall(toolName: string) {
        activeToolName.value = toolName
      },

      onPendingAction(action) {
        // 写操作：弹出确认框
        if (action.conversation_id) {
          currentConversationId.value = action.conversation_id
        }
        pendingAction.value = action
      },

      onDone(conversationId?: number) {
        if (conversationId) {
          currentConversationId.value = conversationId
        }
        const aiMsg = messages.value.find((m) => m.id === aiMsgId)
        if (aiMsg && !aiMsg.content) {
          messages.value = messages.value.filter((m) => m.id !== aiMsgId)
        }
        // 先清除流式标记，再强制替换数组引用触发 Vue 重新渲染
        streamingMsgId.value = null
        messages.value = [...messages.value]
        sending.value = false
        activeToolName.value = ''
        loadConversations()
        nextTick(() => scrollToBottom())
      },

      onError(error: string) {
        const idx = messages.value.findIndex((m) => m.id === aiMsgId)
        if (idx !== -1) {
          messages.value[idx] = { ...messages.value[idx], content: `AI 服务调用失败：${error}` }
        }
        streamingMsgId.value = null
        messages.value = [...messages.value]
        sending.value = false
        activeToolName.value = ''
        nextTick(() => scrollToBottom())
      },
    },
  )
}

// ============ 写操作确认 ============

const confirmAction = async () => {
  if (!pendingAction.value || confirming.value) return
  confirming.value = true

  try {
    const result = await assistantApi.confirm({
      tool_name: pendingAction.value.tool_name,
      tool_args: pendingAction.value.tool_args,
      conversation_id: currentConversationId.value!,
    })

    messages.value.push({
      id: Date.now(),
      role: 'assistant',
      content: result.answer,
      sources: ['用户确认执行'],
    })
  } catch (err: any) {
    messages.value.push({
      id: Date.now(),
      role: 'assistant',
      content: `操作执行失败：${err?.response?.data?.detail || err?.message || '未知错误'}`,
    })
  } finally {
    pendingAction.value = null
    confirming.value = false
    await scrollToBottom()
  }
}

const cancelPendingAction = () => {
  pendingAction.value = null
  messages.value.push({
    id: Date.now(),
    role: 'assistant',
    content: '操作已取消。',
  })
  scrollToBottom()
}

// ============ 初始化 ============

onMounted(async () => {
  await loadConversations()
})
</script>

<style scoped>
.assistant-page {
  height: calc(100vh - 96px);
  min-height: 540px;
  overflow: hidden;
  border-radius: 14px;
  border: 1px solid #f1f5f9;
}

.new-chat-btn {
  border: 1px solid #fbcfe8;
  background: #fff1f7;
  color: #9d174d;
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 13px;
  font-weight: 600;
}

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
}
.conversation-item:hover { background: #f8fafc; }
.conversation-item.active {
  background: #fdf2f8;
  color: #9d174d;
  border-color: #fbcfe8;
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
  margin-left: 4px;
}
.delete-btn:hover {
  background: #fee2e2;
  color: #dc2626;
}
.conversation-item:hover .delete-btn {
  display: inline-block;
}

/* 快捷提示 */
.quick-tip {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 12px;
  color: #64748b;
  cursor: pointer;
  transition: all 0.15s;
}
.quick-tip:hover {
  background: #fdf2f8;
  border-color: #fbcfe8;
  color: #9d174d;
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

/* 工具调用指示 */
.tool-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  border-radius: 6px;
  padding: 3px 10px;
  font-size: 11px;
  color: #2563eb;
  font-weight: 500;
}
.tool-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #3b82f6;
  animation: pulse-dot 1s infinite;
}
@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

/* 思考动画 */
.thinking-dots {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  border-bottom-left-radius: 4px;
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

/* 流式输出纯文本 */
.streaming-text {
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.65;
}
.cursor-blink {
  display: inline;
  color: #94a3b8;
  animation: blink 0.8s step-end infinite;
  font-weight: 300;
}
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

/* 发送按钮 */
.send-btn {
  background: linear-gradient(135deg, #ec4899, #db2777);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 600;
}
.send-btn:disabled { opacity: 0.45; cursor: not-allowed; }

/* 确认弹窗 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-card {
  background: #fff;
  border-radius: 14px;
  width: 520px;
  max-width: 90vw;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
}
.modal-close {
  background: none;
  border: none;
  font-size: 20px;
  color: #94a3b8;
  cursor: pointer;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
}
.modal-close:hover { background: #f1f5f9; color: #475569; }
.modal-body {
  padding: 20px;
  overflow: auto;
  flex: 1;
  font-size: 14px;
  color: #334155;
}
.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 16px 20px;
  border-top: 1px solid #f1f5f9;
}
.cancel-btn {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 13px;
  color: #475569;
  cursor: pointer;
}
.cancel-btn:hover { background: #f1f5f9; }
.confirm-btn {
  background: #dc2626;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  color: #fff;
  cursor: pointer;
}
.confirm-btn:hover { background: #b91c1c; }
.confirm-btn:disabled { opacity: 0.5; cursor: not-allowed; }

@media (max-width: 900px) {
  .assistant-page {
    height: calc(100vh - 96px);
    min-height: 480px;
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
  background: #f8fafc;
}
.prose :deep(th) {
  padding: 8px 12px;
  text-align: left;
  font-weight: 600;
  color: #334155;
  border-bottom: 2px solid #e2e8f0;
  white-space: nowrap;
}
.prose :deep(td) {
  padding: 7px 12px;
  border-bottom: 1px solid #f1f5f9;
  color: #475569;
}
.prose :deep(tr:hover td) {
  background: #f8fafc;
}
.prose :deep(code) {
  background: #f1f5f9;
  color: #be185d;
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
  border-left: 3px solid #e2e8f0;
  padding-left: 12px;
  margin: 8px 0;
  color: #64748b;
  font-style: italic;
}
.prose :deep(hr) {
  border: none;
  border-top: 1px solid #e2e8f0;
  margin: 12px 0;
}
.prose :deep(a) {
  color: #2563eb;
  text-decoration: none;
}
.prose :deep(a:hover) {
  text-decoration: underline;
}
</style>
