<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import Button from 'openvue/button'
import Column from 'openvue/column'
import DataTable from 'openvue/datatable'
import Dialog from 'openvue/dialog'
import InputNumber from 'openvue/inputnumber'
import InputText from 'openvue/inputtext'
import { useApi } from '@/api'

interface Venue {
  id: number
  name: string
  city: string
  capacity: number
}

interface VenueForm {
  name: string
  city: string
  capacity: number | null
}

const venues = ref<Venue[]>([])
const loading = ref(false)
const saving = ref(false)
const error = ref('')
const formError = ref('')

const dialogOpen = ref(false)
const editingId = ref<number | null>(null)
const form = reactive<VenueForm>({ name: '', city: '', capacity: null })

const isEditing = computed(() => editingId.value !== null)
const canSave = computed(
  () => form.name.trim() !== '' && form.city.trim() !== '' && (form.capacity ?? 0) > 1,
)

function errorMessage(data: unknown, fallback: string) {
  if (typeof data === 'object' && data !== null && 'detail' in data) {
    const detail = (data as { detail: unknown }).detail
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) return detail.map((d) => d?.msg ?? String(d)).join(', ')
  }
  return fallback
}

async function loadVenues() {
  loading.value = true
  error.value = ''
  try {
    const { data, error: err } = await useApi('/venues/').get().json()
    if (err.value) {
      error.value = errorMessage(data.value, err.value.message)
      return
    }
    venues.value = data.value.data
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingId.value = null
  Object.assign(form, { name: '', city: '', capacity: null })
  formError.value = ''
  dialogOpen.value = true
}

function openEdit(venue: Venue) {
  editingId.value = venue.id
  Object.assign(form, { name: venue.name, city: venue.city, capacity: venue.capacity })
  formError.value = ''
  dialogOpen.value = true
}

async function save() {
  if (!canSave.value) return
  saving.value = true
  formError.value = ''
  try {
    const body = { name: form.name.trim(), city: form.city.trim(), capacity: form.capacity }
    const request = isEditing.value
      ? useApi(`/venues/${editingId.value}`).patch(body).json()
      : useApi('/venues/').post(body).json()
    const { data, error: err } = await request
    if (err.value) {
      formError.value = errorMessage(data.value, err.value.message)
      return
    }
    dialogOpen.value = false
    await loadVenues()
  } finally {
    saving.value = false
  }
}

async function remove(venue: Venue) {
  if (!window.confirm(`Delete venue "${venue.name}"?`)) return
  error.value = ''
  const { data, error: err } = await useApi(`/venues/${venue.id}`).delete().json()
  if (err.value) {
    error.value = errorMessage(data.value, err.value.message)
    return
  }
  await loadVenues()
}

onMounted(loadVenues)
</script>

<template>
  <div class="venues-header">
    <h1>Venues</h1>
    <Button label="Add venue" icon="oi oi-plus" @click="openCreate" />
  </div>

  <p v-if="error" class="venues-error" role="alert">{{ error }}</p>

  <DataTable :value="venues" :loading="loading" data-key="id" paginator :rows="10"
    empty-message="No venues found.">
    <Column field="name" header="Name" sortable />
    <Column field="city" header="City" sortable />
    <Column field="capacity" header="Capacity" sortable />
    <Column header="Actions" style="width: 10rem">
      <template #body="{ data }">
        <Button label="Edit" size="small" variant="text" @click="openEdit(data)" />
        <Button label="Delete" size="small" variant="text" severity="danger" @click="remove(data)" />
      </template>
    </Column>
  </DataTable>

  <Dialog v-model:visible="dialogOpen" modal :header="isEditing ? 'Edit venue' : 'Add venue'"
    :style="{ width: '28rem' }">
    <form class="venues-form" @submit.prevent="save">
      <label for="venue-name">Name</label>
      <InputText id="venue-name" v-model="form.name" required fluid />

      <label for="venue-city">City</label>
      <InputText id="venue-city" v-model="form.city" required fluid />

      <label for="venue-capacity">Capacity</label>
      <InputNumber v-model="form.capacity" input-id="venue-capacity" :min="2" fluid />

      <p v-if="formError" class="venues-error" role="alert">{{ formError }}</p>

      <div class="venues-actions">
        <Button type="button" label="Cancel" severity="secondary" variant="text" @click="dialogOpen = false" />
        <Button type="submit" :label="isEditing ? 'Save' : 'Create'" :loading="saving" :disabled="!canSave" />
      </div>
    </form>
  </Dialog>
</template>

<style scoped>
.venues-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.venues-form {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.venues-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 12px;
}

.venues-error {
  color: var(--p-red-500);
  margin: 0 0 12px;
}
</style>
