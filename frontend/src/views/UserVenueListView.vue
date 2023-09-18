<script setup>
import { ref } from 'vue';
import { useUserStore } from '../stores/userStore';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const user_store = useUserStore();
const route = useRoute();
const router = useRouter();

const apiUrl = "http://127.0.0.1:5000/api/venues"

const venue_list = ref((await axios.get(
    apiUrl,
    {
        'headers': {
                'Content-Type': 'application/json',
            }
    })).data);

function openVenuePage(venue_id) {
    router.push({'name': 'user_venue', 'params': {'venue_id': venue_id}})
}

</script>

<template>
<ul>
    <li v-for="venue in venue_list">
        <a :href="'/venues/' + venue.id">{{ venue.name }}</a>
    </li>
</ul>
</template>