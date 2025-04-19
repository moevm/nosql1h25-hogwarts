<script setup>
import SpellCard from '@/components/SpellCard.vue'
import Search from '../components/Search.vue'
import AddItem from '../components/AddItem.vue'
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

const items = ref([
  { id: 'aguamenti', name: 'Aguamenti Charm' },
  { id: 'alohomora', name: 'Alohomora' },
  { id: 'aparecium', name: 'Aparecium' }
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

    <Search :modal-toggle="modalToggle" placeholder="Aguamenti" :modal-open="modalOpen" />

    <ul class="w-5/6 grid grid-cols-[2fr_2fr_2fr_2fr] gap-5 overflow-y-auto scrollbar-hide">
      <AddItem />
      <li v-for="item in items" :key="item.id">
        <router-link :to="`/spells/${item.id}`">
          <SpellCard />
        </router-link>
      </li>
    </ul>
  </div>
</template>
