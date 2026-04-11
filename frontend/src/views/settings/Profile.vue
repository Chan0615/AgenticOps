<template>
  <div class="profile-page ant-illustration-page">
    <section class="profile-hero">
      <div>
        <h1>个人设置</h1>
        <p>维护基础资料与登录安全</p>
        <div class="hero-tags">
          <span>资料维护</span>
          <span>账号安全</span>
        </div>
      </div>
      <div class="hero-mini-ill">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </section>

    <section class="profile-grid">
      <article class="panel-card panel-card-info">
        <div class="panel-title">个人信息</div>
        <div class="profile-mini">
          <div class="avatar-bubble">{{ userInitial }}</div>
          <div class="mini-meta">
            <div class="mini-name">{{ authStore.user?.full_name || authStore.user?.username || '未登录用户' }}</div>
            <div class="mini-tags">
              <span>{{ authStore.user?.is_superuser ? '超级管理员' : '普通用户' }}</span>
              <span>{{ authStore.user?.email || '未设置邮箱' }}</span>
            </div>
          </div>
        </div>
        <form class="panel-form" @submit.prevent="handleUpdateProfile">
          <label>
            <span>用户名</span>
            <input v-model="form.username" disabled />
          </label>
          <label>
            <span>显示名称</span>
            <input v-model="form.full_name" placeholder="请输入显示名称" />
          </label>
          <label>
            <span>邮箱</span>
            <input v-model="form.email" type="email" placeholder="请输入邮箱" />
          </label>
          <button class="save-btn" type="submit" :disabled="saving">{{ saving ? '保存中...' : '保存资料' }}</button>
        </form>
      </article>

      <article class="panel-card panel-card-security">
        <div class="panel-title">修改密码</div>
        <form class="panel-form" @submit.prevent="handleChangePassword">
          <label>
            <span>当前密码</span>
            <input v-model="passwordForm.current_password" type="password" placeholder="请输入当前密码" />
          </label>
          <label>
            <span>新密码</span>
            <input v-model="passwordForm.new_password" type="password" placeholder="至少 6 位" />
          </label>
          <label>
            <span>确认新密码</span>
            <input v-model="passwordForm.confirm_password" type="password" placeholder="请再次输入新密码" />
          </label>
          <button class="save-btn dark" type="submit" :disabled="changingPassword">
            {{ changingPassword ? '修改中...' : '更新密码' }}
          </button>
        </form>
      </article>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { message } from 'ant-design-vue'
import { authApi } from '@/api/system/auth'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const form = ref({
  username: '',
  full_name: '',
  email: '',
})

const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: '',
})

const saving = ref(false)
const changingPassword = ref(false)
const userInitial = computed(() => (authStore.user?.username?.charAt(0) || 'U').toUpperCase())

const fillProfile = () => {
  form.value = {
    username: authStore.user?.username || '',
    full_name: authStore.user?.full_name || '',
    email: authStore.user?.email || '',
  }
}

onMounted(async () => {
  if (!authStore.user && authStore.token) {
    try {
      await authStore.fetchUser()
    } catch {
      // ignore
    }
  }
  fillProfile()
})

async function handleUpdateProfile() {
  if (!form.value.email.trim()) {
    message.warning('邮箱不能为空')
    return
  }
  saving.value = true
  try {
    await authStore.updateProfile({
      full_name: form.value.full_name || undefined,
      email: form.value.email,
    })
    message.success('个人信息已更新')
    fillProfile()
  } catch (err: any) {
    message.error(err.response?.data?.detail || '更新失败')
  } finally {
    saving.value = false
  }
}

async function handleChangePassword() {
  if (!passwordForm.value.current_password || !passwordForm.value.new_password || !passwordForm.value.confirm_password) {
    message.warning('请完整填写密码信息')
    return
  }
  if (passwordForm.value.new_password.length < 6) {
    message.warning('新密码至少 6 位')
    return
  }
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    message.warning('两次输入的新密码不一致')
    return
  }

  changingPassword.value = true
  try {
    await authApi.changePassword(passwordForm.value.current_password, passwordForm.value.new_password)
    message.success('密码已修改')
    passwordForm.value = { current_password: '', new_password: '', confirm_password: '' }
  } catch (err: any) {
    message.error(err.response?.data?.detail || '修改失败')
  } finally {
    changingPassword.value = false
  }
}
</script>

