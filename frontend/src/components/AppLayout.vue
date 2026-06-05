<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="logo">
        <span class="logo-icon">🔌</span>
        <span class="logo-text">Uni-API</span>
      </div>
      <nav class="nav">
        <router-link to="/" class="nav-item" exact-active-class="active">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
          <span>{{ t('nav.dashboard') }}</span>
        </router-link>
        <router-link to="/routes" class="nav-item" active-class="active">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16 3 21 3 21 8"/><line x1="4" y1="20" x2="21" y2="3"/><polyline points="21 16 21 21 16 21"/><line x1="15" y1="15" x2="21" y2="21"/><line x1="4" y1="4" x2="9" y2="9"/></svg>
          <span>{{ t('nav.routes') }}</span>
        </router-link>
        <router-link to="/logs" class="nav-item" active-class="active">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
          <span>{{ t('nav.logs') }}</span>
        </router-link>
        <router-link to="/apikeys" class="nav-item" active-class="active">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4"/></svg>
          <span>{{ t('nav.apikeys') }}</span>
        </router-link>
      </nav>
      <div class="sidebar-footer">
        <div class="user-info">
          <span class="user-avatar">{{ auth.user?.username?.charAt(0)?.toUpperCase() }}</span>
          <span class="user-name">{{ auth.user?.username }}</span>
        </div>
        <div class="user-actions">
          <button class="btn-icon" @click="toggleLocale" :title="locale === 'zh' ? 'Switch to English' : '切换到中文'">
            <transition name="locale-flip" mode="out-in">
              <span class="locale-label" :key="locale">{{ locale === 'zh' ? '中' : 'EN' }}</span>
            </transition>
          </button>
          <button class="btn-secondary btn-sm" @click="showPasswordModal = true" :title="t('common.changePw')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
          </button>
          <button class="btn-secondary btn-sm" @click="handleLogout" :title="t('common.logout')">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
          </button>
        </div>
      </div>
    </aside>
    <main class="main">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" :key="locale" />
        </transition>
      </router-view>
    </main>

    <!-- Change Password Modal -->
    <transition name="modal">
      <div v-if="showPasswordModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal card">
        <h3 class="modal-title">{{ t('pw.title') }}</h3>
        <form @submit.prevent="handleChangePassword">
          <div class="form-group">
            <label>{{ t('pw.current') }}</label>
            <input v-model="pwForm.current" type="password" :placeholder="t('pw.placeholderCurrent')" />
          </div>
          <div class="form-group">
            <label>{{ t('pw.new') }}</label>
            <input v-model="pwForm.new" type="password" :placeholder="t('pw.placeholderNew')" />
          </div>
          <div class="form-group">
            <label>{{ t('pw.confirm') }}</label>
            <input v-model="pwForm.confirm" type="password" :placeholder="t('pw.placeholderConfirm')" />
          </div>
          <p v-if="pwError" class="error-msg">{{ pwError }}</p>
          <p v-if="pwSuccess" class="success-msg">{{ pwSuccess }}</p>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="closeModal">{{ t('pw.cancel') }}</button>
            <button type="submit" class="btn-primary" :disabled="pwLoading">{{ pwLoading ? t('pw.saving') : t('pw.change') }}</button>
          </div>
        </form>
      </div>
    </div>
    </transition>
  </div>
</template>

<script setup>
import { onMounted, ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useI18n } from '../i18n'
import api from '../api'

const auth = useAuthStore()
const router = useRouter()
const { locale, t, setLocale } = useI18n()

onMounted(() => {
  auth.fetchUser()
})

function toggleLocale() {
  setLocale(locale.value === 'zh' ? 'en' : 'zh')
}

function handleLogout() {
  auth.logout()
  router.push('/login')
}

const showPasswordModal = ref(false)
const pwLoading = ref(false)
const pwError = ref('')
const pwSuccess = ref('')
const pwForm = reactive({ current: '', new: '', confirm: '' })

function closeModal() {
  showPasswordModal.value = false
  pwForm.current = ''
  pwForm.new = ''
  pwForm.confirm = ''
  pwError.value = ''
  pwSuccess.value = ''
}

async function handleChangePassword() {
  pwError.value = ''
  pwSuccess.value = ''
  if (!pwForm.current || !pwForm.new || !pwForm.confirm) {
    pwError.value = t('pw.allRequired')
    return
  }
  if (pwForm.new.length < 6) {
    pwError.value = t('pw.minLength')
    return
  }
  if (pwForm.new !== pwForm.confirm) {
    pwError.value = t('pw.noMatch')
    return
  }
  pwLoading.value = true
  try {
    await api.put('/api/v1/auth/password', {
      current_password: pwForm.current,
      new_password: pwForm.new,
    })
    pwSuccess.value = t('pw.success')
    setTimeout(closeModal, 1500)
  } catch (e) {
    pwError.value = e.response?.data?.detail || t('pw.failed')
  } finally {
    pwLoading.value = false
  }
}
</script>

<style scoped>
.layout {
  display: flex;
  min-height: 100vh;
}

.sidebar {
  width: 240px;
  background: #171717;
  border-right: 1px solid var(--hairline);
  display: flex;
  flex-direction: column;
  padding: 20px 0;
  flex-shrink: 0;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 20px 24px;
  animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.nav {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 0 12px;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  color: var(--ink-mute);
  border-radius: var(--radius-sm);
  transition: all 0.2s ease;
  font-size: 14px;
  font-weight: 500;
  animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.nav-item:nth-child(1) { animation-delay: 80ms; }
.nav-item:nth-child(2) { animation-delay: 140ms; }
.nav-item:nth-child(3) { animation-delay: 200ms; }
.nav-item:nth-child(4) { animation-delay: 260ms; }

.nav-item:hover {
  background: var(--canvas-hover);
  color: var(--ink);
}

.nav-item.active {
  background: var(--canvas-light);
  color: var(--primary);
}

.sidebar-footer {
  padding: 16px 20px;
  border-top: 1px solid var(--hairline);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) 0.3s both;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow: hidden;
}

.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--primary);
  color: #171717;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  flex-shrink: 0;
}

.user-name {
  font-size: 13px;
  color: var(--ink-mute);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-actions {
  display: flex;
  gap: 4px;
  align-items: center;
}

.btn-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 30px;
  height: 28px;
  border-radius: var(--radius-sm);
  background: var(--canvas-light);
  border: 1px solid var(--hairline);
  color: var(--ink-mute);
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 11px;
  font-weight: 600;
}

.btn-icon:hover {
  background: var(--canvas-hover);
  color: var(--ink);
  border-color: #444;
}

.btn-icon:active {
  transform: scale(0.9);
}

.locale-label {
  line-height: 1;
  display: inline-block;
}

/* Locale flip animation */
.locale-flip-enter-active {
  transition: opacity 0.2s ease, transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.locale-flip-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.locale-flip-enter-from {
  opacity: 0;
  transform: rotateX(90deg) scale(0.8);
}
.locale-flip-leave-to {
  opacity: 0;
  transform: rotateX(-90deg) scale(0.8);
}

/* Nav text smooth transition on locale change */
.nav-item span {
  transition: opacity 0.2s ease;
}

.main {
  flex: 1;
  padding: 32px 40px;
  overflow-y: auto;
  min-width: 0;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal {
  width: 100%;
  max-width: 400px;
  padding: 28px;
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
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
  margin-bottom: 8px;
}

.success-msg {
  color: var(--primary);
  font-size: 13px;
  margin-bottom: 8px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 20px;
}
</style>
