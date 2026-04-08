<template>
  <div class="min-h-screen bg-gradient-to-br from-brand-100 via-white to-brand-50 flex items-center justify-center">
    <div class="w-full h-screen lg:h-[90vh] lg:max-w-[95vw] grid lg:grid-cols-5 rounded-none lg:rounded-3xl overflow-hidden shadow-2xl shadow-brand-200/50 border-0 lg:border border-brand-100/60 bg-white">
    <!-- 左侧动画区 -->
    <div class="relative hidden lg:flex flex-col justify-between lg:col-span-3 bg-gradient-to-br from-brand-400/90 via-brand-500 to-brand-600/80 p-10 text-white overflow-hidden">
      <!-- 装饰 -->
      <div class="absolute inset-0 bg-grid-white/[0.04] bg-[size:20px_20px]"></div>
      <div class="absolute top-1/4 right-1/4 w-64 h-64 bg-white/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/4 left-1/4 w-96 h-96 bg-white/5 rounded-full blur-3xl"></div>

      <!-- Logo -->
      <div class="relative z-20">
        <div class="flex items-center gap-2.5 text-lg font-semibold">
          <div class="w-8 h-8 rounded-lg bg-white/10 backdrop-blur-sm flex items-center justify-center">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <span>CHAN AgenticOps</span>
        </div>
      </div>

      <!-- 角色动画 -->
      <div class="relative z-20 flex items-end justify-center" style="height: 540px;">
        <div ref="sceneRef" class="relative" style="width: 620px; height: 500px;">
          <!-- 紫色角色 -->
          <div
            class="absolute bottom-0 transition-all duration-700 ease-in-out"
            :style="{
              left: '100px', width: '200px',
              height: (isTyping || loginForm.password.length > 0) ? '540px' : '480px',
              backgroundColor: '#EC4899',
              borderRadius: '10px 10px 0 0',
              zIndex: 1,
              transform: purpleTransform,
              transformOrigin: 'bottom center',
            }"
          >
            <div class="absolute flex gap-9 transition-all duration-700 ease-in-out"
              :style="{ left: '52px', top: '45px' }"
            >
              <div v-for="i in 2" :key="'purple-eye-'+i"
                class="rounded-full flex items-center justify-center transition-all duration-150"
                :style="{
                  width: '24px', height: purpleBlinking ? '2px' : '24px',
                  backgroundColor: 'white', overflow: 'hidden',
                }"
              >
                <div v-if="!purpleBlinking" class="rounded-full"
                  :style="{
                    width: '9px', height: '9px', backgroundColor: '#2D2D2D',
                    transform: `translate(${eyePos.x}px, ${eyePos.y}px)`,
                    transition: 'transform 0.1s ease-out',
                  }"
                ></div>
              </div>
            </div>
          </div>

          <!-- 黑色角色 -->
          <div
            class="absolute bottom-0 transition-all duration-700 ease-in-out"
            :style="{
              left: '290px', width: '145px',
              height: '380px',
              backgroundColor: '#2D2D2D',
              borderRadius: '8px 8px 0 0',
              zIndex: 2,
              transform: blackTransform,
              transformOrigin: 'bottom center',
            }"
          >
            <div class="absolute flex gap-7 transition-all duration-700 ease-in-out"
              :style="{ left: '30px', top: '36px' }"
            >
              <div v-for="i in 2" :key="'black-eye-'+i"
                class="rounded-full flex items-center justify-center transition-all duration-150"
                :style="{
                  width: '21px', height: blackBlinking ? '2px' : '21px',
                  backgroundColor: 'white', overflow: 'hidden',
                }"
              >
                <div v-if="!blackBlinking" class="rounded-full"
                  :style="{
                    width: '7px', height: '7px', backgroundColor: '#2D2D2D',
                    transform: `translate(${eyePos.x}px, ${eyePos.y}px)`,
                    transition: 'transform 0.1s ease-out',
                  }"
                ></div>
              </div>
            </div>
          </div>

          <!-- 橙色半圆角色 -->
          <div
            class="absolute bottom-0 transition-all duration-700 ease-in-out"
            :style="{
              left: '0px', width: '290px', height: '240px',
              backgroundColor: '#FF9B6B',
              borderRadius: '110px 110px 0 0',
              zIndex: 3,
              transform: `skewX(${bodySkew}deg)`,
              transformOrigin: 'bottom center',
            }"
          >
            <div class="absolute flex gap-12 transition-all duration-200 ease-out"
              :style="{ left: '95px', top: '100px' }"
            >
              <div v-for="i in 2" :key="'orange-eye-'+i" class="rounded-full"
                :style="{
                  width: '16px', height: '16px', backgroundColor: '#2D2D2D',
                  transform: `translate(${eyePos.x * 0.7}px, ${eyePos.y * 0.7}px)`,
                  transition: 'transform 0.1s ease-out',
                }"
              ></div>
            </div>
          </div>

          <!-- 黄色角色 -->
          <div
            class="absolute bottom-0 transition-all duration-700 ease-in-out"
            :style="{
              left: '370px', width: '165px', height: '280px',
              backgroundColor: '#E8D754',
              borderRadius: '65px 65px 0 0',
              zIndex: 4,
              transform: `skewX(${-bodySkew * 0.5}deg)`,
              transformOrigin: 'bottom center',
            }"
          >
            <div class="absolute flex gap-7 transition-all duration-200 ease-out"
              :style="{ left: '58px', top: '48px' }"
            >
              <div v-for="i in 2" :key="'yellow-eye-'+i" class="rounded-full"
                :style="{
                  width: '16px', height: '16px', backgroundColor: '#2D2D2D',
                  transform: `translate(${eyePos.x * 0.6}px, ${eyePos.y * 0.6}px)`,
                  transition: 'transform 0.1s ease-out',
                }"
              ></div>
            </div>
            <div class="absolute w-24 h-[4px] bg-[#2D2D2D] rounded-full transition-all duration-200 ease-out"
              :style="{ left: '48px', top: '108px' }"
            ></div>
          </div>
        </div>
      </div>

      <!-- 底部空白占位 -->
    </div>

    <!-- 右侧登录表单 -->
    <div class="flex items-center justify-center lg:col-span-2 p-12 bg-white">
      <div class="w-full max-w-[400px]">
        <!-- 移动端 Logo -->
        <div class="lg:hidden flex items-center justify-center gap-2.5 text-lg font-semibold text-surface-900 mb-10">
          <div class="w-8 h-8 rounded-lg bg-brand-100 flex items-center justify-center">
            <svg class="w-4 h-4 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <span>CHAN AgenticOps</span>
        </div>

        <!-- 标题 -->
        <div class="text-center mb-8">
          <div class="inline-flex items-center justify-center w-11 h-11 rounded-xl bg-brand-50 border border-brand-100 mb-4">
            <svg class="w-5 h-5 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
          </div>
          <h1 class="text-2xl font-bold text-surface-900 tracking-tight mb-1.5">欢迎回来</h1>
          <p class="text-surface-400 text-sm">登录 CHAN AgenticOps 智能平台</p>
        </div>

        <!-- 表单 -->
        <form @submit.prevent="handleLogin" class="space-y-5">
          <div class="space-y-1.5">
            <label class="text-xs font-medium text-surface-600">用户名</label>
            <input
              v-model="loginForm.username"
              type="text"
              required
              autocomplete="off"
              @focus="isTyping = true"
              @blur="isTyping = false"
              class="w-full h-11 px-3.5 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
              placeholder="请输入用户名"
            />
          </div>

          <div class="space-y-1.5">
            <label class="text-xs font-medium text-surface-600">密码</label>
            <div class="relative">
              <input
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="w-full h-11 px-3.5 pr-10 bg-surface-50 border border-surface-200 rounded-xl text-sm text-surface-900 placeholder-surface-400 focus:outline-none focus:border-brand-400 focus:ring-2 focus:ring-brand-100 focus:bg-white transition-all"
                placeholder="••••••••"
              />
              <button type="button" @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 -translate-y-1/2 text-surface-400 hover:text-surface-600 transition-colors">
                <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
              </button>
            </div>
          </div>

          <div class="flex items-center justify-between">
            <label class="flex items-center gap-2 text-sm text-surface-500 cursor-pointer">
              <input type="checkbox" checked class="w-4 h-4 rounded border-surface-300 text-brand-500 focus:ring-brand-400 focus:ring-offset-0 accent-brand-500" />
              记住我
            </label>
            <a href="#" class="text-sm text-brand-500 hover:underline font-medium">忘记密码？</a>
          </div>

          <div v-if="error" class="p-3 text-sm text-rose-500 bg-rose-50 border border-rose-200 rounded-xl">
            {{ error }}
          </div>

          <button type="submit" :disabled="loading"
            class="w-full h-11 bg-gradient-to-r from-brand-500 to-brand-600 hover:from-brand-400 hover:to-brand-500 text-white text-sm font-semibold rounded-xl shadow-lg shadow-brand-200/50 hover:shadow-brand-300/50 transition-all duration-200 disabled:opacity-50 mt-2">
            <span v-if="loading" class="flex items-center justify-center gap-2">
              <svg class="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
              </svg>
              登录中...
            </span>
            <span v-else>登 录</span>
          </button>
        </form>

        <p class="text-center text-xs text-surface-400 mt-8">
          登录即表示同意 <a href="#" class="text-brand-500 hover:underline transition-colors">服务条款</a>
        </p>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const error = ref('')
