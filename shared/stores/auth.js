import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    isAuthenticated: !!localStorage.getItem('user')
  }),
  actions: {
    async login(username, password) {
      try {
        const res = await fetch('/api/users/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })
        const data = await res.json()
        this.user = data.user
        this.isAuthenticated = true
        localStorage.setItem('user', JSON.stringify(this.user))
        localStorage.setItem('token', data.token || '')
        return this.user
      } catch (e) {
        throw new Error('登录失败')
      }
    },
    logout() {
      this.user = null
      this.isAuthenticated = false
      localStorage.removeItem('user')
      localStorage.removeItem('token')
    }
  }
})
