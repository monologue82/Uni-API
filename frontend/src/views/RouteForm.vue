<template>
  <div class="route-form-page">
    <div class="page-header">
      <h2 class="page-title">{{ isEdit ? t('form.editRoute') : t('form.addRoute') }}</h2>
      <router-link to="/routes" class="btn-secondary">{{ t('form.back') }}</router-link>
    </div>

    <div class="form-layout">
      <!-- Left: Form -->
      <div class="card form-card">
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label>{{ t('form.routeName') }} <span class="required">*</span></label>
            <input v-model="form.name" :placeholder="t('form.routeNamePlaceholder')" :disabled="isEdit" />
            <p class="form-hint">{{ t('form.routeNameHint') }}</p>
          </div>

          <div class="form-group">
            <label>{{ t('form.baseUrl') }} <span class="required">*</span></label>
            <input v-model="form.base_url" :placeholder="t('form.baseUrlPlaceholder')" />
          </div>

          <!-- Format indicator -->
          <div v-if="selectedPreset" class="format-indicator">
            <span :class="['format-badge', formatClass]">{{ formatLabel }}</span>
            <span class="format-hint">{{ formatHint }}</span>
            <button type="button" class="clear-preset" @click="clearPreset" title="Clear selection">
              <i class="fa-solid fa-xmark"></i>
            </button>
          </div>

          <div class="form-group">
            <label>{{ t('form.description') }}</label>
            <input v-model="form.description" :placeholder="t('form.descriptionPlaceholder')" />
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>{{ t('form.apiKey') }}</label>
              <input v-model="form.api_key" type="password" :placeholder="t('form.apiKeyPlaceholder')" />
            </div>
            <div class="form-group">
              <label>{{ t('form.authHeader') }}</label>
              <input v-model="form.api_key_header" placeholder="Authorization" />
            </div>
          </div>

          <!-- Model selector (for all LLM presets) -->
          <div v-if="selectedPreset && (selectedPreset.models_endpoint || selectedPreset.format === 'openai' || selectedPreset.format === 'anthropic' || selectedPreset.format === 'google')" class="form-group model-section">
            <label>{{ t('form.model') }}</label>
            <div class="model-row">
              <div class="model-input-wrap">
                <input
                  v-model="form.model"
                  :placeholder="t('form.modelPlaceholder')"
                  list="model-list"
                />
                <datalist id="model-list">
                  <option v-for="m in availableModels" :key="m" :value="m" />
                </datalist>
              </div>
              <button
                type="button"
                class="btn-secondary btn-sm fetch-btn"
                @click="fetchModels"
                :disabled="modelsLoading || !form.api_key"
                :title="!form.api_key ? t('form.needApiKey') : ''"
              >
                <i v-if="!modelsLoading" class="fa-solid fa-cloud-arrow-down"></i>
                <i v-else class="fa-solid fa-spinner fa-spin"></i>
                {{ modelsLoading ? t('form.fetching') : t('form.fetchModels') }}
              </button>
            </div>
            <p v-if="modelsError" class="error-msg" style="margin-top:4px;">{{ modelsError }}</p>
            <p v-if="availableModels.length" class="form-hint">{{ t('form.modelsLoaded', { count: availableModels.length }) }}</p>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label>{{ t('form.authPrefix') }}</label>
              <input v-model="form.api_key_prefix" placeholder="Bearer " />
            </div>
            <div class="form-group">
              <label>{{ t('form.timeout') }}</label>
              <input v-model.number="form.timeout" type="number" min="1" max="300" />
            </div>
          </div>

          <div class="form-group">
            <label class="checkbox-label">
              <input v-model="form.is_active" type="checkbox" />
              <span>{{ t('form.enableRoute') }}</span>
            </label>
          </div>

          <p v-if="error" class="error-msg">{{ error }}</p>
          <div class="form-actions">
            <button type="submit" class="btn-primary" :disabled="saving">
              {{ saving ? t('form.saving') : (isEdit ? t('form.updateRoute') : t('form.createRoute')) }}
            </button>
            <router-link to="/routes" class="btn-secondary">{{ t('form.cancel') }}</router-link>
          </div>
        </form>

        <div v-if="showPreview" class="route-preview">
          <h4>{{ t('form.proxyPreview') }}</h4>
          <code>{{ previewUrl }}</code>
        </div>
      </div>

      <!-- Right: Preset Panel -->
      <div v-if="!isEdit" class="preset-panel card">
        <div class="preset-header">
          <h3>{{ t('form.apiType') }} <span v-if="!presetsLoading && !presetsError" class="preset-count">{{ filteredPresets.length }}/{{ apiTypes.length }}</span></h3>
          <div class="preset-search">
            <i class="fa-solid fa-magnifying-glass search-icon"></i>
            <input
              v-model="searchQuery"
              :placeholder="t('form.searchPresets')"
              class="search-input"
            />
          </div>
        </div>

        <!-- Category tabs -->
        <div class="category-tabs">
          <button
            :class="['cat-tab', { active: !activeCategory }]"
            @click="activeCategory = ''"
          >{{ t('form.allPresets') }}</button>
          <button
            v-for="cat in categories"
            :key="cat"
            :class="['cat-tab', { active: activeCategory === cat }]"
            @click="activeCategory = cat"
          >{{ cat }}</button>
        </div>

        <!-- Preset list -->
        <div class="preset-list">
          <div v-if="presetsLoading" class="preset-empty">
            {{ t('routes.loading') }}
          </div>
          <div v-else-if="presetsError" class="preset-empty">
            <p>{{ t('form.loadFailed') }}</p>
            <button class="btn-secondary btn-sm" style="margin-top:8px;" @click="loadPresets">{{ t('logs.refresh') }}</button>
          </div>
          <template v-else>
            <div
              v-for="preset in filteredPresets"
              :key="preset.id"
              :class="['preset-item', { selected: selectedType === preset.id }]"
              @click="selectPreset(preset)"
            >
              <div class="preset-main">
                <span class="preset-name">{{ preset.name }}</span>
                <span v-if="preset.format !== 'rest'" :class="['preset-format', 'fmt-' + preset.format]">
                  {{ preset.format }}
                </span>
              </div>
              <p class="preset-desc">{{ preset.description }}</p>
            </div>
            <div v-if="filteredPresets.length === 0 && apiTypes.length === 0" class="preset-empty">
              <p>{{ t('form.noPresets') }}</p>
              <p class="preset-empty-hint">请检查后端服务是否正常运行</p>
            </div>
            <div v-else-if="filteredPresets.length === 0" class="preset-empty">
              {{ t('form.noPresets') }}
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from '../i18n'
import api from '../api'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)
const { t } = useI18n()