const showPassword = ref(false)
const isTyping = ref(false)
const loginForm = reactive({ username: '', password: '' })

// 鼠标位置
const mouseX = ref(0)
const mouseY = ref(0)
const sceneRef = ref<HTMLElement | null>(null)

// 眨眼
const purpleBlinking = ref(false)
const blackBlinking = ref(false)

// 身体倾斜
const bodySkew = computed(() => {
  if (!sceneRef.value) return 0
  const rect = sceneRef.value.getBoundingClientRect()
  const cx = rect.left + rect.width / 2
  const dx = mouseX.value - cx
  return Math.max(-6, Math.min(6, -dx / 120))
})

// 眼球位置
const eyePos = computed(() => {
  if (!sceneRef.value) return { x: 0, y: 0 }
  const rect = sceneRef.value.getBoundingClientRect()
  const cx = rect.left + rect.width / 2
  const cy = rect.top + rect.height / 3
  const dx = mouseX.value - cx
  const dy = mouseY.value - cy
  const dist = Math.min(Math.sqrt(dx * dx + dy * dy), 8)
  const angle = Math.atan2(dy, dx)
  return { x: Math.cos(angle) * dist, y: Math.sin(angle) * dist }
})

// 紫色高度（输入时变高）
const purpleHeight = computed(() => {
  return (isTyping.value || loginForm.password.length > 0) ? 420 : 380
})

