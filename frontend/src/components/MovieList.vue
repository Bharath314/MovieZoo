<script setup>
import axios from 'axios';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const router = useRouter();

const apiUrl = "http://127.0.0.1:5000/api/movies"

const data = ref((await axios.get(apiUrl)).data);

function deleteMovie(id) {
    axios.delete(
        `http://127.0.0.1:5000/api/movies/${id}`
    );
    data.value = data.value.filter((movie) => movie.id !== id);
}
</script>

<template>
    <li v-for="movie in data">
        {{ movie.name }}
        <a :href="/movies/ + movie.id">Update</a>
        <button @click="deleteMovie(movie.id)">Delete</button>
    </li>
</template>