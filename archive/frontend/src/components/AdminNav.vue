<script setup>
import { RouterLink } from 'vue-router';

</script>

<template>
<ul class="navbar-nav me-auto mb-2 mb-lg-0">
    <li class="nav-item">
        <RouterLink to="/admin-movies" class="nav-link">Movies</RouterLink>
    </li>
    <li class="nav-item">
        <RouterLink to="/admin-venues" class="nav-link">Venues</RouterLink>
    </li>
</ul>
</template>