<style scoped>
.profile-page {
  max-width: 980px;
  margin: 0 auto;
  padding: 14px;
}

.profile-hero {
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 16px;
  border-radius: 16px;
  border: 2px solid #f9a8d4;
  background:
    radial-gradient(120px 70px at 88% 16%, rgba(236, 72, 153, 0.22), rgba(236, 72, 153, 0)),
    linear-gradient(135deg, #fff7fb 0%, #ffe7f5 100%);
  box-shadow: 4px 4px 0 rgba(44, 44, 44, 0.14);
}

.profile-hero h1 {
  margin: 0;
  font-size: 22px;
  color: #831843;
}

.profile-hero p {
  margin: 4px 0 0;
  font-size: 13px;
  color: #9f1239;
}

.hero-tags {
  margin-top: 8px;
  display: flex;
  gap: 6px;
}

.hero-tags span {
  height: 24px;
  line-height: 24px;
  padding: 0 10px;
  border-radius: 999px;
  border: 1px solid #fbcfe8;
  background: rgba(255, 255, 255, 0.92);
  color: #9d174d;
  font-size: 12px;
}

.hero-mini-ill {
  display: flex;
  gap: 8px;
}

.hero-mini-ill span {
  width: 12px;
  height: 12px;
  border-radius: 999px;
  background: #ec4899;
  animation: pulse 1.4s ease-in-out infinite;
}

.hero-mini-ill span:nth-child(2) {
  animation-delay: 0.2s;
}

.hero-mini-ill span:nth-child(3) {
  animation-delay: 0.4s;
}

.profile-grid {
  margin-top: 10px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.panel-card {
  position: relative;
  border-radius: 14px;
  border: 2px solid #fbcfe8;
  background: #fff;
  padding: 14px;
  box-shadow: 4px 4px 0 rgba(44, 44, 44, 0.1);
}

.panel-card::after {
  content: '';
  position: absolute;
  top: 12px;
  right: 12px;
  width: 10px;
  height: 10px;
  border-radius: 999px;
}

.panel-card-info {
  background: linear-gradient(180deg, #ffffff 0%, #fff9fc 100%);
}

.panel-card-security {
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
}

.panel-card-info::after {
  background: #ec4899;
}

.panel-card-security::after {
  background: #475569;
}

.panel-title {
  font-size: 14px;
  font-weight: 700;
  color: #831843;
  margin-bottom: 10px;
}

.profile-mini {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
  padding: 8px;
  border-radius: 12px;
  border: 1px dashed #f9a8d4;
  background: #fff7fb;
}

.avatar-bubble {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #ec4899, #fb7185);
  color: #fff;
  font-weight: 700;
}

.mini-meta {
  min-width: 0;
}

.mini-name {
  font-size: 13px;
  color: #831843;
  font-weight: 700;
}

.mini-tags {
  margin-top: 2px;
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.mini-tags span {
  max-width: 220px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 11px;
  color: #9d174d;
  background: #fff;
  border: 1px solid #fbcfe8;
  border-radius: 999px;
  padding: 1px 8px;
}

.panel-form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.panel-form label {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.panel-form label span {
  font-size: 12px;
  color: #64748b;
}

.panel-form input {
  height: 36px;
  border: 1px solid #dbe4f3;
  border-radius: 10px;
  padding: 0 10px;
  outline: none;
  background: #fff;
}

.panel-form input:focus {
  border-color: #ec4899;
  box-shadow: 0 0 0 2px rgba(236, 72, 153, 0.16);
}

.panel-form input:disabled {
  background: #f8fafc;
  color: #94a3b8;
}

.save-btn {
  height: 36px;
  border: 1px solid #ec4899;
  border-radius: 10px;
  background: #ec4899;
  color: #fff;
  font-size: 13px;
  cursor: pointer;
  box-shadow: 2px 2px 0 rgba(44, 44, 44, 0.2);
}

.save-btn.dark {
  border-color: #334155;
  background: #334155;
}

.save-btn:hover {
  transform: translateY(-1px);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 900px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
}

@keyframes pulse {
  0%,
  100% {
    transform: translateY(0px);
    opacity: 0.6;
  }
  50% {
    transform: translateY(-3px);
    opacity: 1;
  }
}
</style>
