<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import Button from 'openvue/button'
import InputText from 'openvue/inputtext'
import Password from 'openvue/password'
import { useApi } from '@/api'

const router = useRouter()
const fullName = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

export interface UserPublic {
  id: string
  email: string
  full_name: string | null
  is_active: boolean
}

async function onSubmit() {
  error.value = ''
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    return
  }

  loading.value = true
  try {
    const { data, error: requestError } = await useApi<UserPublic>('/users/signup', { updateDataOnError: true }).post({ email: email.value, password: password.value, full_name: fullName.value })
    if (requestError) {
      error.value = data.value
      return
    }
    await router.push('/login')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="auth">
    <h1>Sign Up</h1>
    <form @submit.prevent="onSubmit">
      <label for="full_name">Full name</label>
      <InputText id="full_name" v-model="fullName" maxlength="255" autocomplete="name" fluid />

      <label for="email">Email</label>
      <InputText id="email" v-model="email" type="email" maxlength="255" autocomplete="email" required fluid />

      <label for="password">Password (min 8 characters)</label>
      <Password v-model="password" input-id="password" toggle-mask required
        :input-props="{ minlength: 8, maxlength: 128, autocomplete: 'new-password' }" fluid />

      <label for="confirm_password">Confirm password</label>
      <Password v-model="confirmPassword" input-id="confirm_password" toggle-mask required
        :input-props="{ minlength: 8, maxlength: 128, autocomplete: 'new-password' }" fluid />

      <p v-if="error" class="error" role="alert">{{ error }}</p>
      <Button type="submit" label="Sign Up" :loading="loading" fluid />
    </form>
    <p>Already have an account? <RouterLink to="/login">Login</RouterLink>
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
