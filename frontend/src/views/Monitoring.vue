<template>
  <div class="monitoring">
    <h2 class="page-title">{{ t('monitoring.title') }}</h2>

    <!-- Stat Cards -->
    <div class="stats-grid">
      <div class="stat-card card anim-item">
        <div class="stat-icon" style="background:rgba(62,207,142,0.15);color:var(--primary)">
          <i class="fa-solid fa-bolt"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ summary.current_qps?.toFixed(1) || '0' }}</span>
          <span class="stat-label">QPS</span>
        </div>
      </div>
      <div class="stat-card card anim-item">
        <div class="stat-icon" style="background:rgba(239,68,68,0.15);color:var(--danger)">
          <i class="fa-solid fa-triangle-exclamation"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ summary.error_rate_5min?.toFixed(1) || '0' }}%</span>
          <span class="stat-label">{{ t('monitoring.errorRate') }}</span>
        </div>
      </div>
      <div class="stat-card card anim-item">
        <div class="stat-icon" style="background:rgba(96,165,250,0.15);color:#60a5fa">
          <i class="fa-solid fa-clock"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ formatMs(summary.avg_latency_5min) }}</span>
          <span class="stat-label">{{ t('monitoring.avgLatency') }}</span>
        </div>
      </div>
      <div class="stat-card card anim-item">
        <div class="stat-icon" style="background:rgba(168,85,247,0.15);color:#a855f7">
          <i class="fa-solid fa-link"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ summary.active_connections || 0 }}</span>
          <span class="stat-label">{{ t('monitoring.connections') }}</span>
        </div>
      </div>
      <div class="stat-card card anim-item">
        <div class="stat-icon" style="background:rgba(245,158,11,0.15);color:var(--warning)">
          <i class="fa-solid fa-server"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ sys.cpu_percent?.toFixed(0) || '0' }}%</span>
          <span class="stat-label">CPU</span>
        </div>
      </div>
      <div class="stat-card card anim-item">
        <div class="stat-icon" style="background:rgba(236,72,153,0.15);color:#ec4899">
          <i class="fa-solid fa-memory"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ sys.memory_percent?.toFixed(0) || '0' }}%</span>
          <span class="stat-label">{{ t('monitoring.memory') }}</span>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="charts-row">
      <div class="card chart-card anim-item">
        <h3 class="card-title">{{ t('monitoring.requestTrend') }}</h3>
        <div class="chart-container">
          <svg v-if="tsData.length" :viewBox="`0 0 ${tsData.length - 1} ${maxRequests}`" preserveAspectRatio="none" class="sparkline">
            <polyline :points="requestPoints" fill="none" stroke="var(--primary)" stroke-width="1.5" vector-effect="non-scaling-stroke" />
            <polyline v-if="errorPoints" :points="errorPoints" fill="none" stroke="var(--danger)" stroke-width="1.5" vector-effect="non-scaling-stroke" />
          </svg>
          <div v-else class="chart-empty">{{ t('monitoring.noData') }}</div>
        </div>
        <div class="chart-legend">
          <span class="legend-item"><span class="legend-dot" style="background:var(--primary)"></span>{{ t('monitoring.requests') }}</span>
          <span class="legend-item"><span class="legend-dot" style="background:var(--danger)"></span>{{ t('monitoring.errors') }}</span>
        </div>
      </div>
      <div class="card chart-card anim-item">
        <h3 class="card-title">{{ t('monitoring.latencyTrend') }}</h3>
        <div class="chart-container">
          <svg v-if="tsData.length" :viewBox="`0 0 ${tsData.length - 1} ${maxLatency || 1}`" preserveAspectRatio="none" class="sparkline">
            <polyline :points="latencyPoints" fill="none" stroke="#60a5fa" stroke-width="1.5" vector-effect="non-scaling-stroke" />
          </svg>
          <div v-else class="chart-empty">{{ t('monitoring.noData') }}</div>
        </div>
        <div class="chart-legend">
          <span class="legend-item"><span class="legend-dot" style="background:#60a5fa"></span>{{ t('monitoring.avgLatency') }} (ms)</span>
        </div>
      </div>
    </div>

    <!-- System Resources -->
    <div class="card anim-item" style="margin-top: 16px;">
      <h3 class="card-title">{{ t('monitoring.systemResources') }}</h3>
      <div class="resource-bars">
        <div class="resource-item">
          <div class="resource-header">
            <span>CPU</span>
            <span>{{ sys.cpu_percent?.toFixed(1) || '0' }}%</span>
          </div>
          <div class="resource-bar"><div class="resource-fill cpu" :style="{ width: (sys.cpu_percent || 0) + '%' }"></div></div>
        </div>
        <div class="resource-item">
          <div class="resource-header">
            <span>{{ t('monitoring.memory') }}</span>
            <span>{{ sys.memory_used_mb ? (sys.memory_used_mb / 1024).toFixed(1) : '0' }} / {{ sys.memory_total_mb ? (sys.memory_total_mb / 1024).toFixed(1) : '0' }} GB</span>
          </div>
          <div class="resource-bar"><div class="resource-fill memory" :style="{ width: (sys.memory_percent || 0) + '%' }"></div></div>
        </div>
        <div class="resource-item">
          <div class="resource-header">
            <span>{{ t('monitoring.disk') }}</span>
            <span>{{ sys.disk_used_gb?.toFixed(1) || '0' }} / {{ sys.disk_total_gb?.toFixed(1) || '0' }} GB</span>
          </div>
          <div class="resource-bar"><div class="resource-fill disk" :style="{ width: (sys.disk_percent || 0) + '%' }"></div></div>
        </div>
        <div class="resource-item">
          <div class="resource-header">
            <span>{{ t('monitoring.network') }}</span>
            <span>↑{{ sys.net_sent_rate?.toFixed(2) || '0' }} MB/s ↓{{ sys.net_recv_rate?.toFixed(2) || '0' }} MB/s</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Route Stats Table -->
    <div class="card anim-item" style="margin-top: 16px;">
      <h3 class="card-title">{{ t('monitoring.routeStats') }}</h3>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>{{ t('monitoring.route') }}</th>
              <th>{{ t('monitoring.requests') }}</th>
              <th>{{ t('monitoring.errors') }}</th>
              <th>{{ t('monitoring.errorRate') }}</th>
              <th>{{ t('monitoring.avgLatency') }}</th>
              <th>{{ t('monitoring.maxLatency') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in routes" :key="r.route">
              <td><code>{{ r.route }}</code></td>
              <td>{{ r.requests }}</td>
              <td :class="{ 'text-danger': r.errors > 0 }">{{ r.errors }}</td>
              <td :class="{ 'text-danger': r.error_rate > 5 }">{{ r.error_rate }}%</td>
              <td>{{ formatMs(r.avg_latency) }}</td>
              <td>{{ formatMs(r.max_latency) }}</td>
            </tr>
            <tr v-if="!routes.length">
              <td colspan="6" class="empty-row">{{ t('monitoring.noRoutes') }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Active Alerts -->
    <div class="card anim-item" style="margin-top: 16px;">
      <h3 class="card-title">
        {{ t('monitoring.alerts') }}
        <span v-if="alerts.active?.length" class="badge badge-red" style="margin-left: 8px;">{{ alerts.active.length }}</span>
      </h3>
      <div v-if="alerts.active?.length" class="alerts-list">
        <div v-for="a in alerts.active" :key="a.rule" class="alert-item" :class="'alert-' + a.severity">
          <i class="fa-solid fa-circle-exclamation"></i>
          <div class="alert-body">
            <span class="alert-msg">{{ a.message }}</span>
            <span class="alert-time">{{ t('monitoring.duration') }}: {{ formatDuration(a.duration_seconds) }}</span>
          </div>
        </div>
      </div>
      <div v-else class="empty-state">
        <i class="fa-solid fa-check-circle" style="color: var(--primary); font-size: 24px;"></i>
        <span>{{ t('monitoring.noAlerts') }}</span>
      </div>
    </div>

    <!-- Uptime -->
    <div class="uptime-bar anim-item">
      {{ t('monitoring.uptime') }}: {{ formatDuration(summary.uptime_seconds || 0) }}
      &nbsp;|&nbsp;
      {{ t('monitoring.totalRequests') }}: {{ summary.total_requests || 0 }}
      &nbsp;|&nbsp;
      {{ t('monitoring.p99Latency') }}: {{ formatMs(summary.p99_latency) }}
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from '../i18n'
import api from '../api'

const { t } = useI18n()

const summary = ref({})
const tsData = ref([])
const routes = ref([])
const sys = ref({})
const alerts = ref({ active: [], history: [] })
let timer = null

// Computed: sparkline SVG points
const maxRequests = computed(() => {
  const max = Math.max(...tsData.value.map(d => d.requests), 1)
  return max
})

const maxLatency = computed(() => {
  return Math.max(...tsData.value.map(d => d.avg_latency), 1)
})

const requestPoints = computed(() => {
  return tsData.value.map((d, i) => `${i},${maxRequests.value - d.requests}`).join(' ')
})

const errorPoints = computed(() => {
  if (!tsData.value.some(d => d.errors > 0)) return null
  return tsData.value.map((d, i) => `${i},${maxRequests.value - d.errors}`).join(' ')
})

const latencyPoints = computed(() => {
  const max = maxLatency.value || 1
  return tsData.value.map((d, i) => `${i},${max - d.avg_latency}`).join(' ')
})

function formatMs(ms) {
  if (!ms && ms !== 0) return '-'
  if (ms < 1) return '<1ms'
  if (ms < 1000) return Math.round(ms) + 'ms'
  return (ms / 1000).toFixed(2) + 's'
}

function formatDuration(seconds) {
  if (!seconds) return '0s'
  const h = Math.floor(seconds / 3600)
  const m = Math.floor((seconds % 3600) / 60)
  const s = seconds % 60
  if (h > 0) return `${h}h ${m}m`
  if (m > 0) return `${m}m ${s}s`
  return `${s}s`
}

async function fetchAll() {
  try {
    const [sumRes, tsRes, routeRes, sysRes, alertRes] = await Promise.all([
      api.get('/api/v1/monitoring/summary'),
      api.get('/api/v1/monitoring/timeseries'),
      api.get('/api/v1/monitoring/routes'),
      api.get('/api/v1/monitoring/system'),
      api.get('/api/v1/monitoring/alerts'),
    ])
    summary.value = sumRes.data
    tsData.value = tsRes.data
    routes.value = routeRes.data
    sys.value = sysRes.data
    alerts.value = alertRes.data
  } catch (e) {
    console.error('Failed to fetch monitoring data', e)
  }
}

onMounted(() => {
  fetchAll()
  timer = setInterval(fetchAll, 3000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.page-title {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 24px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 12px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 18px;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 20px;
  font-weight: 600;
}

.stat-label {
  font-size: 12px;
  color: var(--ink-mute);
  margin-top: 2px;
}

.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 16px;
}

.chart-card {
  padding: 20px;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 12px;
}

.chart-container {
  height: 120px;
  position: relative;
}

.sparkline {
  width: 100%;
  height: 100%;
}

.chart-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--ink-mute);
  font-size: 13px;
}

.chart-legend {
  display: flex;
  gap: 16px;
  margin-top: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--ink-mute);
}

.legend-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.resource-bars {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.resource-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.resource-header {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: var(--ink-mute);
}

.resource-bar {
  height: 6px;
  background: var(--canvas);
  border-radius: 3px;
  overflow: hidden;
}

.resource-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.resource-fill.cpu { background: var(--warning); }
.resource-fill.memory { background: #ec4899; }
.resource-fill.disk { background: #a855f7; }

.table-wrap {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.data-table th,
.data-table td {
  text-align: left;
  padding: 10px 12px;
  border-bottom: 1px solid var(--hairline);
}

.data-table th {
  color: var(--ink-mute);
  font-weight: 500;
  font-size: 12px;
}

.data-table code {
  background: var(--canvas);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 12px;
  color: var(--primary);
}

.text-danger { color: var(--danger); }

.empty-row {
  text-align: center;
  color: var(--ink-mute);
  padding: 24px !important;
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.alert-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: var(--radius-sm);
  font-size: 13px;
}

.alert-item.alert-warning {
  background: rgba(245, 158, 11, 0.1);
  border: 1px solid rgba(245, 158, 11, 0.3);
  color: var(--warning);
}

.alert-item.alert-critical {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: var(--danger);
}

.alert-body {
  display: flex;
  flex-direction: column;
}

.alert-msg { font-weight: 500; }
.alert-time { font-size: 11px; opacity: 0.7; margin-top: 2px; }

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 24px;
  color: var(--ink-mute);
  font-size: 13px;
}

.uptime-bar {
  margin-top: 16px;
  padding: 10px 16px;
  background: var(--canvas-light);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  font-size: 12px;
  color: var(--ink-mute);
  text-align: center;
}

@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .charts-row {
    grid-template-columns: 1fr;
  }
}
</style>
