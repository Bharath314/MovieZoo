import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import { ref } from "vue";
import axios from "axios";

export const useSearchStore = defineStore('search', () => {
    const router = useRouter();
    const city = ref()
    const search_term = ref();
    const search_results = ref();


    async function execute_search(term, search_city) {
        search_term.value = term;
        city.value = search_city;
        search_results.value = (await axios.get(
            `http://127.0.0.1:5000/api/search/${term}`
        )).data
        if (city.value) {
            search_results.value = {
                ...search_results.value,
                venues: search_results.value.venues.filter((venue) => venue.city === city.value)
            };
        }
        router.push('/search');
    }
    return {search_term, execute_search, search_results};
})