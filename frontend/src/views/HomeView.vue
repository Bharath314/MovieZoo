<script setup>
import { ref } from 'vue';
import { useUserStore } from '../stores/userStore';
import { useRouter } from 'vue-router';
import axios from 'axios';

const user_store = useUserStore();
const router = useRouter();

const apiUrl = "http://127.0.0.1:5000/api/movies"

const data = ref((await axios.get(
    apiUrl,
    {
        'headers': {
                'Content-Type': 'application/json',
            }
    })).data);

function book(movie_id) {
    if (!user_store.isLoggedIn) router.push({'name': 'login'})
    else {
        router.push({'name': 'user_movie', params:{'movie_id': movie_id}});
    }
}

</script>

<template>
    <main>
        Welcome to MovieZoo! 
        <div v-if="user_store.isLoggedIn">Welcome {{ user_store.email }}</div>
        <div v-if="!user_store.isAdmin">
            <ul>
                <li v-for="movie in data">
                    {{ movie.name }}
                    <button @click="book(movie.id)">Book now</button>
                </li>
            </ul>
        </div>
    </main>
</template>