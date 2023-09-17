<script setup>
import {ref} from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const router = useRouter();
const route = useRoute();

const movie_id = route.params.movie_id;
const movie = (await axios.get(`http://127.0.0.1:5000/api/movies/${movie_id}`)).data
const movie_name = movie.name;
const apiUrl = `http://127.0.0.1:5000/api/movies/${movie_id}/shows`;

const shows_list = ref((await axios.get(apiUrl)).data);


</script>

<template>
<h1>{{ movie_name }}</h1>
<ul>
    <li v-for="show in shows_list">
        {{ show.venue }}
        <a :href="'/book/' + show.id">Book now</a>
    </li>
</ul>
</template>