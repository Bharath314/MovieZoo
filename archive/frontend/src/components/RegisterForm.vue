<script setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue';
import { useUserStore } from '../stores/userStore';
import axios from 'axios';

const router = useRouter();
const user_store = useUserStore();

const email = ref();
const password = ref();
const confirm_password = ref();

function register() {
    const formData = {
        'email': email.value,
        'password': password.value,
        'confirm_password': confirm_password.value,
    }
    axios.post(
        "http://127.0.0.1:5000/register",
        formData,
    )
    .then(function(response) {
        router.push('login')
    })
}
</script>

<template>
<div>
  <form @submit.prevent="register">
    
    <label for="email">Email:</label>
    <input v-model="email" type="text" id="email" required>
    <label for="password">Password:</label>
    <input v-model="password" type="password" id="password" required>
    <label for="confirm_password">Confirm Password:</label>
    <input v-model="confirm_password" type="password" id="confirm_password" required>

    <button type="submit">Register</button>
  </form>
</div>
</template>