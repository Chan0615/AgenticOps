<template>
  <div class="h-[calc(100vh-64px)] bg-white flex">
    <aside class="w-80 border-r border-surface-200 bg-surface-50/60 flex flex-col">
      <div class="p-4 border-b border-surface-200">
        <button class="w-full new-chat-btn" @click="startNewChat">+ 新对话</button>
      </div>

      <div class="flex-1 overflow-auto px-2 py-3 space-y-1">
        <button
          v-for="conv in conversations"
          :key="conv.id"
          class="conversation-item"
          :class="{ active: currentConversationId === conv.id }"
          @click="openConversation(conv.id)"
        >
          <span class="truncate">{{ conv.title || `会话 ${conv.id}` }}</span>
        </button>
      </div>
    </aside>

    <main class="flex-1 min-w-0 flex flex-col">
      <div class="h-14 px-5 border-b border-surface-200 flex items-center justify-between">
        <div>
          <p class="text-sm font-semibold text-surface-900">AI 助手</p>
          <p class="text-xs text-surface-400">用于咨询系统功能与使用问题</p>
        </div>
      </div>

      <div ref="messagesRef" class="flex-1 overflow-auto px-6 py-5">
        <div v-if="!messages.length" class="h-full flex flex-col items-center justify-center text-center">
          <div class="w-14 h-14 rounded-2xl bg-brand-100 flex items-center justify-center mb-4">
            <span class="text-brand-600 text-xl">AI</span>
          </div>
          <p class="text-lg font-semibold text-surface-900">你好，我是系统助手</p>
          <p class="text-sm text-surface-400 mt-1">你可以问我：任务调度、日志查看、脚本分发、服务器管理怎么用。</p>
        </div>

        <div v-else class="space-y-5">
          <div v-for="(msg, idx) in messages" :key="idx">
            <div v-if="msg.role === 'user'" class="flex justify-end">
              <div class="max-w-[72%] bg-brand-500 text-white px-4 py-2.5 rounded-2xl rounded-br-md text-sm">
                {{ msg.content }}
              </div>
            </div>
            <div v-else class="flex justify-start">
              <div class="max-w-[78%] bg-white border border-surface-200 px-4 py-3 rounded-2xl rounded-bl-md text-sm text-surface-800 prose prose-sm max-w-none" v-html="renderMarkdown(msg.content)"></div>
            </div>
          </div>

          <div v-if="sending" class="text-sm text-surface-400">AI 正在思考...</div>
        </div>
      </div>

      <div class="border-t border-surface-200 p-4 bg-white">
        <div class="flex items-end gap-3 bg-surface-50 border border-surface-200 rounded-2xl px-4 py-3">
          <textarea
            v-model="inputText"
            rows="1"
            class="flex-1 bg-transparent resize-none outline-none text-sm text-surface-800 max-h-32"
            placeholder="请输入你想了解的系统功能..."
            @keydown.enter.exact.prevent="sendMessage"
          />
          <button class="send-btn" :disabled="!inputText.trim() || sending" @click="sendMessage">发送</button>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { nextTick, onMounted, ref } from 'vue'
import { marked } from 'marked'
import { assistantApi, type AssistantConversation, type AssistantMessage } from '@/api/assistant'

const conversations = ref<AssistantConversation[]>([])
const currentConversationId = ref<number | null>(null)
const messages = ref<AssistantMessage[]>([])
const inputText = ref('')
const sending = ref(false)
const messagesRef = ref<HTMLElement | null>(null)

const renderMarkdown = (content: string) => marked.parse(content || '')

const scrollToBottom = async () => {
  await nextTick()
  if (messagesRef.value) {
    messagesRef.value.scrollTop = messagesRef.value.scrollHeight
  }
}

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
}

const sendMessage = async () => {
  const text = inputText.value.trim()
  if (!text || sending.value) return

  messages.value.push({ id: Date.now(), role: 'user', content: text })
  inputText.value = ''
  sending.value = true
  await scrollToBottom()

  try {
    const result = await assistantApi.chat({
      message: text,
      conversation_id: currentConversationId.value || undefined,
    })

    if (result.answer) {
      messages.value.push({ id: Date.now() + 1, role: 'assistant', content: result.answer })
    }

    if (result.conversation_id) {
      currentConversationId.value = result.conversation_id
      await loadConversations()
    }
  } finally {
    sending.value = false
    await scrollToBottom()
  }
}

onMounted(async () => {
  await loadConversations()
})
</script>

<style scoped>
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
  text-align: left;
  border: 1px solid transparent;
  background: transparent;
  border-radius: 10px;
  padding: 9px 10px;
  font-size: 13px;
  color: #475569;
}

.conversation-item:hover { background: #f8fafc; }
.conversation-item.active {
  background: #fdf2f8;
  color: #9d174d;
  border-color: #fbcfe8;
}

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
</style>
