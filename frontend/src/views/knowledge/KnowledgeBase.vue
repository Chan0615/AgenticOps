<template>
  <div class="h-full flex flex-col">
    <!-- 页头 -->
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-xl font-bold text-surface-900">知识库管理</h2>
        <p class="text-sm text-surface-400 mt-0.5">管理 RAG 知识库文档与向量索引</p>
      </div>
      <div class="flex items-center gap-3">
        <button 
          @click="showUploadModal = true"
          class="px-4 py-2.5 bg-gradient-to-r from-brand-500 to-brand-600 text-white text-sm font-medium rounded-xl shadow-lg shadow-brand-200/50 hover:shadow-brand-300/50 hover:from-brand-400 hover:to-brand-500 transition-all duration-200 flex items-center gap-2"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
          上传文档
        </button>
        <button 
          @click="rebuildIndex"
          :disabled="rebuilding"
          class="px-4 py-2.5 bg-white border border-surface-200 text-surface-700 text-sm font-medium rounded-xl hover:border-brand-300 hover:text-brand-600 transition-all duration-200 flex items-center gap-2 disabled:opacity-50"
        >
          <svg class="w-4 h-4" :class="rebuilding ? 'animate-spin' : ''" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          {{ rebuilding ? '重建中...' : '重建索引' }}
        </button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-white rounded-2xl border border-surface-100 p-5">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-brand-50 flex items-center justify-center">
            <svg class="w-5 h-5 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div>
            <p class="text-2xl font-bold text-surface-900">{{ stats.totalDocs }}</p>
            <p class="text-xs text-surface-400">文档总数</p>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-2xl border border-surface-100 p-5">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-emerald-50 flex items-center justify-center">
            <svg class="w-5 h-5 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div>
            <p class="text-2xl font-bold text-surface-900">{{ stats.indexedDocs }}</p>
            <p class="text-xs text-surface-400">已索引</p>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-2xl border border-surface-100 p-5">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-amber-50 flex items-center justify-center">
            <svg class="w-5 h-5 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <div>
            <p class="text-2xl font-bold text-surface-900">{{ stats.pendingDocs }}</p>
            <p class="text-xs text-surface-400">待处理</p>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-2xl border border-surface-100 p-5">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl bg-cyan-50 flex items-center justify-center">
            <svg class="w-5 h-5 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
          <div>
            <p class="text-2xl font-bold text-surface-900">{{ stats.totalChunks }}</p>
            <p class="text-xs text-surface-400">向量片段</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 文档列表 -->
    <div class="flex-1 bg-white rounded-2xl border border-surface-100 overflow-hidden flex flex-col">
      <!-- 搜索栏 -->
      <div class="p-4 border-b border-surface-100 flex items-center gap-4">
        <div class="flex-1 relative">
          <svg class="w-4 h-4 text-surface-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
          <input 
            v-model="searchQuery"
            type="text"
            placeholder="搜索文档名称..."
            class="w-full h-10 pl-10 pr-4 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
          />
        </div>
        <select 
          v-model="filterStatus"
          class="h-10 px-4 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-700 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 transition-all"
        >
          <option value="">全部状态</option>
          <option value="indexed">已索引</option>
          <option value="pending">待处理</option>
          <option value="error">处理失败</option>
        </select>
      </div>

      <!-- 列表内容 -->
      <div class="flex-1 overflow-auto">
        <table class="w-full">
          <thead class="bg-surface-50 sticky top-0">
            <tr>
              <th class="px-4 py-3 text-left text-xs font-semibold text-surface-500 uppercase tracking-wider">文档名称</th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-surface-500 uppercase tracking-wider">类型</th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-surface-500 uppercase tracking-wider">大小</th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-surface-500 uppercase tracking-wider">状态</th>
              <th class="px-4 py-3 text-left text-xs font-semibold text-surface-500 uppercase tracking-wider">上传时间</th>
              <th class="px-4 py-3 text-right text-xs font-semibold text-surface-500 uppercase tracking-wider">操作</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-surface-100">
            <tr v-for="doc in filteredDocs" :key="doc.id" class="hover:bg-surface-50 transition-colors">
              <td class="px-4 py-3">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-lg bg-surface-100 flex items-center justify-center">
                    <svg class="w-4 h-4 text-surface-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                  </div>
                  <span class="text-sm font-medium text-surface-900">{{ doc.name }}</span>
                </div>
              </td>
              <td class="px-4 py-3">
                <span class="text-xs px-2 py-1 bg-surface-100 text-surface-600 rounded-full">{{ doc.type }}</span>
              </td>
              <td class="px-4 py-3 text-sm text-surface-600">{{ doc.size }}</td>
              <td class="px-4 py-3">
                <span 
                  class="text-xs px-2 py-1 rounded-full"
                  :class="{
                    'bg-emerald-50 text-emerald-600': doc.status === 'indexed',
                    'bg-amber-50 text-amber-600': doc.status === 'pending',
                    'bg-rose-50 text-rose-600': doc.status === 'error'
                  }"
                >
                  {{ statusText[doc.status] }}
                </span>
              </td>
              <td class="px-4 py-3 text-sm text-surface-500">{{ doc.uploadTime }}</td>
              <td class="px-4 py-3 text-right">
                <div class="flex items-center justify-end gap-2">
                  <button 
                    @click="viewDoc(doc)"
                    class="p-1.5 text-surface-400 hover:text-brand-600 hover:bg-brand-50 rounded-lg transition-colors"
                    title="查看"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                    </svg>
                  </button>
                  <button 
                    @click="deleteDoc(doc)"
                    class="p-1.5 text-surface-400 hover:text-rose-600 hover:bg-rose-50 rounded-lg transition-colors"
                    title="删除"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- 空状态 -->
        <div v-if="filteredDocs.length === 0" class="p-16 text-center">
          <div class="w-14 h-14 rounded-2xl bg-surface-50 border border-surface-100 flex items-center justify-center mx-auto mb-4">
            <svg class="w-7 h-7 text-surface-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <h3 class="text-sm font-medium text-surface-700">暂无文档</h3>
          <p class="text-xs text-surface-400 mt-1">点击上方「上传文档」开始添加</p>
        </div>
      </div>
    </div>

    <!-- 上传文档弹窗 -->
    <div v-if="showUploadModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-lg animate-fade-in">
        <div class="flex items-center justify-between px-6 py-4 border-b border-surface-100">
          <h3 class="text-lg font-semibold text-surface-900">上传文档</h3>
          <button @click="showUploadModal = false" class="p-1.5 text-surface-400 hover:text-surface-600 hover:bg-surface-100 rounded-lg transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-6">
          <!-- 拖拽上传区域 -->
          <div 
            class="border-2 border-dashed border-surface-200 rounded-2xl p-8 text-center hover:border-brand-300 hover:bg-brand-50/30 transition-all cursor-pointer"
            @click="openFilePicker"
            @dragover.prevent
            @drop.prevent="handleDrop"
          >
            <input 
              ref="fileInput"
              type="file" 
              multiple 
              accept=".txt,.pdf,.doc,.docx,.md"
              class="hidden"
              @change="handleFileSelect"
            />
            <div class="w-14 h-14 rounded-2xl bg-brand-50 flex items-center justify-center mx-auto mb-4">
              <svg class="w-7 h-7 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <p class="text-sm font-medium text-surface-700 mb-1">点击或拖拽文件到此处上传</p>
            <p class="text-xs text-surface-400">支持 TXT、PDF、Word、Markdown 格式</p>
          </div>

          <!-- 已选文件列表 -->
          <div v-if="selectedFiles.length > 0" class="mt-4 space-y-2">
            <div v-for="(file, index) in selectedFiles" :key="index" class="flex items-center gap-3 p-3 bg-surface-50 rounded-xl">
              <svg class="w-5 h-5 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-surface-900 truncate">{{ file.name }}</p>
                <p class="text-xs text-surface-400">{{ formatFileSize(file.size) }}</p>
              </div>
              <button @click="removeFile(index)" class="p-1 text-surface-400 hover:text-rose-500 transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <div class="flex items-center justify-end gap-3 px-6 py-4 border-t border-surface-100">
          <button 
            @click="showUploadModal = false"
            class="px-4 py-2 text-sm font-medium text-surface-600 hover:text-surface-900 transition-colors"
          >
            取消
          </button>
          <button 
            @click="uploadFiles"
            :disabled="selectedFiles.length === 0 || uploading"
            class="px-4 py-2 bg-gradient-to-r from-brand-500 to-brand-600 text-white text-sm font-medium rounded-xl hover:from-brand-400 hover:to-brand-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <svg v-if="uploading" class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            {{ uploading ? '上传中...' : '开始上传' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Document {
  id: string
  name: string
  type: string
  size: string
  status: 'indexed' | 'pending' | 'error'
  uploadTime: string
}

