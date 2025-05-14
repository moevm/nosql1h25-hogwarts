<script setup>
import Card from '@/components/Card.vue'
import Search from '../components/Search.vue'
import AddPoison from '../components/AddPoison.vue'
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const items = ref([])

onMounted(async () => {
  try {
    const data = await fetch(`${import.meta.env.VITE_SERVER_URL}/api/potions`, {
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
      placeholder="Amorentia"
      :modal-open="modalOpen"
    />
    <p class="text-gold text-xl my-4">Found {{ items.length }} records</p>


    <ul class="w-5/6 grid grid-cols-[2fr_2fr_2fr_2fr] gap-5 overflow-y-auto scrollbar-hide">
      <AddPoison @fetchUpdate="fetchUpdate" />
      <li v-for="item in items" :key="item.id" class="flex justify-center">
        <router-link :to="`/potions/${item.id}`">
          <Card :title="item.name" :imageUrl="item.image_path" :difficulty="item.difficulty" :effect="item.effect"/>
        </router-link>
      </li>
    </ul>
  </div>
</template>
