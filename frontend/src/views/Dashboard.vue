<template>
  <div class="dashboard-page ant-illustration-page">
    <Card :bordered="false" class="hero-card">
      <Row :gutter="16" align="middle" justify="space-between">
        <Col :xs="24" :lg="8">
          <TypographyText class="hero-subtitle">AGENTICOPS</TypographyText>
          <TypographyTitle :level="2" class="hero-title">运营概览</TypographyTitle>
        </Col>
        <Col :xs="24" :lg="8">
          <div class="hero-center">
            <div class="hero-clock-card">
              <div class="hero-clock-head">
                <span class="hero-clock-dot"></span>
                <span>Live</span>
              </div>
              <div class="hero-clock-time">{{ liveTime }}</div>
              <div class="hero-clock-date">{{ liveDate }}</div>
              <div class="hero-clock-scope">{{ scopeLabel }}</div>
            </div>
          </div>
        </Col>
        <Col :xs="24" :lg="8">
          <Space direction="vertical" size="small" align="end" class="hero-actions">
            <div class="rate-pill">
              <span>任务成功率</span>
              <strong>{{ successRate }}%</strong>
            </div>
            <Button class="refresh-btn" :loading="loading" @click="loadDashboard">刷新数据</Button>
            <TypographyText class="hero-date">更新于 {{ lastUpdatedText }}</TypographyText>
          </Space>
        </Col>
      </Row>
    </Card>

    <Card :bordered="false" class="section-gap">
      <Row :gutter="12" align="middle" class="filter-row">
        <Col :xs="24" :lg="9">
          <Space wrap>
            <Select
              v-model:value="selectedProjectId"
              allow-clear
              placeholder="选择项目"
              style="width: 220px"
              @change="handleProjectChange"
            >
              <SelectOption v-for="project in projectOptions" :key="project.id" :value="project.id">
                {{ project.name }}
              </SelectOption>
            </Select>
            <Select v-model:value="selectedGroupId" allow-clear placeholder="选择分组" style="width: 220px">
              <SelectOption v-for="group in groupOptions" :key="group.id" :value="group.id">
                {{ group.name }}
              </SelectOption>
            </Select>
          </Space>
        </Col>
        <Col :xs="24" :lg="9">
          <div class="quick-actions">
            <span class="quick-inline-label">快捷入口</span>
            <div class="quick-pill-wrap">
              <button
                v-for="entry in displayedQuickEntries"
                :key="entry.path"
                type="button"
                class="quick-pill"
                :class="`quick-pill-${entry.tone}`"
                @click="router.push(entry.path)"
              >
                <span class="quick-pill-icon"><component :is="entry.icon" /></span>
                <span>{{ entry.name }}</span>
              </button>
            </div>
          </div>
        </Col>
        <Col :xs="24" :lg="6">
          <Space class="filter-actions">
            <Button type="primary" :loading="loading" @click="loadDashboard">应用筛选</Button>
            <Button @click="resetFilters">重置</Button>
          </Space>
        </Col>
      </Row>

      <div class="ai-entry" @click="router.push('/assistant')">
        <div class="ai-entry-main">
          <div class="ai-entry-left">
            <div class="ai-entry-badge">AI助手</div>
            <div class="ai-entry-title">进入 AI助手</div>
          </div>
          <div class="ai-entry-center">智能回答，脚本辅助</div>
          <div class="ai-entry-right">
            <div class="ai-entry-go">立即进入</div>
          </div>
        </div>
      </div>
    </Card>

    <Row :gutter="8" class="section-gap">
      <Col v-for="item in kpis" :key="item.label" :xs="12" :sm="8" :md="6" :lg="6" :xl="3">
        <Card :bordered="false" class="kpi-card">
          <Statistic :title="item.label" :value="item.value" />
          <span class="kpi-hint" :style="{ color: item.color }">{{ item.hint }}</span>
        </Card>
      </Col>
    </Row>

    <Row :gutter="12" class="section-gap">
      <Col :xs="24" :lg="12">
        <Card :bordered="false" title="近7天执行趋势" class="trend-card">
          <div ref="runTrendChartRef" class="trend-chart"></div>
        </Card>
      </Col>
      <Col :xs="24" :lg="12">
        <Card :bordered="false" title="近7天失败趋势" class="trend-card">
          <div ref="failTrendChartRef" class="trend-chart"></div>
        </Card>
      </Col>
    </Row>

    <Row :gutter="12" class="section-gap">
      <Col :xs="24" :lg="8">
        <Card :bordered="false" title="系统公告" class="list-card">
          <template #extra>
            <Button type="link" size="small" @click="openNoticeManager">维护信息</Button>
          </template>
          <List :data-source="notices" :split="false">
            <template #renderItem="{ item }">
              <ListItem>
                <ListItemMeta :description="item.time">
                  <template #title>
                    <div class="notice-line">{{ item.content ? `${item.title} · ${item.content}` : item.title }}</div>
                  </template>
                </ListItemMeta>
              </ListItem>
            </template>
          </List>
        </Card>
      </Col>
      <Col :xs="24" :lg="8">
        <Card :bordered="false" title="运行态势" class="list-card">
          <List :data-source="health" :split="false">
            <template #renderItem="{ item }">
              <ListItem>
                <Space direction="vertical" size="small" class="health-stack">
                  <Space class="health-row">
                    <TypographyText>{{ item.name }}</TypographyText>
                    <Tag :color="item.color">{{ item.status }}</Tag>
                  </Space>
                  <TypographyText type="secondary">{{ item.desc }}</TypographyText>
                </Space>
              </ListItem>
            </template>
          </List>
        </Card>
      </Col>
      <Col :xs="24" :lg="8">
        <Card :bordered="false" title="系统脉冲" class="list-card pulse-card">
          <div class="pulse-scroll">
            <Timeline>
              <TimelineItem v-for="event in events" :key="event.id" :color="event.color">
                <Button type="link" class="event-link" @click="jumpToLogDetail(event.log_id)">{{ event.title }}</Button>
                <br />
                <TypographyText type="secondary">{{ event.time }}</TypographyText>
              </TimelineItem>
            </Timeline>
          </div>
        </Card>
      </Col>
    </Row>

    <Modal
      v-model:open="noticeManageVisible"
      title="维护公告信息"
      width="760px"
      :confirm-loading="noticeSubmitting"
      @ok="saveNotice"
      ok-text="保存"
      cancel-text="关闭"
    >
      <div class="notice-form">
        <Input v-model:value="noticeTitle" placeholder="公告标题" />
        <InputTextArea v-model:value="noticeContent" :rows="3" placeholder="公告内容（可选）" />
        <Space>
          <TypographyText>启用显示</TypographyText>
          <Switch v-model:checked="noticeEnabled" />
          <Button v-if="editingNoticeId" size="small" @click="resetNoticeForm">取消编辑</Button>
        </Space>
      </div>

      <List :loading="noticeListLoading" :data-source="noticeItems" class="notice-manage-list">
        <template #renderItem="{ item }">
          <ListItem>
            <ListItemMeta>
              <template #title>
                <Space>
                  <TypographyText>{{ item.title }}</TypographyText>
                  <Tag :color="item.enabled ? 'green' : 'default'">{{ item.enabled ? '启用' : '停用' }}</Tag>
                </Space>
              </template>
              <template #description>
                <div>{{ item.content || '无内容' }}</div>
                <TypographyText type="secondary">更新于 {{ item.updated_at }}</TypographyText>
              </template>
            </ListItemMeta>
            <Space>
              <Button size="small" @click="editNotice(item)">编辑</Button>
              <Popconfirm title="确认删除该公告？" ok-text="删除" cancel-text="取消" @confirm="removeNotice(item.id)">
                <Button size="small" danger>删除</Button>
              </Popconfirm>
            </Space>
          </ListItem>
        </template>
      </List>
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import dayjs from 'dayjs'
import * as echarts from 'echarts'
import {
  AppstoreOutlined,
  BookOutlined,
  ClockCircleOutlined,
  CodeOutlined,
  DesktopOutlined,
  FileTextOutlined,
} from '@ant-design/icons-vue'
import { Button, Card, Col, Input, List, Modal, Popconfirm, Row, Select, Space, Statistic, Switch, Tag, Timeline, Typography, message } from 'ant-design-vue'
import { getGroupList, getProjectList, type OpsGroup, type OpsProject } from '@/api/ops/group'
import {
  createDashboardNotice,
  deleteDashboardNotice,
  getDashboardNotices,
  getDashboardOverview,
  updateDashboardNotice,
  type DashboardEvent,
  type DashboardHealthItem,
  type DashboardNotice,
  type DashboardNoticeItem,
} from '@/api/ops/dashboard'

