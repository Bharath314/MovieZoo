import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import OpenVue from 'openvue/config'
import Aura from '@openvue/themes/aura';

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(OpenVue, {
    theme: {
        preset: Aura
    }
})

app.mount('#app')
