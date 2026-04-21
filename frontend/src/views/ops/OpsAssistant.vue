<template>
  <div class="ops-assistant-page bg-white flex">
    <!-- 左侧对话历史 -->
    <aside class="w-72 border-r border-surface-200 bg-surface-50/60 flex flex-col shrink-0">
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
          <span class="truncate flex-1">{{ conv.title || `对话 ${conv.id}` }}</span>
          <button
            class="del-btn"
            @click.stop="deleteConversation(conv.id)"
            title="删除对话"
          >×</button>
        </div>

        <div v-if="!conversations.length" class="text-xs text-surface-400 text-center py-8">
          暂无对话历史
        </div>
      </div>
    </aside>

    <!-- 右侧对话区 -->
    <main class="flex-1 min-w-0 flex flex-col">
      <!-- 顶部标题栏 -->
      <div class="h-14 px-5 border-b border-surface-200 flex items-center justify-between">
        <div>
          <p class="text-sm font-semibold text-surface-900">运维 AI 助手</p>
          <p class="text-xs text-surface-400">通过自然语言管理服务器、脚本、定时任务和执行日志</p>
        </div>
        <div class="flex items-center gap-2">
          <span
            v-if="streamMode"
            class="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full"
          >流式</span>
          <span
            v-if="toolCallingName"
            class="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full animate-pulse"
          >🔧 {{ toolCallingName }}</span>
        </div>
      </div>

      <!-- 消息列表 -->
      <div ref="messagesRef" class="flex-1 overflow-auto px-6 py-5">
        <!-- 空状态引导 -->
        <div v-if="!messages.length" class="h-full flex flex-col items-center justify-center text-center">
          <div class="w-16 h-16 rounded-2xl bg-green-100 flex items-center justify-center mb-4">
            <span class="text-green-600 text-2xl">🤖</span>
          </div>
          <p class="text-lg font-semibold text-surface-900">你好，我是运维助手</p>
          <p class="text-sm text-surface-400 mt-1 max-w-md">
            可以问我：查看服务器列表、查询失败的任务、执行脚本、创建定时任务等
          </p>
          <div class="mt-6 flex flex-wrap gap-2 justify-center">
            <button
              v-for="tip in quickTips"
              :key="tip"
              class="tip-btn"
              @click="sendQuickMessage(tip)"
            >{{ tip }}</button>
          </div>
        </div>

        <!-- 消息列表 -->
        <div v-else class="space-y-5 pb-2">
          <div v-for="(msg, idx) in messages" :key="idx">
            <!-- 用户消息 -->
            <div v-if="msg.role === 'user'" class="flex justify-end">
              <div class="max-w-[72%] bg-green-500 text-white px-4 py-2.5 rounded-2xl rounded-br-md text-sm">
                {{ msg.content }}
              </div>
            </div>

            <!-- AI 消息 -->
            <div v-else class="flex justify-start gap-3">
              <div class="w-8 h-8 rounded-xl bg-green-100 flex items-center justify-center shrink-0 mt-0.5">
                <span class="text-green-600 text-sm">AI</span>
              </div>
              <div class="max-w-[78%]">
                <div
                  class="bg-white border border-surface-200 px-4 py-3 rounded-2xl rounded-bl-md text-sm text-surface-800 prose prose-sm max-w-none"
                  v-html="renderMarkdown(msg.content)"
                ></div>

                <!-- 来源标签 -->
                <div v-if="msg.sources && msg.sources.length" class="flex flex-wrap gap-1 mt-1.5">
                  <span
                    v-for="src in msg.sources"
                    :key="src"
                    class="text-xs bg-surface-100 text-surface-500 px-2 py-0.5 rounded-full"
                  >{{ src }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 发送中状态 -->
          <div v-if="sending" class="flex justify-start gap-3">
            <div class="w-8 h-8 rounded-xl bg-green-100 flex items-center justify-center shrink-0">
              <span class="text-green-600 text-sm">AI</span>
            </div>
            <div class="bg-white border border-surface-200 px-4 py-3 rounded-2xl rounded-bl-md text-sm text-surface-400">
              <span v-if="toolCallingName">🔧 正在调用工具：{{ toolCallingName }}...</span>
              <span v-else class="thinking-dots">正在思考</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="border-t border-surface-200 p-4 bg-white">
        <div class="flex items-end gap-3 bg-surface-50 border border-surface-200 rounded-2xl px-4 py-3">
          <textarea
            v-model="inputText"
            rows="1"
            class="flex-1 bg-transparent resize-none outline-none text-sm text-surface-800 max-h-32"
            placeholder="描述你想做的运维操作，或查询服务器、任务、日志信息..."
            @keydown.enter.exact.prevent="handleSend"
          />
          <div class="flex items-center gap-2 shrink-0">
            <button
              class="stream-toggle"
              :class="{ active: streamMode }"
              @click="streamMode = !streamMode"
              title="流式输出"
            >流</button>
            <button
              class="send-btn"
              :disabled="!inputText.trim() || sending"
              @click="handleSend"
            >发送</button>
          </div>
        </div>
      </div>
    </main>

    <!-- 写操作确认弹窗 -->
    <a-modal
      v-model:open="confirmModalVisible"
      title="⚠️ 确认执行操作"
      :ok-text="'确认执行'"
      :cancel-text="'取消'"
      :ok-button-props="{ danger: true }"
      :confirm-loading="confirming"
      @ok="handleConfirmAction"
      @cancel="handleCancelAction"
    >
      <div class="confirm-modal-body">
        <p class="text-sm text-surface-500 mb-3">AI 计划执行以下操作，请确认：</p>
        <div
          class="bg-surface-50 border border-surface-200 rounded-xl p-4 text-sm prose prose-sm max-w-none"
          v-html="renderMarkdown(pendingAction?.description || '')"
        ></div>
        <p class="text-xs text-amber-600 mt-3">
          ⚠️ 此操作将在真实环境中执行，请仔细核对后再确认。
        </p>
      </div>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue'
import { marked } from 'marked'
import { Modal, message as antMessage } from 'ant-design-vue'
import { opsAiApi, type OpsConversation, type OpsMessage, type PendingAction } from '@/api/ops/ai'

// ============ 状态 ============

const conversations = ref<OpsConversation[]>([])
const currentConversationId = ref<number | null>(null)
const messages = ref<Array<OpsMessage & { sources?: string[] }>>([])
const inputText = ref('')
const sending = ref(false)
const streamMode = ref(true) // 默认开启流式输出
const toolCallingName = ref<string | null>(null)
const messagesRef = ref<HTMLElement | null>(null)

// 写操作确认弹窗
const confirmModalVisible = ref(false)
const confirming = ref(false)
const pendingAction = ref<(PendingAction & { conversation_id: number }) | null>(null)

// 快捷提示
const quickTips = [
  '查看所有在线服务器',
  '查询最近失败的任务',
  '列出所有启用的定时任务',
  '每天18:30 转成 cron 表达式',
  '最近10条执行日志',
]

// ============ 工具函数 ============

const renderMarkdown = (content: string): string => {
  try {
    return marked.parse(content || '') as string
  } catch {
    return content || ''
  }
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
    const data = await opsAiApi.getConversations()
    conversations.value = Array.isArray(data) ? data : []
  } catch {
    conversations.value = []
  }
}

