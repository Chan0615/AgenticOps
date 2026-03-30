<template>
  <div class="h-[calc(100vh-64px)] flex bg-white">
    <!-- 左侧对话区域 -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- 顶部标题 -->
      <div class="flex items-center justify-between px-8 py-4 border-b border-surface-100">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center shadow-lg shadow-brand-200/50">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <div>
            <h1 class="text-base font-semibold text-surface-900">托马斯回旋喵</h1>
            <p class="text-xs text-surface-400">多 Agent 协作 · 智能知识助手</p>
          </div>
        </div>
        <button 
          @click="clearChat"
          class="p-2 text-surface-400 hover:text-surface-600 hover:bg-surface-100 rounded-lg transition-all"
          title="清空对话"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>

      <!-- 消息区域 -->
      <div ref="messagesRef" class="flex-1 overflow-y-auto px-8 py-6">
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

        <!-- 消息列表 - AI靠左，用户靠右，间距更大 -->
        <div v-else class="space-y-8">
          <div v-for="(msg, i) in messages" :key="i" class="animate-fade-in">
            <!-- 用户消息 - 更靠右 -->
            <div v-if="msg.role === 'user'" class="flex justify-end mb-8 pr-4 lg:pr-12">
              <div class="max-w-[75%] flex gap-3">
                <div class="bg-brand-500 text-white px-6 py-4 rounded-2xl rounded-br-md text-[15px] leading-relaxed shadow-lg shadow-brand-200/30">
                  {{ msg.content }}
                </div>
                <div class="w-9 h-9 rounded-full bg-surface-200 flex items-center justify-center shrink-0">
                  <svg class="w-5 h-5 text-surface-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
              </div>
            </div>
            
            <!-- AI 消息 - 更靠左 -->
            <div v-else class="flex justify-start mb-8 pl-4 lg:pl-12">
              <div class="max-w-[80%] flex gap-3">
                <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center shrink-0 shadow-lg shadow-brand-200/50">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <div class="flex-1 space-y-3">
                  <!-- Agent 思考过程 -->
                  <div v-if="msg.thinking" class="bg-surface-50 border border-surface-100 rounded-xl px-4 py-3">
                    <div class="flex items-center gap-2 text-xs text-surface-400 mb-2">
                      <svg class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      <span>Agent 正在协作处理...</span>
                    </div>
                    <div class="space-y-1.5">
                      <div v-for="(step, si) in msg.thinkingSteps" :key="si" class="flex items-center gap-2 text-xs">
                        <span class="w-1.5 h-1.5 rounded-full" :class="step.done ? 'bg-green-400' : 'bg-brand-400 animate-pulse'"></span>
                        <span :class="step.done ? 'text-surface-500' : 'text-surface-700'">{{ step.text }}</span>
                      </div>
                    </div>
                  </div>
                  
                  <!-- 最终回答 -->
                  <div class="bg-white border border-surface-100 rounded-2xl rounded-tl-md px-6 py-4 shadow-sm">
                    <div class="text-[15px] text-surface-800 leading-relaxed whitespace-pre-wrap">{{ msg.content }}</div>
                  </div>
                  
                  <!-- 引用来源 -->
                  <div v-if="msg.sources?.length" class="flex flex-wrap gap-2 pl-1">
                    <span 
                      v-for="src in msg.sources" 
                      :key="src"
                      class="text-[11px] px-3 py-1 bg-surface-100 text-surface-500 rounded-full hover:bg-brand-50 hover:text-brand-600 transition-colors cursor-pointer"
                    >
                      📄 {{ src }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 加载中 -->
          <div v-if="streaming" class="flex justify-start pl-4 lg:pl-12">
            <div class="max-w-[80%] flex gap-3">
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
      </div>

      <!-- 输入区域 -->
      <div class="border-t border-surface-100 bg-white px-8 py-5">
        <div class="max-w-4xl mx-auto">
          <div class="flex items-end gap-3 bg-surface-50 border border-surface-200 rounded-2xl px-5 py-3 focus-within:border-brand-400 focus-within:ring-2 focus-within:ring-brand-100 transition-all">
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
              class="w-10 h-10 rounded-xl bg-gradient-to-r from-brand-500 to-brand-600 text-white flex items-center justify-center shrink-0 hover:from-brand-400 hover:to-brand-500 transition-all disabled:opacity-40 disabled:cursor-not-allowed shadow-lg shadow-brand-200/30"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
          <p class="text-[11px] text-surface-400 mt-2 text-center">内容由 AI 生成，仅供参考 · 多 Agent 协作检索</p>
        </div>
      </div>
    </div>

    <!-- 右侧信息面板 -->
    <div class="w-80 border-l border-surface-100 bg-surface-50/50 flex flex-col">
      <!-- RAG 流程说明 -->
      <div class="p-5 border-b border-surface-100">
        <h3 class="text-sm font-semibold text-surface-900 mb-4 flex items-center gap-2">
          <svg class="w-4 h-4 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          迭代式 RAG 流程
        </h3>
        <div class="space-y-2.5">
          <div class="flex items-start gap-3">
            <div class="w-6 h-6 rounded-full bg-brand-100 flex items-center justify-center shrink-0 mt-0.5">
              <span class="text-[10px] font-bold text-brand-600">1</span>
            </div>
            <div>
              <p class="text-sm font-medium text-surface-800">问题 → 陈述句</p>
              <p class="text-xs text-surface-400">将疑问转换为肯定形式</p>
            </div>
          </div>
          <div class="flex items-start gap-3">
            <div class="w-6 h-6 rounded-full bg-brand-100 flex items-center justify-center shrink-0 mt-0.5">
              <span class="text-[10px] font-bold text-brand-600">2</span>
            </div>
            <div>
              <p class="text-sm font-medium text-surface-800">陈述句 → RAG 检索</p>
              <p class="text-xs text-surface-400">语义检索相关文档</p>
            </div>
          </div>
          <div class="flex items-start gap-3">
            <div class="w-6 h-6 rounded-full bg-brand-100 flex items-center justify-center shrink-0 mt-0.5">
              <span class="text-[10px] font-bold text-brand-600">3</span>
            </div>
            <div>
              <p class="text-sm font-medium text-surface-800">判断相关性</p>
              <p class="text-xs text-surface-400">评估检索结果质量</p>
            </div>
          </div>
          <div class="flex items-start gap-3">
            <div class="w-6 h-6 rounded-full bg-amber-100 flex items-center justify-center shrink-0 mt-0.5">
              <svg class="w-3 h-3 text-amber-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
            </div>
            <div>
              <p class="text-sm font-medium text-surface-800">不相关 → 迭代</p>
              <p class="text-xs text-surface-400">生成新陈述句重新检索</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 知识库状态 -->
      <div class="p-5 border-b border-surface-100">
        <h3 class="text-sm font-semibold text-surface-900 mb-4 flex items-center gap-2">
          <svg class="w-4 h-4 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
          知识库状态
        </h3>
        <div class="space-y-3">
          <div class="flex items-center justify-between text-sm">
            <span class="text-surface-500">文档数量</span>
            <span class="font-medium text-surface-900">1,247</span>
          </div>
          <div class="flex items-center justify-between text-sm">
            <span class="text-surface-500">向量片段</span>
            <span class="font-medium text-surface-900">8,532</span>
          </div>
          <div class="flex items-center justify-between text-sm">
            <span class="text-surface-500">最后更新</span>
            <span class="font-medium text-surface-900">2小时前</span>
          </div>
        </div>
      </div>

      <!-- Agent 状态 -->
      <div class="p-5 border-b border-surface-100">
        <h3 class="text-sm font-semibold text-surface-900 mb-4 flex items-center gap-2">
          <svg class="w-4 h-4 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          Agent 协作
        </h3>
        <div class="space-y-2">
          <div class="flex items-center gap-3 p-2.5 bg-white rounded-xl border border-surface-100">
            <div class="w-8 h-8 rounded-lg bg-purple-100 flex items-center justify-center">
              <svg class="w-4 h-4 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4" />
              </svg>
            </div>
            <div class="flex-1">
              <div class="text-sm font-medium text-surface-900">查询转换器</div>
              <div class="text-xs text-surface-400">问题 → 陈述句</div>
            </div>
          </div>
          <div class="flex items-center gap-3 p-2.5 bg-white rounded-xl border border-surface-100">
            <div class="w-8 h-8 rounded-lg bg-blue-100 flex items-center justify-center">
              <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <div class="flex-1">
              <div class="text-sm font-medium text-surface-900">检索 Agent</div>
              <div class="text-xs text-surface-400">语义检索相关文档</div>
            </div>
          </div>
          <div class="flex items-center gap-3 p-2.5 bg-white rounded-xl border border-surface-100">
            <div class="w-8 h-8 rounded-lg bg-green-100 flex items-center justify-center">
              <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="flex-1">
              <div class="text-sm font-medium text-surface-900">相关性检查器</div>
              <div class="text-xs text-surface-400">评估检索结果质量</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 最近对话 -->
      <div class="flex-1 p-5 overflow-y-auto">
        <h3 class="text-sm font-semibold text-surface-900 mb-4 flex items-center gap-2">
          <svg class="w-4 h-4 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          最近对话
        </h3>
        <div class="space-y-2">
          <button 
            v-for="(chat, i) in recentChats" 
            :key="i"
            class="w-full text-left p-3 rounded-xl hover:bg-white hover:shadow-sm transition-all group"
          >
            <p class="text-sm text-surface-700 line-clamp-1 group-hover:text-brand-600 transition-colors">{{ chat.title }}</p>
            <p class="text-xs text-surface-400 mt-1">{{ chat.time }}</p>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, nextTick } from 'vue'

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

