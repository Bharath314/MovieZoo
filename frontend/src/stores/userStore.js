import { defineStore } from "pinia";
import { computed, ref } from "vue";
import { useRouter } from "vue-router";
import axios from 'axios';


export const useUserStore = defineStore('user', () => {
    const isLoggedIn = ref(false);
    const isAdmin = ref(false);
    const email = ref();
    const router = useRouter();
    
    function setState() {
        const auth_token = localStorage.getItem('auth_token')
        if (auth_token) {
            fetchUser(auth_token);
        }

    }

    function fetchUser(data) {  
        axios.get("http://127.0.0.1:5000/api/current-user", {
            'headers': {
                'Content-Type': 'application/json',
                'Authentication-Token': data,
            }
        })
        .then(function (response) {
            isLoggedIn.value = true;
            email.value = response.data.email;
            isAdmin.value = (response.data.role === 'admin') ? true : false;
        })
    }

    function logout() {
        const data = localStorage.getItem('auth_token')
        axios.post("http://127.0.0.1:5000/logout", {
            'headers': {
                'Content-Type': 'application/json',
                'Authentication-Token': data,
            }
        })
        .then(function (response) {
            isLoggedIn.value = false;
            email.value = null;
            isAdmin.value = false;
            localStorage.removeItem('auth_token');
            router.push({ name: 'home', })
        })
    }

    return {isLoggedIn, isAdmin, email, logout, fetchUser, setState};
})

