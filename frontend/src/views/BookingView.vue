<script setup>
import {ref} from 'vue';
import {useRoute, useRouter} from 'vue-router';
import axios from 'axios';
import { useUserStore } from '../stores/userStore';

const route = useRoute();
const router = useRouter();
const user_store = useUserStore();
const auth_token = localStorage.getItem('auth_token');

const show_id = route.params.show_id;

const show = (await axios.get(`http://127.0.0.1:5000/api/show/${show_id}`)).data;

const ticket_count = ref();


function submitForm() {
    if (ticket_count.value) {
        axios.post(
            'http://127.0.0.1:5000/api/booking',
            {
                "show_id": show_id,
                "ticket_count": ticket_count.value,
                "user_id": user_store.user_id
            },
            {
                'headers': {
                    'Content-Type': 'application/json',
                    'Authentication-Token': auth_token,
                }
            }
        ).then(() => {
            router.push({'name': 'home'})
        })
        
    }
}

</script>

<template>
<form id="bookTicketForm" @submit.prevent="submitForm" method="POST">
    <div class="mb-3">
        <label for="price" class="form-label">Price</label>
        <input type="number" class="form-control" id="price" :value="show.price" disabled>
    </div>
    <div class="mb-3">
        <label for="ticket_count" class="form-label">Tickets</label>
        <input v-model="ticket_count" type="number" class="form-control" id="ticket_count" min="1">
    </div>
    <button type="submit">Book Tickets</button>
</form>
</template>