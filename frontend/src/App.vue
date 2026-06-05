<template>
  <router-view v-slot="{ Component }">
    <transition name="page" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

:root {
  --primary: #3ecf8e;
  --primary-deep: #24b47e;
  --ink: #e0e0e0;
  --ink-mute: #8a8a8a;
  --canvas: #1c1c1c;
  --canvas-light: #212121;
  --canvas-hover: #2a2a2a;
  --hairline: #333333;
  --danger: #ef4444;
  --warning: #f59e0b;
  --font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --radius-sm: 6px;
  --radius-md: 8px;
  --radius-lg: 12px;
}

body {
  font-family: var(--font);
  background: var(--canvas);
  color: var(--ink);
  min-height: 100vh;
  font-size: 14px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

a {
  color: var(--primary);
  text-decoration: none;
}

input, select, textarea {
  font-family: var(--font);
  font-size: 14px;
  background: var(--canvas);
  color: var(--ink);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-sm);
  padding: 8px 12px;
  outline: none;
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
  width: 100%;
}

input:focus, select:focus, textarea:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(62, 207, 142, 0.12);
}

button {
  font-family: var(--font);
  cursor: pointer;
  border: none;
  outline: none;
  font-size: 14px;
  font-weight: 500;
}

.btn-primary {
  background: var(--primary);
  color: #171717;
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease;
}

.btn-primary:hover {
  background: var(--primary-deep);
  box-shadow: 0 2px 8px rgba(62, 207, 142, 0.25);
}

.btn-primary:active {
  transform: scale(0.97);
}

.btn-secondary {
  background: var(--canvas-light);
  color: var(--ink);
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--hairline);
  transition: background 0.2s ease, border-color 0.2s ease, transform 0.15s ease;
}

.btn-secondary:hover {
  background: var(--canvas-hover);
  border-color: #444;
}

.btn-secondary:active {
  transform: scale(0.97);
}

.btn-danger {
  background: transparent;
  color: var(--danger);
  padding: 8px 16px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--danger);
  transition: all 0.2s ease, transform 0.15s ease;
}

.btn-danger:hover {
  background: var(--danger);
  color: white;
}

.btn-danger:active {
  transform: scale(0.97);
}

.btn-sm {
  padding: 6px 12px;
  font-size: 13px;
}

.card {
  background: var(--canvas-light);
  border: 1px solid var(--hairline);
  border-radius: var(--radius-lg);
  padding: 24px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: 9999px;
  font-size: 12px;
  font-weight: 500;
  transition: transform 0.15s ease;
}

.badge:hover {
  transform: scale(1.05);
}

.badge-green {
  background: rgba(62, 207, 142, 0.15);
  color: var(--primary);
}

.badge-red {
  background: rgba(239, 68, 68, 0.15);
  color: var(--danger);
}

.badge-gray {
  background: rgba(138, 138, 138, 0.15);
  color: var(--ink-mute);
}

.badge-blue {
  background: rgba(96, 165, 250, 0.15);
  color: #60a5fa;
}

/* ===== Page Transition ===== */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.page-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.page-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

/* ===== Modal Transition ===== */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.25s ease;
}
.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
.modal-enter-active .modal,
.modal-enter-active .test-result-card {
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.25s ease;
}
.modal-enter-from .modal,
.modal-enter-from .test-result-card {
  transform: scale(0.92) translateY(12px);
  opacity: 0;
}
.modal-leave-active .modal,
.modal-leave-active .test-result-card {
  transition: transform 0.2s ease, opacity 0.2s ease;
}
.modal-leave-to .modal,
.modal-leave-to .test-result-card {
  transform: scale(0.95);
  opacity: 0;
}

/* ===== Fade Transition (generic) ===== */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ===== List Item Stagger ===== */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.anim-item {
  animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) both;
}

/* Stagger delays via nth-child (up to 12 items) */
.anim-item:nth-child(1)  { animation-delay: 0ms; }
.anim-item:nth-child(2)  { animation-delay: 50ms; }
.anim-item:nth-child(3)  { animation-delay: 100ms; }
.anim-item:nth-child(4)  { animation-delay: 150ms; }
.anim-item:nth-child(5)  { animation-delay: 200ms; }
.anim-item:nth-child(6)  { animation-delay: 250ms; }
.anim-item:nth-child(7)  { animation-delay: 300ms; }
.anim-item:nth-child(8)  { animation-delay: 350ms; }
.anim-item:nth-child(9)  { animation-delay: 400ms; }
.anim-item:nth-child(10) { animation-delay: 450ms; }
.anim-item:nth-child(11) { animation-delay: 500ms; }
.anim-item:nth-child(12) { animation-delay: 550ms; }

/* ===== Auth Card Entrance ===== */
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

.auth-card-enter {
  animation: authEntrance 0.5s cubic-bezier(0.16, 1, 0.3, 1) both;
}

/* ===== Loading Pulse ===== */
@keyframes pulse {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}

.loading {
  animation: pulse 1.5s ease-in-out infinite;
}

/* ===== Skeleton Shimmer (for loading states) ===== */
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
</style>
