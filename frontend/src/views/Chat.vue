<template>
  <div class="h-[calc(100vh-120px)] flex rounded-2xl overflow-hidden border border-surface-100 bg-white">
    <!-- 左侧会话列表 -->
    <div class="w-64 border-r border-surface-100 flex flex-col shrink-0 bg-surface-50/50">
      <div class="p-3">
        <button 
          @click="newChat"
          class="w-full h-10 bg-gradient-to-r from-brand-500 to-brand-600 text-white text-sm font-medium rounded-xl hover:from-brand-400 hover:to-brand-500 transition-all flex items-center justify-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          新建对话
        </button>
      </div>
      <div class="flex-1 overflow-y-auto px-2 pb-2 space-y-0.5">
        <div 
          v-for="conv in conversations" 
          :key="conv.id"
          @click="activeConvId = conv.id"
          :class="[
            'flex items-center gap-3 px-3 py-2.5 rounded-xl cursor-pointer transition-all group',
            activeConvId === conv.id ? 'bg-brand-50 text-brand-700' : 'text-surface-600 hover:bg-surface-100'
          ]"
        >
          <svg class="w-4 h-4 shrink-0 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
          </svg>
          <span class="text-sm truncate flex-1">{{ conv.title }}</span>
          <button 
            @click.stop="deleteConv(conv.id)"
            class="w-6 h-6 rounded-lg hover:bg-surface-200 items-center justify-center hidden group-hover:flex shrink-0"
          >
            <svg class="w-3.5 h-3.5 text-surface-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- 右侧对话区 -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- 消息区 -->
      <div ref="messagesRef" class="flex-1 overflow-y-auto px-4 py-6">
        <!-- 空状态 -->
        <div v-if="!activeConv?.messages.length" class="h-full flex flex-col items-center justify-center text-center">
          <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center mb-4 shadow-lg shadow-brand-200/50">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <h2 class="text-lg font-bold text-surface-900 mb-1">托马斯回旋喵</h2>
          <p class="text-sm text-surface-400 mb-8">基于知识库的智能问答助手</p>
          <div class="grid grid-cols-2 gap-3 max-w-lg w-full">
            <button 
              v-for="q in suggestions" 
              :key="q"
              @click="sendQuick(q)"
              class="px-4 py-3 text-left text-sm text-surface-600 bg-surface-50 border border-surface-100 rounded-xl hover:border-brand-200 hover:bg-brand-50/50 transition-all"
            >
              {{ q }}
            </button>
          </div>
        </div>

        <!-- 消息列表 - 更宽的对话区域 -->
        <div v-else class="max-w-5xl mx-auto space-y-6 px-4">
          <div v-for="(msg, i) in activeConv.messages" :key="i" class="animate-fade-in">
            <!-- 用户消息 - 更宽 -->
            <div v-if="msg.role === 'user'" class="flex justify-end">
              <div class="max-w-[85%] bg-brand-500 text-white px-5 py-3.5 rounded-2xl rounded-br-md text-sm leading-relaxed">
                {{ msg.content }}
              </div>
            </div>
            <!-- AI 消息 - 更宽 -->
            <div v-else class="flex gap-4">
              <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center shrink-0 mt-0.5 shadow-lg shadow-brand-200/50">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div class="flex-1 min-w-0 max-w-[calc(100%-3rem)]">
                <div class="text-sm text-surface-800 leading-relaxed whitespace-pre-wrap">{{ msg.content }}</div>
                <div v-if="msg.sources?.length" class="mt-3 flex flex-wrap gap-2">
                  <span 
                    v-for="src in msg.sources" 
                    :key="src"
                    class="text-[10px] px-2 py-0.5 bg-surface-100 text-surface-500 rounded-full"
                  >📚 {{ src }}</span>
                </div>
              </div>
            </div>
          </div>
          <!-- 加载中 -->
          <div v-if="streaming" class="flex gap-4">
            <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center shrink-0 shadow-lg shadow-brand-200/50">
              <svg class="w-5 h-5 text-white animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <div class="flex items-center gap-1.5 pt-3">
              <span class="w-2 h-2 bg-brand-400 rounded-full animate-bounce" style="animation-delay:0ms"></span>
              <span class="w-2 h-2 bg-brand-400 rounded-full animate-bounce" style="animation-delay:150ms"></span>
              <span class="w-2 h-2 bg-brand-400 rounded-full animate-bounce" style="animation-delay:300ms"></span>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区 -->
      <div class="border-t border-surface-100 p-4">
        <div class="max-w-5xl mx-auto">
          <div class="flex items-end gap-3 bg-surface-50 border border-surface-200 rounded-2xl px-4 py-3 focus-within:border-brand-400 focus-within:ring-2 focus-within:ring-brand-100 transition-all">
            <textarea 
              ref="inputRef"
              v-model="inputText"
              @keydown.enter.exact.prevent="sendMessage"
              rows="1"
              class="flex-1 bg-transparent text-sm text-surface-900 placeholder-surface-400 resize-none outline-none max-h-32"
              placeholder="输入你的问题..."
            ></textarea>
            <button 
              @click="sendMessage"
              :disabled="!inputText.trim() || streaming"
              class="w-9 h-9 rounded-xl bg-gradient-to-r from-brand-500 to-brand-600 text-white flex items-center justify-center shrink-0 hover:from-brand-400 hover:to-brand-500 transition-all disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
          <p class="text-[10px] text-surface-400 mt-2 text-center">托马斯回旋喵 · 基于知识库生成回答，内容仅供参考</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, reactive } from 'vue'
