<template>
  <Layout class="main-layout">
    <Sider v-model:collapsed="collapsed" :trigger="null" collapsible :width="250" class="main-sider">
      <div class="logo-wrap">
        <Avatar shape="square" :size="36" class="logo-avatar">A</Avatar>
        <div v-if="!collapsed" class="logo-title">CHAN AgenticOps</div>
      </div>

      <div class="menu-wrap">
        <Skeleton v-if="loading" active :paragraph="{ rows: 8 }" />
        <Menu
          v-else
          mode="inline"
          :selected-keys="selectedKeys"
          v-model:openKeys="openKeys"
          :items="menuItems"
          @click="handleMenuClick"
        />
      </div>
    </Sider>

    <Layout>
      <Header class="main-header">
        <Space>
          <Button type="text" @click="collapsed = !collapsed">{{ collapsed ? '展开' : '收起' }}</Button>
          <TypographyText type="secondary">{{ currentTitle }}</TypographyText>
        </Space>

        <Dropdown :trigger="['click']">
          <Space class="user-area">
            <Avatar>{{ userInitial }}</Avatar>
            <span>{{ authStore.user?.full_name || authStore.user?.username }}</span>
          </Space>
          <template #overlay>
            <Menu>
              <MenuItem key="profile" @click="router.push('/settings/profile')">个人设置</MenuItem>
              <MenuItem key="logout" danger @click="handleLogout">退出登录</MenuItem>
            </Menu>
          </template>
        </Dropdown>
      </Header>

      <Content class="main-content ant-illustration-page">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" :key="$route.path" />
          </transition>
        </router-view>
      </Content>
    </Layout>
  </Layout>
</template>

<script setup lang="ts">
import { computed, h, onMounted, ref, watch, type Component } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Avatar,
  Button,
  Dropdown,
  Layout,
  Menu,
  Skeleton,
  Space,
  Typography,
  message,
} from 'ant-design-vue'
import type { MenuProps } from 'ant-design-vue'
import {
  AppstoreOutlined,
  BookOutlined,
  ClockCircleOutlined,
  CodeOutlined,
  DashboardOutlined,
  DesktopOutlined,
  FileTextOutlined,
  MenuOutlined,
  MessageOutlined,
  RobotOutlined,
  SettingOutlined,
  TeamOutlined,
  ToolOutlined,
  UserOutlined,
} from '@ant-design/icons-vue'
import { menuApi } from '@/api/system/menu'
import { useAuthStore } from '@/stores/auth'
import type { Menu as SysMenu } from '@/api/system/types'

const Header = Layout.Header
const Content = Layout.Content
const Sider = Layout.Sider
const MenuItem = Menu.Item
const TypographyText = Typography.Text

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const collapsed = ref(false)
const loading = ref(true)
const menuTree = ref<SysMenu[]>([])
const openKeys = ref<string[]>([])

const userInitial = computed(() => authStore.user?.username?.charAt(0).toUpperCase() || 'U')

const currentTitle = computed(() => {
  const meta = route.meta as Record<string, any>
  return meta?.title || 'CHAN AgenticOps'
})

const selectedKeys = computed(() => [route.path])

const iconMap: Record<string, Component> = {
  DataBoard: DashboardOutlined,
  DashboardOutlined,
  Brain: RobotOutlined,
  RobotOutlined,
  ChatDotRound: MessageOutlined,
  MessageOutlined,
  Collection: BookOutlined,
  BookOutlined,
  Tool: ToolOutlined,
  ToolOutlined,
  Desktop: DesktopOutlined,
  DesktopOutlined,
  Code: CodeOutlined,
  CodeOutlined,
  ClockCircle: ClockCircleOutlined,
  ClockCircleOutlined,
  File: FileTextOutlined,
  FileTextOutlined,
  Setting: SettingOutlined,
  SettingOutlined,
  User: UserOutlined,
  UserOutlined,
  UserFilled: TeamOutlined,
  TeamOutlined,
  Menu: MenuOutlined,
  MenuOutlined,
}

const resolveMenuIcon = (icon?: string) => {
  if (!icon) return AppstoreOutlined
  const IconComponent = iconMap[icon] || AppstoreOutlined
  return IconComponent
}

