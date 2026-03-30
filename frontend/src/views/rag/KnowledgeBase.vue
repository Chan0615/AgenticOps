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
        <div class="w-80 relative">
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
              <th class="px-4 py-3 text-left text-xs font-semibold text-surface-500 uppercase tracking-wider">分片数</th>
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
                  <div>
                    <span class="text-sm font-medium text-surface-900 block">{{ doc.name }}</span>
                    <span v-if="doc.description" class="text-xs text-surface-400 truncate max-w-[200px] block">{{ doc.description }}</span>
                  </div>
                </div>
              </td>
              <td class="px-4 py-3">
                <span class="text-xs px-2 py-1 bg-surface-100 text-surface-600 rounded-full">{{ doc.type }}</span>
              </td>
              <td class="px-4 py-3 text-sm text-surface-600">{{ doc.size }}</td>
              <td class="px-4 py-3 text-sm text-surface-600">{{ doc.chunk_count || '-' }}</td>
              <td class="px-4 py-3">
                <span 
                  class="text-xs px-2 py-1 rounded-full"
                  :class="{
                    'bg-emerald-50 text-emerald-600': doc.status === 'indexed',
                    'bg-amber-50 text-amber-600': doc.status === 'pending',
                    'bg-blue-50 text-blue-600': doc.status === 'processing',
                    'bg-rose-50 text-rose-600': doc.status === 'error'
                  }"
                >
                  {{ statusText[doc.status] }}
                </span>
              </td>
              <td class="px-4 py-3 text-sm text-surface-500">{{ doc.uploadTime }}</td>
              <td class="px-4 py-3 text-right">
                <div class="flex items-center justify-end gap-1">
                  <button 
                    v-if="doc.status === 'pending' || doc.status === 'error'"
                    @click="processDoc(doc)"
                    class="p-1.5 text-surface-400 hover:text-brand-600 hover:bg-brand-50 rounded-lg transition-colors"
                    title="处理文档"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </button>
                  <button 
                    @click="viewDoc(doc)"
                    class="p-1.5 text-surface-400 hover:text-brand-600 hover:bg-brand-50 rounded-lg transition-colors"
                    title="查看分片"
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
          <button @click="closeUploadModal" class="p-1.5 text-surface-400 hover:text-surface-600 hover:bg-surface-100 rounded-lg transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="p-6 space-y-4">
          <!-- 文档名称 -->
          <div>
            <label class="block text-sm font-medium text-surface-700 mb-1.5">文档名称 <span class="text-rose-500">*</span></label>
            <input 
              v-model="uploadForm.name"
              type="text"
              placeholder="请输入文档名称"
              class="w-full h-10 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
            />
          </div>
          
          <!-- 文档描述 -->
          <div>
            <label class="block text-sm font-medium text-surface-700 mb-1.5">文档描述</label>
            <textarea 
              v-model="uploadForm.description"
              rows="2"
              placeholder="请输入文档描述（可选）"
              class="w-full px-3.5 py-2.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all resize-none"
            ></textarea>
          </div>
          
          <!-- 拖拽上传区域 -->
          <div 
            v-if="!selectedFile"
            class="border-2 border-dashed border-surface-200 rounded-2xl p-6 text-center hover:border-brand-300 hover:bg-brand-50/30 transition-all cursor-pointer"
            @click="$refs.fileInput.click()"
            @dragover.prevent
            @drop.prevent="handleDrop"
          >
            <input 
              ref="fileInput"
              type="file" 
              accept=".txt,.pdf,.doc,.docx,.md"
              class="hidden"
              @change="handleFileSelect"
            />
            <div class="w-12 h-12 rounded-xl bg-brand-50 flex items-center justify-center mx-auto mb-3">
              <svg class="w-6 h-6 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <p class="text-sm font-medium text-surface-700 mb-1">点击或拖拽文件到此处上传</p>
            <p class="text-xs text-surface-400">支持 TXT、PDF、Word、Markdown 格式</p>
          </div>

          <!-- 已选文件 -->
          <div v-if="selectedFile" class="p-3 bg-surface-50 rounded-xl border border-surface-200">
            <div class="flex items-center gap-3">
              <svg class="w-5 h-5 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-surface-900 truncate">{{ selectedFile.name }}</p>
                <p class="text-xs text-surface-400">{{ formatFileSize(selectedFile.size) }}</p>
              </div>
              <button @click="removeFile" class="p-1 text-surface-400 hover:text-rose-500 transition-colors">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
        </div>

        <div class="flex items-center justify-end gap-3 px-6 py-4 border-t border-surface-100">
          <button 
            @click="closeUploadModal"
            class="px-4 py-2 text-sm font-medium text-surface-600 hover:text-surface-900 transition-colors"
          >
            取消
          </button>
          <button 
            @click="uploadFile"
            :disabled="!canUpload"
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
    
    <!-- 分片预览弹窗 -->
    <div v-if="showChunkModal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-xl w-full max-w-3xl max-h-[80vh] flex flex-col animate-fade-in">
        <div class="flex items-center justify-between px-6 py-4 border-b border-surface-100">
          <div>
            <h3 class="text-lg font-semibold text-surface-900">分片预览</h3>
            <p class="text-sm text-surface-400">{{ selectedDoc?.name }} - 共 {{ chunks.length }} 个分片</p>
          </div>
          <button @click="showChunkModal = false" class="p-1.5 text-surface-400 hover:text-surface-600 hover:bg-surface-100 rounded-lg transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="flex-1 overflow-y-auto p-6">
          <div class="space-y-4">
            <div v-for="(chunk, index) in chunks" :key="chunk.id" class="border border-surface-200 rounded-xl overflow-hidden">
              <div class="bg-surface-50 px-4 py-2 border-b border-surface-200 flex items-center justify-between">
                <span class="text-sm font-medium text-surface-700">分片 #{{ chunk.chunk_index + 1 }}</span>
                <span class="text-xs text-surface-400">{{ chunk.char_count }} 字符</span>
              </div>
              <div class="p-4 bg-white">
                <p class="text-sm text-surface-800 leading-relaxed whitespace-pre-wrap">{{ chunk.content }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import api from '@/api'

interface Document {
  id: string
  name: string
  description?: string
  type: string
  size: string
  status: 'indexed' | 'pending' | 'error' | 'processing'
  chunk_count: number
  uploadTime: string
}

interface Chunk {
  id: number
  chunk_index: number
  content: string
  char_count: number
}

const searchQuery = ref('')
const filterStatus = ref('')
const showUploadModal = ref(false)
const selectedFile = ref<File | null>(null)
const uploading = ref(false)
const rebuilding = ref(false)
const showChunkModal = ref(false)
const selectedDoc = ref<Document | null>(null)
const chunks = ref<Chunk[]>([])

const uploadForm = ref({
  name: '',
  description: ''
})

const stats = ref({
  totalDocs: 0,
  indexedDocs: 0,
  pendingDocs: 0,
  totalChunks: 0
})

const statusText: Record<string, string> = {
  indexed: '已索引',
  pending: '待处理',
  processing: '处理中',
  error: '处理失败'
}

const documents = ref<Document[]>([])

const filteredDocs = computed(() => {
  return documents.value.filter(doc => {
    const matchQuery = doc.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchStatus = !filterStatus.value || doc.status === filterStatus.value
    return matchQuery && matchStatus
  })
})

const canUpload = computed(() => {
  return uploadForm.value.name.trim() && selectedFile.value && !uploading.value
})

// 获取文档列表
async function fetchDocuments() {
  try {
    const data = await api.get('/v1/common/knowledge/documents')
    documents.value = data.map((doc: any) => ({
      id: doc.id.toString(),
      name: doc.name,
      description: doc.description,
      type: doc.file_type.toUpperCase(),
      size: formatFileSize(doc.file_size),
      status: doc.status,
      chunk_count: doc.chunk_count,
      uploadTime: new Date(doc.created_at).toLocaleString('zh-CN')
    }))
    updateStats()
  } catch (error) {
    console.error('获取文档列表失败:', error)
  }
}

function updateStats() {
  stats.value.totalDocs = documents.value.length
  stats.value.indexedDocs = documents.value.filter(d => d.status === 'indexed').length
  stats.value.pendingDocs = documents.value.filter(d => d.status === 'pending').length
  stats.value.totalChunks = documents.value.reduce((sum, d) => sum + (d.chunk_count || 0), 0)
}

function handleFileSelect(e: Event) {
  const files = (e.target as HTMLInputElement).files
  if (files && files.length > 0) {
    selectedFile.value = files[0]
    // 自动填充文件名（如果用户未输入）
    if (!uploadForm.value.name) {
      uploadForm.value.name = files[0].name.replace(/\.[^/.]+$/, '')
    }
  }
}

function handleDrop(e: DragEvent) {
  const files = e.dataTransfer?.files
  if (files && files.length > 0) {
    selectedFile.value = files[0]
    if (!uploadForm.value.name) {
      uploadForm.value.name = files[0].name.replace(/\.[^/.]+$/, '')
    }
  }
}

function removeFile() {
  selectedFile.value = null
}

function closeUploadModal() {
  showUploadModal.value = false
  selectedFile.value = null
  uploadForm.value = { name: '', description: '' }
}

function formatFileSize(bytes: number): string {
  if (bytes === 0) return '0 Bytes'
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

async function uploadFile() {
  if (!selectedFile.value) return
  
  uploading.value = true
  
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    formData.append('name', uploadForm.value.name)
    if (uploadForm.value.description) {
      formData.append('description', uploadForm.value.description)
    }
    
    await api.post('/v1/common/knowledge/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    
    await fetchDocuments()
    closeUploadModal()
  } catch (error) {
    console.error('上传失败:', error)
    alert('上传失败，请重试')
  } finally {
    uploading.value = false
  }
}

async function rebuildIndex() {
  rebuilding.value = true
  // 实际项目中这里会调用重建索引的API
  await new Promise(r => setTimeout(r, 2000))
  rebuilding.value = false
}

async function viewDoc(doc: Document) {
  selectedDoc.value = doc
  
  if (doc.status === 'indexed' && doc.chunk_count > 0) {
    try {
      const data = await api.get(`/v1/common/knowledge/documents/${doc.id}/chunks`)
      chunks.value = data
      showChunkModal.value = true
    } catch (error) {
      console.error('获取分片失败:', error)
    }
  } else {
    alert('该文档尚未建立索引，无法预览分片')
  }
}

async function processDoc(doc: Document) {
  try {
    // 更新状态为处理中
    const docIndex = documents.value.findIndex(d => d.id === doc.id)
    if (docIndex !== -1) {
      documents.value[docIndex].status = 'processing'
    }
    
    // 使用更长的超时时间（60秒）
    await api.post(`/v1/common/knowledge/documents/${doc.id}/process`, null, {
      timeout: 60000
    })
    
    alert('文档处理完成')
    await fetchDocuments()
  } catch (error: any) {
    console.error('处理失败:', error)
    if (error.code === 'ECONNABORTED') {
      alert('处理时间较长，请稍后刷新查看处理结果')
    } else {
      alert('处理失败，请重试')
    }
    await fetchDocuments() // 刷新状态
  }
}

async function deleteDoc(doc: Document) {
  if (confirm(`确定要删除文档「${doc.name}」吗？`)) {
    try {
      await api.delete(`/v1/common/knowledge/documents/${doc.id}`)
      await fetchDocuments()
    } catch (error) {
      console.error('删除失败:', error)
      alert('删除失败，请重试')
    }
  }
}

// 初始化加载
fetchDocuments()
</script>
