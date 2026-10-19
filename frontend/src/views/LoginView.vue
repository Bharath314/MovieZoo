<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import Button from 'openvue/button'
import InputText from 'openvue/inputtext'
import Password from 'openvue/password'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const authStore = useAuthStore();

async function onSubmit() {
  error.value = ''
  loading.value = true
  try {
    const { data, error: requestError } = await authStore.login(email.value, password.value)
    if (requestError.value) {
      const responseData = data.value
      error.value =
        typeof responseData === 'object' &&
        responseData !== null &&
        'detail' in responseData &&
        typeof responseData.detail === 'string'
          ? responseData.detail
          : requestError.value.message
      return
    }
    await router.push('/')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="auth">
    <h1>Login</h1>
    <form @submit.prevent="onSubmit">
      <label for="email">Email</label>
      <InputText id="email" v-model="email" type="email" autocomplete="email" required fluid />

      <label for="password">Password</label>
      <Password v-model="password" input-id="password" :feedback="false" toggle-mask required fluid />

      <p v-if="error" class="error" role="alert">{{ error }}</p>
      <Button type="submit" label="Login" :loading="loading" fluid />
    </form>
    <p>No account? <RouterLink to="/signup">Sign Up</RouterLink>
    </p>
  </main>
</template>

<style scoped>
.auth {
  max-width: 24rem;
  margin: 2rem auto;
  padding: 0 1rem;
}

form {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.error {
  color: var(--p-red-500, red);
}
</style>