const purpleTransform = computed(() => {
  const skew = isTyping.value ? bodySkew.value - 12 : bodySkew.value
  const shift = isTyping.value ? ' translateX(30px)' : ''
  return `skewX(${skew}deg)${shift}`
})

const blackTransform = computed(() => {
  const skew = isTyping.value ? bodySkew.value * 1.5 : bodySkew.value
  return `skewX(${skew}deg)`
})

// 鼠标事件
function onMouseMove(e: MouseEvent) {
  mouseX.value = e.clientX
  mouseY.value = e.clientY
}

onMounted(() => {
  document.addEventListener('mousemove', onMouseMove)
  startBlinking()
})

onUnmounted(() => {
  document.removeEventListener('mousemove', onMouseMove)
})

function startBlinking() {
  const blink = (setter: (v: boolean) => void) => {
    const delay = Math.random() * 4000 + 3000
    setTimeout(() => {
      setter(true)
      setTimeout(() => {
        setter(false)
        blink(setter)
      }, 150)
    }, delay)
  }
  blink((v) => purpleBlinking.value = v)
  blink((v) => blackBlinking.value = v)
}

async function handleLogin() {
  loading.value = true
  error.value = ''
  try {
    await authStore.login(loginForm)
    router.push('/dashboard')
  } catch (err: any) {
    error.value = err.response?.data?.detail || '登录失败，请检查用户名和密码'
  } finally {
    loading.value = false
  }
}
</script>
