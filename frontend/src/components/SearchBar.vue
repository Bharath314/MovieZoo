<script setup>
import { ref } from 'vue';
import { useSearchStore } from '../stores/searchStore';

const search_term = ref();
const search_store = useSearchStore();

</script>

<template>
<ul class="navbar-nav me-auto mb-2 mb-lg-0">
    <li @submit.prevent="search_store.execute_search(search_term)" class="nav-item" method="POST">
        <form class="d-flex" role="search">
            <input v-model="search_term" class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
            <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
    </li>
</ul>
</template>