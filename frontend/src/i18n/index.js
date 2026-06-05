import { ref, computed } from 'vue'
import zh from './zh'
import en from './en'

const messages = { zh, en }

function detectLocale() {
  const saved = localStorage.getItem('locale')
  if (saved && messages[saved]) return saved
  const lang = navigator.language || ''
  return lang.startsWith('zh') ? 'zh' : 'en'
}

const locale = ref(detectLocale())

function t(key, params) {
  let str = messages[locale.value]?.[key] || messages.en[key] || key
  if (params) {
    Object.entries(params).forEach(([k, v]) => {
      str = str.replace(`{${k}}`, v)
    })
  }
  return str
}

function setLocale(lang) {
  if (!messages[lang]) return
  locale.value = lang
  localStorage.setItem('locale', lang)
}

export function useI18n() {
  return { locale, t, setLocale }
}
