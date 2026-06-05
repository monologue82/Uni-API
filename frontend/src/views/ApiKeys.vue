<template>
  <div class="apikeys-page">
    <div class="page-header">
      <h2 class="page-title">{{ t('apikeys.title') }}</h2>
      <button class="btn-primary" @click="showCreate = true">{{ t('apikeys.create') }}</button>
    </div>

    <p class="page-desc">{{ t('apikeys.description') }}</p>

    <div v-if="loading" class="loading">{{ t('routes.loading') }}</div>
    <div v-else-if="keys.length === 0" class="empty card">
      <p>{{ t('apikeys.empty') }}</p>
      <button class="btn-primary" style="margin-top:16px;" @click="showCreate = true">{{ t('apikeys.createFirst') }}</button>
    </div>
    <div v-else class="keys-list">
      <div v-for="k in keys" :key="k.id" class="key-card card anim-item">
        <div class="key-main">
          <div class="key-info">
            <div class="key-name">
              <span class="key-ident">{{ k.name }}</span>
              <span :class="['badge', k.is_active ? 'badge-green' : 'badge-red']">
                {{ k.is_active ? t('apikeys.active') : t('apikeys.disabled') }}
              </span>
            </div>
            <div class="key-value">
              <code>{{ showKeys[k.id] ? k.key : maskKey(k.key) }}</code>
              <button class="btn-icon-sm" @click="toggleShowKey(k.id)" :title="showKeys[k.id] ? t('apikeys.hide') : t('apikeys.show')">
                <svg v-if="!showKeys[k.id]" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
                <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>
              </button>
              <button class="btn-icon-sm" @click="copyKey(k.key)" :title="t('apikeys.copy')">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
              </button>
            </div>
            <p class="key-meta">
              {{ t('apikeys.createdAt') }}: {{ formatDate(k.created_at) }}
              <span v-if="k.username"> · {{ t('apikeys.creator') }}: {{ k.username }}</span>
            </p>
          </div>
          <div class="key-actions">
            <button class="btn-secondary btn-sm" @click="toggleKey(k)">
              {{ k.is_active ? t('apikeys.disable') : t('apikeys.enable') }}
            </button>
            <button class="btn-danger btn-sm" @click="deleteKey(k)">{{ t('routes.delete') }}</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create Modal -->
    <transition name="modal">
      <div v-if="showCreate" class="modal-overlay" @click.self="showCreate = false">
        <div class="modal card">
          <h3 class="modal-title">{{ t('apikeys.create') }}</h3>
          <form @submit.prevent="handleCreate">
            <div class="form-group">
              <label>{{ t('apikeys.keyName') }}</label>
              <input v-model="newName" :placeholder="t('apikeys.keyNamePlaceholder')" />
            </div>
            <p v-if="createError" class="error-msg">{{ createError }}</p>
            <div class="modal-actions">
              <button type="button" class="btn-secondary" @click="showCreate = false">{{ t('form.cancel') }}</button>
              <button type="submit" class="btn-primary" :disabled="creating">
                {{ creating ? t('form.saving') : t('apikeys.create') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useI18n } from '../i18n'
import api from '../api'

const { t } = useI18n()
const keys = ref([])
const loading = ref(true)
const showKeys = reactive({})
const showCreate = ref(false)
const newName = ref('')
const creating = ref(false)
const createError = ref('')

onMounted(() => loadKeys())

async function loadKeys() {
  loading.value = true
  try {
    const res = await api.get('/api/v1/apikeys')
    keys.value = res.data.items
  } catch (e) {
    console.error('Failed to load API keys:', e)
  } finally {
    loading.value = false
  }
}

function maskKey(key) {
  if (!key) return ''
  return key.slice(0, 6) + '•'.repeat(20) + key.slice(-4)
}

function toggleShowKey(id) {
  showKeys[id] = !showKeys[id]
}

async function copyKey(key) {
  try {
    await navigator.clipboard.writeText(key)
  } catch {
    // Fallback
    const ta = document.createElement('textarea')
    ta.value = key
    document.body.appendChild(ta)
    ta.select()
    document.execCommand('copy')
    document.body.removeChild(ta)
  }
}

function formatDate(iso) {
  if (!iso) return '-'
  return new Date(iso).toLocaleString()
}

async function handleCreate() {
  createError.value = ''
  if (!newName.value.trim()) {
    createError.value = t('apikeys.nameRequired')
    return
  }
  creating.value = true
  try {
    await api.post('/api/v1/apikeys', {
      name: newName.value.trim(),
    })
    showCreate.value = false
    newName.value = ''
    await loadKeys()
  } catch (e) {
    createError.value = e.response?.data?.detail || t('form.saveFailed')
  } finally {
    creating.value = false
  }
}

async function toggleKey(key) {
  try {
    await api.put(`/api/v1/apikeys/${key.id}/toggle`)
    await loadKeys()
  } catch (e) {
    alert(e.response?.data?.detail || 'Error')
  }
}

async function deleteKey(key) {
  if (!confirm(t('apikeys.confirmDelete', { name: key.name }))) return
  try {
    await api.delete(`/api/v1/apikeys/${key.id}`)
    await loadKeys()
  } catch (e) {
    alert(e.response?.data?.detail || 'Error')
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.page-title {
  font-size: 22px;
  font-weight: 600;
}

.page-desc {
  color: var(--ink-mute);
  font-size: 13px;
  margin-bottom: 24px;
}

.loading, .empty {
  text-align: center;
  padding: 48px;
  color: var(--ink-mute);
  animation: fadeIn 0.4s ease both;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.keys-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.key-card {
  padding: 20px 24px;
}

.key-card:hover {
  border-color: #444;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.key-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
}

.key-name {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.key-ident {
  font-size: 16px;
  font-weight: 600;
}

.key-value {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
}

.key-value code {
  font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
  font-size: 13px;
  background: var(--canvas);
  padding: 4px 10px;
  border-radius: 4px;
  color: var(--primary);
  letter-spacing: 0.03em;
}

.btn-icon-sm {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: var(--radius-sm);
  background: none;
  border: 1px solid var(--hairline);
  color: var(--ink-mute);
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-icon-sm:hover {
  background: var(--canvas-hover);
  color: var(--ink);
  border-color: #444;
}

.key-meta {
  font-size: 12px;
  color: var(--ink-mute);
}

.key-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

/* Modal */
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
  max-width: 420px;
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

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 20px;
}
</style>
