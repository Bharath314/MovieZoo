<template>
    <div>
        <form @submit.prevent="login">
            <label for="username">Username:</label>
            <input v-model="username" type="text" id="username" required>

            <label for="password">Password:</label>
            <input v-model="password" type="password" id="password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</template>
<script setup>

</script>