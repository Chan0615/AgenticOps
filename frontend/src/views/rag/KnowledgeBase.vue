<template>
  <div class="kb-page ant-illustration-page">
    <div class="kb-layout">
      <!-- 左侧知识库列表 -->
      <div class="kb-sidebar">
        <div class="kb-sidebar-header">
          <span class="kb-sidebar-title">知识库</span>
          <Button type="primary" size="small" @click="openCreateKBModal">新建</Button>
        </div>
        <div class="kb-sidebar-list">
          <Spin v-if="kbLoading" style="display: block; text-align: center; padding: 32px 0" />
          <div v-else-if="!knowledgeBases.length" class="kb-sidebar-empty">
            暂无知识库，请点击「新建」创建
          </div>
          <div
            v-for="kb in knowledgeBases"
            :key="kb.id"
            class="kb-sidebar-item"
            :class="{ active: selectedKB?.id === kb.id }"
            @click="selectKB(kb)"
          >
            <div class="kb-sidebar-item-row">
              <div class="kb-sidebar-item-name">{{ kb.name }}</div>
              <div class="kb-sidebar-item-meta">
                <span>{{ kb.document_count }} 文档</span>
                <span>·</span>
                <span>{{ kb.chunk_count }} 片段</span>
              </div>
            </div>
            <div v-if="kb.description" class="kb-sidebar-item-desc">{{ kb.description }}</div>
            <div class="kb-sidebar-item-actions" @click.stop>
              <Button type="text" size="small" @click="openEditKBModal(kb)">编辑</Button>
              <Popconfirm title="确定删除该知识库？删除后不可恢复。" @confirm="handleDeleteKB(kb.id)">
                <Button type="text" size="small" danger>删除</Button>
              </Popconfirm>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧主区域 -->
      <div class="kb-main">
        <!-- 未选中状态 -->
        <div v-if="!selectedKB" class="kb-main-empty">
          <div class="kb-main-empty-icon">
            <DatabaseOutlined style="font-size: 48px; color: #cbd5e1" />
          </div>
          <div class="kb-main-empty-text">请从左侧选择一个知识库</div>
        </div>

        <!-- 已选中 -->
        <template v-else>
          <!-- 统计卡片 -->
          <Row :gutter="16" class="kb-stats-row">
            <Col :span="6">
              <Card :bordered="false" class="kb-stat-card">
                <Statistic title="文档总数" :value="kbStats.document_count" :value-style="{ color: '#1677ff' }">
                  <template #prefix><FileTextOutlined /></template>
                </Statistic>
              </Card>
            </Col>
            <Col :span="6">
              <Card :bordered="false" class="kb-stat-card">
                <Statistic title="片段总数" :value="kbStats.chunk_count" :value-style="{ color: '#722ed1' }">
                  <template #prefix><BlockOutlined /></template>
                </Statistic>
              </Card>
            </Col>
            <Col :span="6">
              <Card :bordered="false" class="kb-stat-card">
                <Statistic title="已索引片段" :value="kbStats.indexed_chunks" :value-style="{ color: '#52c41a' }">
                  <template #prefix><CheckCircleOutlined /></template>
                </Statistic>
              </Card>
            </Col>
            <Col :span="6">
              <Card :bordered="false" class="kb-stat-card">
                <Statistic title="已索引文档" :value="kbStats.indexed_docs" :value-style="{ color: '#13c2c2' }">
                  <template #prefix><FolderOpenOutlined /></template>
                </Statistic>
              </Card>
            </Col>
          </Row>

          <!-- 工具栏 -->
          <Card :bordered="false" class="kb-toolbar-card">
            <Space>
              <Button type="primary" @click="openUploadModal">上传文档</Button>
              <Button @click="openAddTextModal">添加文本</Button>
            </Space>
          </Card>

          <!-- 文档列表 -->
          <Card :bordered="false" class="kb-doc-card">
            <Table
              :columns="docColumns"
              :data-source="documents"
              :loading="docLoading"
              :pagination="false"
              row-key="id"
              size="middle"
            >
              <template #bodyCell="{ column, record }">
                <template v-if="column.key === 'title'">
                  <span class="doc-title">{{ record.title }}</span>
                </template>
                <template v-else-if="column.key === 'doc_type'">
                  <Tag :color="docTypeColor(record.doc_type)">{{ record.doc_type }}</Tag>
                </template>
                <template v-else-if="column.key === 'chunk_count'">
                  {{ record.chunk_count ?? 0 }}
                </template>
                <template v-else-if="column.key === 'status'">
                  <Badge
                    :status="record.status ? 'success' : 'warning'"
                    :text="record.status ? '已索引' : '未索引'"
                  />
                </template>
                <template v-else-if="column.key === 'created_at'">
                  {{ dayjs(record.created_at).format('YYYY-MM-DD HH:mm') }}
                </template>
                <template v-else-if="column.key === 'action'">
                  <Space>
                    <Button type="link" size="small" @click="handleViewChunks(record)">片段</Button>
                    <Button type="link" size="small" :loading="reindexingId === record.id" @click="handleReindex(record)">
                      重新索引
                    </Button>
                    <Popconfirm title="确定删除此文档？" @confirm="handleDeleteDoc(record.id)">
                      <Button type="link" size="small" danger>删除</Button>
                    </Popconfirm>
                  </Space>
                </template>
              </template>
              <template #emptyText>
                <div class="kb-doc-empty">暂无文档，请点击「上传文档」或「添加文本」</div>
              </template>
            </Table>
          </Card>
        </template>
      </div>
    </div>

    <!-- 创建/编辑知识库弹窗 -->
    <Modal
      v-model:open="kbModalVisible"
      :title="kbModalMode === 'create' ? '新建知识库' : '编辑知识库'"
      :confirm-loading="kbSubmitting"
      @ok="handleKBSubmit"
    >
      <Form ref="kbFormRef" :model="kbFormData" :rules="kbFormRules" layout="vertical" style="margin-top: 16px">
        <FormItem label="知识库名称" name="name">
          <Input v-model:value="kbFormData.name" placeholder="请输入知识库名称" />
        </FormItem>
        <FormItem label="描述" name="description">
          <Textarea v-model:value="kbFormData.description" :rows="3" placeholder="请输入描述（可选）" />
        </FormItem>
      </Form>
    </Modal>

    <!-- 上传文档弹窗 -->
    <Modal
      v-model:open="uploadModalVisible"
      title="上传文档"
      :confirm-loading="uploading"
      ok-text="开始上传"
      @ok="handleUpload"
    >
      <div class="upload-area" style="margin-top: 16px">
        <UploadDragger
          v-model:fileList="uploadFileList"
          :before-upload="beforeUpload"
          :max-count="1"
          accept=".txt,.md,.pdf,.docx"
        >
          <p class="ant-upload-drag-icon">
            <InboxOutlined />
          </p>
          <p class="ant-upload-text">点击或拖拽文件到此处上传</p>
          <p class="ant-upload-hint">支持 .txt, .md, .pdf, .docx 格式</p>
        </UploadDragger>
        <div class="upload-option">
          <Checkbox v-model:checked="useLlmSplit">使用 LLM 语义切分</Checkbox>
          <span class="upload-option-hint">开启后由大模型进行语义分段，切分质量更高但速度较慢</span>
        </div>
      </div>
    </Modal>

    <!-- 添加文本弹窗 -->
    <Modal
      v-model:open="textModalVisible"
      title="添加文本"
      :confirm-loading="textSubmitting"
      @ok="handleAddText"
    >
      <Form ref="textFormRef" :model="textFormData" :rules="textFormRules" layout="vertical" style="margin-top: 16px">
        <FormItem label="标题" name="title">
          <Input v-model:value="textFormData.title" placeholder="请输入文档标题" />
        </FormItem>
        <FormItem label="内容" name="content">
          <Textarea v-model:value="textFormData.content" :rows="8" placeholder="请输入文档内容" />
        </FormItem>
        <FormItem label="来源" name="source">
          <Input v-model:value="textFormData.source" placeholder="来源标注（可选）" />
        </FormItem>
      </Form>
    </Modal>

    <!-- 查看片段抽屉 -->
    <Drawer
      v-model:open="chunksDrawerVisible"
      :title="`文档片段 — ${chunksDocTitle}`"
      :width="640"
      placement="right"
    >
      <div v-if="chunksLoading" style="text-align: center; padding: 48px 0">
        <Spin tip="加载中..." />
      </div>
      <div v-else-if="!chunksList.length" style="text-align: center; padding: 48px 0; color: #94a3b8">
        暂无片段数据
      </div>
      <div v-else>
        <div style="margin-bottom: 12px; font-size: 13px; color: #64748b">
          共 {{ chunksList.length }} 个片段
        </div>
        <div class="chunks-list">
          <div v-for="chunk in chunksList" :key="chunk.id" class="chunk-item">
            <div class="chunk-header">
              <Tag color="blue">片段 {{ chunk.chunk_index + 1 }}</Tag>
              <span class="chunk-chars">{{ chunk.char_count }} 字</span>
            </div>
            <div class="chunk-content">{{ chunk.content }}</div>
          </div>
        </div>
      </div>
    </Drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import {
  Badge,
  Button,
  Card,
  Checkbox,
  Col,
  Drawer,
  Form,
  Input,
  Modal,
  Popconfirm,
  Row,
  Space,
  Spin,
  Statistic,
  Table,
  Tag,
  Upload,
  message,
} from 'ant-design-vue'
import {
  BlockOutlined,
  CheckCircleOutlined,
  DatabaseOutlined,
  FileTextOutlined,
  FolderOpenOutlined,
  InboxOutlined,
} from '@ant-design/icons-vue'
import dayjs from 'dayjs'
import { ragApi, type KnowledgeBase, type KBStats, type Document } from '@/api/agent/index'

