<script setup>
import PoisonCard from '@/components/PoisonCard.vue'
import Search from '../components/Search.vue'
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

const items = ref([
  { id: 'amortentia', name: 'Amortentia' },
  { id: 'anti-jinx', name: 'Anti-jinx varnish' },
  { id: 'volubilis', name: 'Volubilis Potion' }
])

const modalOpen = ref(false)

const modalToggle = () => {
  modalOpen.value = !modalOpen.value
}
</script>

<template>
  <div>
    <router-link to="/" class="text-5xl text-gold font-display flex">
      Harry Potter Wiki
    </router-link>

    <Search :modal-toggle="modalToggle" placeholder="Amorentia" :modal-open="modalOpen" />

    <ul class="w-5/6 grid grid-cols-[2fr_2fr_2fr_2fr] gap-5 overflow-y-auto scrollbar-hide">
      <li class="flex justify-center">
        <div class="w-50 h-50 bg-bg flex flex-col items-center pt-2 rounded-md">
          <img
            class="my-4 w-3/5 rounded-md border-3 border-gold border-dashed"
            src="/images/add.svg"
          />
          <p class="text-gold text-lg">Add Item</p>
        </div>
      </li>
      <li v-for="item in items" :key="item.id">
        <router-link :to="`/poisons/${item.id}`">
          <PoisonCard />
        </router-link>
      </li>
    </ul>
  </div>
</template>
