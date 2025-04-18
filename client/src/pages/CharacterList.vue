<script setup>
import Card from '../components/Card.vue'
import { ref } from 'vue'
import Search from '../components/Search.vue'

const items = ref([
  { id: 'harry', name: 'Harry Potter', imageUrl: '/images/HarryPotter.png' },
  { id: 'hermione-granger', name: 'Hermione Granger', imageUrl: '/images/HermioneGranger.png' },
  { id: 'ron', name: 'Ron Weasley', imageUrl: '/images/RonWeasley.png' },
  { id: 'hermione-granger', name: 'Hermione Granger', imageUrl: '/images/HermioneGranger.png' },
  { id: 'hermione-granger', name: 'Hermione Granger', imageUrl: '/images/HermioneGranger.png' },
  { id: 'hermione-granger', name: 'Hermione Granger', imageUrl: '/images/HermioneGranger.png' },
  { id: 'hermione-granger', name: 'Hermione Granger', imageUrl: '/images/HermioneGranger.png' },
  { id: 'hermione-granger', name: 'Hermione Granger', imageUrl: '/images/HermioneGranger.png' }
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
    <Search :modal-toggle="modalToggle" placeholder="Harry Potter" :modal-open="modalOpen" />
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
      <li v-for="item in items" :key="item.id" class="flex justify-center">
        <router-link :to="`/character/${item.id}`">
          <Card :title="item.name" :image-url="item.imageUrl" />
        </router-link>
      </li>
    </ul>
  </div>
</template>