const apiTypes = ref([])
const selectedType = ref('')
const searchQuery = ref('')
const activeCategory = ref('')
const presetsLoading = ref(true)
const presetsError = ref(false)
const availableModels = ref([])
const modelsLoading = ref(false)
const modelsError = ref('')
const form = ref({
  name: '',
  base_url: '',
  description: '',
  api_key: '',
  api_key_header: 'Authorization',
  api_key_prefix: 'Bearer ',
  api_type: 'custom',
  model: '',
  timeout: 30,
  is_active: true,
})

const saving = ref(false)
const error = ref('')

const selectedPreset = computed(() =>
  apiTypes.value.find(p => p.id === selectedType.value) || null
)

const showPreview = computed(() => form.value.name.length > 0)

const previewUrl = computed(() => {
  const name = form.value.name || '{name}'
  const fmt = selectedPreset.value?.format
  if (fmt === 'anthropic') return `POST http://localhost:8000/api/v1/gateway/${name}/v1/messages`
  if (fmt === 'google') return `POST http://localhost:8000/api/v1/gateway/${name}/v1beta/models/{model}:generateContent`
  return `POST http://localhost:8000/api/v1/gateway/${name}/v1/chat/completions`
})

const formatClass = computed(() => {
  const fmt = selectedPreset.value?.format
  if (fmt === 'openai') return 'format-openai'
  if (fmt === 'anthropic') return 'format-anthropic'
  if (fmt === 'google') return 'format-google'
  return 'format-rest'
})