interface RecentChat {
  title: string
  time: string
}

const inputText = ref('')
const streaming = ref(false)
const messagesRef = ref<HTMLElement | null>(null)
const inputRef = ref<HTMLTextAreaElement | null>(null)

const messages = reactive<Message[]>([])

const suggestions = [
  '介绍一下 AgenticOps 的功能',
  'FastAPI 最佳实践是什么？',
  '如何优化 RAG 检索效果？',
  '解释一下多 Agent 协作机制',
]

const recentChats = reactive<RecentChat[]>([
  { title: 'FastAPI 异步数据库操作', time: '10分钟前' },
  { title: 'Vue3 Composition API 最佳实践', time: '1小时前' },
  { title: 'RAG 向量检索原理', time: '昨天' },
  { title: 'Redis 缓存设计模式', time: '2天前' },
])

function clearChat() {
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
      { text: '检索 Agent 分析查询意图...', done: false },
      { text: '执行语义检索获取相关文档...', done: false },
      { text: '推理 Agent 分析检索结果...', done: false },
      { text: '回答 Agent 生成最终回复...', done: false },
    ]
  }
  messages.push(thinkingMsg)

  try {
    // 模拟多 Agent 协作过程
    for (let i = 0; i < thinkingMsg.thinkingSteps!.length; i++) {
      await new Promise(r => setTimeout(r, 600))
      thinkingMsg.thinkingSteps![i].done = true
    }

    await new Promise(r => setTimeout(r, 500))
    
    // 移除思考状态，显示最终回答
    const reply = generateReply(text)
    messages.pop()
    messages.push(reply)
  } catch (e) {
    messages.pop()
    messages.push({
      role: 'assistant',
      content: '抱歉，服务暂时不可用，请稍后重试。',
    })
  }

  streaming.value = false
  scrollToBottom()
}

