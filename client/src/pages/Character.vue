<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

import Graph from '../components/Graph.vue'

const route = useRoute()

const item = ref({})
const modalView = ref(false)

onMounted(async () => {
  try {
    const data = await fetch(
      `${import.meta.env.VITE_SERVER_URL}/api/characters/${route.params.id}`,
      {
        method: 'GET'
      }
    )
    item.value = await data.json()
    console.log(item.value)
  } catch (err) {
    console.error(err)
  }
})

const closeModal = () => {
  modalView.value = false
}
const openModal = () => {
  modalView.value = true
}
</script>

<template>
  <div class="flex flex-col items-center text-center p-4 min-w-3/5 mt-[-150px]">
    <router-link to="/" class="text-5xl text-gold font-display flex mb-[50px]">
      Harry Potter Wiki
    </router-link>
    <div class="bg-[#09306260] p-[70px] w-full rounded-md overflow-y-auto scrollbar-hide">
      <div class="flex flex-col float-left mr-10 mb-10">
        <img
          class="rounded-md w-[250px] h-[250px] mb-10 border-3 border-gold"
          :src="item.image_path || ''"
          :alt="item.name"
        />
        <button class="bg-bg rounded-[5px] border-3 border-gold text-gold px-4 py-2" @click="openModal">Graph</button>
        <Graph v-if="modalView" @close-modal="closeModal"/>
      </div>
      <h2 class="text-5xl text-gold font-display pb-5">{{ item.name }}</h2>
      <p class="text-2xl text-gold font-display text-start">Description: {{ item.description }}</p>
      <p class="text-2xl text-gold font-display text-start">
        Blood Status: {{ item.blood_status }}
      </p>
      <p class="text-2xl text-gold font-display text-start">Born: {{ item.born }}</p>
      <p class="text-2xl text-gold font-display text-start">
        Died: {{ item.died ? item.died : 'No' }}
      </p>
      <p class="text-2xl text-gold font-display text-start">Gender: {{ item.gender }}</p>
      <p class="text-2xl text-gold font-display text-start">House: {{ item.house }}</p>
    </div>
  </div>
</template>
