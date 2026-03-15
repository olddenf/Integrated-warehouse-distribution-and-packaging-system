import { defineStore } from 'pinia'
import api from '@/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: JSON.parse(localStorage.getItem('user') || 'null')
  }),
  
  getters: {
    isLoggedIn: (state) => !!state.token,
    userRole: (state) => state.user?.role
  },
  
  actions: {
    async login(username: string, password: string) {
      try {
        const response = await api.post('/auth/login', { username, password })
        const { access_token, user } = response.data
        
        this.token = access_token
        this.user = user
        
        localStorage.setItem('token', access_token)
        localStorage.setItem('user', JSON.stringify(user))
        
        return user
      } catch (error) {
        throw error
      }
    },
    
    logout() {
      this.token = ''
      this.user = null
      
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },
    
    hasPermission(roles: string[]) {
      if (!this.user) return false
      return roles.includes(this.user.role)
    }
  }
})
