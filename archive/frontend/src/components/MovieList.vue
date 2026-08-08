<script setup>
import axios from 'axios';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const router = useRouter();

const apiUrl = "http://127.0.0.1:5000/api/movies"
const auth_token = localStorage.getItem('auth_token');

const data = ref((await axios.get(
    apiUrl,
    {
        'headers': {
                'Content-Type': 'application/json',
                'Authentication-Token': auth_token,
            }
    })).data);

function deleteMovie(id) {
    axios.delete(
        `http://127.0.0.1:5000/api/movies/${id}`,
        {
            'headers': {
                'Authentication-Token': auth_token,
            }
        }
    );
    data.value = data.value.filter((movie) => movie.id !== id);
}
</script>

<template>
<ul>
    <li v-for="movie in data">
        {{ movie.name }}
        <a :href="/admin-movies/ + movie.id">Update</a>
        <button @click="deleteMovie(movie.id)">Delete</button>
    </li>
</ul>
</template>