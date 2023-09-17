<script setup>
import MovieList from '../components/MovieList.vue'
</script>

<template>
<main>
    <Suspense>
        <MovieList />
    </Suspense>
    <a href="/admin-movies/add">Add Movie</a>
</main>
</template>