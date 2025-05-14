<script setup>
import Card from '@/components/Card.vue'
import Search from '../components/Search.vue'
import AddSpell from '../components/AddSpell.vue'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const items = ref([])

onMounted(async () => {
  try {
    const data = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/spells`, {
      method: 'GET'
    })
    items.value = await data.json()
    console.log(items.value)
  } catch (err) {
    console.error(err)
  }
})

const fetchUpdate = async (str) => {
  try {
    const data = await fetch(str, {
      method: 'GET'
    })
    items.value = await data.json()
    console.log(items.value)
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
      placeholder="Aguamenti"
      :modal-open="modalOpen"
    />
    <p class="text-gold text-xl my-4">Found {{ items.length }} records</p>

    <ul class="w-5/6 grid grid-cols-[2fr_2fr_2fr_2fr] gap-5 overflow-y-auto scrollbar-hide">
      <AddSpell @fetchUpdate="fetchUpdate" />
      <li v-for="item in items" :key="item.id" class="flex justify-center">
        <router-link :to="`/spells/${item.id}`">
          <Card :title="item.name" :imageUrl="item.image_path" :category="item.category" :light="item.light" :effect="item.effect" />
        </router-link>
      </li>
    </ul>
  </div>
</template>
