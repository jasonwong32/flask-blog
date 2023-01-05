import { defineStore } from 'pinia'

interface LoginData {
  email: string
  token: string
  isLogin: boolean
}

export const useLoginStatusStore = defineStore('userData', {
  state: () => {
    return {
      userData:
        ({
          email: '',
          token: '',
          isLogin: false,
        } as LoginData) || null,
    }
  },
  getters: {
    getAccessToken: (state) => state.userData.token || '',
    getEmail: (state) => state.userData.email || '',
    getLoginStatus: (state) => state.userData.isLogin,
  },
  actions: {
    setLoginStatus(data: LoginData): void {
      this.userData.token = data.token
      this.userData.email = data.email
      this.userData.isLogin = data.isLogin
    },
  },
})
