<script setup>
import { ref } from 'vue';

const count = ref(0);
const object = { id: ref(1) };
</script>

<template>
    <main>
        Welcome to MovieZoo! 
        <button @click="count++">{{ count }}</button>
    </main>
</template>