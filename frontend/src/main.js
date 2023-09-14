import { createApp, watch } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';

const pinia = createPinia()
const app = createApp(App)

app.use(router)
app.use(pinia)

app.mount('#app')

// watch(
//     pinia.state,
//     (state) => {
//         localStorage.setItem("user", JSON.stringify({"isLoggedIn":state.isLoggedIn.value, "isAdmin": state.isAdmin.value, "email": state.email.value}));
//         console.log("set");
//     },
//     { deep: true }
// );
