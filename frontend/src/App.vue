<script setup>
import { RouterLink, RouterView } from 'vue-router';
import { useUserStore } from './stores/userStore';
import AdminNav from './components/AdminNav.vue';

const user_store = useUserStore();
user_store.setState();

</script>

<template>
  <header>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <RouterLink to="/" class="navbar-brand">MovieZoo</RouterLink>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <AdminNav v-if="user_store.isAdmin"/>
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <RouterLink v-if="!user_store.isLoggedIn" to="/login" class="btn btn-primary">Login</RouterLink>
              <button @click="user_store.logout()" v-else href="#" class="btn btn-secondary">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>

  <RouterView />
</template>


