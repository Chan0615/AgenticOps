<template>
  <div class="h-[calc(100vh-64px)] flex bg-white">
    <!-- 左侧对话历史 -->
    <div class="w-80 border-r border-surface-100 bg-surface-50/30 flex flex-col">
      <!-- 顶部标题 -->
      <div class="p-4 border-b border-surface-100">
        <button 
          @click="startNewChat"
          class="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-white border border-surface-200 rounded-xl text-sm font-medium text-surface-700 hover:border-brand-300 hover:text-brand-600 hover:shadow-sm transition-all"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          新对话
        </button>
      </div>

      <!-- 历史列表 -->
      <div class="flex-1 overflow-y-auto py-2">
        <div class="px-3 py-2 text-xs font-semibold text-surface-400 uppercase tracking-wider">今天</div>
        <div class="space-y-0.5 px-2">
          <button 
            v-for="chat in todayChats" 
            :key="chat.id"
            @click="loadChat(chat.id)"
            :class="[
              'w-full text-left px-3 py-2.5 rounded-lg text-sm transition-all group',
              currentChatId === chat.id 
                ? 'bg-brand-50 text-brand-700' 
                : 'text-surface-600 hover:bg-surface-100'
            ]"
          >
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4 shrink-0" :class="currentChatId === chat.id ? 'text-brand-500' : 'text-surface-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <span class="truncate flex-1">{{ chat.title }}</span>
            </div>
          </button>
        </div>

        <div class="px-3 py-2 mt-4 text-xs font-semibold text-surface-400 uppercase tracking-wider">昨天</div>
        <div class="space-y-0.5 px-2">
          <button 
            v-for="chat in yesterdayChats" 
            :key="chat.id"
            @click="loadChat(chat.id)"
            :class="[
              'w-full text-left px-3 py-2.5 rounded-lg text-sm transition-all group',
              currentChatId === chat.id 
                ? 'bg-brand-50 text-brand-700' 
                : 'text-surface-600 hover:bg-surface-100'
            ]"
          >
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4 shrink-0" :class="currentChatId === chat.id ? 'text-brand-500' : 'text-surface-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <span class="truncate flex-1">{{ chat.title }}</span>
            </div>
          </button>
        </div>

        <div class="px-3 py-2 mt-4 text-xs font-semibold text-surface-400 uppercase tracking-wider">更早</div>
        <div class="space-y-0.5 px-2">
          <button 
            v-for="chat in olderChats" 
            :key="chat.id"
            @click="loadChat(chat.id)"
            :class="[
              'w-full text-left px-3 py-2.5 rounded-lg text-sm transition-all group',
              currentChatId === chat.id 
                ? 'bg-brand-50 text-brand-700' 
                : 'text-surface-600 hover:bg-surface-100'
            ]"
          >
            <div class="flex items-center gap-2">
              <svg class="w-4 h-4 shrink-0" :class="currentChatId === chat.id ? 'text-brand-500' : 'text-surface-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              <span class="truncate flex-1">{{ chat.title }}</span>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- 右侧对话区域 -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- 顶部标题栏 -->
      <div class="flex items-center justify-between px-6 py-3 border-b border-surface-100">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center shadow-md shadow-brand-200/50">
            <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <div>
            <h1 class="text-sm font-semibold text-surface-900">托马斯回旋喵</h1>
            <p class="text-xs text-surface-400">迭代式 RAG · 智能知识助手</p>
          </div>
        </div>
        <button 
          @click="clearCurrentChat"
          class="p-2 text-surface-400 hover:text-surface-600 hover:bg-surface-100 rounded-lg transition-all"
          title="清空对话"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>

      <!-- 消息区域 -->
      <div ref="messagesRef" class="flex-1 overflow-y-auto px-4 py-6">
        <!-- 空状态 -->
        <div v-if="!messages.length" class="h-full flex flex-col items-center justify-center">
          <div class="w-16 h-16 rounded-2xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center mb-5 shadow-xl shadow-brand-200/50">
            <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <h2 class="text-xl font-semibold text-surface-900 mb-2">有什么可以帮你的？</h2>
          <p class="text-sm text-surface-400 mb-6">迭代式 RAG · 问题→陈述句→检索→迭代优化</p>
          
          <div class="flex flex-wrap justify-center gap-2 max-w-xl">
            <button 
              v-for="q in suggestions" 
              :key="q"
              @click="sendQuick(q)"
              class="px-4 py-2 text-sm text-surface-600 bg-surface-50 border border-surface-200 rounded-xl hover:border-brand-300 hover:bg-white hover:shadow-md transition-all"
            >
              {{ q }}
            </button>
          </div>
        </div>

        <!-- 消息列表 -->
        <div v-else class="space-y-6">
          <div v-for="(msg, i) in messages" :key="i" class="animate-fade-in">
            <!-- 用户消息 - 靠右边缘 -->
            <div v-if="msg.role === 'user'" class="flex justify-end mb-6 pr-2">
              <div class="max-w-[70%] bg-brand-500 text-white px-5 py-3 rounded-2xl rounded-br-md text-[15px] leading-relaxed shadow-lg shadow-brand-200/30">
                {{ msg.content }}
              </div>
            </div>
            
            <!-- AI 消息 - 靠左边缘 -->
            <div v-else class="flex justify-start mb-6 pl-2">
              <div class="max-w-[75%] flex gap-3">
                <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center shrink-0 shadow-lg shadow-brand-200/50">
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <div class="flex-1 space-y-2">
                  <!-- 思考过程 -->
                  <div v-if="msg.thinking" class="bg-surface-50 border border-surface-100 rounded-xl px-4 py-3">
                    <div class="flex items-center gap-2 text-xs text-surface-400 mb-2">
                      <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      <span>Agent 正在协作处理...</span>
                    </div>
                    <div class="space-y-1">
                      <div v-for="(step, si) in msg.thinkingSteps" :key="si" class="flex items-center gap-2 text-xs">
                        <span class="w-1.5 h-1.5 rounded-full" :class="step.done ? 'bg-green-400' : 'bg-brand-400 animate-pulse'"></span>
                        <span :class="step.done ? 'text-surface-500' : 'text-surface-700'">{{ step.text }}</span>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 最终回答 -->
                  <div class="bg-white border border-surface-100 rounded-2xl rounded-tl-md px-5 py-4 shadow-sm">
                    <div class="prose prose-sm max-w-none text-[15px] text-surface-800 leading-relaxed" v-html="marked.parse(msg.content)"></div>
                  </div>
                  
                  <!-- 引用来源 -->
                  <div v-if="msg.sources?.length" class="flex flex-wrap gap-1.5 pl-1">
                    <span 
                      v-for="src in msg.sources" 
                      :key="src"
                      class="text-[11px] px-2.5 py-1 bg-surface-100 text-surface-500 rounded-full hover:bg-brand-50 hover:text-brand-600 transition-colors cursor-pointer"
                    >
                      📄 {{ src }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 加载中 -->
          <div v-if="streaming" class="flex justify-start pl-2">
            <div class="max-w-[75%] flex gap-3">
              <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center shrink-0 shadow-lg shadow-brand-200/50">
                <svg class="w-4 h-4 text-white animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div class="flex items-center gap-1.5 pt-2">
                <span class="w-2 h-2 bg-brand-400 rounded-full animate-bounce" style="animation-delay:0ms"></span>
                <span class="w-2 h-2 bg-brand-400 rounded-full animate-bounce" style="animation-delay:150ms"></span>
                <span class="w-2 h-2 bg-brand-400 rounded-full animate-bounce" style="animation-delay:300ms"></span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 输入区域 -->
      <div class="border-t border-surface-100 bg-white p-4">
        <div class="px-2">
          <div class="flex items-end gap-3 bg-surface-50 border border-surface-200 rounded-2xl px-4 py-3 focus-within:border-brand-400 focus-within:ring-2 focus-within:ring-brand-100 transition-all">
            <textarea 
              ref="inputRef"
              v-model="inputText"
              @keydown.enter.exact.prevent="sendMessage"
              rows="1"
              class="flex-1 bg-transparent text-[15px] text-surface-900 placeholder-surface-400 resize-none outline-none max-h-32 py-1"
              placeholder="输入你的问题，按 Enter 发送..."
            ></textarea>
            <button 
              @click="sendMessage"
              :disabled="!inputText.trim() || streaming"
              class="w-9 h-9 rounded-xl bg-gradient-to-r from-brand-500 to-brand-600 text-white flex items-center justify-center shrink-0 hover:from-brand-400 hover:to-brand-500 transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-lg shadow-brand-200/30"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
          <p class="text-[11px] text-surface-400 mt-2 text-center">内容由 AI 生成，仅供参考 · 托马斯回旋喵</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, nextTick, computed } from 'vue'
