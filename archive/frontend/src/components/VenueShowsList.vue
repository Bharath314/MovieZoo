<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const auth_token = localStorage.getItem('auth_token');

const venue_id = route.params.id;
const apiUrl = `http://127.0.0.1:5000/api/venues/${venue_id}/shows`;
const shows_list = ref((await axios.get(apiUrl)).data);

function deleteShow(id) {
    axios.delete(
        `http://127.0.0.1:5000/api/show/${id}`,
        {
            'headers': {
                'Authentication-Token': auth_token,
            }
        }
    );
    shows_list.value = shows_list.value.filter((show) => show.id !== id);
}

</script>

<template>
<h2>Shows</h2>
<ul>
    <li v-for="show in shows_list">
        {{ show.movie }}
        {{ show.tickets_booked }}
        <button @click="deleteShow(show.id)">Delete</button>
    </li>
</ul>
<a :href="'/admin-venues/' + venue_id + '/shows/add'">Add Show</a>
</template>