const FormItem = Form.Item
const Textarea = Input.TextArea
const UploadDragger = Upload.Dragger

// ============ 知识库列表 ============
const kbLoading = ref(false)
const knowledgeBases = ref<KnowledgeBase[]>([])
const selectedKB = ref<KnowledgeBase | null>(null)

const loadKnowledgeBases = async () => {
  kbLoading.value = true
  try {
    knowledgeBases.value = await ragApi.getKnowledgeBases()
  } catch {
    knowledgeBases.value = []
    message.error('加载知识库列表失败')
  } finally {
    kbLoading.value = false
  }
}

const selectKB = async (kb: KnowledgeBase) => {
  selectedKB.value = kb
  await Promise.all([loadKBStats(kb.id), loadDocuments(kb.id)])
}

// ============ 知识库统计 ============
const kbStats = reactive<KBStats>({
  kb_id: 0,
  name: '',
  document_count: 0,
  chunk_count: 0,
  indexed_chunks: 0,
  indexed_docs: 0,
})

const loadKBStats = async (kbId: number) => {
  try {
    const data = await ragApi.getKBStats(kbId)
    Object.assign(kbStats, data)
  } catch {
    kbStats.document_count = 0
    kbStats.chunk_count = 0
    kbStats.indexed_chunks = 0
    kbStats.indexed_docs = 0
  }
}