const router = useRouter()

const SelectOption = Select.Option
const ListItem = List.Item
const ListItemMeta = List.Item.Meta
const TimelineItem = Timeline.Item
const TypographyText = Typography.Text
const TypographyTitle = Typography.Title
const InputTextArea = Input.TextArea

const loading = ref(false)
const dashboardPrimary = '#ec4899'
const dashboardPrimaryLight = '#f472b6'
const dashboardPrimarySoft = 'rgba(236, 72, 153, 0.18)'
const scopeLabel = ref('全局')
const lastUpdatedText = ref(dayjs().format('YYYY-MM-DD HH:mm:ss'))
const liveNow = ref(dayjs())
const selectedProjectId = ref<number | undefined>(undefined)
const selectedGroupId = ref<number | undefined>(undefined)
const projectOptions = ref<OpsProject[]>([])
const groupOptions = ref<OpsGroup[]>([])
let clockTimer: number | null = null

const liveTime = computed(() => liveNow.value.format('HH:mm:ss'))
const liveDate = computed(() => liveNow.value.format('YYYY-MM-DD dddd'))

const buildDefaultDates = () =>
  Array.from({ length: 7 }, (_, i) => dayjs().subtract(6 - i, 'day').format('MM-DD'))

const trends = ref({
  dates: buildDefaultDates(),
  totalRuns: Array(7).fill(0),
  failedRuns: Array(7).fill(0),
})