function generateReply(question: string): Message {
  const replies: Record<string, Message> = {
    '介绍一下 AgenticOps 的功能': {
      role: 'assistant',
      content: 'AgenticOps 是一个基于**多 Agent 协作**的智能知识管理平台：\n\n**核心能力：**\n• 检索 Agent - 语义检索 + 关键词匹配\n• 推理 Agent - 分析、综合、反思检索结果\n• 回答 Agent - 生成精准、结构化的回复\n\n**技术栈：** FastAPI + Vue3 + 阿里云通义千问 + 向量数据库',
      sources: ['系统介绍', '架构文档']
    },
    '解释一下多 Agent 协作机制': {
      role: 'assistant',
      content: '多 Agent 协作机制是我们的核心创新：\n\n1️⃣ **检索 Agent** 接收用户问题，执行多策略检索\n2️⃣ **推理 Agent** 分析检索结果，判断信息是否充分\n3️⃣ **回答 Agent** 综合所有信息，生成最终回复\n\n如果信息不足，Agent 会自动重新检索，直到获得满意答案。',
      sources: ['Agent 架构设计']
    },
  }

  return replies[question] || {
    role: 'assistant',
    content: `关于「${question}」，我已通过多 Agent 协作完成检索和分析。

检索 Agent 从知识库中找到相关文档，推理 Agent 分析了 3 个关键信息点，最终由回答 Agent 为你生成这个回复。

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
