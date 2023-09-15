<script setup>
import axios from 'axios';

const apiUrl = "http://127.0.0.1:5000/api/movies"

let data;

data = (await axios.get(apiUrl)).data;
console.log(data)
</script>

<template>
    <li v-for="movie in data">
        {{ movie.name }}
        <a :href="/movies/ + movie.id">Update</a>
        <a href="#">Delete</a>
    </li>
</template>