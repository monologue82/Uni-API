import { createRouter, createWebHistory } from 'vue-router'
import api from '../api'

const routes = [
  {
    path: '/setup',
    name: 'Setup',
    component: () => import('../views/Setup.vue'),
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
  },
  {
    path: '/',
    component: () => import('../components/AppLayout.vue'),
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
      },
      {
        path: 'routes',
        name: 'Routes',
        component: () => import('../views/Routes.vue'),
      },
      {
        path: 'routes/add',
        name: 'RouteAdd',
        component: () => import('../views/RouteForm.vue'),
      },
      {
        path: 'routes/:id/edit',
        name: 'RouteEdit',
        component: () => import('../views/RouteForm.vue'),
      },
      {
        path: 'logs',
        name: 'Logs',
        component: () => import('../views/Logs.vue'),
      },
      {
        path: 'apikeys',
        name: 'ApiKeys',
        component: () => import('../views/ApiKeys.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

let setupChecked = false
let isInitialized = false

router.beforeEach(async (to, from, next) => {
  if (!setupChecked) {
    try {
      const res = await api.get('/api/v1/setup/status')
      isInitialized = res.data.initialized
    } catch {
      // Server not reachable — let the page handle it
    }
    setupChecked = true
  }

  // Setup page: only allow if NOT initialized
  if (to.path === '/setup') {
    if (isInitialized) {
      next('/login')
      return
    }
    next()
    return
  }

  // Not initialized? Force setup (except for setup itself, handled above)
  if (!isInitialized) {
    next('/setup')
    return
  }

  // Normal auth check
  const token = localStorage.getItem('token')
  if (to.path !== '/login' && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/')
  } else {
    next()
  }
})

export default router