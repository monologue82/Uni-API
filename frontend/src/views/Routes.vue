<template>
  <div class="routes-page">
    <div class="page-header">
      <h2 class="page-title">{{ t('routes.title') }}</h2>
      <router-link to="/routes/add" class="btn-primary">
        <i class="fa-solid fa-plus"></i>
        {{ t('routes.addRoute') }}
      </router-link>
    </div>
    <div v-if="loading" class="loading">{{ t('routes.loading') }}</div>
    <div v-else-if="routes.length === 0" class="empty card">
      <i class="fa-solid fa-route empty-icon"></i>
      <p>{{ t('routes.empty') }}</p>
      <router-link to="/routes/add" class="btn-primary" style="margin-top:16px;display:inline-block;">
        <i class="fa-solid fa-plus"></i>
        {{ t('routes.addFirst') }}
      </router-link>
    </div>
    <div v-else class="routes-list">
      <div v-for="route in routes" :key="route.id" class="route-card card anim-item">
        <div class="route-main">
          <div class="route-info">
            <div class="route-name">
              <span class="route-ident">{{ route.name }}</span>
              <span v-if="route.model" class="badge badge-blue">{{ route.model }}</span>
              <span :class="['badge', route.is_active ? 'badge-green' : 'badge-red']">
                {{ route.is_active ? t('routes.active') : t('routes.disabled') }}
              </span>
            </div>
            <p class="route-url">{{ route.base_url }}</p>
            <p class="route-desc">{{ route.description || t('routes.noDesc') }}</p>
          </div>
          <div class="route-actions">
            <button class="btn-secondary btn-sm" @click="testRoute(route)">
              <i class="fa-solid fa-paper-plane"></i>
              {{ t('routes.test') }}
            </button>
            <router-link :to="`/routes/${route.id}/edit`" class="btn-secondary btn-sm">
              <i class="fa-solid fa-pen-to-square"></i>
              {{ t('routes.edit') }}
            </router-link>
            <button class="btn-danger btn-sm" @click="confirmDelete(route)">
              <i class="fa-solid fa-trash"></i>
              {{ t('routes.delete') }}
            </button>
          </div>
        </div>
        <div class="route-preview" v-if="route.is_active">
          <code>POST http://localhost:8000/api/v1/gateway/{{ route.name }}/...</code>
        </div>
      </div>
    </div>
    <transition name="modal">
      <div v-if="testResult" class="test-overlay" @click.self="testResult = null">
      <div class="card test-result-card">
        <h4>{{ t('routes.testResult') }}: {{ testTarget }}</h4>
        <div class="test-status" :class="testResult.success ? 'test-ok' : 'test-fail'">
          <i v-if="testResult.success" class="fa-solid fa-circle-check"></i>
          <i v-else class="fa-solid fa-circle-xmark"></i>
          {{ testResult.success ? t('routes.connectSuccess') : t('routes.connectFail') }}
        </div>
        <p v-if="testResult.status_code">HTTP {{ testResult.status_code }}</p>
        <p>{{ testResult.message }}</p>
        <button class="btn-secondary" @click="testResult = null" style="margin-top:12px;">{{ t('routes.close') }}</button>
      </div>
    </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from '../i18n'
import api from '../api'

const { t } = useI18n()
const routes = ref([])
const loading = ref(true)
const testResult = ref(null)
const testTarget = ref('')

onMounted(async () => {
  await loadRoutes()
})

async function loadRoutes() {
  loading.value = true
  try {
    const res = await api.get('/api/v1/routes')
    routes.value = res.data.items
  } finally {
    loading.value = false
  }
}

async function testRoute(route) {
  testTarget.value = route.name
  try {
    const res = await api.post(`/api/v1/routes/${route.id}/test`)
    testResult.value = res.data
  } catch (e) {
    testResult.value = { success: false, message: e.message }
  }
}

async function confirmDelete(route) {
  if (!confirm(t('routes.confirmDelete', { name: route.name }))) return
  try {
    await api.delete(`/api/v1/routes/${route.id}`)
    await loadRoutes()
  } catch (e) {
    alert(t('routes.deleteFailed') + ': ' + (e.response?.data?.detail || e.message))
  }
}
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.page-title {
  font-size: 22px;
  font-weight: 600;
}

.loading, .empty {
  text-align: center;
  padding: 48px;
  color: var(--ink-mute);
  animation: fadeIn 0.4s ease both;
}

.empty-icon {
  display: block;
  font-size: 48px;
  margin-bottom: 16px;
  color: var(--hairline);
}

.btn-primary i,
.btn-secondary i,
.btn-danger i {
  margin-right: 6px;
  font-size: 12px;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.routes-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.route-card {
  padding: 20px 24px;
  cursor: default;
}

.route-card:hover {
  border-color: #444;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.route-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
}

.route-ident {
  font-size: 16px;
  font-weight: 600;
  margin-right: 8px;
}

.route-name {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.route-url {
  color: var(--ink-mute);
  font-size: 13px;
  word-break: break-all;
}

.route-desc {
  color: var(--ink-mute);
  font-size: 12px;
  margin-top: 4px;
}

.route-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.route-preview {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--hairline);
}

.route-preview code {
  background: var(--canvas);
  padding: 6px 10px;
  border-radius: 4px;
  font-size: 12px;
  color: var(--primary);
  word-break: break-all;
  display: block;
}

.test-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.test-result-card {
  max-width: 400px;
  width: 100%;
}

.test-result-card h4 {
  margin-bottom: 12px;
}

.test-status {
  font-size: 16px;
  margin-bottom: 8px;
}

.test-ok { color: var(--primary); }
.test-fail { color: var(--danger); }
</style>
