<template>
  <div class="login-page">
    <div class="login-shell">
      <section class="illustration-panel">
        <div class="brand-row">
          <div class="brand-icon">A</div>
          <div class="brand-text">CHAN AgenticOps</div>
        </div>

        <div class="illustration-card">
          <svg viewBox="0 0 760 520" class="illustration-svg" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="运维插画">
            <defs>
              <linearGradient id="bgGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#60a5fa" stop-opacity="0.25"/>
                <stop offset="100%" stop-color="#22d3ee" stop-opacity="0.18"/>
              </linearGradient>
              <linearGradient id="serverGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0%" stop-color="#f8fafc"/>
                <stop offset="100%" stop-color="#dbeafe"/>
              </linearGradient>
            </defs>

            <rect x="28" y="20" width="704" height="470" rx="36" fill="url(#bgGrad)"/>
            <circle cx="130" cy="110" r="54" fill="#fde68a"/>
            <circle cx="650" cy="92" r="38" fill="#c4b5fd"/>
            <rect x="82" y="320" width="590" height="120" rx="24" fill="#0f172a" opacity="0.14"/>

            <rect x="130" y="180" width="160" height="190" rx="18" fill="url(#serverGrad)" stroke="#1e293b" stroke-width="4"/>
            <rect x="150" y="205" width="120" height="18" rx="9" fill="#38bdf8"/>
            <rect x="150" y="237" width="120" height="18" rx="9" fill="#22c55e"/>
            <rect x="150" y="269" width="120" height="18" rx="9" fill="#f59e0b"/>
            <circle cx="160" cy="335" r="7" fill="#10b981"/>
            <circle cx="186" cy="335" r="7" fill="#10b981"/>

            <rect x="330" y="146" width="290" height="190" rx="24" fill="#ffffff" stroke="#1e293b" stroke-width="4"/>
            <rect x="358" y="178" width="232" height="16" rx="8" fill="#e2e8f0"/>
            <rect x="358" y="206" width="180" height="12" rx="6" fill="#bfdbfe"/>
            <rect x="358" y="226" width="156" height="12" rx="6" fill="#a7f3d0"/>
            <rect x="358" y="246" width="198" height="12" rx="6" fill="#fde68a"/>
            <rect x="358" y="274" width="94" height="30" rx="10" fill="#22c55e"/>
            <text x="382" y="294" fill="#ffffff" font-size="16" font-weight="700">RUN</text>

            <path d="M290 252 C320 252, 320 240, 330 240" stroke="#1e293b" stroke-width="4" fill="none" stroke-linecap="round"/>
            <path d="M290 288 C320 288, 320 300, 330 300" stroke="#1e293b" stroke-width="4" fill="none" stroke-linecap="round"/>

            <rect x="486" y="342" width="160" height="80" rx="16" fill="#ffffff" stroke="#1e293b" stroke-width="4"/>
            <rect x="504" y="360" width="124" height="12" rx="6" fill="#cbd5e1"/>
            <rect x="504" y="380" width="88" height="12" rx="6" fill="#93c5fd"/>
          </svg>
        </div>

        <div class="illustration-caption">
          <span>智能编排</span>
          <span>脚本分发</span>
          <span>作业监控</span>
        </div>
      </section>

      <section class="form-panel">
        <div class="floating-note note-top">Daily Jobs</div>
        <div class="floating-note note-bottom">Script Center</div>

        <Card :bordered="false" class="login-card">
          <div class="login-title-wrap">
            <h1 class="login-title">欢迎回来</h1>
            <p class="login-subtitle">登录 CHAN AgenticOps 平台</p>
          </div>

          <Form layout="vertical" :model="loginForm" @finish="handleLogin">
            <FormItem label="用户名" name="username" :rules="[{ required: true, message: '请输入用户名' }]">
              <Input v-model:value="loginForm.username" size="large" placeholder="请输入用户名" />
            </FormItem>

            <FormItem label="密码" name="password" :rules="[{ required: true, message: '请输入密码' }]">
              <InputPassword v-model:value="loginForm.password" size="large" placeholder="请输入密码" />
            </FormItem>

            <div class="login-tools">
              <Checkbox v-model:checked="rememberMe">记住我</Checkbox>
              <a class="forgot-link">忘记密码？</a>
            </div>

            <Alert v-if="error" :message="error" type="error" show-icon style="margin-bottom: 14px" />

            <Button html-type="submit" type="primary" block size="large" :loading="loading">登录</Button>
          </Form>
        </Card>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Alert, Button, Card, Checkbox, Form, Input } from 'ant-design-vue'
import { useAuthStore } from '@/stores/auth'

const FormItem = Form.Item
const InputPassword = Input.Password

const router = useRouter()
const authStore = useAuthStore()

const loading = ref(false)
const error = ref('')
const rememberMe = ref(true)
const loginForm = reactive({ username: '', password: '' })

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

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  background:
    radial-gradient(900px 500px at 10% 10%, rgba(59, 130, 246, 0.2), transparent 60%),
    radial-gradient(900px 500px at 90% 0%, rgba(14, 165, 233, 0.18), transparent 60%),
    linear-gradient(180deg, #eef5ff 0%, #f8fbff 100%);
}

