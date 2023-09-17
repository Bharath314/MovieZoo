<script setup>
import { ref } from 'vue';
import { useUserStore } from '../stores/userStore';
import axios from 'axios';

const user_store = useUserStore();

const apiUrl = "http://127.0.0.1:5000/api/movies"

const data = ref((await axios.get(
    apiUrl,
    {
        'headers': {
                'Content-Type': 'application/json',
            }
    })).data);
</script>

<template>
    <main>
        Welcome to MovieZoo! 
        <div v-if="user_store.isLoggedIn">Welcome {{ user_store.email }}</div>
        <div v-if="!user_store.isAdmin">
            <ul>
                <li v-for="movie in data">
                    {{ movie.name }}
                    <button @click="book">Book now</button>
                </li>
            </ul>
        </div>
    </main>
</template>