// ============ 文档列表 ============
const docLoading = ref(false)
const documents = ref<Document[]>([])

const docColumns = [
  { title: '标题', dataIndex: 'title', key: 'title', ellipsis: true },
  { title: '类型', dataIndex: 'doc_type', key: 'doc_type', width: 100 },
  { title: '片段数', dataIndex: 'chunk_count', key: 'chunk_count', width: 100, align: 'center' as const },
  { title: '状态', key: 'status', width: 120 },
  { title: '创建时间', key: 'created_at', width: 180 },
  { title: '操作', key: 'action', width: 180, fixed: 'right' as const },
]

const loadDocuments = async (kbId: number) => {
  docLoading.value = true
  try {
    documents.value = await ragApi.getDocuments(kbId)
  } catch {
    documents.value = []
    message.error('加载文档列表失败')
  } finally {
    docLoading.value = false
  }
}

const docTypeColor = (docType: string) => {
  const map: Record<string, string> = {
    pdf: 'red',
    txt: 'blue',
    md: 'green',
    docx: 'orange',
    markdown: 'green',
    text: 'blue',
  }
  return map[docType?.toLowerCase()] || 'default'
}

// ============ 创建/编辑知识库 ============
const kbModalVisible = ref(false)
const kbModalMode = ref<'create' | 'edit'>('create')
const kbSubmitting = ref(false)
const kbFormRef = ref()
const editingKBId = ref<number | null>(null)

const kbFormData = reactive({
  name: '',
  description: '',
})

const kbFormRules = {
  name: [{ required: true, message: '请输入知识库名称' }],
}

const openCreateKBModal = () => {
  kbModalMode.value = 'create'
  editingKBId.value = null
  kbFormData.name = ''
  kbFormData.description = ''
  kbModalVisible.value = true
}

const openEditKBModal = (kb: KnowledgeBase) => {
  kbModalMode.value = 'edit'
  editingKBId.value = kb.id
  kbFormData.name = kb.name
  kbFormData.description = kb.description || ''
  kbModalVisible.value = true
}

