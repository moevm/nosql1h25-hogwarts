<script setup>
import { ref } from 'vue'
import CharacterFilters from './CharacterFilters.vue'
import PoisonFilter from './PoisonsFilters.vue'
import SpellFilter from './SpellFilter.vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const options = ref([])
const searchQuery = ref('') 

const props = defineProps({
  modalDisable: Function,
  modalToggle: Function,
  placeholder: String,
  modalOpen: Boolean
})

const emit = defineEmits(['fetchUpdate'])

const filterRef = ref()

const updateItems = async () => {
  try {
    const query = options.value
      .map((el) => {
        const key = encodeURIComponent(el.key.toLowerCase())
        const value = encodeURIComponent(el.value)
        return `${key}=${value}`
      })
      .join('&')

    const searchParam = searchQuery.value
      ? `name=${encodeURIComponent(searchQuery.value)}`
      : ''

    const combinedQuery = [query, searchParam].filter(Boolean).join('&')

    const apiBase = import.meta.env.VITE_SERVER_URL
    const endpointPath = route.path
    const fullUrl = `${apiBase}/api${endpointPath}?${combinedQuery}`

    console.log('Full API request:', fullUrl)

    emit('fetchUpdate', fullUrl)

    options.value = []

    props.modalDisable()
  } catch (error) {
    console.error('Error fetching data:', error)
  }
}

const makeOptions = (data) => {
  options.value = data
  
}
</script>

<template>
  <div class="w-5/6 my-5 relative">
    <div class="flex w-full gap-5">
      <div class="w-full flex items-center bg-bg rounded-md border border-gold overflow-hidden">
        <input
          class="flex-1 pl-3 py-3 bg-bg text-gold outline-none font-display placeholder:text-[#6C6F27]"
          :placeholder="placeholder"
          v-model="searchQuery"
        />
        <button
          class="text-bg h-14 w-14 rounded-md border border-gold flex justify-center items-center"
          @click="updateItems"
        >
          <img class="w-6 h-6" src="/images/search.svg" />
        </button>
      </div>
      <button
        class="text-bg w-25 h-14 bg-bg rounded-md border border-gold flex justify-center items-center text-gold outline-none flex gap-2"
        @click="() => modalToggle()"
      >
        Search
        <span :class="['transition-transform duration-200', modalOpen ? 'rotate-180' : 'rotate-0']">
          ▼
        </span>
      </button>
    </div>
    <transition name="fade">
      <div
        v-if="modalOpen"
        class="bg-bg w-full h-[400px] rounded-md border border-gold absolute b-[-1px] l-0 p-6 flex gap-[300px]"
      >
        <template v-if="route.path.includes('/character')">
          <CharacterFilters @makeOptions="makeOptions" ref="filterRef"/>
        </template>

        <template v-else-if="route.path.includes('/spell')">
          <SpellFilter @makeOptions="makeOptions" ref="filterRef"/>
        </template>

        <template v-else-if="route.path.includes('/potion')">
          <PoisonFilter @makeOptions="makeOptions" ref="filterRef"/>
        </template>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.25s ease-in-out;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