const searchQuery = ref('')
const filterStatus = ref('')
const showUploadModal = ref(false)
const selectedFiles = ref<File[]>([])
const fileInput = ref<HTMLInputElement | null>(null)
const uploading = ref(false)
const rebuilding = ref(false)

const stats = ref({
  totalDocs: 12,
  indexedDocs: 10,
  pendingDocs: 1,
  totalChunks: 156
})

const statusText: Record<string, string> = {
  indexed: '已索引',
  pending: '待处理',
  error: '处理失败'
}

// 模拟文档数据
const documents = ref<Document[]>([
  { id: '1', name: 'FastAPI 最佳实践指南.txt', type: 'TXT', size: '12.5 KB', status: 'indexed', uploadTime: '2024-01-15 14:30' },
  { id: '2', name: 'Vue3 Composition API 文档.md', type: 'MD', size: '8.2 KB', status: 'indexed', uploadTime: '2024-01-14 09:15' },
  { id: '3', name: 'RAG 技术白皮书.pdf', type: 'PDF', size: '2.4 MB', status: 'indexed', uploadTime: '2024-01-13 16:45' },
  { id: '4', name: '项目架构设计.docx', type: 'DOCX', size: '156 KB', status: 'pending', uploadTime: '2024-01-15 10:20' },
])

