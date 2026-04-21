import { createRouter, createWebHistory, type RouteLocationNormalized, type NavigationGuardNext } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/Login.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      component: () => import('@/layouts/MainLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        {
          path: '',
          redirect: '/dashboard'
        },
        {
          path: 'dashboard',
          name: 'dashboard',
          component: () => import('@/views/Dashboard.vue'),
          meta: { title: '仪表盘' }
        },
        {
          path: 'assistant',
          name: 'assistant',
          component: () => import('@/views/assistant/SystemAssistant.vue'),
          meta: { title: 'AI助手' }
        },
        {
          path: 'rag',
          component: () => import('@/layouts/BlankLayout.vue'),
          meta: { title: 'RAG知识库' },
          children: [
            {
              path: '',
              name: 'rag',
              redirect: '/rag/chat'
            },
            {
              path: 'chat',
              name: 'rag-chat',
              component: () => import('@/views/rag/Chat.vue'),
              meta: { title: 'AI 问答' }
            },
            {
              path: 'knowledge',
              name: 'rag-knowledge',
              component: () => import('@/views/rag/KnowledgeBase.vue'),
              meta: { title: '知识库管理' }
            }
          ]
        },
        {
          path: 'server/:pathMatch(.*)*',
          redirect: '/ops/servers'
        },
        {
          path: 'ops',
          component: () => import('@/layouts/BlankLayout.vue'),
          meta: { title: '运维管理' },
          children: [
            {
              path: '',
              redirect: '/ops/servers'
            },
            {
              path: 'servers',
              name: 'ops-servers',
              component: () => import('@/views/ops/ServerList.vue'),
              meta: { title: '服务器列表', keepAlive: false }
            },
            {
              path: 'scripts',
              name: 'ops-scripts',
              component: () => import('@/views/ops/ScriptList.vue'),
              meta: { title: '脚本管理', keepAlive: false }
            },
            {
              path: 'tasks',
              name: 'ops-tasks',
              component: () => import('@/views/ops/TaskList.vue'),
              meta: { title: '定时任务', keepAlive: false }
            },
            {
              path: 'logs',
              name: 'ops-logs',
              component: () => import('@/views/ops/LogList.vue'),
              meta: { title: '执行日志', keepAlive: false }
            },
            {
              path: 'groups',
              name: 'ops-groups',
              component: () => import('@/views/ops/GroupManagement.vue'),
              meta: { title: '项目分组', keepAlive: false }
            },
            {
              path: 'assistant',
              name: 'ops-assistant',
              component: () => import('@/views/ops/OpsAssistant.vue'),
              meta: { title: '运维助手', keepAlive: false }
            }
          ]
        },
        {
          path: 'settings',
          name: 'settings',
          component: () => import('@/views/Settings.vue'),
          meta: { title: '设置' },
          children: [
            {
              path: 'profile',
              name: 'profile',
              component: () => import('@/views/settings/Profile.vue'),
              meta: { title: '个人设置' }
            },
            {
              path: 'users',
              name: 'user-management',
              component: () => import('@/views/settings/UserManagement.vue'),
              meta: { title: '用户管理' }
            },
            {
              path: 'roles',
              name: 'role-management',
              component: () => import('@/views/settings/RoleManagement.vue'),
              meta: { title: '角色管理' }
            },
            {
              path: 'menus',
              name: 'menu-management',
              component: () => import('@/views/settings/MenuManagement.vue'),
              meta: { title: '菜单管理' }
            }
          ]
        },
        {
          path: 'system/:path(.*)*',
          redirect: (to) => {
            const subPath = to.params.path || 'users'
            return `/settings/${subPath}`
          }
        }
      ]
    }
  ]
})

router.beforeEach((to: RouteLocationNormalized, _from: RouteLocationNormalized, next: NavigationGuardNext) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth !== false && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
