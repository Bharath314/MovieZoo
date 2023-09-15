<script setup>
import {useRoute} from 'vue-router';

const route = useRoute();
</script>

<template>
    Movie {{ route.params.id }}
</template>