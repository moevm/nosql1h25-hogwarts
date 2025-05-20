<script setup>
import Card from '../components/Card.vue'
import { computed, nextTick, onMounted, ref } from 'vue'
import Search from '../components/Search.vue'
import AddCharacter from '../components/AddCharacter.vue'

const items = ref([])
const currentPage = ref(1)
const totalPages = ref(1)
const baseQueryUrl = ref(`${import.meta.env.VITE_SERVER_URL}/api/characters`)

onMounted(() => {
  fetchUpdate(baseQueryUrl.value, 1)
})

const listContainer = ref(null)

const goToPage = async (page) => {
  if (page < 1 || page > totalPages.value) return
  await fetchUpdate(baseQueryUrl.value, page)
  nextTick(() => {
    listContainer.value?.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  })
}

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

const visiblePages = computed(() => {
  const pages = []
  const maxVisible = 5 // число видимых страниц вокруг текущей
  const showDots = totalPages.value > maxVisible + 4

  const start = Math.max(2, currentPage.value - 2)
  const end = Math.min(totalPages.value - 1, currentPage.value + 2)

  pages.push(1)

  if (start > 2) pages.push('...')

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }

  if (end < totalPages.value - 1) pages.push('...')

  if (totalPages.value > 1) pages.push(totalPages.value)

  return pages
})

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
    <ul ref="listContainer" class="w-5/6 grid grid-cols-[2fr_2fr_2fr_2fr] gap-5 overflow-y-auto items-start scrollbar-hide h-[500px]">
      <AddCharacter @fetchUpdate="fetchUpdate" />
      <li v-for="item in items" :key="item.id" class="flex justify-center">
        <router-link :to="`/characters/${item.id}`">
          <Card :title="item.name" :image-url="item.image_path" :blood-status="item.blood_status" :born="item.born" :died="item.died? item.died : 'No'" :house="item.house" :gender="item.gender"/>
        </router-link>
      </li>
    </ul>
    <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-6 text-gold flex-wrap">
  <button
    class="px-4 py-2 border border-gold rounded hover:bg-gold hover:text-black transition"
    :disabled="currentPage === 1"
    @click="goToPage(currentPage - 1)"
  >
    Prev
  </button>

  <button
    v-for="page in visiblePages"
    :key="page"
    class="px-3 py-1 border rounded"
    :class="[
  'border',
  page === currentPage ? 'bg-gold text-black' : '',
  page !== '...' ? 'border-gold' : '',
  page === '...' ? 'cursor-default' : ''
]"
    @click="page !== '...' && goToPage(page)"
    :disabled="page === '...'"
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
