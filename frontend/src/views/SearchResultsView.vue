<script setup>
import { useRouter } from 'vue-router';
import { useSearchStore } from '../stores/searchStore';
import { ref } from 'vue';

const search_store = useSearchStore();
const router = useRouter();



</script>


<template>
    <h3>Search results for {{ search_store.search_term }}</h3>
    <div v-if="search_store.search_results.movies">
        <h4>Movies</h4>
        <ul>
            <li v-for="movie in search_store.search_results.movies">
                {{ movie.name }}
                <a :href="'/movies/'+movie.id">Book now</a>
            </li>
        </ul>
    </div>
    <div v-if="search_store.search_results.venues">
        <h4>Venues</h4>
        <ul>
            <li v-for="venue in search_store.search_results.venues">
                {{ venue.name }}
                <a :href="'/venues/'+ venue.id">Book now</a>
            </li>
        </ul>
    </div>
</template>