import { marked } from 'marked'
import api from '@/api'

interface ThinkingStep {
  text: string
  done: boolean
}

interface Message {
  role: 'user' | 'assistant'
  content: string
  thinking?: boolean
  thinkingSteps?: ThinkingStep[]
  sources?: string[]
}

interface Chat {
  id: string
  title: string
  date: Date
}

const inputText = ref('')
const streaming = ref(false)
const messagesRef = ref<HTMLElement | null>(null)
const inputRef = ref<HTMLTextAreaElement | null>(null)
const currentChatId = ref<string>('')

const messages = reactive<Message[]>([])

// 模拟历史对话数据
const chatHistory = reactive<Chat[]>([
  { id: '1', title: 'FastAPI 异步数据库操作', date: new Date() },
  { id: '2', title: 'Vue3 Composition API 最佳实践', date: new Date() },
  { id: '3', title: 'RAG 向量检索原理', date: new Date(Date.now() - 86400000) },
  { id: '4', title: 'Redis 缓存设计模式', date: new Date(Date.now() - 86400000) },
  { id: '5', title: 'Docker 部署指南', date: new Date(Date.now() - 172800000) },
])

const todayChats = computed(() => chatHistory.filter(c => isToday(c.date)))
const yesterdayChats = computed(() => chatHistory.filter(c => isYesterday(c.date)))
const olderChats = computed(() => chatHistory.filter(c => !isToday(c.date) && !isYesterday(c.date)))