const formatLabel = computed(() => {
  const fmt = selectedPreset.value?.format
  if (fmt === 'openai') return t('form.formatOpenai')
  if (fmt === 'anthropic') return t('form.formatAnthropic')
  if (fmt === 'google') return t('form.formatGoogle')
  return 'REST'
})

const formatHint = computed(() => {
  const fmt = selectedPreset.value?.format
  if (fmt === 'openai') return t('form.formatHintOpenai')
  if (fmt === 'anthropic') return t('form.formatHintAnthropic')
  if (fmt === 'google') return t('form.formatHintGoogle')
  return ''
})

const categories = computed(() => {
  const cats = [...new Set(apiTypes.value.map(p => p.category))]
  return cats
})

const filteredPresets = computed(() => {
  let list = apiTypes.value
  // When searching, filter across all categories
  if (searchQuery.value.trim()) {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(p =>
      p.name.toLowerCase().includes(q) ||
      p.description.toLowerCase().includes(q) ||
      p.base_url.toLowerCase().includes(q) ||
      p.category.toLowerCase().includes(q)
    )
    return list
  }
  // Otherwise filter by active category
  if (activeCategory.value) {
    list = list.filter(p => p.category === activeCategory.value)
  }
  return list
})

function selectPreset(preset) {
  selectedType.value = preset.id
  if (preset.base_url) form.value.base_url = preset.base_url
  form.value.api_key_header = preset.api_key_header
  form.value.api_key_prefix = preset.api_key_prefix
  form.value.api_type = preset.id
  form.value.model = ''
  availableModels.value = []
  modelsError.value = ''
}

function clearPreset() {
  selectedType.value = ''
  form.value.base_url = ''
  form.value.api_key_header = 'Authorization'
  form.value.api_key_prefix = 'Bearer '
  form.value.api_type = 'custom'
  form.value.model = ''
  availableModels.value = []
}

async function fetchModels() {
  if (!selectedPreset.value || !form.value.api_key) return
  modelsLoading.value = true
  modelsError.value = ''
  availableModels.value = []
  const preset = selectedPreset.value
  try {
    // Try direct API call first (user's own environment)
    const url = preset.base_url.replace(/\/+$/, '') + preset.models_endpoint
    const headers = {}
    if (preset.api_key_header) {
      headers[preset.api_key_header] = `${preset.api_key_prefix}${form.value.api_key}`
    }
    const res = await fetch(url, { headers })
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    const data = await res.json()
    const models = _extractModels(data, preset.models_key)
    availableModels.value = models
    if (models.length === 0) {
      modelsError.value = t('form.noModelsFound')
    }
  } catch (e) {
    // CORS or network error — fall back to backend proxy
    try {
      const res = await api.get(`/api/v1/models/${preset.id}`, {
        params: { api_key: form.value.api_key },
      })
      availableModels.value = res.data.models || []
      if (availableModels.value.length === 0) {
        modelsError.value = t('form.noModelsFound')
      }
    } catch (e2) {
      const detail = e2.response?.data?.detail || ''
      if (detail.toLowerCase().includes('authentication failed')) {
        // Show localized auth error; append upstream reason in parentheses if present
        const match = detail.match(/\((.+)\)\s*$/)
        modelsError.value = match
          ? `${t('form.authFailed')} (${match[1]})`
          : t('form.authFailed')
      } else {
        modelsError.value = detail || t('form.fetchModelsFailed')
      }
    }
  } finally {
    modelsLoading.value = false
  }
}

function _extractModels(data, keyPath) {
  const parts = keyPath.split('.')
  let current = data
  for (let i = 0; i < parts.length; i++) {
    const part = parts[i]
    if (part === '*') {
      if (!Array.isArray(current)) return []
      const remaining = parts.slice(i + 1).join('.')
      const results = []
      for (const item of current) {
        results.push(...(remaining ? _extractModels(item, remaining) : [String(item)]))
      }
      return results
    }
    if (current && typeof current === 'object') {
      current = current[part]
    } else {
      return []
    }
  }
  if (Array.isArray(current) && parts.length >= 2) {
    const field = parts[parts.length - 1]
    return current
      .filter(item => item && typeof item === 'object' && item[field])
      .map(item => item[field])
      .sort()
  }
  return []
}

