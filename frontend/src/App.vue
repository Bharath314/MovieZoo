<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router';
import { useUserStore } from './stores/userStore';
import AdminNav from './components/AdminNav.vue';
import SearchBar from './components/SearchBar.vue';
import SearchResultsView from './views/SearchResultsView.vue';

const user_store = useUserStore();
const router = useRouter();

if (!user_store.isLoggedIn) user_store.setState();

function search(search_term) {
  SearchResultsView.search(search_term);
}


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
          <ul v-if="!user_store.isAdmin" class="navbar-nav me-auto mb-2 mb-lg-0">
            <RouterLink to="/venues" class="nav-link">Venues</RouterLink>
          </ul>
          <SearchBar @search-pressed="search"></SearchBar>
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li v-if="!user_store.isLoggedIn" class="nav-item">
              <RouterLink  to="/login" class="btn btn-primary">Login</RouterLink>
            </li>
            <li v-if="!user_store.isLoggedIn" class="nav-item">
              <RouterLink to="/register" class="nav-link">Sign Up</RouterLink>
            </li>
            <li v-else @click="user_store.logout()" class="nav-item">
              <button class="btn btn-secondary">Logout</button>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </header>
  <Suspense>
    <RouterView />
  </Suspense>
</template>