function isToday(date: Date) {
  const today = new Date()
  return date.toDateString() === today.toDateString()
}

function isYesterday(date: Date) {
  const yesterday = new Date(Date.now() - 86400000)
  return date.toDateString() === yesterday.toDateString()
}

const suggestions = [
  '介绍一下 AgenticOps 的功能',
  'FastAPI 最佳实践是什么？',
  '如何优化 RAG 检索效果？',
  '解释一下多 Agent 协作机制',
]

function startNewChat() {
  messages.length = 0
  currentChatId.value = ''
}

function loadChat(chatId: string) {
  currentChatId.value = chatId
  // 模拟加载历史消息
  messages.length = 0
}

function clearCurrentChat() {
  messages.length = 0
}

function sendQuick(q: string) {
  inputText.value = q
  sendMessage()
}

async function sendMessage() {
  const text = inputText.value.trim()
  if (!text || streaming.value) return

  messages.push({ role: 'user', content: text })
  inputText.value = ''
  scrollToBottom()

  streaming.value = true

  // 添加思考中的消息
  const thinkingMsg: Message = {
    role: 'assistant',
    content: '',
    thinking: true,
    thinkingSteps: [
      { text: '将问题转化为陈述句...', done: false },
      { text: '执行 RAG 检索...', done: false },
      { text: '判断检索结果相关性...', done: false },
      { text: '生成回答...', done: false },
    ]
  }
  messages.push(thinkingMsg)

  try {
    // 调用后端 RAG API（增加超时时间，因为 LLM 调用较慢）
    interface ChatResponse {
      answer: string
      sources: string[]
      confidence: number
      steps: any[]
    }
    const response = await api.post('/rag/chat', {
      message: text,
      conversation_id: currentChatId.value || undefined
    }, { timeout: 60000 }) as ChatResponse
    
    console.log('RAG API 响应:', response)
    
    // 更新思考步骤为完成
    thinkingMsg.thinkingSteps?.forEach(step => step.done = true)
    await new Promise(r => setTimeout(r, 300))
    
    // 移除思考状态，显示最终回答
    messages.pop()
    messages.push({
      role: 'assistant',
      content: response.answer || '抱歉，未能获取到有效回答',
      sources: response.sources || []
    })
    
    // 添加到历史记录
    if (!currentChatId.value) {
      const newChat: Chat = {
        id: Date.now().toString(),
        title: text.slice(0, 20) + (text.length > 20 ? '...' : ''),
        date: new Date()
      }
      chatHistory.unshift(newChat)
      currentChatId.value = newChat.id
    }
  } catch (e: any) {
    messages.pop()
    console.error('RAG API 错误:', e)
    console.error('错误响应:', e.response)
    console.error('错误详情:', e.response?.data)
    const errorMsg = e.response?.data?.detail || e.message || '抱歉，服务暂时不可用，请稍后重试。'
    messages.push({
      role: 'assistant',
      content: `请求失败：${errorMsg}`,
    })
  }

  streaming.value = false
  scrollToBottom()
}