async function loadPresets() {
  presetsLoading.value = true
  presetsError.value = false
  try {
    const res = await api.get('/api/v1/routes/types')
    console.log('Presets API response:', res.data)
    if (Array.isArray(res.data)) {
      apiTypes.value = res.data
    } else if (res.data && typeof res.data === 'object') {
      // Maybe wrapped in { items: [...] } or similar
      apiTypes.value = res.data.items || res.data.data || res.data.presets || []
    } else {
      apiTypes.value = []
    }
    console.log('Loaded presets:', apiTypes.value.length)
  } catch (e) {
    console.error('Failed to load presets:', e)
    presetsError.value = true
    apiTypes.value = []
  } finally {
    presetsLoading.value = false
  }
}

onMounted(async () => {
  await loadPresets()

  if (isEdit.value) {
    try {
      const res = await api.get(`/api/v1/routes/${route.params.id}`)
      const d = res.data
      form.value = {
        name: d.name,
        base_url: d.base_url,
        description: d.description,
        api_key: '',
        api_key_header: d.api_key_header,
        api_key_prefix: d.api_key_prefix,
        api_type: d.api_type || 'custom',
        model: d.model || '',
        timeout: d.timeout,
        is_active: d.is_active,
      }
      selectedType.value = d.api_type || 'custom'
    } catch {
      error.value = t('form.loadFailed')
    }
  }
})

