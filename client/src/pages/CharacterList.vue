<script setup>
import Card from '../components/Card.vue'
import { onMounted, ref } from 'vue'
import Search from '../components/Search.vue'

import AddCharacterForm from '../components/AddCharacterForm.vue'
import AddItem from '../components/AddItem.vue'

const items = ref([])

onMounted(async () => {
  try{
    const data = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/characters`, {
      method: 'GET'
    })
    items.value = await data.json()
    console.log(items.value)
  }
  catch(err){
    console.error(err)
  }
})

const isAddModalOpen = ref(false)
const isSearchPanelOpen = ref(false)

const openAddModal = () => {
  isAddModalOpen.value = true
}

const closeAddModal = () => {
  isAddModalOpen.value = false
}

const toggleSearchPanel = () => {
  isSearchPanelOpen.value = !isSearchPanelOpen.value
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
  <div class="mt-[-150px]">
    <router-link to="/" class="text-5xl text-gold font-display flex">
      Harry Potter Wiki
    </router-link>

    <Search
      :modal-toggle="toggleSearchPanel"
      placeholder="Harry Potter"
      :modal-open="isSearchPanelOpen"
    />

    <ul class="w-5/6 grid grid-cols-[2fr_2fr_2fr_2fr] gap-5 overflow-y-auto scrollbar-hide">
      <li class="flex justify-center">
        <div
          class="w-50 h-50 bg-bg flex flex-col items-center pt-2 rounded-md cursor-pointer"
          @click="openAddModal"
        >
          <img
            class="my-4 w-3/5 rounded-md border-3 border-gold border-dashed"
            src="/images/add.svg"
          />
          <p class="text-gold text-lg">Add Item</p>
        </div>
      </li>

      <li v-for="item in items" :key="item.id" class="flex justify-center">
        <router-link :to="`/characters/${item.id}`">
          <Card :title="item.name" :image-url="item.image_path" />
        </router-link>
      </li>
    </ul>

    <AddCharacterForm v-if="isAddModalOpen" @close="closeAddModal" @add="addCharacter" />
  </div>
</template>