function generateReply(question: string): Message {
  // 检查是否是时间相关问题
  const timeKeywords = ['现在', '今天', '明天', '昨天', '时间', '几点', '日期', '星期', '周日', '周一', '周二', '周三', '周四', '周五', '周六']
  const isTimeQuestion = timeKeywords.some(kw => question.includes(kw))
  
  if (isTimeQuestion) {
    const now = new Date()
    const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
    const timeStr = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    const dateStr = now.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
    const weekday = weekdays[now.getDay()]
    
    return {
      role: 'assistant',
      content: `⏰ 当前时间：${timeStr}\n📅 ${dateStr} ${weekday}\n\n🔧 这是通过 **Tool 工具调用** 获取的实时信息（get_current_time）`,
      sources: ['工具调用']
    }
  }
  
  // 检查是否是计算问题
  const calcKeywords = ['计算', '等于', '多少', '加', '减', '乘', '除']
  if (calcKeywords.some(kw => question.includes(kw))) {
    return {
      role: 'assistant',
      content: `🧮 计算结果：42\n\n🔧 这是通过 **Tool 工具调用** 计算得出的结果（calculate）`,
      sources: ['工具调用']
    }
  }
  
  // 检查是否是问候语
  const greetKeywords = ['你好', '您好', 'hello', 'hi', '在吗']
  if (greetKeywords.some(kw => question.toLowerCase().includes(kw))) {
    return {
      role: 'assistant',
      content: '你好！我是托马斯回旋喵，你的智能知识助手。\n\n我可以：\n• 🔍 通过知识库检索专业信息\n• ⏰ 查询当前时间等实时信息\n• 🧮 进行简单的数学计算\n\n有什么可以帮你的吗？',
      sources: ['模型回答']
    }
  }

  const replies: Record<string, Message> = {
    '介绍一下 AgenticOps 的功能': {
      role: 'assistant',
      content: 'AgenticOps 是一个基于**迭代式 RAG** 的智能知识管理平台：\n\n**核心能力：**\n• 查询转换器 - 问题→陈述句\n• 检索 Agent - 语义检索相关文档\n• 相关性检查器 - 评估检索结果\n• 迭代优化 - 不相关时重新检索\n\n**技术栈：** FastAPI + Vue3 + 阿里云通义千问 + 向量数据库',
      sources: ['系统介绍', '架构文档']
    },
    '解释一下多 Agent 协作机制': {
      role: 'assistant',
      content: '迭代式 RAG 的核心流程：\n\n1️⃣ **查询转换** - 将问题转化为陈述句\n2️⃣ **语义检索** - 基于陈述句检索相关文档\n3️⃣ **相关性判断** - 评估检索结果质量\n4️⃣ **迭代优化** - 不相关时生成新陈述句重新检索\n\n如果知识库中没有相关信息，会直接使用大模型回答。',
      sources: ['Agent 架构设计']
    },
  }

  return replies[question] || {
    role: 'assistant',
    content: `关于「${question}」，我已通过迭代式 RAG 完成检索和分析。

检索 Agent 从知识库中找到相关文档，相关性检查器评估了匹配度，最终为你生成这个回复。

如需了解更多细节，可以继续追问。`,
    sources: ['知识库检索结果']
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}
</script>
