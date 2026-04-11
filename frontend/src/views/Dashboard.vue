<template>
  <div class="dashboard-page ant-illustration-page">
    <Card :bordered="false" class="hero-card">
      <Row :gutter="16" align="middle" justify="space-between">
        <Col>
          <TypographyText type="secondary">AGENTICOPS DASHBOARD</TypographyText>
          <TypographyTitle :level="2" class="hero-title">运营概览</TypographyTitle>
        </Col>
        <Col>
          <Space direction="vertical" size="small" align="end">
            <TypographyText type="secondary">{{ today }}</TypographyText>
            <Tag color="blue">任务成功率 {{ successRate }}%</Tag>
          </Space>
        </Col>
      </Row>
    </Card>

    <Row :gutter="12" class="section-gap">
      <Col v-for="item in kpis" :key="item.label" :xs="12" :sm="8" :md="6" :lg="6" :xl="3">
        <Card :bordered="false" class="kpi-card">
          <Statistic :title="item.label" :value="item.value" />
          <span class="kpi-hint" :style="{ color: item.color }">{{ item.hint }}</span>
        </Card>
      </Col>
    </Row>

    <Card :bordered="false" class="section-gap">
      <TypographyTitle :level="5" class="quick-title">快捷入口</TypographyTitle>
      <Space wrap>
        <Button v-for="entry in quickEntries" :key="entry.path" @click="router.push(entry.path)">
          {{ entry.name }}
        </Button>
      </Space>
    </Card>

    <Row :gutter="12" class="section-gap">
      <Col :xs="24" :lg="8">
        <Card :bordered="false" title="系统公告" class="list-card">
          <List :data-source="notices" :split="false">
            <template #renderItem="{ item }">
              <ListItem>
                <ListItemMeta :description="item.time">
                  <template #title>{{ item.title }}</template>
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
        <Card :bordered="false" title="系统脉冲" class="list-card">
          <Timeline>
            <TimelineItem v-for="event in events" :key="event.title + event.time" :color="event.color">
              <TypographyText>{{ event.title }}</TypographyText>
              <br />
              <TypographyText type="secondary">{{ event.time }}</TypographyText>
            </TimelineItem>
          </Timeline>
        </Card>
      </Col>
    </Row>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  Button,
  Card,
  Col,
  List,
  Row,
  Space,
  Statistic,
  Tag,
  Timeline,
  Typography,
} from 'ant-design-vue'

const router = useRouter()

const ListItem = List.Item
const ListItemMeta = List.Item.Meta
const TimelineItem = Timeline.Item
const TypographyText = Typography.Text
const TypographyTitle = Typography.Title

const now = new Date()
const today = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`

const stats = ref({
  activeUsers: 9,
  docs: 24,
  indexedDocs: 20,
  servers: 18,
  todayRuns: 214,
  failedRuns: 6,
  chats: 15,
  chunks: 1560,
})

const successRate = computed(() => {
  if (!stats.value.todayRuns) return '100.0'
  return (((stats.value.todayRuns - stats.value.failedRuns) / stats.value.todayRuns) * 100).toFixed(1)
})

const kpis = computed(() => [
  { label: '活跃用户', value: stats.value.activeUsers, hint: '近 7 日', color: '#2563eb' },
  { label: '知识文档', value: stats.value.docs, hint: `${stats.value.indexedDocs} 已索引`, color: '#16a34a' },
  { label: '运维主机', value: stats.value.servers, hint: '在线 16', color: '#0891b2' },
  { label: '今日会话', value: stats.value.chats, hint: 'AI 请求', color: '#d97706' },
  { label: '执行总量', value: stats.value.todayRuns, hint: '今日任务', color: '#475569' },
  { label: '失败次数', value: stats.value.failedRuns, hint: '需关注', color: '#e11d48' },
  { label: '向量片段', value: stats.value.chunks, hint: '检索基座', color: '#7c3aed' },
  { label: '任务成功率', value: `${successRate.value}%`, hint: '稳定运行', color: '#0f766e' },
])

const quickEntries = [
  { name: '任务中心', path: '/ops/tasks' },
  { name: '执行日志', path: '/ops/logs' },
  { name: '知识库管理', path: '/rag/knowledge' },
  { name: '服务器列表', path: '/ops/servers' },
  { name: 'AI助手', path: '/assistant' },
]

const notices = ref([
  { title: '日志归档策略已开启（保留 90 天）', time: '今天 09:30' },
  { title: '请关注 2 台离线主机恢复', time: '今天 10:10' },
  { title: '夜间巡检任务已生效', time: '今天 11:00' },
])

const events = ref([
  { title: 'AI检测脚本执行失败', time: '12 分钟前', color: 'red' },
  { title: '日志归档任务完成', time: '43 分钟前', color: 'green' },
  { title: '新增知识库文档', time: '2 小时前', color: 'gold' },
  { title: '主机连通性巡检', time: '3 小时前', color: 'blue' },
])

const health = ref([
  { name: '计划任务调度', status: '正常', color: 'green', desc: '每分钟检查，无积压' },
  { name: 'Celery 队列', status: '可用', color: 'blue', desc: 'Worker 在线，平均延迟 < 2s' },
  { name: '日志存储', status: '关注', color: 'gold', desc: '建议保持 90 天在线数据' },
])
</script>

<style scoped>
.hero-card {
  border-radius: 18px;
}

.hero-title {
  margin: 6px 0 0 !important;
}

.section-gap {
  margin-top: 12px;
}

.quick-title {
  margin-bottom: 12px !important;
}

.health-stack {
  width: 100%;
}

.health-row {
  justify-content: space-between;
  width: 100%;
}

.kpi-card {
  margin-bottom: 12px;
  border-radius: 16px;
}

.kpi-hint {
  display: inline-block;
  font-size: 12px;
}

.list-card {
  min-height: 330px;
}
</style>
