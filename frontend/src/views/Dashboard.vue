<template>
  <div class="dashboard">
    <h2 class="page-title">{{ t('dashboard.title') }}</h2>
    <div class="stats-grid">
      <div class="stat-card card anim-item">
        <div class="stat-icon routes-icon">
          <i class="fa-solid fa-route"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.totalRoutes }}</span>
          <span class="stat-label">{{ t('dashboard.totalRoutes') }}</span>
        </div>
      </div>
      <div class="stat-card card anim-item">
        <div class="stat-icon active-icon">
          <i class="fa-solid fa-check"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.activeRoutes }}</span>
          <span class="stat-label">{{ t('dashboard.activeRoutes') }}</span>
        </div>
      </div>
      <div class="stat-card card anim-item">
        <div class="stat-icon logs-icon">
          <i class="fa-solid fa-file-lines"></i>
        </div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.totalLogs || 0 }}</span>
          <span class="stat-label">{{ t('dashboard.todayCalls') }}</span>
        </div>
      </div>
    </div>
    <div class="card guide-card" style="margin-top: 24px;">
      <h3 style="margin-bottom: 16px; font-size: 16px; font-weight: 500;">{{ t('dashboard.quickStart') }}</h3>
      <div class="guide">
        <div class="guide-step anim-item">
          <span class="step-num">1</span>
          <div>
            <strong>{{ t('dashboard.step1Title') }}</strong>
            <p>{{ t('dashboard.step1Desc') }}</p>
          </div>
        </div>
        <div class="guide-step anim-item">
          <span class="step-num">2</span>
          <div>
            <strong>{{ t('dashboard.step2Title') }}</strong>
            <p>{{ t('dashboard.step2Desc') }}<code>http://your-host:8000/api/v1/gateway/{route_name}/{path}</code></p>
          </div>
        </div>
        <div class="guide-step anim-item">
          <span class="step-num">3</span>
          <div>
            <strong>{{ t('dashboard.step3Title') }}</strong>
            <p>{{ t('dashboard.step3Desc') }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from '../i18n'
import api from '../api'

const { t } = useI18n()
const stats = ref({ totalRoutes: 0, activeRoutes: 0, totalLogs: 0 })

onMounted(async () => {
  try {
    const [routesRes, logsRes] = await Promise.all([
      api.get('/api/v1/routes'),
      api.get('/api/v1/logs?page_size=1&today=true'),
    ])
    stats.value.totalRoutes = routesRes.data.total
    stats.value.activeRoutes = routesRes.data.items.filter(r => r.is_active).length
    stats.value.totalLogs = logsRes.data.total
  } catch (e) {
    console.error('Failed to load dashboard stats', e)
  }
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
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: default;
}

.stat-card:hover {
  border-color: #444;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.guide-card {
  animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) 0.35s both;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 22px;
}

.routes-icon {
  background: rgba(62, 207, 142, 0.15);
  color: var(--primary);
}
.active-icon {
  background: rgba(34, 197, 94, 0.15);
  color: #22c55e;
}
.logs-icon {
  background: rgba(96, 165, 250, 0.15);
  color: #60a5fa;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
}

.stat-label {
  font-size: 13px;
  color: var(--ink-mute);
  margin-top: 2px;
}

.guide {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.guide-step {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.step-num {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--primary);
  color: #171717;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  flex-shrink: 0;
  margin-top: 1px;
}

.guide-step strong {
  display: block;
  font-weight: 500;
  margin-bottom: 2px;
}

.guide-step p {
  color: var(--ink-mute);
  font-size: 13px;
}

code {
  background: var(--canvas);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'SF Mono', 'Menlo', 'Consolas', monospace;
  font-size: 12px;
  color: var(--primary);
}
</style>
