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
          path: 'chat',
          name: 'chat',
          component: () => import('@/views/Chat.vue'),
          meta: { title: 'AI 问答' }
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
