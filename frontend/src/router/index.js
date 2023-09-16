import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/LoginView.vue')
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('../views/RegisterView.vue')
        },
        {
            path: '/',
            name: 'home',
            component: HomeView
        },
        {
            path: '/movies',
            name: 'movies',
            component: () => import('../views/MovieListView.vue')
        },
        {
            path: '/movies/add',
            name: 'add_movies',
            component: () => import('../views/AddMovieView.vue')
        },
        {
            path: '/movies/:id',
            component: () => import('../views/Movie.vue')
        },
        {
            path: '/venues',
            name: 'venues',
            component: () => import('../views/VenueListView.vue')
        },
        {
            path: '/venues/add',
            name: 'add_venues',
            component: () => import('../views/AddVenueView.vue')
        },
        {
            path: '/venues/:id',
            component: () => import('../views/Venue.vue')
        }
    ]
})

export default router