const resolveMenuTone = (key?: string) => {
  const value = (key || '').toLowerCase()
  if (value.includes('/dashboard')) return 'tone-dashboard'
  if (value.includes('/assistant')) return 'tone-assistant'
  if (value.includes('/rag')) return 'tone-rag'
  if (value.includes('/ops/servers')) return 'tone-server'
  if (value.includes('/ops/scripts')) return 'tone-script'
  if (value.includes('/ops/tasks')) return 'tone-task'
  if (value.includes('/ops/logs')) return 'tone-log'
  if (value.includes('/ops/groups')) return 'tone-group'
  if (value.includes('/settings')) return 'tone-settings'
  return 'tone-default'
}

const buildMenuIcon = (icon?: string, key?: string) => {
  const IconComponent = resolveMenuIcon(icon)
  return h('span', { class: ['menu-icon-chip', resolveMenuTone(key)] }, [h(IconComponent)])
}

const buildMenuItems = (items: SysMenu[]): any[] => {
  return items
    .filter((item) => item.type !== 'button' && item.status)
    .map((item) => {
      const children = item.children?.filter((child) => child.type !== 'button' && child.status) || []
      if (children.length) {
        return {
          key: item.code,
          label: item.name,
          icon: buildMenuIcon(item.icon, item.path || item.code),
          children: children.map((child) => ({
            key: child.path || child.code,
            label: child.name,
            icon: buildMenuIcon(child.icon, child.path || child.code),
          })),
        }
      }
      return {
        key: item.path || item.code,
        label: item.name,
        icon: buildMenuIcon(item.icon, item.path || item.code),
      }
    })
}

const menuItems = computed(() => buildMenuItems(menuTree.value))

const syncOpenKeysByRoute = () => {
  for (const parent of menuTree.value) {
    const children = parent.children || []
    if (children.some((child) => child.path === route.path)) {
      openKeys.value = [parent.code]
      break
    }
  }
}

const handleMenuClick: MenuProps['onClick'] = (info) => {
  const key = String(info?.key ?? '')
  if (!key) return
  if (key.startsWith('/')) {
    router.push(key)
  }
}

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}

watch(
  () => route.meta.title,
  (newTitle) => {
    document.title = newTitle ? `${newTitle} - CHAN AgenticOps` : 'CHAN AgenticOps'
  },
  { immediate: true },
)

onMounted(async () => {
  try {
    const data = await menuApi.getMyMenus()
    menuTree.value = Array.isArray(data) ? data : []
    if (!menuTree.value.length) {
      message.error('菜单数据为空，请检查菜单配置与权限')
    }
    syncOpenKeysByRoute()
  } catch (error) {
    console.error('加载菜单失败:', error)
    menuTree.value = []
    message.error('菜单加载失败，请检查菜单接口')
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  background: transparent;
}

.main-sider {
  background: #fff !important;
  border-right: 1px solid #dbeafe;
}

.logo-wrap {
  height: 68px;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 14px;
  border-bottom: 1px solid #e2e8f0;
}

.logo-avatar {
  background: linear-gradient(135deg, #22c55e, #4dabf7);
  font-weight: 700;
}

.logo-title {
  font-size: 14px;
  font-weight: 700;
  color: #0f172a;
}

.menu-wrap {
  padding: 12px 10px;
}

.main-header {
  height: 64px;
  background: rgba(255, 255, 255, 0.84);
  backdrop-filter: blur(6px);
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
}

.main-content {
  padding: 16px;
}

.user-area {
  cursor: pointer;
}

:deep(.menu-icon-chip) {
  width: 20px;
  height: 20px;
  border-radius: 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
}

:deep(.menu-icon-chip.tone-dashboard) { background: #dbeafe; color: #1d4ed8; }
:deep(.menu-icon-chip.tone-assistant) { background: #fce7f3; color: #be185d; }
:deep(.menu-icon-chip.tone-rag) { background: #fef3c7; color: #b45309; }
:deep(.menu-icon-chip.tone-server) { background: #d1fae5; color: #047857; }
:deep(.menu-icon-chip.tone-script) { background: #e0f2fe; color: #0e7490; }
:deep(.menu-icon-chip.tone-task) { background: #ede9fe; color: #6d28d9; }
:deep(.menu-icon-chip.tone-log) { background: #fee2e2; color: #b91c1c; }
:deep(.menu-icon-chip.tone-group) { background: #fce7f3; color: #9d174d; }
:deep(.menu-icon-chip.tone-settings) { background: #e2e8f0; color: #334155; }
:deep(.menu-icon-chip.tone-default) { background: #f3f4f6; color: #4b5563; }
</style>