async function handleSubmit() {
  error.value = ''
  if (!form.value.name || !form.value.base_url) {
    error.value = t('form.nameAndUrlRequired')
    return
  }
  saving.value = true
  try {
    if (isEdit.value) {
      await api.put(`/api/v1/routes/${route.params.id}`, form.value)
    } else {
      await api.post('/api/v1/routes', form.value)
    }
    router.push('/routes')
  } catch (e) {
    error.value = e.response?.data?.detail || t('form.saveFailed')
  } finally {
    saving.value = false
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

/* Two-column layout */
.form-layout {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.form-card {
  flex: 1;
  min-width: 0;
  animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 13px;
  color: var(--ink-mute);
}

.required { color: var(--danger); }

.form-hint {
  font-size: 12px;
  color: var(--ink-mute);
  margin-top: 4px;
}

/* Model section */
.model-section {
  background: var(--canvas);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  padding: 14px;
  margin-bottom: 16px;
}

.model-section label {
  margin-bottom: 8px;
}

.model-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.model-input-wrap {
  flex: 1;
}

.model-input-wrap input {
  width: 100%;
}

.fetch-btn {
  white-space: nowrap;
  flex-shrink: 0;
}

.fetch-btn i {
  margin-right: 6px;
  font-size: 12px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.checkbox-label {
  display: flex !important;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: auto;
  accent-color: var(--primary);
}

.error-msg {
  color: var(--danger);
  font-size: 13px;
  margin-bottom: 12px;
}

.form-actions {
  display: flex;
  gap: 8px;
  margin-top: 24px;
}

.route-preview {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid var(--hairline);
}

.route-preview h4 {
  margin-bottom: 8px;
  font-size: 14px;
  font-weight: 500;
}

.route-preview code {
  background: var(--canvas);
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 12px;
  color: var(--primary);
  word-break: break-all;
  display: block;
}

/* Format indicator */
.format-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 16px;
  padding: 10px 14px;
  background: var(--canvas);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  animation: fadeIn 0.3s ease both;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.format-badge {
  display: inline-flex;
  padding: 3px 10px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

.format-openai { background: rgba(16, 163, 127, 0.15); color: #10a37f; }
.format-anthropic { background: rgba(204, 148, 79, 0.15); color: #cc944f; }
.format-google { background: rgba(66, 133, 244, 0.15); color: #4285f4; }
.format-rest { background: rgba(138, 138, 138, 0.15); color: var(--ink-mute); }

.format-hint {
  font-size: 12px;
  color: var(--ink-mute);
  flex: 1;
}

.clear-preset {
  background: none;
  border: none;
  color: var(--ink-mute);
  cursor: pointer;
  font-size: 14px;
  padding: 2px 6px;
  border-radius: 4px;
  transition: all 0.15s ease;
}

.clear-preset:hover {
  background: var(--canvas-hover);
  color: var(--danger);
}

/* ===== Preset Panel ===== */
.preset-panel {
  width: 380px;
  flex-shrink: 0;
  padding: 0;
  animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) 0.15s both;
  position: sticky;
  top: 32px;
  align-self: flex-start;
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 64px);
  overflow: hidden;
}

.preset-header {
  padding: 20px 20px 0;
}

.preset-header h3 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.preset-count {
  font-size: 11px;
  font-weight: 500;
  color: var(--ink-mute);
  background: var(--canvas);
  padding: 2px 8px;
  border-radius: 9999px;
}

.preset-search {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 10px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--ink-mute);
  pointer-events: none;
  font-size: 13px;
}

.search-input {
  width: 100%;
  padding: 7px 12px 7px 32px;
  font-size: 13px;
  background: var(--canvas);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  color: var(--ink);
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
}

.search-input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(62, 207, 142, 0.12);
  outline: none;
}

/* Category tabs */
.category-tabs {
  display: flex;
  gap: 0;
  padding: 12px 20px 0;
  overflow-x: auto;
  overflow-y: visible;
  scrollbar-width: none;
  -ms-overflow-style: none;
  flex-wrap: wrap;
}

.category-tabs::-webkit-scrollbar { display: none; }

.cat-tab {
  padding: 5px 10px;
  font-size: 11px;
  font-weight: 500;
  color: var(--ink-mute);
  background: none;
  border: 1px solid transparent;
  border-radius: 9999px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
  margin-bottom: 4px;
}

.cat-tab:hover {
  color: var(--ink);
  background: var(--canvas-hover);
}

.cat-tab.active {
  color: var(--primary);
  background: rgba(62, 207, 142, 0.1);
  border-color: rgba(62, 207, 142, 0.3);
}

/* Preset list */
.preset-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px 12px 12px;
  scrollbar-width: thin;
  scrollbar-color: var(--hairline) transparent;
}

.preset-list::-webkit-scrollbar {
  width: 5px;
}

.preset-list::-webkit-scrollbar-track {
  background: transparent;
}

.preset-list::-webkit-scrollbar-thumb {
  background: var(--hairline);
  border-radius: 3px;
}

.preset-item {
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid transparent;
}

.preset-item:hover {
  background: var(--canvas-hover);
}

.preset-item.selected {
  background: rgba(62, 207, 142, 0.08);
  border-color: rgba(62, 207, 142, 0.25);
}

.preset-main {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 2px;
}

.preset-name {
  font-size: 13px;
  font-weight: 500;
  color: var(--ink);
}

.preset-format {
  font-size: 10px;
  font-weight: 600;
  padding: 1px 6px;
  border-radius: 9999px;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.fmt-openai { background: rgba(16, 163, 127, 0.12); color: #10a37f; }
.fmt-anthropic { background: rgba(204, 148, 79, 0.12); color: #cc944f; }
.fmt-google { background: rgba(66, 133, 244, 0.12); color: #4285f4; }

.preset-desc {
  font-size: 11px;
  color: var(--ink-mute);
  line-height: 1.4;
}

.preset-empty {
  text-align: center;
  padding: 32px 16px;
  color: var(--ink-mute);
  font-size: 13px;
}

.preset-empty-hint {
  font-size: 11px;
  color: var(--ink-mute);
  margin-top: 4px;
  opacity: 0.7;
}

/* Responsive */
@media (max-width: 900px) {
  .form-layout {
    flex-direction: column;
  }
  .preset-panel {
    width: 100%;
    position: static;
    max-height: none;
  }
}
</style>