const runTrendChartRef = ref<HTMLDivElement | null>(null)
const failTrendChartRef = ref<HTMLDivElement | null>(null)
let runTrendChart: echarts.ECharts | null = null
let failTrendChart: echarts.ECharts | null = null

const stats = ref({
  activeUsers: 0,
  totalUsers: 0,
  knowledgeBases: 0,
  docs: 0,
  indexedDocs: 0,
  servers: 0,
  onlineServers: 0,
  todayRuns: 0,
  failedRuns: 0,
  chats: 0,
  chunks: 0,
  enabledTasks: 0,
  totalTasks: 0,
})

const successRate = computed(() => {
  if (!stats.value.todayRuns) return '100.0'
  return (((stats.value.todayRuns - stats.value.failedRuns) / stats.value.todayRuns) * 100).toFixed(1)
})

const kpis = computed(() => [
  { label: '活跃用户', value: stats.value.activeUsers, hint: `总计 ${stats.value.totalUsers}`, color: '#2563eb' },
  {
    label: '知识文档',
    value: stats.value.docs,
    hint: `${stats.value.knowledgeBases} 库 / ${stats.value.indexedDocs} 已索引`,
    color: '#16a34a',
  },
  { label: '运维主机', value: stats.value.servers, hint: `在线 ${stats.value.onlineServers}`, color: '#0891b2' },
  { label: '今日会话', value: stats.value.chats, hint: 'AI 请求', color: '#d97706' },
  { label: '执行总量', value: stats.value.todayRuns, hint: '今日任务', color: '#475569' },
  { label: '失败次数', value: stats.value.failedRuns, hint: '需关注', color: '#e11d48' },
  { label: '向量片段', value: stats.value.chunks, hint: '检索基座', color: '#7c3aed' },
  { label: '启用任务', value: stats.value.enabledTasks, hint: `总计 ${stats.value.totalTasks}`, color: '#0f766e' },
])

const quickEntries = [
  { name: '服务器列表', path: '/ops/servers', icon: DesktopOutlined, tone: 'ops' },
  { name: '脚本管理', path: '/ops/scripts', icon: CodeOutlined, tone: 'script' },
  { name: '定时任务', path: '/ops/tasks', icon: ClockCircleOutlined, tone: 'task' },
  { name: '执行日志', path: '/ops/logs', icon: FileTextOutlined, tone: 'log' },
  { name: '项目分组', path: '/ops/groups', icon: AppstoreOutlined, tone: 'group' },
  { name: '知识库管理', path: '/rag/knowledge', icon: BookOutlined, tone: 'kb' },
]
const displayedQuickEntries = computed(() => quickEntries.slice(0, 6))

