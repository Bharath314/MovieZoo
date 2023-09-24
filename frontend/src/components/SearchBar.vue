<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useSearchStore } from '../stores/searchStore';

const search_term = ref();
const search_city = ref();
const search_store = useSearchStore();

const drop_down_data = ref((await axios.get(
    "http://127.0.0.1:5000/api/venues",
    {
        'headers': {
                'Content-Type': 'application/json',
            }
    })).data);

const drop_down_options = ref([]);

drop_down_data.value.forEach((obj) => {
    const value = obj['city'];
    if (!drop_down_options.value.includes(value)) {
        drop_down_options.value.push(value);
    }
});



</script>

<template>
<ul class="navbar-nav me-auto mb-2 mb-lg-0">
    <li  class="nav-item" method="POST">
        <form @submit.prevent="search_store.execute_search(search_term, search_city)" class="d-flex" role="search">
            <select id="location-select" v-model="search_city" >
                <option value="" disabled selected hidden >Choose Location</option>
                <option v-for="city in drop_down_options" :value="city">{{ city }}</option>
            </select>
            <input v-model="search_term" class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
            <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
    </li>
</ul>
</template>