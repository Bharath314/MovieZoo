<script setup>
import {ref} from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useUserStore } from '../stores/userStore';

const user_store = useUserStore();
const router = useRouter();
const route = useRoute();

const movie_id = route.params.movie_id;
const movie = (await axios.get(`http://127.0.0.1:5000/api/movies/${movie_id}`)).data;
const apiUrl = `http://127.0.0.1:5000/api/movies/${movie_id}/shows`;

const shows_list = ref((await axios.get(apiUrl)).data);

function book(show_id) {
    if (!user_store.isLoggedIn) router.push({'name': 'login'})
    else {
        router.push({'name': 'book', params:{'show_id': show_id}});
    }
}

</script>

<template>
<h1>{{ movie.name }}</h1>
<div>
    <p>Release date: <span v-if="movie.release_date">{{ movie.release_date }}</span><span v-else>TBA</span></p>
    <img :src="'http://127.0.0.1:5000/'+movie.poster.slice(4)">
</div>
<ul v-if="shows_list.length">
    <li v-for="show in shows_list">
        {{ show.venue }}
        <button @click="book(show.id)">Book now</button>
    </li>
</ul>
<p v-else>No shows available</p>
</template>