const notices = ref<DashboardNotice[]>([{ id: 0, title: '暂无公告', time: '刚刚', source: 'system' }])
const noticeManageVisible = ref(false)
const noticeListLoading = ref(false)
const noticeSubmitting = ref(false)
const noticeItems = ref<DashboardNoticeItem[]>([])
const editingNoticeId = ref<number | null>(null)
const noticeTitle = ref('')
const noticeContent = ref('')
const noticeEnabled = ref(true)
const events = ref<DashboardEvent[]>([{ id: 0, log_id: 0, title: '暂无执行记录', time: '刚刚', color: 'blue' }])
const health = ref<DashboardHealthItem[]>([
  { name: '计划任务调度', status: '待检测', color: 'gold', desc: '等待实时数据' },
])

const renderRunTrendChart = () => {
  if (!runTrendChartRef.value) return
  if (!runTrendChart) {
    runTrendChart = echarts.init(runTrendChartRef.value)
  }
  runTrendChart.setOption({
    grid: { left: 36, right: 20, top: 24, bottom: 26 },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: trends.value.dates },
    yAxis: { type: 'value', minInterval: 1 },
    series: [
      {
        name: '执行量',
        type: 'line',
        smooth: true,
        data: trends.value.totalRuns,
        areaStyle: { color: dashboardPrimarySoft },
        lineStyle: { width: 3, color: dashboardPrimary },
        itemStyle: { color: dashboardPrimaryLight },
      },
    ],
  })
}

const renderFailTrendChart = () => {
  if (!failTrendChartRef.value) return
  if (!failTrendChart) {
    failTrendChart = echarts.init(failTrendChartRef.value)
  }
  failTrendChart.setOption({
    grid: { left: 36, right: 20, top: 24, bottom: 26 },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: trends.value.dates },
    yAxis: { type: 'value', minInterval: 1 },
    series: [
      {
        name: '失败量',
        type: 'bar',
        data: trends.value.failedRuns,
        itemStyle: { color: '#f43f5e' },
        barMaxWidth: 28,
      },
    ],
  })
}

const resizeCharts = () => {
  runTrendChart?.resize()
  failTrendChart?.resize()
}

const loadProjects = async () => {
  try {
    const res = await getProjectList({ page: 1, page_size: 200 })
    projectOptions.value = res.data || []
  } catch {
    message.error('项目列表加载失败')
  }
}

const loadGroups = async (projectId?: number) => {
  try {
    const res = await getGroupList({ page: 1, page_size: 500, project_id: projectId })
    groupOptions.value = res.data || []
  } catch {
    message.error('分组列表加载失败')
  }
}

const handleProjectChange = async () => {
  selectedGroupId.value = undefined
  await loadGroups(selectedProjectId.value)
}

const resetFilters = async () => {
  selectedProjectId.value = undefined
  selectedGroupId.value = undefined
  await loadGroups()
  await loadDashboard()
}

const loadDashboard = async () => {
  loading.value = true
  try {
    const params: { project_id?: number; group_id?: number } = {}
    if (selectedProjectId.value) params.project_id = selectedProjectId.value
    if (selectedGroupId.value) params.group_id = selectedGroupId.value

    const res = await getDashboardOverview(params)
    const summary = res.data.summary
    const filters = res.data.filters || {}
    scopeLabel.value = filters.group_name || filters.project_name || '全局'
    lastUpdatedText.value = res.data.generated_at
      ? dayjs(res.data.generated_at).format('YYYY-MM-DD HH:mm:ss')
      : '--'
    stats.value = {
      activeUsers: summary.active_users,
      totalUsers: summary.total_users,
      knowledgeBases: summary.knowledge_bases,
      docs: summary.documents,
      indexedDocs: summary.indexed_documents,
      servers: summary.servers,
      onlineServers: summary.online_servers,
      todayRuns: summary.today_runs,
      failedRuns: summary.failed_runs,
      chats: summary.today_chats,
      chunks: summary.chunks,
      enabledTasks: summary.enabled_tasks,
      totalTasks: summary.total_tasks,
    }

    notices.value = res.data.notices.length
      ? res.data.notices
      : [{ id: 0, title: '暂无公告', time: '刚刚', source: 'system' }]
    events.value = res.data.events.length
      ? res.data.events
      : [{ id: 0, log_id: 0, title: '暂无执行记录', time: '刚刚', color: 'blue' }]
    health.value = res.data.health.length
      ? res.data.health
      : [{ name: '系统状态', status: '未知', color: 'gold', desc: '暂无健康数据' }]

    trends.value = {
      dates: res.data.trends?.dates?.length ? res.data.trends.dates : buildDefaultDates(),
      totalRuns: res.data.trends?.total_runs?.length ? res.data.trends.total_runs : Array(7).fill(0),
      failedRuns: res.data.trends?.failed_runs?.length ? res.data.trends.failed_runs : Array(7).fill(0),
    }

    await nextTick()
    renderRunTrendChart()
    renderFailTrendChart()
  } catch {
    message.error('仪表盘数据加载失败')
  } finally {
    loading.value = false
  }
}

