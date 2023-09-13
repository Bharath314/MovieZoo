<script setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import axios from 'axios';

const router = useRouter();
const username = ref('');
const password = ref('');

// console.log(formData)

function login() {
    const formData = {
        'email': username.value,
        'password': password.value
    }
    axios.post(
        "http://127.0.0.1:5000/login?include_auth_token",
        formData,
        {
            headers: {
                'Content-Type': 'application/json'
            }
        }
    )
        .then(function (response) {
            localStorage.auth_token = response.data.response.user.authentication_token;
            router.push({ name: 'home', });
        });

}
</script>

<template>
    <div>
        <form @submit.prevent="login">

            <label for="username">Username:</label>
            <input v-model="username" type="text" id="username" required>
            <label for="password">Password:</label>
            <input v-model="password" type="password" id="password" required>

            <button type="submit">Login</button>
        </form>
    </div>
</template>