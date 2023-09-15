<script setup>
import { ref } from 'vue';
import { useUserStore } from '../stores/userStore';

const object = { id: ref(1) };
const user_store = useUserStore();
</script>

<template>
    <main>
        Welcome to MovieZoo! 
        <div v-if="user_store.isLoggedIn">Welcome {{ user_store.email }}</div>
    </main>
</template>