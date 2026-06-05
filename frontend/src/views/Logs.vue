<template>
  <div class="logs-page">
    <div class="page-header">
      <h2 class="page-title">{{ t('logs.title') }}</h2>
      <button class="btn-secondary btn-sm" @click="loadLogs">{{ t('logs.refresh') }}</button>
    </div>
    <div v-if="loading" class="loading">{{ t('logs.loading') }}</div>
    <div v-else-if="logs.length === 0" class="empty card">{{ t('logs.empty') }}</div>
    <div v-else class="table-wrap card" style="padding:0;overflow:hidden;">
      <table class="logs-table">
        <thead>
          <tr>
            <th>{{ t('logs.time') }}</th>
            <th>{{ t('logs.route') }}</th>
            <th>{{ t('logs.method') }}</th>
            <th>{{ t('logs.path') }}</th>
            <th>{{ t('logs.statusCode') }}</th>
            <th>{{ t('logs.duration') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in logs" :key="log.id" class="anim-row">
            <td class="cell-time">{{ formatTime(log.created_at) }}</td>
            <td>
              <span class="badge badge-green">{{ log.route_name }}</span>
            </td>
            <td>
              <span :class="['badge', methodBadge(log.method)]">{{ log.method }}</span>
            </td>
            <td class="cell-path">{{ log.path }}</td>
            <td>
              <span :class="['badge', statusBadge(log.status_code)]">{{ log.status_code }}</span>
            </td>
            <td class="cell-dur">{{ log.duration_ms }}ms</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-if="totalPages > 1" class="pagination">
      <button class="btn-secondary btn-sm" :disabled="page <= 1" @click="page--; loadLogs()">{{ t('logs.prev') }}</button>
      <span>{{ t('logs.pageInfo', { page, totalPages, total }) }}</span>
      <button class="btn-secondary btn-sm" :disabled="page >= totalPages" @click="page++; loadLogs()">{{ t('logs.next') }}</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useI18n } from '../i18n'
import api from '../api'

const { t } = useI18n()
const logs = ref([])
const loading = ref(true)
const page = ref(1)
const pageSize = 50
const total = ref(0)

const totalPages = computed(() => Math.max(1, Math.ceil(total.value / pageSize)))

onMounted(() => loadLogs())

async function loadLogs() {
  loading.value = true
  try {
    const res = await api.get('/api/v1/logs', { params: { page: page.value, page_size: pageSize } })
    logs.value = res.data.items
    total.value = res.data.total
  } finally {
    loading.value = false
  }
}

function formatTime(iso) {
  if (!iso) return '-'
  const d = new Date(iso)
  return d.toLocaleString('zh-CN', { hour12: false })
}

function methodBadge(method) {
  const map = { GET: 'badge-green', POST: 'badge-yellow', PUT: 'badge-blue', DELETE: 'badge-red', PATCH: 'badge-purple' }
  return map[method] || 'badge-gray'
}

function statusBadge(code) {
  if (!code) return 'badge-gray'
  if (code < 300) return 'badge-green'
  if (code < 500) return 'badge-yellow'
  return 'badge-red'
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

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.table-wrap {
  overflow-x: auto;
}

.logs-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.logs-table th {
  text-align: left;
  padding: 12px 16px;
  color: var(--ink-mute);
  font-weight: 500;
  border-bottom: 1px solid var(--hairline);
  white-space: nowrap;
}

.logs-table td {
  padding: 10px 16px;
  border-bottom: 1px solid var(--hairline);
}

.logs-table tbody tr:hover {
  background: var(--canvas-hover);
  transition: background 0.15s ease;
}

.anim-row {
  animation: rowSlide 0.35s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.anim-row:nth-child(1)  { animation-delay: 0ms; }
.anim-row:nth-child(2)  { animation-delay: 30ms; }
.anim-row:nth-child(3)  { animation-delay: 60ms; }
.anim-row:nth-child(4)  { animation-delay: 90ms; }
.anim-row:nth-child(5)  { animation-delay: 120ms; }
.anim-row:nth-child(6)  { animation-delay: 150ms; }
.anim-row:nth-child(7)  { animation-delay: 180ms; }
.anim-row:nth-child(8)  { animation-delay: 210ms; }
.anim-row:nth-child(9)  { animation-delay: 240ms; }
.anim-row:nth-child(10) { animation-delay: 270ms; }
.anim-row:nth-child(n+11) { animation-delay: 300ms; }

@keyframes rowSlide {
  from {
    opacity: 0;
    transform: translateX(-8px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.cell-time {
  white-space: nowrap;
  color: var(--ink-mute);
  font-size: 12px;
}

.cell-path {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: var(--ink-mute);
}

.cell-dur {
  white-space: nowrap;
  color: var(--ink-mute);
  font-size: 12px;
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 16px;
  font-size: 13px;
  color: var(--ink-mute);
}

.badge-yellow {
  background: rgba(245, 158, 11, 0.15);
  color: var(--warning);
}

.badge-blue {
  background: rgba(96, 165, 250, 0.15);
  color: #60a5fa;
}

.badge-purple {
  background: rgba(168, 85, 247, 0.15);
  color: #a855f7;
}
</style>