const filteredDocs = computed(() => {
  return documents.value.filter(doc => {
    const matchQuery = doc.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchStatus = !filterStatus.value || doc.status === filterStatus.value
    return matchQuery && matchStatus
  })
})

function handleFileSelect(e: Event) {
  const files = (e.target as HTMLInputElement).files
  if (files) {
    selectedFiles.value.push(...Array.from(files))
  }
}

function handleDrop(e: DragEvent) {
  const files = e.dataTransfer?.files
  if (files) {
    selectedFiles.value.push(...Array.from(files))
  }
}

function openFilePicker() {
  fileInput.value?.click()
}

function removeFile(index: number) {
  selectedFiles.value.splice(index, 1)
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

async function uploadFiles() {
  uploading.value = true
  // 模拟上传
  await new Promise(r => setTimeout(r, 1500))
  
  // 添加到列表
  for (const file of selectedFiles.value) {
    documents.value.unshift({
      id: Date.now().toString(),
      name: file.name,
      type: file.name.split('.').pop()?.toUpperCase() || 'UNKNOWN',
      size: formatFileSize(file.size),
      status: 'pending',
      uploadTime: new Date().toLocaleString('zh-CN')
    })
  }
  
  stats.value.totalDocs += selectedFiles.value.length
  stats.value.pendingDocs += selectedFiles.value.length
  
  selectedFiles.value = []
  uploading.value = false
  showUploadModal.value = false
}

async function rebuildIndex() {
  rebuilding.value = true
  // 模拟重建
  await new Promise(r => setTimeout(r, 2000))
  rebuilding.value = false
}

function viewDoc(doc: Document) {
  console.log('查看文档:', doc)
}

function deleteDoc(doc: Document) {
  if (confirm(`确定要删除文档「${doc.name}」吗？`)) {
    documents.value = documents.value.filter(d => d.id !== doc.id)
    stats.value.totalDocs--
    if (doc.status === 'indexed') {
      stats.value.indexedDocs--
    } else if (doc.status === 'pending') {
      stats.value.pendingDocs--
    }
  }
}
</script>
