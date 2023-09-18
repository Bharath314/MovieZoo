<script setup>
import {ref} from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useUserStore } from '../stores/userStore';

const router = useRouter();
const route = useRoute();

const user_store = useUserStore();
const venue_id = route.params.venue_id;
const venue = (await axios.get(`http://127.0.0.1:5000/api/venues/${venue_id}`)).data;
const apiUrl = `http://127.0.0.1:5000/api/venues/${venue_id}/shows`;

const shows_list = ref((await axios.get(apiUrl)).data);

function book(show_id) {
    if (!user_store.isLoggedIn) router.push({'name': 'login'})
    else {
        router.push({'name': 'book', params:{'show_id': show_id}});
    }
}

</script>

<template>
<h1>{{ venue.name }}</h1>
<div>
    <p>City: {{ venue.city }}</p>
</div>
<ul>
    <li v-for="show in shows_list">
        {{ show.movie }}
        <button @click="book(show.id)">Book now</button>
    </li>
</ul>
</template>