const handleKBSubmit = async () => {
  try {
    await kbFormRef.value?.validateFields()
  } catch {
    return
  }
  kbSubmitting.value = true
  try {
    if (kbModalMode.value === 'create') {
      await ragApi.createKnowledgeBase({
        name: kbFormData.name,
        description: kbFormData.description || undefined,
      })
      message.success('知识库创建成功')
    } else if (editingKBId.value !== null) {
      const updated = await ragApi.updateKnowledgeBase(editingKBId.value, {
        name: kbFormData.name,
        description: kbFormData.description || undefined,
      })
      // If editing the currently selected KB, refresh it
      if (selectedKB.value?.id === editingKBId.value) {
        selectedKB.value = updated
      }
      message.success('知识库更新成功')
    }
    kbModalVisible.value = false
    await loadKnowledgeBases()
  } catch (err: any) {
    message.error(err?.response?.data?.detail || '操作失败')
  } finally {
    kbSubmitting.value = false
  }
}

const handleDeleteKB = async (id: number) => {
  try {
    await ragApi.deleteKnowledgeBase(id)
    message.success('删除成功')
    if (selectedKB.value?.id === id) {
      selectedKB.value = null
      documents.value = []
    }
    await loadKnowledgeBases()
  } catch (err: any) {
    message.error(err?.response?.data?.detail || '删除失败')
  }
}

// ============ 上传文档 ============
const uploadModalVisible = ref(false)
const uploading = ref(false)
const uploadFileList = ref<any[]>([])
const useLlmSplit = ref(true)

const openUploadModal = () => {
  uploadFileList.value = []
  useLlmSplit.value = true
  uploadModalVisible.value = true
}

const beforeUpload = () => {
  // Prevent auto upload; we handle it manually
  return false
}

const handleUpload = async () => {
  if (!selectedKB.value) return
  if (!uploadFileList.value.length) {
    message.warning('请选择要上传的文件')
    return
  }
  const file = uploadFileList.value[0].originFileObj || uploadFileList.value[0]
  uploading.value = true
  try {
    const res = await ragApi.uploadDocument(selectedKB.value.id, file, useLlmSplit.value)
    message.success(res.message || '上传成功')
    uploadModalVisible.value = false
    await refreshCurrentKB()
  } catch (err: any) {
    message.error(err?.response?.data?.detail || '上传失败')
  } finally {
    uploading.value = false
  }
}

// ============ 添加文本 ============
const textModalVisible = ref(false)
const textSubmitting = ref(false)
const textFormRef = ref()

const textFormData = reactive({
  title: '',
  content: '',
  source: '',
})

const textFormRules = {
  title: [{ required: true, message: '请输入文档标题' }],
  content: [{ required: true, message: '请输入文档内容' }],
}

const openAddTextModal = () => {
  textFormData.title = ''
  textFormData.content = ''
  textFormData.source = ''
  textModalVisible.value = true
}

const handleAddText = async () => {
  if (!selectedKB.value) return
  try {
    await textFormRef.value?.validateFields()
  } catch {
    return
  }
  textSubmitting.value = true
  try {
    await ragApi.createDocument(selectedKB.value.id, {
      title: textFormData.title,
      content: textFormData.content,
      source: textFormData.source || undefined,
    })
    message.success('文档添加成功')
    textModalVisible.value = false
    await refreshCurrentKB()
  } catch (err: any) {
    message.error(err?.response?.data?.detail || '添加失败')
  } finally {
    textSubmitting.value = false
  }
}

// ============ 文档操作 ============
const reindexingId = ref<number | null>(null)

const handleReindex = async (doc: Document) => {
  reindexingId.value = doc.id
  try {
    const res = await ragApi.reindexDocument(doc.id)
    message.success(res.message || '重新索引成功')
    await refreshCurrentKB()
  } catch (err: any) {
    message.error(err?.response?.data?.detail || '重新索引失败')
  } finally {
    reindexingId.value = null
  }
}

const handleDeleteDoc = async (docId: number) => {
  try {
    await ragApi.deleteDocument(docId)
    message.success('文档已删除')
    await refreshCurrentKB()
  } catch (err: any) {
    message.error(err?.response?.data?.detail || '删除失败')
  }
}

// ============ 查看片段 ============
const chunksDrawerVisible = ref(false)
const chunksLoading = ref(false)
const chunksDocTitle = ref('')
const chunksList = ref<{ id: number; chunk_index: number; content: string; char_count: number }[]>([])

