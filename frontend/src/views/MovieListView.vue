<script setup>
import MovieList from '../components/MovieList.vue'
</script>

<template>
    <main>
        <Suspense>
            <MovieList />
        </Suspense>
        <a href="/movies/add">Add Movie</a>
    </main>
</template>