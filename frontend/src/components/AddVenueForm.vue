<script setup>
import { useRouter } from 'vue-router';
import axios from 'axios';
import { ref } from 'vue';

const router = useRouter();
const name = ref();
const capacity = ref();
const city = ref();
const auth_token = localStorage.getItem('auth_token')


async function submitForm() {
    const form = document.getElementById('newVenueForm');
    const formData = new FormData(form);

    formData.forEach((value, key) => {
        if (value === '' || value === null) {
            formData.delete(key);
        }
    });

    const { Data } = await axios.post(
        "http://127.0.0.1:5000/api/venues",
        formData,
        {
            'headers': {
                'Content-Type': 'application/json',
                'Authentication-Token': auth_token,
            }
        }
    );

    router.push({ name: 'venues', });

}
</script>

<template>
    <form id="newVenueForm" @submit.prevent="submitForm" method="POST">
        <div class="mb-3">
            <label for="name" class="form-label">Name</label>
            <input v-model="name" name="name" type="text" class="form-control" id="name">
        </div>
        <div class="mb-3">
            <label for="capacity" class="form-label">Capacity</label>
            <input v-model="capacity" name="capacity" type="number" class="form-control" id="capacity">
        </div>
        <div class="mb-3">
            <label for="City" class="form-label">City</label>
            <input name="city" class="form-control" type="text" id="city">
        </div>
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
</template>