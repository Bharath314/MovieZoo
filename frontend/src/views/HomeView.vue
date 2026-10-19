<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { MegaMenu, Button } from 'openvue';
import { RouterLink, RouterView } from 'vue-router';

const authStore = useAuthStore();
</script>

<template>
  <header>
    <MegaMenu class>
      <template #start>
        <RouterLink to="/" class="brand">
          <h2>MovieZoo</h2>
        </RouterLink>
      </template>
      <template #end>
        <span v-if="!authStore.access_token">
          <Button as="RouterLink" to="/login" label="Login" variant="text" />
          <Button as="RouterLink" to="/signup" label="Sign Up" />
        </span>
        <span v-else>
          <Button label="Sign out" @click="authStore.logout" />
        </span>
      </template>
    </MegaMenu>
  </header>
  <main class="landing">
    <section class="hero">
      <h1>Book your next movie</h1>
      <p>Find movies, pick a show, and reserve your seats.</p>
      <div class="actions">
        <button type="button">Browse Movies</button>
        <button type="button">Find Theatres</button>
      </div>
    </section>

    <section>
      <h2>Now Showing</h2>
      <div class="grid">
        <div v-for="n in 4" :key="n" class="card">
          <div class="poster">Poster</div>
          <p>Movie Title {{ n }}</p>
          <button type="button">Book Now</button>
        </div>
      </div>
    </section>
  </main>
</template>

<style scoped>
nav {
  display: flex;
  gap: 0.5rem;
}

.brand {
  color: inherit;
  text-decoration: none;
}

nav {
  display: flex;
  gap: 0.5rem;
}

.brand {
  color: inherit;
  text-decoration: none;
}

.landing {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.hero {
  text-align: center;
  padding: 2rem 0;
}

.actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 1rem;
}

.card {
  border: 1px solid #ccc;
  padding: 0.75rem;
  text-align: center;
}

.poster {
  background: #eee;
  height: 160px;
  display: grid;
  place-items: center;
  color: #777;
}
</style>
