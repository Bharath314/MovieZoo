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
            path: '/admin-movies',
            name: 'admin-movies',
            component: () => import('../views/MovieListView.vue')
        },
        {
            path: '/admin-movies/add',
            name: 'add_movies',
            component: () => import('../views/AddMovieView.vue')
        },
        {
            path: '/admin-movies/:id',
            component: () => import('../views/Movie.vue')
        },
        {
            path: '/admin-venues',
            name: 'admin-venues',
            component: () => import('../views/VenueListView.vue')
        },
        {
            path: '/admin-venues/add',
            name: 'add_venues',
            component: () => import('../views/AddVenueView.vue')
        },
        {
            path: '/admin-venues/:id',
            name: 'admin-venue_show_list',
            component: () => import('../views/Venue.vue')
        },
        {
            path: '/admin-venues/:id/shows/add',
            name: 'add_show',
            component: () => import('../views/AddShowView.vue')
        },
        {
            path: '/movies/:movie_id',
            name: 'user_movie',
            component: () => import('../views/UserMovieView.vue')
        },
        {
            path: '/book/:show_id',
            name: 'book',
            component: () => import('../views/BookingView.vue')
        }
    ]
})

export default router