const resetNoticeForm = () => {
  editingNoticeId.value = null
  noticeTitle.value = ''
  noticeContent.value = ''
  noticeEnabled.value = true
}

const formatNoticeRelativeTime = (isoTime?: string) => {
  if (!isoTime) return '刚刚'
  const value = dayjs(isoTime)
  if (!value.isValid()) return '刚刚'
  const sec = dayjs().diff(value, 'second')
  if (sec < 60) return '刚刚'
  if (sec < 3600) return `${Math.floor(sec / 60)} 分钟前`
  if (sec < 86400) return `${Math.floor(sec / 3600)} 小时前`
  return `${Math.floor(sec / 86400)} 天前`
}

const applyManualNoticesToPanel = () => {
  const manual = noticeItems.value
    .filter((item) => item.enabled)
    .map((item) => ({
      id: item.id,
      title: item.title,
      content: item.content || '',
      time: formatNoticeRelativeTime(item.updated_at || item.created_at),
      source: 'manual' as const,
    }))
  const system = notices.value.filter((item) => item.source === 'system')
  const merged = [...manual, ...system].slice(0, 3)
  notices.value = merged.length ? merged : [{ id: 0, title: '暂无公告', time: '刚刚', source: 'system' }]
}

const loadNoticeItems = async () => {
  noticeListLoading.value = true
  try {
    const res = await getDashboardNotices()
    noticeItems.value = res.data || []
    applyManualNoticesToPanel()
  } catch {
    message.error('公告列表加载失败')
  } finally {
    noticeListLoading.value = false
  }
}

const openNoticeManager = async () => {
  noticeManageVisible.value = true
  resetNoticeForm()
  await loadNoticeItems()
}

const editNotice = (item: DashboardNoticeItem) => {
  editingNoticeId.value = item.id
  noticeTitle.value = item.title
  noticeContent.value = item.content || ''
  noticeEnabled.value = item.enabled
}

const saveNotice = async () => {
  if (!noticeTitle.value.trim()) {
    message.warning('请输入公告标题')
    return
  }
  noticeSubmitting.value = true
  try {
    const payload = {
      title: noticeTitle.value.trim(),
      content: noticeContent.value.trim(),
      enabled: noticeEnabled.value,
    }
    if (editingNoticeId.value) {
      await updateDashboardNotice(editingNoticeId.value, payload)
      message.success('公告已更新')
    } else {
      await createDashboardNotice(payload)
      message.success('公告已新增')
    }
    await loadNoticeItems()
    resetNoticeForm()
    noticeManageVisible.value = false
  } catch {
    message.error('公告保存失败')
  } finally {
    noticeSubmitting.value = false
  }
}

const removeNotice = async (noticeId: number) => {
  try {
    await deleteDashboardNotice(noticeId)
    message.success('公告已删除')
    await loadNoticeItems()
  } catch {
    message.error('公告删除失败')
  }
}

const jumpToLogDetail = (logId: number) => {
  if (!logId) return
  router.push({ path: '/ops/logs', query: { log_id: String(logId) } })
}

