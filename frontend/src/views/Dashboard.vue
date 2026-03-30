<template>
  <div class="h-[calc(100vh-80px)] flex flex-col">
    <!-- 顶部标题栏 -->
    <div class="flex items-center justify-between px-6 py-4 border-b border-surface-100 bg-white">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center shadow-lg shadow-brand-200/50">
          <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <div>
          <h1 class="text-lg font-bold text-surface-900">托马斯回旋喵</h1>
          <p class="text-xs text-surface-400">基于知识库的 AI 智能助手</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button 
          @click="clearChat"
          class="flex items-center gap-2 px-4 py-2 text-sm text-surface-600 hover:text-surface-900 hover:bg-surface-100 rounded-xl transition-all"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          清空对话
        </button>
      </div>
    </div>

    <!-- 消息区域 -->
    <div ref="messagesRef" class="flex-1 overflow-y-auto bg-surface-50/50">
      <div class="max-w-4xl mx-auto py-6 px-4">
        <!-- 空状态 -->
        <div v-if="!messages.length" class="h-full flex flex-col items-center justify-center py-20">
          <div class="w-20 h-20 rounded-3xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center mb-6 shadow-xl shadow-brand-200/50">
            <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <h2 class="text-2xl font-bold text-surface-900 mb-2">有什么可以帮你的？</h2>
          <p class="text-sm text-surface-400 mb-8">基于知识库的智能问答，精准理解你的问题</p>
          
          <!-- 快捷问题 -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-2xl">
            <button 
              v-for="q in suggestions" 
              :key="q"
              @click="sendQuick(q)"
              class="px-5 py-4 text-left text-sm text-surface-600 bg-white border border-surface-100 rounded-2xl hover:border-brand-300 hover:shadow-lg hover:shadow-brand-100/50 transition-all group"
            >
              <span class="group-hover:text-brand-600 transition-colors">{{ q }}</span>
              <svg class="w-4 h-4 text-surface-300 group-hover:text-brand-400 float-right mt-0.5 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </div>

        <!-- 消息列表 -->
        <div v-else class="space-y-6">
          <div v-for="(msg, i) in messages" :key="i" class="animate-fade-in">
            <!-- 用户消息 -->
            <div v-if="msg.role === 'user'" class="flex justify-end mb-6">
              <div class="max-w-[85%] bg-brand-500 text-white px-5 py-3.5 rounded-2xl rounded-br-md text-sm leading-relaxed shadow-lg shadow-brand-200/30">
                {{ msg.content }}
              </div>
            </div>
            <!-- AI 消息 -->
            <div v-else class="flex gap-4 mb-6">
              <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-400 to-brand-600 flex items-center justify-center shrink-0 mt-0.5 shadow-lg shadow-brand-200/50">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                </svg>
              </div>
              <div class="flex-1 min-w-0 max-w-[calc(100%-3.5rem)]">
                <div class="text-sm text-surface-800 leading-relaxed whitespace-pre-wrap bg-white px-5 py-4 rounded-2xl rounded-tl-md shadow-sm border border-surface-100">{{ msg.content }}</div>
                <div v-if="msg.sources?.length" class="mt-3 flex flex-wrap gap-2">
                  <span 
                    v-for="src in msg.sources" 
                    :key="src"
                    class="text-[11px] px-3 py-1 bg-surface-100 text-surface-500 rounded-full hover:bg-surface-200 transition-colors cursor-pointer"
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
    </div>

    <!-- 输入区域 -->
    <div class="border-t border-surface-100 bg-white p-4">
      <div class="max-w-4xl mx-auto">
        <div class="flex items-end gap-3 bg-surface-50 border border-surface-200 rounded-2xl px-4 py-3 focus-within:border-brand-400 focus-within:ring-2 focus-within:ring-brand-100 transition-all shadow-sm">
          <textarea 
            ref="inputRef"
            v-model="inputText"
            @keydown.enter.exact.prevent="sendMessage"
            rows="1"
            class="flex-1 bg-transparent text-sm text-surface-900 placeholder-surface-400 resize-none outline-none max-h-32 py-1"
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
        <p class="text-[11px] text-surface-400 mt-2 text-center">内容由 AI 生成，仅供参考 · 托马斯回旋喵</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick, reactive } from 'vue'

interface Message {
  role: 'user' | 'assistant'
  content: string
  sources?: string[]
}

const inputText = ref('')
const streaming = ref(false)
const messagesRef = ref<HTMLElement | null>(null)
const inputRef = ref<HTMLTextAreaElement | null>(null)

const messages = reactive<Message[]>([])

const suggestions = [
  '介绍一下 AgenticOps 知识库的功能',
  '如何创建一个新的知识文档？',
  'FastAPI 最佳实践是什么？',
  '帮我总结一下最近的技术文档',
]

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

  try {
    // 模拟 API 调用
    await new Promise(r => setTimeout(r, 1500))
    
    const mockReply = generateReply(text)
    messages.push(mockReply)
  } catch (e) {
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
    '介绍一下 AgenticOps 知识库的功能': {
      role: 'assistant',
      content: 'AgenticOps 知识库平台是一个基于 AI 的智能知识管理系统，主要功能包括：\n\n1. **知识文档管理** - 支持创建、编辑、分类管理各类技术文档\n2. **AI 智能问答** - 基于知识库内容，使用 RAG 技术进行精准问答\n3. **权限控制** - 细粒度的用户、角色、菜单权限管理\n4. **知识检索** - 支持全文搜索和语义检索\n\n你可以通过左侧菜单访问各个功能模块。',
      sources: ['系统介绍文档', '功能概览']
    },
    '如何创建一个新的知识文档？': {
      role: 'assistant',
      content: '创建知识文档的步骤：\n\n1. 点击「新建知识文档」按钮\n2. 填写文档标题和内容\n3. 选择知识分类\n4. 点击保存即可\n\n文档创建后会自动进行向量化处理，可用于 AI 问答检索。',
      sources: ['用户操作手册']
    },
    'FastAPI 最佳实践是什么？': {
      role: 'assistant',
      content: '根据知识库中的 FastAPI 文档，最佳实践包括：\n\n1. **项目结构** - 按功能模块拆分，使用清晰的目录结构\n2. **依赖注入** - 充分利用 FastAPI 的 Depends 机制\n3. **异步优先** - 数据库操作使用 async/await\n4. **Pydantic 模型** - 使用 Pydantic v2 进行数据验证\n5. **错误处理** - 统一异常处理和错误响应格式',
      sources: ['FastAPI 最佳实践', '技术文档 v2.1']
    },
  }

  return replies[question] || {
    role: 'assistant',
    content: `关于「${question}」，我已从知识库中检索到相关信息。\n\n这是一个基于阿里云通义千问大模型的智能问答系统，能够结合知识库内容为你提供精准回答。你可以继续提问，我会尽力帮助你。`,
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
