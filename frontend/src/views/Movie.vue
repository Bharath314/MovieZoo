<script setup>
import axios from 'axios';
import {useRoute, useRouter} from 'vue-router';

const route = useRoute();
const router = useRouter();

const id = route.params.id;
const apiUrl = `http://127.0.0.1:5000/api/movies/${id}`;
const movie_data = (await axios.get(apiUrl)).data;


async function submitForm() {
    const form = document.getElementById('updateMovieForm');
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

    const { Data } = await axios.patch(
        apiUrl,
        formData,
        {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        }
    );

    router.push({ name: 'movies', });

}

</script>

<template>
Movie {{ route.params.id }}
<form id="updateMovieForm" @submit.prevent="submitForm" method="POST" enctype="multipart/form-data">
    <div class="mb-3">
        <label for="name" class="form-label">Name</label>
        <input name="name" type="text" class="form-control" id="name" :value="movie_data.name">
    </div>
    <div class="mb-3">
        <label for="release_date" class="form-label">Release Date</label>
        <input name="release_date" type="date" class="form-control" id="release_date" :value="movie_data.release_date">
    </div>
    <div class="mb-3">
        <label for="poster" class="form-label">Poster</label>
        <input name="poster" class="form-control" type="file" id="poster">
    </div>
    <button type="submit" class="btn btn-primary">Update</button>
</form>
</template>