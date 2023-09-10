import { defineStore } from 'pinia';

export const loginFormStore = defineStore('loginForm', () => {
    const email = ref('')
    const password = ref('')
    return {email, password}
})