import { agentApi } from '@/api/agent'

interface Message {
  role: 'user' | 'assistant'
  content: string
  sources?: string[]
}

interface Conversation {
  id: number
  title: string
  messages: Message[]
}

const inputText = ref('')
const streaming = ref(false)
const activeConvId = ref(1)
const messagesRef = ref<HTMLElement | null>(null)
const inputRef = ref<HTMLTextAreaElement | null>(null)

let convIdCounter = 2

const conversations = reactive<Conversation[]>([
  { id: 1, title: '新对话', messages: [] }
])

const activeConv = computed(() => conversations.find(c => c.id === activeConvId.value))

const suggestions = [
  '介绍一下这个知识库的功能',
  '如何创建一个新的知识文档？',
  'FastAPI 最佳实践是什么？',
  '帮我总结一下最近的技术文档',
]

function newChat() {
  const conv: Conversation = { id: convIdCounter++, title: '新对话', messages: [] }
  conversations.unshift(conv)
  activeConvId.value = conv.id
}

function deleteConv(id: number) {
  const idx = conversations.findIndex(c => c.id === id)
  if (idx > -1) {
    conversations.splice(idx, 1)
    if (activeConvId.value === id && conversations.length) {
      activeConvId.value = conversations[0].id
    }
  }
}

function sendQuick(q: string) {
  inputText.value = q
  sendMessage()
}

async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || streaming.value) return

  const conv = activeConv.value
  if (!conv) return

  if (!conv.messages.length) {
    conv.title = text.length > 20 ? text.slice(0, 20) + '...' : text
  }

  conv.messages.push({ role: 'user', content: text })
  inputText.value = ''
  scrollToBottom()

  streaming.value = true

  try {
    const res = await agentApi.chat({
      message: text,
      conversation_id: conv.id > 100000 ? undefined : conv.id,
    })
    conv.messages.push({
      role: 'assistant',
      content: res.answer || '没有收到回复',
      sources: res.sources,
    })
    if (res.conversation_id && conv.id > 100000) {
      conv.id = res.conversation_id
    }
  } catch (e: any) {
    // API 不可用时 fallback 到 mock
    const mockReply = await mockRAGReply(text)
    conv.messages.push(mockReply)
  }

  streaming.value = false
  scrollToBottom()
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}

// 模拟 RAG 回复
async function mockRAGReply(question: string): Promise<Message> {
  await new Promise(r => setTimeout(r, 1500))
  
  const replies: Record<string, Message> = {
    '介绍一下这个知识库的功能': {
      role: 'assistant',
      content: 'AgenticOps 知识库平台是一个基于 AI 的智能知识管理系统，主要功能包括：\n\n1. **知识文档管理** - 支持创建、编辑、分类管理各类技术文档\n2. **AI 智能问答** - 基于知识库内容，使用 RAG 技术进行精准问答\n3. **权限控制** - 细粒度的用户、角色、菜单权限管理\n4. **知识检索** - 支持全文搜索和语义检索\n\n你可以通过左侧菜单访问各个功能模块。',
      sources: ['系统介绍文档', '功能概览']
    },
    '如何创建一个新的知识文档？': {
      role: 'assistant',
      content: '创建知识文档的步骤：\n\n1. 点击仪表盘的「新建知识文档」按钮\n2. 填写文档标题和内容\n3. 选择知识分类\n4. 点击保存即可\n\n文档创建后会自动进行向量化处理，可用于 AI 问答检索。',
      sources: ['用户操作手册']
    },
    'FastAPI 最佳实践是什么？': {
      role: 'assistant',
      content: '根据知识库中的 FastAPI 文档，最佳实践包括：\n\n1. **项目结构** - 按功能模块拆分，使用清晰的目录结构\n2. **依赖注入** - 充分利用 FastAPI 的 Depends 机制\n3. **异步优先** - 数据库操作使用 async/await\n4. **Pydantic 模型** - 使用 Pydantic v2 进行数据验证\n5. **错误处理** - 统一异常处理和错误响应格式\n6. **API 版本管理** - 使用 prefix 进行版本控制',
      sources: ['FastAPI 最佳实践', '技术文档 v2.1']
    },
  }

  return replies[question] || {
    role: 'assistant',
    content: `关于「${question}」，我从知识库中检索到了相关信息。\n\n目前系统正在对接 AI 模型，后续将提供更精准的基于知识库的智能回答。你可以继续提问，我会尽力帮助你。`,
    sources: ['知识库检索结果']
  }
}
</script>
