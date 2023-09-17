<script setup>
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ref } from 'vue';

const router = useRouter();
const name = ref();
const release_date = ref();
const auth_token = localStorage.getItem('auth_token')


async function submitForm() {
    const form = document.getElementById('newMovieForm');
    const fileInput = form.querySelector('input[type="file"]');
    const formData = new FormData(form);

    formData.forEach((value, key) => {
        if (value === '' || value === null) {
            formData.delete(key);
        }
    });

    if (fileInput.files.length === 0) {
        formData.delete('poster');
    }

    const { Data } = await axios.post(
        "http://127.0.0.1:5000/api/movies",
        formData,
        {
            'headers': {
                'Content-Type': 'multipart/form-data',
                'Authentication-Token': auth_token,
            }
        }
    );

    router.push({ name: 'admin-movies', });

}
</script>

<template>
    <form id="newMovieForm" @submit.prevent="submitForm" method="POST" enctype="multipart/form-data">
        <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input v-model="name" name="name" type="text" class="form-control" id="name">
        </div>
        <div class="mb-3">
            <label for="release_date" class="form-label">Release Date</label>
            <input v-model="release_date" name="release_date" type="date" class="form-control" id="release_date">
        </div>
        <div class="mb-3">
            <label for="poster" class="form-label">Poster</label>
            <input name="poster" class="form-control" type="file" id="poster">
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
</template>