onMounted(async () => {
  clockTimer = window.setInterval(() => {
    liveNow.value = dayjs()
  }, 1000)
  await loadProjects()
  await loadGroups()
  await loadDashboard()
  window.addEventListener('resize', resizeCharts)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeCharts)
  if (clockTimer !== null) {
    window.clearInterval(clockTimer)
    clockTimer = null
  }
  runTrendChart?.dispose()
  failTrendChart?.dispose()
  runTrendChart = null
  failTrendChart = null
})
</script>

<style scoped>
.hero-card {
  position: relative;
  overflow: hidden;
  border-radius: 18px;
  background:
    radial-gradient(180px 120px at 12% 10%, rgba(255, 255, 255, 0.55), rgba(255, 255, 255, 0)),
    radial-gradient(220px 160px at 88% 84%, rgba(236, 72, 153, 0.22), rgba(236, 72, 153, 0)),
    linear-gradient(135deg, #ffe4f1 0%, #ffd3e8 54%, #ffc2de 100%);
}

.hero-card::before,
.hero-card::after {
  content: '';
  position: absolute;
  pointer-events: none;
}

.hero-card::before {
  width: 150px;
  height: 150px;
  right: -34px;
  top: -52px;
  border-radius: 28px;
  transform: rotate(20deg);
  background: rgba(255, 255, 255, 0.34);
  border: 1px solid rgba(236, 72, 153, 0.28);
}

.hero-card::after {
  width: 112px;
  height: 112px;
  left: -24px;
  bottom: -44px;
  border-radius: 999px;
  background: rgba(236, 72, 153, 0.18);
  border: 1px dashed rgba(190, 24, 93, 0.3);
}

.hero-subtitle {
  color: #9d174d;
  letter-spacing: 1px;
}

.hero-title {
  margin: 6px 0 0 !important;
  color: #831843 !important;
}

.hero-desc {
  color: #9f1239;
}

.hero-date {
  color: #9f1239;
  text-align: right;
}

.hero-actions {
  width: 100%;
  align-items: flex-end;
}

.hero-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

.hero-clock-card {
  min-width: 240px;
  text-align: center;
  border-radius: 16px;
  border: 1px solid rgba(236, 72, 153, 0.28);
  background: rgba(255, 255, 255, 0.72);
  padding: 12px 16px;
}

.hero-clock-head {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #831843;
  margin-bottom: 4px;
}

.hero-clock-dot {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #ec4899;
  animation: pulse-dot 1.2s ease-in-out infinite;
}

.hero-clock-time {
  font-size: 34px;
  line-height: 1.1;
  font-weight: 700;
  color: #831843;
  letter-spacing: 1px;
}

.hero-clock-date {
  margin-top: 2px;
  color: #9f1239;
  font-size: 12px;
}

.hero-clock-scope {
  margin: 8px auto 0;
  width: fit-content;
  padding: 2px 10px;
  border-radius: 999px;
  background: #fdf2f8;
  color: #9d174d;
  border: 1px solid #fbcfe8;
  font-size: 12px;
}

.rate-pill {
  display: flex;
  align-items: baseline;
  gap: 8px;
  color: #831843;
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid #f9a8d4;
  border-radius: 999px;
  padding: 8px 14px;
}

.rate-pill strong {
  font-size: 20px;
  line-height: 1;
}

.section-gap {
  margin-top: 12px;
}

.refresh-btn {
  border-color: #ec4899;
  color: #9d174d;
  background: #fff;
}

.refresh-btn:hover,
.refresh-btn:focus {
  border-color: #db2777;
  color: #831843;
  background: #fff;
}

.quick-inline-label {
  padding: 0 8px;
  height: 30px;
  line-height: 30px;
  border-radius: 999px;
  background: #fdf2f8;
  color: #9d174d;
  border: 1px solid #fbcfe8;
  font-size: 12px;
}

.filter-row {
  row-gap: 10px;
}

.quick-actions {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.quick-pill-wrap {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
  width: 100%;
}

.quick-pill {
  height: 30px;
  padding: 0 12px;
  border: 1px solid #f9a8d4;
  border-radius: 999px;
  background: #fff;
  color: #9d174d;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.quick-pill-icon {
  display: inline-flex;
  font-size: 12px;
}

.quick-pill:hover {
  border-color: #ec4899;
  color: #831843;
  transform: translateY(-1px);
  box-shadow: 0 6px 14px rgba(236, 72, 153, 0.16);
}

.quick-pill-ops {
  border-color: #93c5fd;
  color: #1d4ed8;
}

.quick-pill-script {
  border-color: #a7f3d0;
  color: #047857;
}

.quick-pill-task {
  border-color: #f9a8d4;
  color: #be185d;
}

.quick-pill-log {
  border-color: #fecaca;
  color: #b91c1c;
}

.quick-pill-group {
  border-color: #c4b5fd;
  color: #6d28d9;
}

.quick-pill-kb {
  border-color: #fde68a;
  color: #b45309;
}

.filter-actions {
  width: 100%;
  justify-content: flex-end;
}

.ai-entry {
  margin-top: 12px;
  border-radius: 16px;
  padding: 14px 18px;
  cursor: pointer;
  border: 1px solid #f9a8d4;
  background:
    radial-gradient(220px 80px at 80% 30%, rgba(236, 72, 153, 0.25), rgba(236, 72, 153, 0)),
    linear-gradient(135deg, #fff7fb 0%, #ffe7f5 100%);
  animation: ai-breath 2.6s ease-in-out infinite;
}

.ai-entry-main {
  display: grid;
  grid-template-columns: 1fr 1fr auto;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.ai-entry-left {
  text-align: left;
}

.ai-entry-center {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  text-align: center;
  color: #9f1239;
  font-size: 14px;
  font-weight: 500;
  min-height: 40px;
  padding-left: 12px;
}

.ai-entry-right {
  display: flex;
  justify-content: flex-end;
}

.ai-entry-badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 999px;
  border: 1px solid #fbcfe8;
  background: #fff;
  color: #9d174d;
  font-size: 12px;
}

.ai-entry-title {
  margin-top: 8px;
  color: #831843;
  font-size: 18px;
  font-weight: 700;
}

.ai-entry-go {
  flex: 0 0 auto;
  padding: 8px 14px;
  border-radius: 999px;
  background: #fff;
  border: 1px solid #f9a8d4;
  color: #831843;
  font-size: 12px;
  animation: pulse-dot 1.8s ease-in-out infinite;
}

.health-stack {
  width: 100%;
}

.health-row {
  justify-content: space-between;
  width: 100%;
}

.kpi-card {
  margin-bottom: 8px;
  border-radius: 12px;
}

.kpi-card :deep(.ant-card-body) {
  padding: 10px 12px;
}

.kpi-card :deep(.ant-statistic-title) {
  margin-bottom: 2px;
  font-size: 12px;
  line-height: 1.2;
}

.kpi-card :deep(.ant-statistic-content) {
  font-size: 22px;
  line-height: 1.1;
}

.kpi-hint {
  display: inline-block;
  font-size: 11px;
  line-height: 1.1;
}

.list-card {
  height: 330px;
}

.pulse-card :deep(.ant-card-body) {
  height: 266px;
  padding-right: 12px;
}

.pulse-scroll {
  height: 100%;
  overflow-y: auto;
  padding-right: 4px;
}

.trend-card {
  border-radius: 16px;
}

.trend-chart {
  height: 260px;
  width: 100%;
}

.event-link {
  padding: 0;
  height: auto;
}

.notice-line {
  color: #1f2937;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.notice-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 12px;
}

.notice-manage-list {
  max-height: 280px;
  overflow-y: auto;
  border-top: 1px solid #f3f4f6;
  padding-top: 8px;
}

@media (max-width: 991px) {
  .hero-center {
    margin: 8px 0;
  }

  .quick-actions,
  .filter-actions {
    justify-content: flex-start;
  }

  .quick-actions {
    flex-direction: column;
    align-items: flex-start;
  }

  .quick-pill-wrap {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .ai-entry-main {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .ai-entry-left,
  .ai-entry-right {
    text-align: center;
    justify-content: center;
  }
}

@keyframes pulse-dot {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.65;
  }
  50% {
    transform: scale(1.25);
    opacity: 1;
  }
}

@keyframes ai-breath {
  0%,
  100% {
    box-shadow: 0 8px 20px rgba(236, 72, 153, 0.12);
  }
  50% {
    box-shadow: 0 12px 26px rgba(236, 72, 153, 0.22);
  }
}
</style>