const handleViewChunks = async (doc: Document) => {
  chunksDocTitle.value = doc.title
  chunksDrawerVisible.value = true
  chunksLoading.value = true
  try {
    const res = await ragApi.getDocumentChunks(doc.id)
    chunksList.value = res.chunks || []
  } catch {
    chunksList.value = []
    message.error('加载片段失败')
  } finally {
    chunksLoading.value = false
  }
}

// ============ 辅助 ============
const refreshCurrentKB = async () => {
  if (!selectedKB.value) return
  await Promise.all([
    loadKBStats(selectedKB.value.id),
    loadDocuments(selectedKB.value.id),
    loadKnowledgeBases(),
  ])
}

// ============ 初始化 ============
onMounted(() => {
  loadKnowledgeBases()
})
</script>

<style scoped>
.kb-page {
  height: 100%;
}

.kb-layout {
  display: flex;
  height: 100%;
  gap: 16px;
}

/* ---- 左侧边栏 ---- */
.kb-sidebar {
  width: 220px;
  min-width: 220px;
  background: #fff;
  border: 1px solid #f0f0f0;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.kb-sidebar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  border-bottom: 1px solid #f0f0f0;
}

.kb-sidebar-title {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.kb-sidebar-list {
  flex: 1;
  overflow-y: auto;
  padding: 6px;
}

.kb-sidebar-empty {
  text-align: center;
  color: #94a3b8;
  font-size: 12px;
  padding: 32px 12px;
}

.kb-sidebar-item {
  position: relative;
  padding: 8px 10px;
  border-radius: 8px;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.2s;
  margin-bottom: 2px;
}

.kb-sidebar-item:hover {
  background: #f8fafc;
  border-color: #e2e8f0;
}

.kb-sidebar-item.active {
  background: #eff6ff;
  border-color: #bfdbfe;
}

.kb-sidebar-item-row {
  display: flex;
  align-items: baseline;
  gap: 8px;
}

.kb-sidebar-item-name {
  font-size: 13px;
  font-weight: 500;
  color: #1f2937;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex-shrink: 0;
}

.kb-sidebar-item-meta {
  display: flex;
  gap: 4px;
  font-size: 11px;
  color: #94a3b8;
  white-space: nowrap;
  flex-shrink: 0;
}

.kb-sidebar-item-desc {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 2px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.kb-sidebar-item-actions {
  display: none;
  position: absolute;
  right: 4px;
  bottom: 4px;
  gap: 0;
  background: inherit;
}

.kb-sidebar-item:hover .kb-sidebar-item-actions {
  display: flex;
}

/* ---- 右侧主区域 ---- */
.kb-main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
}

.kb-main-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #fff;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
}

.kb-main-empty-icon {
  margin-bottom: 16px;
}

.kb-main-empty-text {
  font-size: 14px;
  color: #94a3b8;
}

/* ---- 统计卡片 ---- */
.kb-stats-row {
  flex-shrink: 0;
}

.kb-stat-card {
  border: 1px solid #f0f0f0;
  border-radius: 8px;
}

/* ---- 工具栏 ---- */
.kb-toolbar-card {
  flex-shrink: 0;
  border-radius: 8px;
}

/* ---- 文档表格 ---- */
.kb-doc-card {
  flex: 1;
  min-height: 0;
  border-radius: 8px;
}

.doc-title {
  font-weight: 500;
  color: #1f2937;
}

.kb-doc-empty {
  padding: 48px 0;
  text-align: center;
  color: #94a3b8;
  font-size: 13px;
}

/* ---- 上传选项 ---- */
.upload-option {
  margin-top: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.upload-option-hint {
  font-size: 12px;
  color: #94a3b8;
}

/* ---- 片段列表 ---- */
.chunks-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chunk-item {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  overflow: hidden;
  transition: border-color 0.2s;
}

.chunk-item:hover {
  border-color: #93c5fd;
}

.chunk-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 14px;
  background: #fff;
  border-bottom: 1px solid #f1f5f9;
}

.chunk-chars {
  font-size: 11px;
  color: #94a3b8;
}

.chunk-content {
  padding: 12px 14px;
  font-size: 13px;
  line-height: 1.7;
  color: #334155;
  white-space: pre-wrap;
  word-break: break-word;
  max-height: 200px;
  overflow-y: auto;
}
</style>
