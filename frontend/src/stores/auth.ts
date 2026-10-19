import { useFetch } from "@vueuse/core";
import { acceptHMRUpdate, defineStore } from "pinia";
import { ref } from "vue";
import { API_URL } from "../api";

export const useAuthStore = defineStore('auth', () => {
    const id = ref();
    const role = ref();
    const full_name = ref();
    const created_at = ref();
    const access_token = ref();

    async function login(email: string, password: string) {
        const {error, data} = await useFetch(API_URL + "/login/access-token", {
            method: "POST",
            body: new URLSearchParams({ username: email, password }),
        }, {
            updateDataOnError: true,
            afterFetch(ctx) {
                if (ctx.data) {
                    access_token.value = ctx.data.access_token
                    localStorage.setItem('access_token', access_token.value)
                }
                me()
                return ctx
            },
        }).json()
        return { error, data }      
    }

    async function me() {
        const {error, data} = await useFetch(API_URL + "/users/me", {
            headers: {
                Authorization: `Bearer ${access_token.value}`
            }
        }, {
            updateDataOnError: true,
        }).json()
        if (data) {
            id.value = data.value.id
            role.value = data.value.role
            // temp
            role.value = 'superuser'
            full_name.value = data.value.full_name
            created_at.value = data.value.created_at
        }
        return { error, data }
    }

    async function logout() {
        id.value = undefined
        role.value = undefined
        full_name.value = undefined
        created_at.value = undefined
        access_token.value = undefined
        localStorage.removeItem('access_token')
    }
    return {id, role, full_name, created_at, access_token, login, me, logout}
})

if (import.meta.hot) {
  import.meta.hot.accept(acceptHMRUpdate(useAuthStore, import.meta.hot))
}