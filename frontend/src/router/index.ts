import { createRouter, createWebHistory } from 'vue-router'
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
          path: 'system',
          name: 'system',
          component: () => import('@/views/Settings.vue'),
          meta: { title: '系统管理' },
          children: [
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
        }
      ]
    }
  ]
})

router.beforeEach((to, from, next) => {
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
