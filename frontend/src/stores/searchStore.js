import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import { ref } from "vue";
import axios from "axios";

export const useSearchStore = defineStore('search', () => {
    const search_term = ref();
    const search_results = ref();
    const router = useRouter();

    async function execute_search(term) {
        search_term.value = term;
        search_results.value = (await axios.get(
            `http://127.0.0.1:5000/api/search/${term}`
        )).data
        router.push('/search');
    }
    return {search_term, execute_search, search_results};
})