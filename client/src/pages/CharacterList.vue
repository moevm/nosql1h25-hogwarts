<script setup>
import Card from '../components/Card.vue'
import { onMounted, ref } from 'vue'
import Search from '../components/Search.vue'
import AddCharacter from '../components/AddCharacter.vue'

const items = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const baseQueryUrl = ref(`${import.meta.env.VITE_SERVER_URL}/api/characters`)

onMounted(() => {
  fetchUpdate(baseQueryUrl.value, 1)
})

const goToPage = (page) => {
  if (page < 1 || page > totalPages.value) return
fetchUpdate(baseQueryUrl.value, page)}

const fetchUpdate = async (url, page = 1) => {
  try {
    baseQueryUrl.value = url

    // Добавим page в query-параметры
    const fullUrl = new URL(url)
    fullUrl.searchParams.set('page', page)

    const res = await fetch(fullUrl.toString())
    const json = await res.json()

    items.value = json.data
    currentPage.value = json.pagination.page
    totalPages.value = json.pagination.total_pages
  } catch (err) {
    console.error(err)
  }
}

const modalOpen = ref(false)

const modalToggle = () => {
  modalOpen.value = !modalOpen.value
}

const modalDisable = () => {
  modalOpen.value = false
}
</script>

<template>
  <div class="mt-[-150px]">
    <router-link to="/" class="text-5xl text-gold font-display flex">
      Harry Potter Wiki
    </router-link>
    <Search
      @fetchUpdate="fetchUpdate"
      :modal-disable="modalDisable"
      :modal-toggle="modalToggle"
      placeholder="Harry Potter"
      :modal-open="modalOpen"
    />
    <p class="text-gold text-xl my-4">Found {{ items.length }} records</p>
    <ul class="w-5/6 grid grid-cols-[2fr_2fr_2fr_2fr] gap-5 overflow-y-auto items-start scrollbar-hide h-[500px]">
      <AddCharacter @fetchUpdate="fetchUpdate" />
      <li v-for="item in items" :key="item.id" class="flex justify-center">
        <router-link :to="`/characters/${item.id}`">
          <Card :title="item.name" :image-url="item.image_path" :blood-status="item.blood_status" :born="item.born" :died="item.died? item.died : 'No'" :house="item.house" :gender="item.gender"/>
        </router-link>
      </li>
    </ul>
    <div v-if="totalPages > 1" class="flex justify-center gap-4 mt-6 text-gold">
  <button
    class="px-4 py-2 border border-gold rounded hover:bg-gold hover:text-black transition"
    :disabled="currentPage === 1"
    @click="goToPage(currentPage - 1)"
  >
    Prev
  </button>

  <button
    v-for="page in totalPages"
    :key="page"
    class="px-3 py-1 border rounded"
    :class="{
      'bg-gold text-black': page === currentPage,
      'border-gold': true
    }"
    @click="goToPage(page)"
  >
    {{ page }}
  </button>

  <button
    class="px-4 py-2 border border-gold rounded hover:bg-gold hover:text-black transition"
    :disabled="currentPage === totalPages"
    @click="goToPage(currentPage + 1)"
  >
    Next
  </button>
</div>
  </div>
</template>
