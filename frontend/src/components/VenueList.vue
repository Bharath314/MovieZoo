<script setup>
import axios from 'axios';
import { useRouter } from 'vue-router';
import { ref } from 'vue';

const router = useRouter();

const apiUrl = "http://127.0.0.1:5000/api/venues"
const auth_token = localStorage.getItem('auth_token');

const data = ref((await axios.get(
    apiUrl,
    {
        'headers': {
                'Content-Type': 'application/json',
                'Authentication-Token': auth_token,
            }
    })).data);

function deleteVenue(id) {
    axios.delete(
        `http://127.0.0.1:5000/api/venues/${id}`,
        {
            'headers': {
                'Authentication-Token': auth_token,
            }
        }
    );
    data.value = data.value.filter((venue) => venue.id !== id);
}
</script>

<template>
    <li v-for="venue in data">
        {{ venue.name }}
        <a :href="/venues/ + venue.id">Update</a>
        <button @click="deleteVenue(venue.id)">Delete</button>
    </li>
</template>