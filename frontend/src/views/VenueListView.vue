<script setup>
import VenueList from '../components/VenueList.vue'
</script>

<template>
<main>
    <Suspense>
        <VenueList />
    </Suspense>
    <a href="/venues/add">Add Venue</a>
</main>
</template>