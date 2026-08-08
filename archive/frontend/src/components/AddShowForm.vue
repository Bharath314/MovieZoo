<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const router = useRouter();
const auth_token = localStorage.getItem('auth_token');

const venue_id = route.params.id;

const movies_list = ref((await axios.get(
    "http://127.0.0.1:5000/api/movies",
    {
        'headers': {
                'Content-Type': 'application/json',
                'Authentication-Token': auth_token,
            }
    })).data);

async function submitForm() {
    const form = document.getElementById('newShowForm');
    const formData = new FormData(form);

    formData.forEach((value, key) => {
        if (value === '' || value === null) {
            formData.delete(key);
        }
    });

    const { Data } = await axios.post(
        `http://127.0.0.1:5000/api/venues/${venue_id}/shows`,
        formData,
        {
            'headers': {
                'Content-Type': 'application/json',
                'Authentication-Token': auth_token,
            }
        }
    );

    router.push({ name: 'admin-venue_show_list', params:{'id': venue_id}});

}

</script>

<template>
<form id="newShowForm" @submit.prevent="submitForm" method="POST">
    <div class="mb-3">
        <label for="movie-select" class="form-label">Movie</label>
        <select name="movie_id" id="movie-select">
            <option v-for="movie in movies_list" :value="movie.id">{{ movie.name }}</option>
        </select>
    </div>
    <div class="mb-3">
        <label for="price">Price</label>
        <input type="number" name="price" id="price">
    </div>
    <button type="submit">Add Show</button>
</form>
</template>