<script setup>
import axios from 'axios';
import {useRoute, useRouter} from 'vue-router';
import VenueShowsList from '../components/VenueShowsList.vue'

const route = useRoute();
const router = useRouter();

const id = route.params.id;
const apiUrl = `http://127.0.0.1:5000/api/venues/${id}`;
const venue_data = (await axios.get(apiUrl)).data;


async function submitForm() {
    const form = document.getElementById('updateVenueForm');
    const formData = new FormData(form);
    const auth_token = localStorage.getItem('auth_token')

    formData.forEach((value, key) => {
        if (value === '' || value === null) {
            formData.delete(key);
        }
    });

    const jsonFormData = {}

    formData.forEach((value, key) => {
        jsonFormData[key] = value;
    });

    const { Data } = await axios.patch(
        apiUrl,
        jsonFormData,
        {
            headers: {
                'Authentication-Token': auth_token,
            }
        }
    );

    router.push({ name: 'admin-venues', });

}

</script>

<template>
<form id="updateVenueForm" @submit.prevent="submitForm" method="POST" enctype="application/json">
    <div class="mb-3">
        <label for="name" class="form-label">Name</label>
        <input name="name" type="text" class="form-control" id="name" :value="venue_data.name">
    </div>
    <div class="mb-3">
        <label for="capacity" class="form-label">Capacity</label>
        <input name="capacity" type="number" class="form-control" id="capacity" :value="venue_data.capacity">
    </div>
    <div class="mb-3">
        <label for="City" class="form-label">City</label>
        <input name="city" class="form-control" type="text" id="city" :value="venue_data.city">
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>
<VenueShowsList></VenueShowsList>
</template>