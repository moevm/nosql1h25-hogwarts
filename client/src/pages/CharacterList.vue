<script setup>
import Card from '../components/Card.vue'
import { ref } from 'vue'
import Search from '../components/Search.vue'
import AddCharacterForm from '../components/AddCharacterForm.vue'

const items = ref([
  { id: 'harry', name: 'Harry Potter', imageUrl: '/images/HarryPotter.png' },
  { id: 'hermione-granger', name: 'Hermione Granger', imageUrl: '/images/HermioneGranger.png' },
  { id: 'ron', name: 'Ron Weasley', imageUrl: '/images/RonWeasley.png' }
])

const modalOpen = ref(false)

const modalToggle = () => {
  modalOpen.value = !modalOpen.value
}

const addCharacter = (character) => {
  const id = character.name.toLowerCase().replace(/\s+/g, '-')
  items.value.unshift({
    id,
    name: character.name,
    imageUrl: character.imageUrl,
    description: character.description
  })
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
        <div
          class="w-50 h-50 bg-bg flex flex-col items-center pt-2 rounded-md cursor-pointer"
          @click="modalToggle"
        >
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

    <AddCharacterForm v-if="modalOpen" @close="modalToggle" @add="addCharacter" />
  </div>
</template>
