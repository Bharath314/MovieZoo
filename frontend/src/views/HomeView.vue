<script setup>
import { ref } from 'vue';
import { useUserStore } from '../stores/userStore';

const count = ref(0);
const object = { id: ref(1) };
const user_store = useUserStore();
</script>

<template>
    <main>
        Welcome to MovieZoo! 
        <button @click="count++">{{ count }}</button>
        <div v-if="user_store.isLoggedIn">It's working Priya!</div>
    </main>
</template>