.login-shell {
  width: min(1460px, 100%);
  min-height: min(840px, calc(100vh - 28px));
  display: grid;
  grid-template-columns: 1.28fr 0.72fr;
  border-radius: 24px;
  overflow: hidden;
  border: 1px solid #dbeafe;
  background: #fff;
  box-shadow: 0 24px 60px rgba(30, 64, 175, 0.12);
}

.illustration-panel {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 28px;
  color: #fff;
  background: linear-gradient(155deg, #1d4ed8 0%, #2563eb 42%, #0ea5e9 100%);
  overflow: hidden;
}

.illustration-panel::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image: linear-gradient(rgba(255, 255, 255, 0.06) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.06) 1px, transparent 1px);
  background-size: 24px 24px;
  opacity: 0.35;
}

.brand-row {
  position: absolute;
  top: 28px;
  left: 28px;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-icon {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.18);
}

.brand-text {
  font-size: 15px;
  font-weight: 700;
}

.illustration-card {
  position: relative;
  z-index: 2;
  width: min(740px, 100%);
  margin: 12px auto 0;
  border-radius: 28px;
  border: 3px solid rgba(255, 255, 255, 0.85);
  background: rgba(255, 255, 255, 0.08);
  box-shadow: 0 18px 36px rgba(15, 23, 42, 0.2);
  padding: 12px;
}

.illustration-svg {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 20px;
}

.illustration-caption {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 16px;
}

.illustration-caption span {
  padding: 8px 12px;
  border-radius: 999px;
  border: 2px solid rgba(255, 255, 255, 0.82);
  background: rgba(255, 255, 255, 0.16);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.5px;
}

.form-panel {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
  overflow: hidden;
}

.form-panel::before,
.form-panel::after {
  content: '';
  position: absolute;
  pointer-events: none;
}

.form-panel::before {
  right: -46px;
  top: -34px;
  width: 170px;
  height: 170px;
  border-radius: 24px;
  border: 3px solid #2c2c2c;
  background: linear-gradient(145deg, #bfdbfe, #93c5fd);
  box-shadow: 6px 6px 0 #2c2c2c;
  transform: rotate(12deg);
}

.form-panel::after {
  left: -52px;
  bottom: -50px;
  width: 190px;
  height: 190px;
  border-radius: 50%;
  border: 3px solid #2c2c2c;
  background: radial-gradient(circle at 35% 35%, #fde68a, #f59e0b);
  box-shadow: 6px 6px 0 #2c2c2c;
}

.floating-note {
  position: absolute;
  z-index: 1;
  padding: 7px 12px;
  border: 3px solid #2c2c2c;
  border-radius: 12px;
  box-shadow: 4px 4px 0 #2c2c2c;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.4px;
}

.note-top {
  top: 98px;
  right: 44px;
  background: #d9f99d;
}

.note-bottom {
  left: 42px;
  bottom: 84px;
  background: #bae6fd;
}

.login-card {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 500px;
  border-radius: 20px;
  border: 1px solid #e6eefc;
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06);
}

.login-card::before {
  content: '';
  position: absolute;
  right: 18px;
  top: 14px;
  width: 42px;
  height: 16px;
  border: 3px solid #2c2c2c;
  border-radius: 999px;
  background: #86efac;
  box-shadow: 3px 3px 0 #2c2c2c;
}

.login-card::after {
  content: '';
  position: absolute;
  left: -12px;
  top: 32px;
  width: 18px;
  height: 68px;
  border: 3px solid #2c2c2c;
  border-right: none;
  border-radius: 12px 0 0 12px;
  background: #67e8f9;
}

.login-card :deep(.ant-input),
.login-card :deep(.ant-input-affix-wrapper) {
  min-height: 48px;
  border-radius: 12px;
}

.login-card :deep(.ant-input-affix-wrapper .ant-input) {
  border: none !important;
  box-shadow: none !important;
  background: transparent !important;
  min-height: auto;
}

.login-title-wrap {
  margin-bottom: 18px;
  text-align: center;
}

.login-title {
  margin: 0;
  font-size: 28px;
  font-weight: 700;
  color: #0f172a;
}

.login-subtitle {
  margin: 6px 0 0;
  font-size: 13px;
  color: #64748b;
  text-align: center;
}

.login-tools {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.forgot-link {
  color: #2563eb;
  font-size: 13px;
}

@media (max-width: 1200px) {
  .illustration-caption {
    flex-wrap: wrap;
  }
}

@media (max-width: 1024px) {
  .login-shell {
    grid-template-columns: 1fr;
    min-height: auto;
  }

  .illustration-panel {
    min-height: 280px;
  }

  .illustration-caption,
  .form-panel::before,
  .form-panel::after,
  .login-card::before,
  .login-card::after,
  .floating-note {
    display: none;
  }
}
</style>
