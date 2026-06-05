<template>
  <div class="setup-page">
    <div class="setup-card">
      <div class="setup-header">
        <span class="setup-icon">🔌</span>
        <h1>{{ t('setup.title') }}</h1>
        <p>{{ t('setup.subtitle') }}</p>
      </div>
      <div class="setup-info card">
        <p>{{ t('setup.info') }}</p>
      </div>
      <form @submit.prevent="handleSetup" class="setup-form">
        <div class="form-group">
          <label>{{ t('setup.username') }}</label>
          <input v-model="username" type="text" :placeholder="t('setup.placeholderUser')" autocomplete="off" />
        </div>
        <div class="form-group">
          <label>{{ t('setup.password') }}</label>
          <input v-model="password" type="password" :placeholder="t('setup.placeholderPass')" autocomplete="new-password" />
        </div>
        <div class="form-group">
          <label>{{ t('setup.confirmPassword') }}</label>
          <input v-model="confirmPassword" type="password" :placeholder="t('setup.placeholderConfirm')" autocomplete="new-password" />
        </div>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <button type="submit" class="btn-primary setup-btn" :disabled="loading">
          {{ loading ? t('setup.creating') : t('setup.createAdmin') }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useI18n } from '../i18n'
import api from '../api'

const router = useRouter()
const auth = useAuthStore()
const { t } = useI18n()
const username = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

onMounted(async () => {
  try {
    const res = await api.get('/api/v1/setup/status')
    if (res.data.initialized) {
      router.replace('/login')
    }
  } catch {
    // Server down — stay on setup, user will retry
  }
})

async function handleSetup() {
  error.value = ''
  if (!username.value || !password.value) {
    error.value = t('setup.allRequired')
    return
  }
  if (username.value.length < 3) {
    error.value = t('setup.userMinLength')
    return
  }
  if (password.value.length < 6) {
    error.value = t('setup.passMinLength')
    return
  }
  if (password.value !== confirmPassword.value) {
    error.value = t('setup.passNoMatch')
    return
  }
  loading.value = true
  try {
    const res = await fetch('/api/v1/setup/initialize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value }),
    })
    const data = await res.json()
    if (!res.ok) {
      throw new Error(data.detail || t('setup.setupFailed'))
    }
    localStorage.setItem('token', data.access_token)
    await auth.fetchUser()
    router.push('/')
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.setup-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
}

.setup-card {
  background: var(--canvas-light);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-lg);
  padding: 48px;
  width: 100%;
  max-width: 420px;
  animation: authEntrance 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes authEntrance {
  from {
    opacity: 0;
    transform: translateY(24px) scale(0.96);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.setup-header {
  text-align: center;
  margin-bottom: 24px;
}

.setup-icon {
  font-size: 48px;
  display: block;
  margin-bottom: 16px;
  animation: iconFloat 3s ease-in-out infinite;
}

@keyframes iconFloat {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

.setup-header h1 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 4px;
}

.setup-header p {
  color: var(--ink-mute);
  font-size: 14px;
}

.setup-info {
  padding: 14px 18px;
  margin-bottom: 20px;
  font-size: 13px;
  color: var(--ink-mute);
  background: rgba(62, 207, 142, 0.05);
  border-color: rgba(62, 207, 142, 0.2);
}

.setup-info p {
  margin: 0;
}

.form-group {
  margin-bottom: 14px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  color: var(--ink-mute);
}

.error-msg {
  color: var(--danger);
  font-size: 13px;
  margin-bottom: 12px;
}

.setup-btn {
  width: 100%;
  padding: 10px;
  font-size: 15px;
}
</style>