const openConversation = async (id: number) => {
  currentConversationId.value = id
  try {
    const detail = await opsAiApi.getConversation(id)
    messages.value = (detail.messages || []).map((m) => ({
      id: m.id,
      role: m.role,
      content: m.content,
      sources: m.sources || [],
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
  toolCallingName.value = null
}

const deleteConversation = async (id: number) => {
  try {
    await opsAiApi.deleteConversation(id)
    if (currentConversationId.value === id) {
      startNewChat()
    }
    await loadConversations()
  } catch {
    antMessage.error('删除失败')
  }
}

// ============ 发送消息 ============

const handleSend = () => {
  if (streamMode.value) {
    sendMessageStream()
  } else {
    sendMessage()
  }
}

const sendQuickMessage = (tip: string) => {
  inputText.value = tip
  handleSend()
}

// 非流式发送
const sendMessage = async () => {
  const text = inputText.value.trim()
  if (!text || sending.value) return

  messages.value.push({ id: Date.now(), role: 'user', content: text })
  inputText.value = ''
  sending.value = true
  await scrollToBottom()

  try {
    const result = await opsAiApi.chat({
      message: text,
      conversation_id: currentConversationId.value || undefined,
    })

    if (result.conversation_id) {
      currentConversationId.value = result.conversation_id
    }

    // 处理写操作待确认
    if (result.pending_action) {
      pendingAction.value = {
        ...result.pending_action,
        conversation_id: result.conversation_id,
      }
      confirmModalVisible.value = true
    }

    messages.value.push({
      id: Date.now() + 1,
      role: 'assistant',
      content: result.answer,
      sources: result.sources,
    })

    await loadConversations()
  } catch (err: any) {
    const detail = err?.response?.data?.detail || err?.message || 'AI 服务暂时不可用'
    messages.value.push({
      id: Date.now() + 2,
      role: 'assistant',
      content: `❌ ${detail}`,
    })
  } finally {
    sending.value = false
    await scrollToBottom()
  }
}

// 流式发送
const sendMessageStream = async () => {
  const text = inputText.value.trim()
  if (!text || sending.value) return

  messages.value.push({ id: Date.now(), role: 'user', content: text })
  inputText.value = ''
  sending.value = true
  toolCallingName.value = null
  await scrollToBottom()

  // 预先添加一个空的 AI 消息，后续追加内容
  const aiMsgId = Date.now() + 1
  messages.value.push({ id: aiMsgId, role: 'assistant', content: '' })
  const aiMsgIndex = messages.value.length - 1

  let conversationId = currentConversationId.value || undefined

  await opsAiApi.chatStream(
    { message: text, conversation_id: conversationId },
    {
      onChunk: async (chunk: string) => {
        messages.value[aiMsgIndex].content += chunk
        await scrollToBottom()
      },
      onToolCall: (toolName: string) => {
        toolCallingName.value = toolName
      },
      onPendingAction: (action) => {
        conversationId = action.conversation_id
        currentConversationId.value = action.conversation_id
        pendingAction.value = action
        confirmModalVisible.value = true
      },
      onDone: async (convId?: number) => {
        if (convId) {
          currentConversationId.value = convId
        }
        toolCallingName.value = null
        sending.value = false
        await loadConversations()
        await scrollToBottom()
      },
      onError: async (error: string) => {
        messages.value[aiMsgIndex].content = `❌ ${error}`
        toolCallingName.value = null
        sending.value = false
        await scrollToBottom()
      },
    },
  )
}

// ============ 写操作确认 ============

const handleConfirmAction = async () => {
  if (!pendingAction.value) return

  confirming.value = true
  try {
    const result = await opsAiApi.confirm({
      tool_name: pendingAction.value.tool_name,
      tool_args: pendingAction.value.tool_args,
      conversation_id: pendingAction.value.conversation_id,
    })

    messages.value.push({
      id: Date.now(),
      role: 'assistant',
      content: result.answer,
      sources: ['用户确认执行'],
    })

    currentConversationId.value = result.conversation_id
    confirmModalVisible.value = false
    pendingAction.value = null
    await loadConversations()
    await scrollToBottom()
  } catch (err: any) {
    antMessage.error(err?.response?.data?.detail || '执行失败')
  } finally {
    confirming.value = false
  }
}

const handleCancelAction = () => {
  confirmModalVisible.value = false
  pendingAction.value = null

  // 告知 AI 用户取消了操作
  messages.value.push({
    id: Date.now(),
    role: 'assistant',
    content: '好的，操作已取消。如需重新执行，请再次告诉我。',
  })
}

// ============ 生命周期 ============

onMounted(async () => {
  await loadConversations()
})
</script>

<style scoped>
.ops-assistant-page {
  height: calc(100vh - 96px);
  min-height: 540px;
  overflow: hidden;
  border-radius: 14px;
  border: 1px solid #f1f5f9;
}

.new-chat-btn {
  border: 1px solid #bbf7d0;
  background: #f0fdf4;
  color: #15803d;
  border-radius: 10px;
  padding: 10px 12px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.new-chat-btn:hover {
  background: #dcfce7;
}

.conversation-item {
  display: flex;
  align-items: center;
  width: 100%;
  text-align: left;
  border: 1px solid transparent;
  background: transparent;
  border-radius: 10px;
  padding: 9px 10px;
  font-size: 13px;
  color: #475569;
  cursor: pointer;
  gap: 6px;
}

.conversation-item:hover {
  background: #f8fafc;
}

.conversation-item.active {
  background: #f0fdf4;
  color: #15803d;
  border-color: #bbf7d0;
}

.del-btn {
  opacity: 0;
  color: #94a3b8;
  font-size: 15px;
  line-height: 1;
  padding: 1px 4px;
  border-radius: 4px;
  transition: all 0.1s;
  background: transparent;
  border: none;
  cursor: pointer;
}

.conversation-item:hover .del-btn {
  opacity: 1;
}

.del-btn:hover {
  background: #fee2e2;
  color: #dc2626;
}

.tip-btn {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #15803d;
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s;
}

.tip-btn:hover {
  background: #dcfce7;
  border-color: #86efac;
}

.send-btn {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.send-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.send-btn:not(:disabled):hover {
  background: linear-gradient(135deg, #16a34a, #15803d);
}

.stream-toggle {
  background: transparent;
  border: 1px solid #e2e8f0;
  color: #94a3b8;
  border-radius: 8px;
  padding: 6px 10px;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s;
}

.stream-toggle.active {
  background: #f0fdf4;
  border-color: #86efac;
  color: #15803d;
}

.confirm-modal-body {
  padding: 4px 0;
}

/* 思考中动画 */
.thinking-dots::after {
  content: '...';
  animation: dots 1.2s steps(3, end) infinite;
}

@keyframes dots {
  0%,
  20% {
    color: rgba(0, 0, 0, 0);
    text-shadow: 0.25em 0 0 rgba(0,0,0,0), 0.5em 0 0 rgba(0,0,0,0);
  }
  40% {
    color: #94a3b8;
    text-shadow: 0.25em 0 0 rgba(0,0,0,0), 0.5em 0 0 rgba(0,0,0,0);
  }
  60% {
    text-shadow: 0.25em 0 0 #94a3b8, 0.5em 0 0 rgba(0,0,0,0);
  }
  80%,
  100% {
    text-shadow: 0.25em 0 0 #94a3b8, 0.5em 0 0 #94a3b8;
  }
}

/* prose 样式调整 */
:deep(.prose) {
  font-size: 13px;
  line-height: 1.6;
}

:deep(.prose p) {
  margin: 0.4em 0;
}

:deep(.prose ul),
:deep(.prose ol) {
  margin: 0.4em 0;
  padding-left: 1.4em;
}

:deep(.prose pre) {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 12px;
  overflow-x: auto;
}

:deep(.prose code) {
  background: #f1f5f9;
  border-radius: 4px;
  padding: 1px 5px;
  font-size: 12px;
}

:deep(.prose pre code) {
  background: transparent;
  padding: 0;
}

:deep(.prose h1),
:deep(.prose h2),
:deep(.prose h3) {
  margin: 0.6em 0 0.3em;
  font-weight: 600;
}

:deep(.prose table) {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

:deep(.prose th),
:deep(.prose td) {
  border: 1px solid #e2e8f0;
  padding: 6px 10px;
}

:deep(.prose th) {
  background: #f8fafc;
  font-weight: 600;
}
</style>
