import { defineStore } from "pinia";
import { computed, ref } from "vue";
import axios from 'axios';

export const useUserStore = defineStore('user', () => {
    const isLoggedIn = ref(false);
    const isAdmin = ref(false);
    const email = ref();

    function setState() {
        if (localStorage.getItem('user')) {
            const user = JSON.parse(localStorage.getItem('user'))
            isLoggedIn.value = user.isLoggedIn;
            //add additional validation to check for admin auth
            isAdmin.value = user.isAdmin;
            email.value = user.email;
        }
        else logout();
    }

    function login(data) {
        isLoggedIn.value = true;
        email.value = data;
        isAdmin.value = true;
        localStorage.setItem("user", JSON.stringify({"isLoggedIn":isLoggedIn.value, "isAdmin": isAdmin.value, "email": email.value}));
        console.log("set");
    }

    function logout(data) {
        isLoggedIn.value = false;
        email.value = null;
        isAdmin.value = false;
        localStorage.removeItem('user');
        localStorage.removeItem('auth_token');
    }

    return {isLoggedIn, isAdmin, email, login, logout, setState};
})

